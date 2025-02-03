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
        if request.content_type.startswith("multipart/form-data"):
            data = request.form
            uploaded_file = request.files.get("content")
        else:
            data = request.json
            uploaded_file = None
            content = data.get("content", "")
            if not content:
                return jsonify({"error": "No content provided"}), 400
            
            summary = generate_summary(content)
            return jsonify({"summary": summary}), 200
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health_check():
    return "Python -Falsk backend is running", 200


if __name__ == "__main__":
    app.run(debug=True)