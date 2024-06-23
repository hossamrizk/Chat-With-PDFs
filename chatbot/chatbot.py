from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.llms.huggingface_hub import HuggingFaceHub
from dotenv import load_dotenv
import os

load_dotenv()


# Retrieve Hugging Face Hub API token from environment variable
huggingfacehub_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")


def get_conversation_chain(vectorestore):
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl",
                         model_kwargs={"temperature":0.5, "max_length":512},
                         huggingfacehub_api_token=huggingfacehub_token)
    
    memory = ConversationBufferMemory(memory_key="chat_history",
                                      return_messages=True)
    
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm,retriever=vectorestore.as_retriever(),
                                                               memory=memory)
    return conversation_chain