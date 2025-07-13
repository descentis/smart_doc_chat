# backend/app/rag/chain.py
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from backend.app.core.config import settings
import os

llm = ChatGroq(model="deepseek-r1-distill-llama-70b", api_key=settings.groq_api_key)
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory="chroma", embedding_function=embedding)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever()
)

def ask(query: str) -> str:
    return qa_chain.run(query)

