from flask import Flask, request, jsonify
from google.cloud import speech_v1 as speech
import spacy
from transformers import pipeline
import nltk

nltk.download('punkt')
nltk.download('stopwords')