from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS


class PDFProcess:
    def __init__(self, chunk_size=1000, chunk_over_lap=200,model_name="hkunlp/instructor-xl"):
        self.chunk_size = chunk_size
        self.chunk_over_lap = chunk_over_lap
        self.model_name = model_name

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
            chunks_size=self.chunk_size,
            chunk_over_lap=self.chunk_over_lap,
            length = len
        )
        chunks = text_splitter.split_text(text)
        return chunks

    # Create vectore store
    def get_vectorstore(self, text_chunks):
        embeddings = HuggingFaceInstructEmbeddings(model_name=self.model_name)
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore