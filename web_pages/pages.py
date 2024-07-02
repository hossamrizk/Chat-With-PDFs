import streamlit as st
from handle_text import PDFProcess
from chatbot import get_conversation_chain_huggingface,get_conversation_chain_openai
import pickle
from langchain.vectorstores.faiss import FAISS
#import torch

class AppPages:

    def __init__(self):
        self.vectorstore = None
        self.embeddings = None
        self.pdf_processor = PDFProcess()

        # Initialize session state variables
        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = None

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

    def handle_userinput_huggingface(self, user_question):
        if st.session_state.conversation:
            if callable(st.session_state.conversation):
                try:
                    response = st.session_state.conversation({'question': user_question})
                    st.write(f"**User:** {user_question}")
                    st.write(f"**Bot:** {response['answer']}")
                    st.session_state.chat_history = response.get('chat_history', [])  # Ensure chat_history exists
                except Exception as e:
                    st.error(f"Error during conversation: {e}")
            else:
                st.warning("Conversation object is not callable.")
        else:
            st.warning("Conversation not initialized. Please upload PDFs and start processing.")

    def chat_page_huggingface(self):

        self.contact_me()
        st.title("Try with your PDFs!")

        # Initialize session state variables if not already initialized
        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = None

        pdf_docs = st.file_uploader("Upload Files", accept_multiple_files=True)
        if pdf_docs:
            if st.button("Upload"):
                with st.spinner("Processing"):
                    try:
                        # Create vectorstore
                        with open('/home/hossam/Chat with PDFs/vectoestoe/index.pkl', 'rb') as f:
                            embeddings = pickle.load(f)
                        
                        vectorstore = FAISS.load_local(
                            folder_path='/home/hossam/Chat with PDFs/vectoestoe/',
                            embeddings=embeddings, 
                            #allow_dangerous_deserialization=True
                        )

                        st.success("Loaded Faiss index and embeddings!")
                        # Create conversation chain
                        conversation_chain = get_conversation_chain_huggingface(vectorstore)
                        st.session_state.conversation = conversation_chain
                        st.write(f"Conversation Chain: {type(conversation_chain)}")  # Debug line to check type

                    except IOError as e:
                        st.error(f"Error loading files: {e}")

        user_question = st.text_input("Ask")
        if user_question:
            self.handle_userinput_huggingface(user_question)

    def handle_userinput(user_question):
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response.get('chat_history', [])

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(f"User: {message.content}")
            else:
                st.write(f"Bot: {message.content}")

    def chat_page_openai(self):

        self.contact_me()
        st.title("Try with your PDFs!")

        pdf_docs = st.file_uploader("Upload Files",accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):

                #torch.cuda.empty_cache()
            
                # get pdf text
                raw_text = self.pdf_processor.get_pdf_text(pdf_docs)

                # Get Text Chunks
                text_chunks = self.pdf_processor.get_text_chunks(raw_text)

                # Create vectorstore
                vectorstore = self.pdf_processor.get_vectorestore_openai(text_chunks)

                # Create Conversation chain
                conversation = get_conversation_chain_openai(vectorstore)

        user_question = st.text_input("Ask a question.")
        if user_question:
            self.handle_userinput_openai(user_question)        

        

