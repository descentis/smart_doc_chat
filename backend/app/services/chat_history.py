from typing import List
from sqlmodel import Session, select
from backend.app.core.database import engine
from backend.app.models.chat import ChatMessage

def fetch_history(username: str) -> List[dict]:
    with Session(engine) as s:
        rows = s.exec(
            select(ChatMessage).where(ChatMessage.username == username).order_by(ChatMessage.ts)
        ).all()
        return [{"role": row.role, "text": row.text} for row in rows]

def append_turn(username: str, role: str, text: str):
    with Session(engine) as s:
        s.add(ChatMessage(username=username, role=role, text=text))
        s.commit()

