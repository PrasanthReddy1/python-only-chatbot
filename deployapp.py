import os
import streamlit as st
from openai import OpenAI

# ---------- Setup ----------
st.set_page_config(page_title="Python-only Chat", page_icon="🐍", layout="centered")

# Read API key from environment (Streamlit Secrets or local env var)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ Missing OpenAI API key. Please set OPENAI_API_KEY in your environment or Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)
model_name = "gpt-4o-mini"  # default model

# System prompt to enforce Python-only answers
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

# Render chat history (skip hidden system message)
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
        st.markdown(msg["content"])

# ---------- Model Call ----------
def ask_model(messages):
    try:
        resp = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        msg = str(e)
        if "insufficient_quota" in msg:
            return "⚠️ API error: insufficient quota. Please add billing/credit to your OpenAI account."
        if "invalid_api_key" in msg:
            return "⚠️ API error: invalid API key."
        if "Rate limit" in msg or "429" in msg:
            return "⚠️ API error: rate limit hit. Please wait and try again."
        return f"⚠️ Backend error: {msg}"

# ---------- Input ----------
user_text = st.chat_input("Type your message… (Python only!)")

if user_text:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # Get assistant reply
    assistant_reply = ask_model(st.session_state.messages)

    # Show + store assistant reply
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

# ---------- Footer ----------
st.caption("Model will refuse anything non-Python. Examples are for Python 3.11+.")
