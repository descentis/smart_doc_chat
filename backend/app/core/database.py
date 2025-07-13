from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("sqlite:///./users.db", echo=False)  # echo=True for SQL logs

def init_db():
    from backend.app.models import chat
    SQLModel.metadata.create_all(engine)

# dependency
def get_session():
    with Session(engine) as session:
        yield session
