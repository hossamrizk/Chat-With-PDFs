from handle_text import PDFProcess
from chatbot import get_conversation_chain_huggingface
import pickle
from InstructorEmbedding import INSTRUCTOR
from langchain.vectorstores.faiss import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceInstructEmbeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import dotenv
import os

class SimpleTest:

    def __init__(self):
        self.vectorstore = None
        self.embeddings = None
        self.include_prompts = None

    def load_vectorstore(self):
        try:
            self.vectorstore = FAISS.load_local(
                folder_path='/home/hossam/Chat with PDFs/vectoestoe/',
                embeddings=HuggingFaceInstructEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                ),
                #embeddings = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
                #allow_dangerous_deserialization=True
            )
            if isinstance(self.vectorstore, tuple):
                print(f"vectorstore contents: {self.vectorstore}")
            else:
                print("vectorstore contents", type(self.vectorstore))
            print("Loaded Faiss index and embeddings!")
            return self.vectorstore

        except IOError as e:
            print(f"Error loading files: {e}")
            return None

    def create_conversation_chain(self):
        if self.vectorstore:
            try:
                conversation_chain = get_conversation_chain_huggingface(self.vectorstore)
                print(f"Conversation Chain: {type(conversation_chain)}")  # Debug line to check type
                return conversation_chain
            except Exception as e:
                print(f"Error creating conversation chain: {e}")
                return None
        else:
            print("Vectorstore not loaded.")
            return None

    def handle_userinput(self, conversation, user_question):
        if conversation:
            try:
                response = conversation.invoke({'question': user_question})
                print(f"**User:** {user_question}")
                print(f"**Bot:** {response['answer']}")
                chat_history = response.get('chat_history', [])  # Ensure chat_history exists
                return chat_history
            except Exception as e:
                print(f"Error during conversation: {e}")
                return None
        else:
            print("Conversation not initialized. Please upload PDFs and start processing.")
            return None

# Main testing execution
if __name__ == "__main__":
    import os
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
    tester = SimpleTest()
    tester.load_vectorstore()
    conversation_chain = tester.create_conversation_chain()

    # Example user question for testing
    user_question = "What is the content of the PDF?"
    chat_history = tester.handle_userinput(conversation_chain, user_question)
    if chat_history:
        print("Chat History:", chat_history)
