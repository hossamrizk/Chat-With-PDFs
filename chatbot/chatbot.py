from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain

def get_conversation_chain(vectorstore):
    
    memory = ConversationBufferMemory(memory_key="memory_history",
                                      return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm()