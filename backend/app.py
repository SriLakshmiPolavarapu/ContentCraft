from flask import Flask, request, jsonify
from google.cloud import speech_v1 as speech
import spacy
from transformers import pipeline
import nltk

nltk.download('punkt')
#stopwords: and, is, in (common words)
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
        #if it is not video i.e. plain text
    else:
        transcript = content  
        
    #NLP Processing
    #Using spaCy model, the transcript is processed to tokenize, analyze and extract key features.
    doc = nlp(transcript)
    #summary is generated by removing stopwords and punctuations.
    summary = ' '.join([token.text for token in doc if not token.is_stop and not token.is_punct])
    
    #Text generation
    #Text generation pipeline is used -- GPT-NEO 2.7B
    post_generation = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")
    linkedin_post = post_generation(summary, max_length=250)[0]['generated_text']
    
    #return a JSON response
    return jsonify({"linkedin_post": linkedin_post})

if __name__ == "__main__":
    app.run(debug=True)
