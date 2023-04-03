import os

import openai
from flask import Flask, redirect, render_template, request, url_for
from src.note_process import preprocess_notes

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

def generate_questions(text):
    named_entities = [ent.text for ent in text.ents]
    prompt = f"Generate questions based on the following named entities: " \
             f"{', '.join(named_entities)}\n\nText: {text}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        timeout=1000,
    )

    print(response)
    # Extract the generated question from the OpenAI API response
    generated_question = response.choices[0].text.strip()

    return generated_question

@app.route('/upload')
def upload_notes():
    return render_template('upload_note.html')


@app.route('/process_notes', methods=['POST'])
def process_notes():
    # Get the uploaded file from the request
    uploaded_file = request.files['notes_file']

    # Save the uploaded file to a temporary folder
    temp_folder = 'temp'
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    file_path = os.path.join(temp_folder, uploaded_file.filename)
    uploaded_file.save(file_path)

    # Preprocess the uploaded notes
    preprocessed_text = preprocess_notes(file_path)

    print(preprocessed_text)
    # Generate questions from the preprocessed text
    generated_questions = generate_questions(preprocessed_text)

    # Render the results page with the generated questions
    return render_template('results.html', generated_questions=generated_questions)