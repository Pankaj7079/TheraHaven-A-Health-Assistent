import streamlit as st
import requests
import re
from datetime import datetime

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
BACKEND_URL = "http://localhost:8000/ask"   # change if your backend uses different host/port/route
BACKEND_TIMEOUT = 8  # seconds

st.set_page_config(page_title="TheraHaven – Your AI Mental Health Companion", layout="wide")

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def remove_emojis(text: str) -> str:
    emoji_pattern = re.compile("[" 
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               "]+", flags=re.UNICODE)
    cleaned = emoji_pattern.sub(r'', text)
    return cleaned.strip()

def local_fallback_response(user_text: str) -> str:
    user_text = user_text.lower().strip()
    if any(w in user_text for w in ("hi", "hello", "hey")) and len(user_text.split()) <= 3:
        return "Hello — I'm here to listen. How are you feeling today?"
    if "sad" in user_text or "depress" in user_text:
        return "I'm sorry you're feeling that way. Can you tell me more about what's been happening?"
    if "anx" in user_text or "nerv" in user_text or "stress" in user_text:
        return "Sounds stressful. What helps you calm down usually?"
    return "Thanks for sharing. Could you say a bit more so I can better support you?"

def query_backend(user_text: str) -> (str, str):
    try:
        resp = requests.post(BACKEND_URL, json={"message": user_text}, timeout=BACKEND_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            ai_resp = data.get("response")
            tool_called = data.get("tool_called", None)
            if ai_resp:
                return ai_resp, tool_called
    except Exception:
        pass
    return None, None

# -----------------------------------------------------------------------------
# Styling
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        body { background-color: #0f1113; color: #e6eef3; }
        .app-title { text-align: center; margin-top: -10px; }
        h1, h3 { margin: 0; }
        .tagline { font-style: italic; color: #99a3ac; margin-bottom: 22px; }

        .chat-container { display: flex; flex-direction: column; gap: 10px; padding: 8px 4px; }

        .assistant-msg {
            background: linear-gradient(180deg, #1f2426, #212426);
            color: #e9f0f2;
            padding: 12px 16px;
            border-radius: 12px;
            max-width: 76%;
            align-self: flex-start;
            box-shadow: 0 4px 16px rgba(0,0,0,0.35);
            border: 1px solid rgba(255,255,255,0.03);
            word-wrap: break-word;
        }

        .user-msg {
            background: linear-gradient(180deg, #17181a, #1b1c1e);
            color: #d7e6ef;
            padding: 12px 16px;
            border-radius: 12px;
            max-width: 76%;
            align-self: flex-end;
            box-shadow: 0 4px 16px rgba(0,0,0,0.35);
            border: 1px solid rgba(255,255,255,0.03);
            word-wrap: break-word;
        }

        .timestamp { font-size: 11px; color: #7f8a90; margin-top: -6px; }

        .sidebar .sidebar-content {
            background-color: #1f2428;
            padding: 16px;
            border-radius: 8px;
            color: #cfe1ea;
        }

        .chat-input { width: 100%; border-radius: 24px; padding: 12px 16px; }
    </style>
    """, unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# Sidebar (Updated)
# -----------------------------------------------------------------------------
st.sidebar.title("About TheraHaven")
st.sidebar.markdown(
    """
**TheraHaven** is an AI-powered mental health companion designed to provide a safe, confidential, and understanding space where you can share your thoughts freely.

**How TheraHaven Supports You**
- Empathetic listening to truly understand your feelings
- Gentle, thoughtful guidance to help you move forward
- TheraHavenm — here to listen and support you.
"""
)

# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-title">
        <h1>🧠 <strong>TheraHaven</strong></h1>
        <h3>Your AI Mental Health Companion</h3>
        <div class="tagline">Here to listen, support, and guide you toward a healthier mind.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Initialize chat history
# -----------------------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": "Hello, I’m TheraHaven. How are you feeling today?",
            "timestamp": datetime.now().strftime("%H:%M")
        }
    ]

# -----------------------------------------------------------------------------
# Chat display
# -----------------------------------------------------------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.chat_history:
    content = remove_emojis(str(msg.get("content", "")))
    if msg.get("role") == "user":
        st.markdown(f"<div class='user-msg'>{content}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-msg'>{content}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='timestamp'>{msg.get('timestamp','')}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Input
# -----------------------------------------------------------------------------
user_input = st.chat_input("What's on your mind today?")

if user_input:
    clean_user = remove_emojis(user_input)
    st.session_state.chat_history.append({
        "role": "user",
        "content": clean_user,
        "timestamp": datetime.now().strftime("%H:%M")
    })

    ai_resp, tool_called = query_backend(clean_user)

    if ai_resp is None:
        ai_resp = local_fallback_response(clean_user)
        tool_called = None

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": ai_resp,
        "timestamp": datetime.now().strftime("%H:%M")
    })

    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# -----------------------------------------------------------------------------
# Footer

