import os
import requests
import streamlit as st
from sseclient import SSEClient  # future use for SSE
from typing import List, Dict

# ─── Config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="📄 SmartDoc Chat", layout="centered")

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

# ─── Session State ────────────────────────────────────────────────────────
if "token" not in st.session_state:
    st.session_state.token = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history: List[Dict] = []

# ─── Sidebar ──────────────────────────────────────────────────────────────
st.sidebar.title("📄 SmartDoc Chat")
st.sidebar.caption("Chat with your documents (Groq • LangGraph • Chroma)")

# Helper to fetch persisted history once after login
def load_history_from_backend():
    try:
        r = requests.get(
            f"{BACKEND}/chat/history",
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )
        if r.ok:
            st.session_state.chat_history = r.json()
    except Exception:
        pass  # silently ignore if endpoint not present

# ─── Auth Flow ────────────────────────────────────────────────────────────
if st.session_state.token is None:
    tab_login, tab_register = st.tabs(["🔐 Login", "🆕 Register"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Log in"):
                try:
                    r = requests.post(
                        f"{BACKEND}/auth/login",
                        json={"username": username, "password": password},
                    )
                    if r.status_code == 200:
                        st.session_state.token = r.json()["access_token"]
                        st.success("✅ Logged in! Reloading…")
                        load_history_from_backend()
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                except Exception as e:
                    st.error(f"Backend unreachable: {e}")

    with tab_register:
        with st.form("register_form"):
            new_user = st.text_input("New Username")
            new_pass = st.text_input("New Password", type="password")
            if st.form_submit_button("Register"):
                try:
                    r = requests.post(
                        f"{BACKEND}/auth/register",
                        json={"username": new_user, "password": new_pass},
                    )
                    if r.ok:
                        st.success("User created! Please log in.")
                    else:
                        st.error("Registration failed: " + r.text)
                except Exception as e:
                    st.error(f"Backend unreachable: {e}")

# ─── Main Chat UI ─────────────────────────────────────────────────────────
else:
    st.subheader("💬 Chat with SmartDoc")
    st.markdown("<hr>", unsafe_allow_html=True)

    # --- Upload ---
    with st.expander("📂 Upload document"):
        upload = st.file_uploader("PDF or TXT", type=["pdf", "txt"])
        if upload and st.button("Upload & Ingest"):
            files = {"file": (upload.name, upload.getvalue())}
            r = requests.post(
                f"{BACKEND}/docs/upload",
                headers={"Authorization": f"Bearer {st.session_state.token}"},
                files=files,
            )
            if r.ok:
                st.success(f"Indexed {r.json()['chunks']} new chunks.")
            else:
                st.error("Upload failed: " + r.text)

    # --- Render history ---
    for turn in st.session_state.chat_history:
        st.chat_message(turn["role"]).write(turn["text"])

    # --- Chat input ---
    if prompt := st.chat_input("Ask a question…"):
        # Show user bubble immediately
        st.chat_message("user").write(prompt)
        st.session_state.chat_history.append({"role": "user", "text": prompt})

        # Assistant placeholder
        placeholder = st.chat_message("assistant")
        box = placeholder.empty()

        try:
            with requests.post(
                f"{BACKEND}/chat/stream",
                json={"query": prompt},
                headers={"Authorization": f"Bearer {st.session_state.token}"},
                stream=True,
            ) as r:
                answer = ""
                for chunk in r.iter_lines(decode_unicode=True):
                    if chunk:
                        answer += chunk
                        box.markdown(answer + "▌")
                box.markdown(answer)
                st.session_state.chat_history.append({"role": "assistant", "text": answer})
        except Exception as e:
            box.markdown(f"❌ Error: {e}")

    # --- Logout ---
    if st.sidebar.button("🔒 Logout"):
        st.session_state.clear()
        st.rerun()

