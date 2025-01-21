from flask import Flask, request, jsonify
from google.cloud import speech_v1 as speech
import spacy
from transformers import pipeline
import nltk

nltk.download('punkt')
nltk.download('stopwords')

#initializing Flask application by creating an instance of Flask class
app = Flask(__name__)

#NLP setup
nlp = spacy.load("en_core_web_sm")

#API Route
@app.route("/generate_linkedin_post", methods=["POST"])

#function to generate LinkedIn post, which handles POST request
def generate_linkedin_post():
    data = request.json
    input_type = data.get('input_type')
    content = data.get('content')
    
    #Processing audio input (speech-to-text)
    if input_type == "video":
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US"
        )
        response = client.recognize(config=config, audio=audio)
        text = response.results[0].alternatives[0].transcript
    else:
        transcript = content    

