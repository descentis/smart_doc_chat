from datetime import timedelta, datetime
from passlib.context import CryptContext
from jose import jwt, JWTError
from backend.app.core.config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGO = "HS256"
ACCESS_EXPIRE = timedelta(hours=1)

def hash_password(pw: str) -> str:
    return pwd_ctx.hash(pw)

def verify_password(pw: str, hashed: str) -> bool:
    return pwd_ctx.verify(pw, hashed)

def create_access_token(subject: str):
    exp = datetime.utcnow() + ACCESS_EXPIRE
    return jwt.encode({"sub": subject, "exp": exp}, settings.jwt_secret, algorithm=ALGO)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGO])
        return payload.get("sub")
    except JWTError:
        return None
