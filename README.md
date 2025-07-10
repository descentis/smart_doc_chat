# Implementation Roadmap
------------------------
| Phase     | Scope | Key Deliverabls|
| --------- |:-----:|:--------------:|
| 0. Prereqs| Install Docker & Compose◦ Obtain Groq API key◦ python -m venv .venv if running locally | Local dev environment ready|
|1. Repo Bootstrap|git init rag-mvp Scaffold folder layout exactly as in §3◦ Add backend/requirements.txt and frontend/requirements.txt with minimal deps|Compilable empty services|
|2. Backend Core|Implement main.py factory◦ Wire /ping and CORS◦ Add config.py (env parsing)|uvicorn app.main:app responds 200 on /ping|
|3. Auth & SQLite|Create models/user.py, hashing in security.py◦ CRUD in auth.py (register/login)◦ Issue JWT (use python-jose)|Able to register & obtain token via cURL|
|4. RAG Engine|Add chain.py with Groq LLM & Chroma vectorstore◦ Build ingest.py for sample docs◦ Expose /chat/ask endpoint|Answers questions from seeded docs|
|5. Streamlit UI|Basic login page & chat panel◦ Token persisted in st.session_state◦ Async calls using httpx|Functional local front‑end|
|6. Containerization|Write Dockerfiles◦ docker-compose.yml with volumes & envs◦ Verify multi‑service up|One‑command deployment|
|7. Docs & CI|Update README.md quick‑start◦ GitHub Actions: docker build + unit tests|Green build badge|
|8. Polish|Add SSE streaming◦ Swap LangGraph experiment◦ Helm chart for k8s (optional)|Prod‑ready MVP|
