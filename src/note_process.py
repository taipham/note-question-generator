import spacy

# Load the pre-trained spaCy model for English language
nlp = spacy.load('en_core_web_sm')


# Define a function to preprocess the notes
def preprocess_notes(file_path):
    # Load the spaCy English language model
    nlp = spacy.load('en_core_web_sm')

    # Read in the text file and preprocess it with spaCy
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    doc = nlp(text)

    # Remove stop words and punctuation
    #preprocessed_text = [token.text for token in doc if not token.is_stop and not token.is_punct]

    # Convert the preprocessed text back to a string
    #preprocessed_text = ' '.join(preprocessed_text)

    #return preprocessed_text
    return doc

if __name__ == "__main__":
    test = preprocess_notes("The cat sat on the mat.")
    print(test)