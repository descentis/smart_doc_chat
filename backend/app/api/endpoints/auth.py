from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, Token
from backend.app.core.security import hash_password, verify_password, create_access_token
from backend.app.core.database import get_session

router = APIRouter()

@router.post("/register", status_code=201)
def register(payload: UserCreate, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.username == payload.username)).first():
        raise HTTPException(409, "Username already exists")
    user = User(username=payload.username, password_hash=hash_password(payload.password))
    session.add(user)
    session.commit()
    return {"msg": "registered"}

@router.post("/login", response_model=Token)
def login(payload: UserCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == payload.username)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    token = create_access_token(user.username)
    return Token(access_token=token)

