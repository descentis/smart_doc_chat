# backend/app/api/endpoints/chat.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.app.rag.chain import ask
from backend.app.rag.langgraph_chain import ask_with_graph, stream_with_graph
from backend.app.api.deps import get_current_user
from backend.app.services.chat_history import fetch_history, append_turn
from fastapi.responses import StreamingResponse
from typing import Generator

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/stream")
def chat_stream(request: ChatRequest, user: str = Depends(get_current_user)) -> StreamingResponse:
    def token_generator() -> Generator[str, None, None]:
        for tok in stream_with_graph(request.query):
            yield tok
    return StreamingResponse(token_generator(), media_type="text/plain")

@router.post("/ask")
def chat(request: ChatRequest, user: str = Depends(get_current_user)):
    answer = ask_with_graph(request.query)
    return {"answer": answer}

@router.post("/stream")
def chat_stream(req: ChatRequest, user: str = Depends(get_current_user)):
    history = fetch_history(user)

    # generator
    def token_gen():
        collected = ""
        for tok in stream_with_graph(req.query, history):
            collected += tok
            yield tok
        # Persist after full answer streamed
        append_turn(user, "user", req.query)
        append_turn(user, "assistant", collected)

    return StreamingResponse(token_gen(), media_type="text/plain")
