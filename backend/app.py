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

#YAKE
#function to extract most important keywords from the text
def extract_keywords(text, max_keywords = 10):
    try:
        keywords = yake.KeywordExtractor().extract_keywords(text)
        top_words = [kwords[0] for kwords in keywords[:max_keywords]]
        return top_words
    except Exception as e:
        return []

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
        content = content.strip()  
        content = " ".join(content.split())  

        max_input_length = 1024  
        if len(content.split()) > max_input_length:
            content = " ".join(content.split()[:max_input_length])

        important_keywords = extract_keywords(content)

        summary = summarizer(content, max_length=150, min_length=50, do_sample=False)
        summary_text = summary[0]["summary_text"]

        if any(keyword.lower() in summary_text.lower() for keyword in important_keywords):
            return summary_text
        else:
            summary = summarizer(content, max_length=150, min_length=50, do_sample=True)
            return summary[0]["summary_text"]
    except Exception as e:
        return f"Error generating summary: {e}"
       
     

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