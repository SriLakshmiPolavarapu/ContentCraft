from flask import Flask, request, jsonify
import yake
from transformers import pipeline

from transformers import BartTokenizer, BartForConditionalGeneration

# Initializing Flask application
app = Flask(__name__)

# Hugging Face model pipelines
#summary_model = pipeline("summarization", model="facebook/bart-large-cnn")
question_answer_model = pipeline("question-answering", model="deepset/roberta-large-squad2")

tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
summary_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")


# YAKE for keyword extraction
def extract_keywords(text, max_keywords=10):
    try:
        keywords = yake.KeywordExtractor().extract_keywords(text)
        top_words = [kwords[0] for kwords in keywords[:max_keywords]]
        return top_words
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

# Generate summary function
def generate_summary(content):
    try:
        content = content.strip()
        content = " ".join(content.split())  # Normalize whitespace

        if not content:
            return "No content provided for summary."

        # Tokenize the content
        inputs = tokenizer(content, return_tensors="pt", truncation=True, padding=True, max_length=1024)

        # Log content to be passed to the model
        print(f"Content being passed to summary model: {content}")
        
        # Generate the summary
        summary_ids = summary_model.generate(inputs['input_ids'], max_length=150, min_length=20, do_sample=False)
        summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        if not summary_text:
            print("No summary generated.")
            return "Error: Summary generation failed."

        print(f"Generated summary: {summary_text}")
        return summary_text

    except Exception as e:
        print(f"Error generating summary: {e}")
        return f"Error generating summary: {e}"


# Function for answering questions
def answer_question(context, question):
    try:
        if not question.strip().endswith("?"):
            question = question.strip() + "?"
            
        response = question_answer_model(question=question, context=context)
         
        threshold = 0.05  # Confidence score threshold
        if response["score"] > threshold:
            return response['answer']
        else:
            return "No relevant answer found. Please try rephrasing your question!"
    except Exception as e:
        return f"Error answering question: {e}"

# Flask endpoints
@app.route("/generate_summary", methods=["POST"])
def generate_summary_endpoint():
    try:
        content = request.json.get("content", "")
        if not content:
            return jsonify({"error": "No content provided."}), 400

        summary = generate_summary(content)
        return jsonify({"summary": summary}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ask_question", methods=["POST"])
def ask_question_endpoint():
    try:
        data = request.json
        content = data.get("content", "")
        question = data.get("question", "")

        if not content or not question:
            return jsonify({"error": "Content and question must be provided."}), 400

        answer = answer_question(content, question)
        return jsonify({"answer": answer}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health_check():
    return "Python - Flask backend is running", 200

if __name__ == "__main__":
    app.run(debug=True)
