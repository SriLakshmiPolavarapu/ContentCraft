from flask import Flask, request, jsonify
import spacy
import os

#initializing Flask application by creating an instance of Flask class
app = Flask(__name__)

#NLP setup
nlp = spacy.load("en_core_web_sm")


#function to generate summary
def generate_summary(content):
    try:
        #process input
        doc = nlp(content)
        
        #count words to decide summary length
        word_count = len(content.split())
        max_length = 10 if word_count > 100 else 5
        
        #extract important words from the input
        main_words = [token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN","VERB", "ADJ", "ADV"]]
    except Exception as e:
        print(f"There was an error in generating summary: {e}")   
        raise 



#fucntion to handle summary generation
def generate_summary_endpoint():
     
        
@app.route("/generate_summary", methods=["POST"])


if __name__ == "__main__":
    app.run(debug=True)