import os
import streamlit as st
from openai import OpenAI

# ---------- Setup ----------
st.set_page_config(page_title="Python-only Chat", page_icon="🐍", layout="centered")

# Let users paste a key in the sidebar (or use env var)
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
model_name = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], index=0)

if not api_key:
    st.info("Add your OpenAI API key in the sidebar to start.", icon="🔑")

# Init client when we have a key
client = OpenAI(api_key=api_key) if api_key else None

# System message that ENFORCES Python-only answers
SYSTEM_PROMPT = (
    "You are a helpful assistant that ONLY answers questions about the Python "
    "programming language and its ecosystem (standard library, popular third-party "
    "libraries, packaging, tooling, internals). If the user asks anything outside Python, "
    "respond exactly: 'Sorry, I can only answer Python-related questions.' "
    "When answering Python questions, be concise and provide minimal runnable examples "
    "for Python 3.11+ when useful."
)

# ---------- Chat State ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hi! Ask me anything about Python 🐍."}
    ]

st.title("🐍 Python-only Chat")

# Render history (skip the hidden system message)
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
        st.markdown(msg["content"])

# ---------- Input ----------
user_text = st.chat_input("Type your message… (Python only!)")

def ask_model(messages):
    try:
        resp = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        # Common OpenAI errors turned into user-friendly text
        msg = str(e)
        if "insufficient_quota" in msg or "quota" in msg:
            return ("API error: insufficient quota. Please add billing/credit to your OpenAI "
                    "account and try again.")
        if "Rate limit" in msg or "429" in msg:
            return ("API error: rate limit hit. Please wait a few seconds and try again.")
        if "invalid_api_key" in msg:
            return ("API error: invalid API key. Double-check and paste a valid key.")
        return f"Backend error: {msg}"


# ---------- Handle New User Message ----------
if user_text:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # Get assistant reply (only if we have a key)
    if not client:
        assistant_reply = "Please add your OpenAI API key in the sidebar."
    else:
        # Build message list: system + history (Streamlit state already has system at index 0)
        history = st.session_state.messages
        assistant_reply = ask_model(history)

    # Show + store assistant reply
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

# ---------- Footer ----------
st.caption("Model will refuse anything non-Python. Examples are for Python 3.11+.")