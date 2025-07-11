import streamlit as st
import requests, os
from streamlit_extras.switch_page_button import switch_page

# ---- App config ----
st.set_page_config(page_title="SmartDoc Chat", layout="centered")

# ---- Constants ----
BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

# ---- Session state ----
if "token" not in st.session_state:
    st.session_state.token = None

# ---- Sidebar ----
st.sidebar.title("📄 SmartDoc Chat")
st.sidebar.info("Chat with your documents using Groq-powered RAG.")

if st.session_state.token is None:
    with st.form("login_form"):
        st.subheader("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")

    if submitted:
        try:
            res = requests.post(f"{BACKEND}/auth/login", json={"username": username, "password": password})
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.success("Logged in! Reloading...")
                st.rerun()
            else:
                st.error("❌ Login failed: invalid credentials")
        except Exception as e:
            st.error(f"🚫 Could not connect to backend: {e}")

else:
    st.subheader("💬 Chat with SmartDoc")
    st.markdown("<hr>", unsafe_allow_html=True)

    with st.expander("📂 Upload document"):
        uploaded = st.file_uploader("Choose PDF or TXT", type=["pdf", "txt"])
        if uploaded and st.button("Upload & Ingest"):
            files = {"file": (uploaded.name, uploaded.getvalue())}
            res = requests.post(f"{BACKEND}/docs/upload",
                                headers={"Authorization": f"Bearer {st.session_state.token}"},
                                files=files)
            if res.ok:
                st.success(f"Ingested {res.json()['chunks']} new chunks!")
            else:
                st.error("Upload failed: " + res.text)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["text"])

    if prompt := st.chat_input("Ask a question..."):
        st.chat_message("user").write(prompt)
        st.session_state.chat_history.append({"role": "user", "text": prompt})

        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        try:
            res = requests.post(f"{BACKEND}/chat/ask", json={"query": prompt}, headers=headers)
            if res.ok:
                answer = res.json()["answer"]
                st.chat_message("assistant").write(answer)
                st.session_state.chat_history.append({"role": "assistant", "text": answer})
            else:
                st.chat_message("assistant").write("❌ Error from backend: " + res.text)
        except Exception as e:
            st.chat_message("assistant").write(f"🚫 Could not connect to backend: {e}")

    st.sidebar.button("🔒 Logout", on_click=lambda: st.session_state.clear())
