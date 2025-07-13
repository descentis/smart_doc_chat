from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

CHROMA_DIR = "vectorstore"

# shared components
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# called at startup (static doc)
def ingest_static():
    loader = TextLoader("docs/sample.txt")
    docs = loader.load()
    chunks = text_splitter.split_documents(docs)
    vectordb = Chroma.from_documents(chunks, embedding=embedding, persist_directory=CHROMA_DIR)
    return len(chunks)

# called by /docs/upload or similar
def ingest_file(path: str):
    if path.endswith(".pdf"):
        loader = PyPDFLoader(path)
    else:
        loader = TextLoader(path)

    docs = loader.load()
    chunks = text_splitter.split_documents(docs)

    vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding)
    vectordb.add_documents(chunks)
    return len(chunks)
