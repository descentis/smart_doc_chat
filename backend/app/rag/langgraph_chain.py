"""
LangGraph‑powered Conversational RAG chain
• Persistent Chroma (langchain_chroma, Chroma ≥1.0)
• Embeddings: all‑MiniLM‑L6‑v2
• LLM: Groq deepseek‑r1‑distill‑llama‑70b
"""

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langgraph.graph import END, StateGraph
from langchain_core.messages import HumanMessage, AIMessage
from typing import Dict, Generator

from backend.app.core.config import settings

# -------- Config -------------------------------------------------
CHROMA_DIR = "vectorstore"
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_retriever():
    """Open up‑to‑date Chroma retriever each call."""
    vectordb = Chroma(persist_directory=CHROMA_DIR,
                      embedding_function=embedding)
    return vectordb.as_retriever(search_kwargs={"k": 4})

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    api_key=settings.groq_api_key,
    temperature=0,
)

base_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant who answers using the provided context."
     "Do **NOT** reveal or describe your reasoning process."
     "Use the chat history to stay consistent with your prior responses."
     "If the answer is not contained in the context, say you don't know."),
    ("placeholder", "{chat_history}"),
    ("human", "{full_question}")
])

# -------- State definition --------------------------------------
class GraphState(Dict):
    question: str
    docs: list
    answer: str

# -------- Nodes --------------------------------------------------
def retrieve_docs(state: GraphState) -> GraphState:
    state["docs"] = get_retriever().get_relevant_documents(state["question"])
    return state

def format_chat_history(chat_history: list) -> list:
    """
    Converts chat history [{"role": "user"/"assistant", "text": ...}]
    to list of LangChain message objects.
    """
    messages = []
    for turn in chat_history:
        if turn["role"] == "user":
            messages.append(HumanMessage(content=turn["text"]))
        else:
            messages.append(AIMessage(content=turn["text"]))
    return messages

def generate_answer(state: GraphState) -> GraphState:
    context = "\n\n".join(doc.page_content for doc in state["docs"])
    question = state["question"]
    history_msgs = format_chat_history(state.get("chat_history", []))

    # Inject context and question at the end
    history_msgs.append(HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{question}"))

    response = llm.invoke(history_msgs)
    answer = getattr(response, "content", response)

    # Save back to state
    state["answer"] = answer
    state["chat_history"] = state.get("chat_history", []) + [
        {"role": "user", "text": question},
        {"role": "assistant", "text": answer}
    ]
    return state

'''
def generate_answer(state: GraphState) -> GraphState:
    context = "\n\n".join(doc.page_content for doc in state["docs"])
    full_q = f"Context:\n{context}\n\nQuestion:\n{state['question']}"
    prompt_in = base_prompt.invoke({"full_question": full_q})
    history = format_chat_history(state.get("chat_history", []))
    response = llm.invoke(prompt_in)
    state["answer"] = getattr(response, "content", response)
    return state
'''

# -------- Compile LangGraph -------------------------------------
builder = StateGraph(GraphState)
builder.add_node("retrieve", retrieve_docs)
builder.add_node("respond",  generate_answer)
builder.set_entry_point("retrieve")
builder.add_edge("retrieve", "respond")
builder.add_edge("respond",  END)
graph_chain = builder.compile()

# -------- Public helpers ----------------------------------------
def ask_with_graph(question: str, history=[]) -> str:
    state = {
        "question": question,
        "docs": [],
        "answer": "",
        "chat_history": history
    }
    final = graph_chain.invoke(state)
    return final["answer"], final["chat_history"]

def stream_with_graph(question: str, history=[]) -> Generator[str, None, None]:
    docs = get_retriever().get_relevant_documents(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    messages = format_chat_history(history)
    messages.append(HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{question}"))

    response_so_far = ""
    for chunk in llm.stream(messages):
        token = getattr(chunk, "content", "")
        if token:
            response_so_far += token
            yield token

