import streamlit as st
import requests
import PyPDF2

# Set up the Streamlit page
st.set_page_config(
    page_title="Content Craft",
    layout="wide"
)

# Backend API URLs
SUMMARY_API_URL = "http://127.0.0.1:5000/generate_summary"
QA_API_URL = "http://127.0.0.1:5000/ask_question"

# Store actual content, summary, and question in session state
if 'generated_summary' not in st.session_state:
    st.session_state.generated_summary = ""
if 'actual_content' not in st.session_state:
    st.session_state.actual_content = ""
if 'question' not in st.session_state:
    st.session_state.question = ""
if 'answer' not in st.session_state:
    st.session_state.answer = ""  # Store answer in session state

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text

# Main Streamlit application
def main():
    st.title("Content Craft")

    # Sidebar for input options (Enter Text and Upload File)
    st.sidebar.title("Input Options")
    input_type = st.sidebar.radio(
        "Select the input type:", options=["Enter Text", "Upload File"]
    )

    content = None

    # Input for entering text
    if input_type == "Enter Text":
        st.subheader("Paste the text below to generate the summary:")
        content = st.text_area(
            "",
            placeholder="Write or paste the text here...",
            height=200
        )

    # Input for uploading a file (either text or PDF)
    elif input_type == "Upload File":
        st.subheader("Upload a file to extract content:")
        uploaded_file = st.file_uploader("", type=["txt", "pdf"])
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                content = extract_text_from_pdf(uploaded_file)
            else:
                content = uploaded_file.read().decode("utf-8")

    # Generate Summary button
    if st.button("Generate Summary"):
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
                        st.session_state.actual_content = content
                        st.session_state.question = ""  # Reset question after summary
                        st.session_state.answer = ""  # Reset answer after summary
                    else:
                        st.error("Error generating summary.")
                        st.write(f"Details: {response.json().get('error', 'Unknown error')}")
                except Exception as e:
                    st.error("An unexpected error occurred while generating the summary.")
                    st.write(f"Error details: {e}")

    if st.session_state.generated_summary:
        st.subheader("This is the Generated Summary:")
        st.write(st.session_state.generated_summary)

        # Ask a question based on the input
        st.subheader("Ask a question based on the input:")
        question = st.text_input("Enter your question here:", placeholder="Enter your question here:")

        # Reset the question in session state when a new question is asked
        if question != st.session_state.question:
            st.session_state.question = question
            st.session_state.answer = ""  # Reset answer when a new question is asked

        get_answer_button = st.button("Get Answer")

        if get_answer_button:
            if not question.strip():
                st.error("Please enter a question.")
            else:
                with st.spinner("Fetching answer..."):
                    try:
                        data = {"content": st.session_state.actual_content, "question": question}
                        response = requests.post(QA_API_URL, json=data)
                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.answer = result["answer"]  # Store the new answer
                            st.success("Answer:")
                            st.write(st.session_state.answer)
                        else:
                            st.error("Error fetching the answer.")
                            st.write(f"Details: {response.json().get('error', 'Unknown error')}")
                    except Exception as e:
                        st.error("An unexpected error occurred while answering the question.")
                        st.write(f"Error details: {e}")

# Run the app
if __name__ == "__main__":
    main()
