import streamlit as st
from handle_text import PDFProcess
from chatbot import get_conversation_chain
import pickle
from langchain.vectorstores.faiss import FAISS


class AppPages:

    def __init__(self):
        self.vectorstore = None
        self.embeddings = None
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
    
    def handle_userinput(self, user_question):
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

    
    # Define your chat_page function
    def chat_page(self):
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
                        # Create vectorestore
                        with open('/home/hossam/Chat with PDFs/vectoestoe/index.pkl', 'rb') as f:
                            embeddings = pickle.load(f)
                        
                        vectorstore = FAISS.load_local(
                            folder_path='/home/hossam/Chat with PDFs/vectoestoe/',
                            embeddings=embeddings, 
                            allow_dangerous_deserialization=True
                        )

                        st.success("Loaded Faiss index and embeddings!")
                        # Create conversation chain
                        st.session_state.conversation = get_conversation_chain(vectorstore)

                    except IOError as e:
                        st.error(f"Error loading files: {e}")

        user_question = st.text_input("Ask")
        if user_question:
            self.handle_userinput(user_question)
                

    """
    def chat_page_local_embeddings(self):
        self.contact_me()
        st.title("Try with your PDFs!")

        pdf_docs = st.file_uploader("Upload Files",accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):

                torch.cuda.empty_cache()
            
                # Instance from the class
                pdf_processor = PDFProcess()

                # get pdf text
                raw_text = pdf_processor.get_pdf_text(pdf_docs)

                # Get Text Chunks
                text_chunks = pdf_processor.get_text_chunks(raw_text)

                # Create vectorstore
                vectorstore = pdf_processor.get_vectorstore(text_chunks)

        st.text_input("What is in your mind?")
        """