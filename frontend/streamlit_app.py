import streamlit as st
import requests

st.set_page_config(
    page_title="Content Craft - Sri Lakshmi",
    layout="wide"
)

API_URL = "http://127.0.0.1:5000/generate_summary"

def main():
    st.title("Content Craft - Sri Lakshmi")
    st.write("This generates summary of the content provided")
    
    st.sidebar.title("Input Options:")
    input_type = st.sidebar.radio(
        "Choose the input type:", options=["Enter Text", "Upload Text File"]
    )
    
    if input_type == "Enter Text":
        st.subheader("Enter your text below:")
        text = st.text_area("Enter or paste your text here", placeholder="Enter or paste your text here", height=400)
        
    elif input_type == "Upload Text File":
        st.subheader("Upload your text file")
        uploaded_file = st.file_uploader("Upload your text file", type=["txt"])
        
    else:
        return "Error processing input"    