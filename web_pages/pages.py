import streamlit as st
from handle_text import PDFProcess

class AppPages:

    def __init__(self):
        self

    def contact_me(self):
        if st.sidebar.button("Contact me"):
            st.sidebar.markdown(
                """
                **Contact:-**\n
                *Hossam Eldein Rizk.*\n
                *AI Engineer.*\n
                hossamrizk048@gmail.com\n
                [Linkedin](https://www.linkedin.com/in/hossamrizk10/)\n
                [Github](https://github.com/hossamrizk)\n
                [Kaggle](https://www.kaggle.com/hossamrizk)\n
                """
            )

    def home_page(self):
        self.contact_me()
        st.title("Welcome to the Chatbot Application")
        st.write("**Interact with your documents effortlessly**")
        st.write(
            "This platform allows you to upload your PDFs and start a conversation with my chatbot about the content. "
            "My chatbot is designed to help you extract insights, answer questions, and provide a deeper understanding of your documents."
        )
        st.header("Features:")
        st.write("""
        - Upload multiple PDFs.
        - Ask questions about the content of your PDFs.
        - Receive accurate and context-aware responses.
        - Easy-to-use interface for seamless interaction.
        """)

    def chat_page(self):
        self.contact_me()
        st.title("Try with your PDFs!")

        pdf_docs = st.file_uploader("Upload Files",accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # Instance from class
                pdf_processor = PDFProcess()

                # get pdf text
                raw_text = pdf_processor.get_pdf_text(pdf_docs)

                # Get Text Chunks
                text_chunks = pdf_processor.get_text_chunks(raw_text)

                # Create vectorstore
                vectorstore = pdf_processor.get_vectorstore(text_chunks)

        st.text_input("What is in your mind?")
    