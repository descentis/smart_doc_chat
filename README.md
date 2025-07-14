# SmartDoc Chat – RAG App
---------------------------
SmartDoc Chat is a full-stack Retrieval-Augmented Generation (RAG) application that allows users to chat with uploaded documents using Groq LLMs. It combines LangGraph, FastAPI, Streamlit, and Docker to deliver blazing-fast, document-aware answers with user login and memory.

# Features
* User login with JWT authentication (SQLite + FastAPI)

* Chat with documents using Groq + LangGraph

* Upload .pdf or .txt files and ingest into Chroma vector store

* Streamed answers with memory per user (stored + retrieved)

* Fully Dockerized (backend + frontend)

* Ultra-low latency with Groq API

# Installation
## Prerequisites
Python 3.11+

Docker

Groq API Key


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
