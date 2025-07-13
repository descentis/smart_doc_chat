# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# App settings and DB init
from backend.app.core.config import settings
from backend.app.core.database import init_db

# Routers
from backend.app.api.endpoints import auth, chat, docs  # chat.py must define `router`

def create_app() -> FastAPI:
    app = FastAPI(
        title="RAG MVP",
        description="FastAPI backend for the Streamlit-based RAG demo.",
        version="0.1.0",
    )
    init_db()
    # --- CORS (allow Streamlit frontend) ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],          # tighten in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Health probe ---
    @app.get("/ping", tags=["utility"])
    async def ping():
        return {"status": "ok"}

    # --- Include feature routers ---
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(chat.router, prefix="/chat", tags=["chat"])
    app.include_router(docs.router, prefix="/docs", tags=["docs"])
    return app


# ASGI entrypoint for Uvicorn
app = create_app()


# --- Startup tasks ---
@app.on_event("startup")
def on_startup() -> None:
    init_db()                       # create SQLite tables
    # Optionally: preload RAG vector store on boot
    # from backend.app.rag.chain import qa_chain   # noqa: E402
    # qa_chain.retriever.vectorstore  # touch to ensure load

