import streamlit as st
import requests
import PyPDF2

# Set up the Streamlit page
st.set_page_config(
    page_title="Content Craft",
    layout="wide"
)

# Backend API URL's
SUMMARY_API_URL = "http://127.0.0.1:5000/generate_summary"
QA_API_URL = "http://127.0.0.1:5000/ask_question"

#to store actual content, summary and question 
if 'generated_summary' not in st.session_state:
   st.session_state.generated_summary = ""
if 'actual_content' not in st.session_state:
   st.session_state.actual_content = ""
if 'question' not in st.session_state:
   st.session_state.question = ""

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text

def main():
    st.title("Content Craft")

    # Sidebar for input options
    st.sidebar.title("Input Options")
    input_type = st.sidebar.radio(
        "Select the input type:", options=["Transcript", "Upload Text File"]
    )

    content = None

    #input for text
    if input_type == "Transcript":
        st.subheader("Paste the text below to generate the summary:")
        content = st.text_area(
            "",
            placeholder="Write or paste the text here...",
            height=200
        )

    #input for upload text file
    elif input_type == "Upload Text File":
        st.subheader("Upload the text file below to generate the summary:")
        uploaded_file = st.file_uploader("", type=["txt"])
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")

    #input for upload pdf file
    elif input_type == "Upload PDF File":
        st.subheader("Upload the PDF file below to extract text:")
        uploaded_file = st.file_uploader("", type=["pdf"])
        if uploaded_file:
            content = extract_text_from_pdf(uploaded_file)

    # Generate Summary button ***
    if st.button("Generate Summary"):
        #instead of giving text and file inputs separetly, give 'content'
        if not content or not content.strip():
            st.error("Please provide content to generate the summary")
        else:
            with st.spinner("Generating summary..."):
                try:
                    # Handle response
                    data = {"content": content}
                    response = requests.post(SUMMARY_API_URL, json=data)
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.generated_summary = result["summary"]
                        st.session_state.original_content = content
                    else:
                        st.error("Error generating summary.")
                        st.write(f"Details: {response.json().get('error', 'Unknown error')}")

                except Exception as e:
                    st.error("An unexpected error occurred while generating the summary.")
                    st.write(f"Error details: {e}")
    

# Run the app
if __name__ == "__main__":
    main()