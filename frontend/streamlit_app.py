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
    
    #this section is for generating summary - button click
    if st.button("Generate Summary"):
        if input_type == "Enter Text" and not text.strip():
            st.error("Please enter or paste your text before generating summary")
        elif input_type == "Upload Text File" and not uploaded_file:
            st.error("Please upload a text file before generating summary")
        else:
            with st.spinner("Generating summary..."):
                try:
                    if input_type == "Transcript":
                        # Send text data to backend
                        data = {"input_type": "Transcript", "content": transcript}
                        response = requests.post(API_URL, json=data)

                    elif input_type == "Text File":
                        # Send file data to backend
                        files = {"content": (uploaded_file.name, uploaded_file, "text/plain")}
                        data = {"input_type": "Text File"}
                        response = requests.post(API_URL, files=files, data=data)
                    else:
                        return "###"
                    
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("Summary Generated:")
                        st.markdown("---")
                        st.write(result["summary"])
                        st.markdown("---")
                    else:
                        st.error("Error generating summary.")
                        st.write(f"Details: {response.json().get('error', 'Unknown error')}")
                except Exception as e:
                    st.error("An unexpected error occurred while generating the summary.")
                    st.write(f"Error details: {e}")
                   
            
