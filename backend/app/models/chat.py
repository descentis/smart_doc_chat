from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    role: str                  # "user" | "assistant"
    text: str
    ts: datetime = Field(default_factory=datetime.utcnow)

