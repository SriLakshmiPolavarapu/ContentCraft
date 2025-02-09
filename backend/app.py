from flask import Flask, request, jsonify
import spacy
import os
import yake
from transformers import pipeline

#initializing Flask application by creating an instance of Flask class
app = Flask(__name__)

#Instaed of NLP setup, i'm using Hugging Face models are better summary as well as better Q&A system
summarizer = pipeline("summary", model="facebook/bart-large-cnn")
question_answer = pipeline("question_answering", model="deepset/roberta-large-squad2")

#need to initialize YAKE
keyword_extractor = yake.KeywordExtractor();

#upload file option
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#function to read content from the text file
def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error reading the input file: {e}")
        return ""

#function to generate summary
def generate_summary(content):
    try:
        #process input
        doc = nlp(content)
        
        #count words to decide summary length
        word_count = len(content.split())
        max_sentence_length = 10 if word_count > 100 else 5
        
        #extract important words from the input
        main_words = [token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN","VERB", "ADJ", "ADV"]]
        
        #score is calculated
        sentence_scores={}
        for sent in doc.sents:
            score = sum(1 for token in sent if token.text.lower() in main_words)
            sentence_scores[sent.text] = score
         
        #top ranked sentences are selected    
        sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
        summary_sentence = sorted_sentences[:max_sentence_length]
        
        summary = " ".join(summary_sentence)
        return summary.strip()
       
    except Exception as e:
        print(f"There was an error in generating summary: {e}")   
        raise 

@app.route("/generate_summary", methods=["POST"])
#fucntion to handle summary generation
def generate_summary_endpoint():
    try:
        if "content" in request.files:
            #if the input is file upload
            uploaded_file = request.files["content"]
            if uploaded_file.filename == "":
                return jsonify({"error": "No file uploaded"}), 400
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
            uploaded_file.save(file_path)
            content = read_file(file_path)
        else:
            data = request.json
            content = data.get("content", "")
        if not content:
                return jsonify({"error": "No content provided, please provide content or upload a file"}), 400
            
        summary = generate_summary(content)
        return jsonify({"summary": summary}), 200
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health_check():
    return "Python - Flask backend is running", 200


if __name__ == "__main__":
    app.run(debug=True)