from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import torch
from dotenv import load_dotenv
import os
class PDFProcess:
    def __init__(self, chunk_size=1000, chunk_overlap=250,model_name="hkunlp/instructor-xl", use_gpu=True, batch_size=1):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() and use_gpu else "cpu")
        self.batch_size=batch_size

    # Get PDF Text
    def get_pdf_text(self, pdf_docs):
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    # Get Text Chunks
    def get_text_chunks(self, text):
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        chunks = text_splitter.split_text(text)
        return chunks
    
    def get_vectorstore_huggingface(self, text_chunks):

        
        # Initialize the embedding model
        embeddings = HuggingFaceInstructEmbeddings(model_name=self.model_name)
        embeddings.client = embeddings.client.to(self.device)

        # Initialize FAISS index
        embedding_dim = embeddings.embed_documents(["test"])[0].shape[0]  # Get embedding dimension
        index = FAISS.IndexFlatL2(embedding_dim)
        
        for i in range(0, len(text_chunks), self.batch_size):
            batch_chunks = text_chunks[i:i + self.batch_size]
            with torch.no_grad():
                # Compute embeddings on the correct device
                batch_embeddings = embeddings.embed_documents(batch_chunks)
            
            # Convert embeddings to numpy array
            batch_embeddings_np = batch_embeddings.cpu().numpy()
            
            # Add embeddings to FAISS index
            index.add(batch_embeddings_np)
            
            # Explicitly clear GPU cache to free up memory
            torch.cuda.empty_cache()

        # Return the FAISS vector store
        vectorstore = FAISS(index=index)
        return vectorstore
    
    def get_vectorestore_openai(self, text_chunks):
        load_dotenv()
        openai_key = os.getenv("OPENAI_API_KEY")

        embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
        vectorestore = FAISS.from_texts(texts=text_chunks,
                                        embedding=embeddings)
        return vectorestore