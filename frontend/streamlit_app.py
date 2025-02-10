import streamlit as st
import requests
import PyPDF2

# Set up the Streamlit page
st.set_page_config(
    page_title="Content Craft",
    layout="wide"
)

# Backend API URL
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

# Main function for the Streamlit app
def main():
    st.title("Content Craft")

    # Sidebar for input options
    st.sidebar.title("Input Options")
    input_type = st.sidebar.radio(
        "Select the input type:", options=["Transcript", "Upload Text File"]
    )

    content = None

    # Input for Transcript
    if input_type == "Transcript":
        st.subheader("Paste the text below to generate the summary:")
        content = st.text_area(
            "",
            placeholder="Write or paste the text here...",
            height=200
        )

    # Input for Upload Text File
    elif input_type == "Upload Text File":
        st.subheader("Upload the text file below to generate the summary:")
        uploaded_file = st.file_uploader("", type=["txt"])
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")

    elif input_type == "Upload PDF File":
        st.subheader("Upload the PDF file below to extract text:")
        uploaded_file = st.file_uploader("", type=["pdf"])
        if uploaded_file:
            content = extract_text_from_pdf(uploaded_file)

    # Generate Summary button
    if st.button("Generate Summary"):
        if input_type == "Transcript" and not content.strip():
            st.error("Please provide a transcript to generate the summary.")
        elif input_type == "Upload Text File" and not uploaded_file:
            st.error("Please upload a text file to generate the summary.")
        else:
            with st.spinner("Generating summary..."):
                try:
                    if input_type == "Transcript":
                        # Send text data to backend
                        data = {"content": content}
                        response = requests.post(API_URL, json=data)

                    elif input_type == "Upload Text File":
                        # Read and send text file content
                        files = {"content": (uploaded_file.name, uploaded_file, "text/plain")}
                        response = requests.post(API_URL, files=files)


                    # Handle response
                    if response.status_code == 200:
                        result = response.json()
                        st.success("Summary Generated:")
                        st.write(result["summary"])
                    else:
                        st.error("Error generating summary.")
                        st.write(f"Details: {response.json().get('error', 'Unknown error')}")

                except Exception as e:
                    st.error("An unexpected error occurred while generating the summary.")
                    st.write(f"Error details: {e}")
    

# Run the app
if __name__ == "__main__":
    main()