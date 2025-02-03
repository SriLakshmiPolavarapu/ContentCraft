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
        #....   
    except Exception as e:
        print(f"There was an error in generating summary: {e}")   
        raise 



#fucntion to handle summary generation
def generate_summary_endpoint():
     
        
@app.route("/generate_summary", methods=["POST"])


if __name__ == "__main__":
    app.run(debug=True)