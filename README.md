# 🐍 Python-Only Chatbot

An AI-powered chatbot built with **Streamlit** and the **OpenAI API** that *only* answers **Python-related questions**.  
If the user asks something unrelated, the bot politely refuses.

---

## ✨ Features
- ✅ **Python-only responses** — the model refuses non-Python questions.
- 💬 **Interactive chat UI** built with Streamlit.
- ⚡ Powered by **OpenAI GPT models** (`gpt-4o-mini` by default).
- 🛡️ Handles API errors (quota, invalid key, rate limit).
- 🌐 Ready to deploy on **Streamlit Cloud** or **Render**.

---

## 📸 Demo
<img width="667" height="818" alt="image" src="https://github.com/user-attachments/assets/6614a1d0-9a7e-4ca5-9e12-2988fbf4b995" />

🛠️ Installation & Running Locally
    1. Clone the repo
        git clone https://github.com/PrasanthReddy1/python-only-chatbot.git
        cd python-only-chatbot
    2. Create virtual environment
        python -m venv venv
        .\venv\Scripts\activate   # On Windows
        # or
        source venv/bin/activate  # On macOS/Linux
    3. Install dependencies
        pip install -r requirements.txt
    4. Run the app
        streamlit run app.py
        
🔑 API Key Setup
    1. Get key from https://platform.openai.com/settings
    2. Paste it into the sidebar of the app

🌐 Deployment
  This app can be deployed on Streamlit Cloud or Render.
  Streamlit Cloud
    Push this repo to GitHub.
    Go to Streamlit Cloud → New app → select app.py.
    Add your API key under Secrets.
