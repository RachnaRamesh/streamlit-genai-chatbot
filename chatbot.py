import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

# ========= ENV =========
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# ========= PAGE =========
st.set_page_config(page_title="Chatty", page_icon="💬", layout="wide")

# ========= CSS =========
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600&display=swap" rel="stylesheet">

<style>

/* FONT */
html, body, [class*="css"] {
    font-family: 'Baloo 2', cursive;
}

/* REMOVE STREAMLIT TOP SPACE */
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 7rem;
}

/* BACKGROUND GRADIENT */
.stApp {
    background: linear-gradient(180deg, #ffd6e7 0%, #ffe3f0 40%, #fff0f6 100%);
}

/* REMOVE HEADER LINE */
header, footer {
    background: transparent !important;
}

/* TITLE — MOVE UP */
.title {
    margin-top: 0px;
    margin-bottom: 12px;
    font-size: 42px;
    font-weight: 600;
    color: #ff4d88;
}

/* USER BUBBLE */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: #ffc2d1;
    color: black !important;
    border-radius: 22px;
    padding: 14px 18px;
    margin: 8px 0;
}

/* ASSISTANT BUBBLE */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: #ffeaf1;
    color: black !important;
    border-radius: 22px;
    padding: 14px 18px;
    margin: 8px 0;
}

/* FORCE TEXT BLACK */
[data-testid="stChatMessage"] p {
    color: black !important;
}

/* NAME LABEL */
.name-label {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 2px;
    color: #ff4d88;
}

/* INPUT BAR */
.stChatFloatingInputContainer {
    background: linear-gradient(135deg, #ff8fb1, #ff6f9f);
    border-top: none;
}

.stChatInputContainer {
    background: transparent;
    border-radius: 25px;
    border: 2px solid rgba(255,255,255,0.4);
}

/* INPUT TEXT WHITE */
textarea {
    color: white !important;
}

textarea::placeholder {
    color: rgba(255,255,255,0.85) !important;
}

</style>
""", unsafe_allow_html=True)

# ========= TITLE =========
st.markdown('<div class="title">Chatty - Your AI Companion</div>', unsafe_allow_html=True)

# ========= STATE =========
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ========= SHOW CHAT =========
for msg in st.session_state.chat_history:
    name = "You" if msg["role"] == "user" else "Chatty"

    with st.chat_message(msg["role"]):
        st.markdown(f'<div class="name-label">{name}</div>', unsafe_allow_html=True)
        st.markdown(msg["content"])

# ========= LLM =========
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7
)

# ========= INPUT =========
prompt = st.chat_input("Ask me anything! 💭")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    st.chat_message("user").markdown(
        '<div class="name-label">You</div>' + prompt,
        unsafe_allow_html=True
    )

    response = llm.invoke(
        input=[
            {"role": "system", "content": "You are a cute and helpful AI assistant."},
            *st.session_state.chat_history
        ]
    )

    reply = response.content
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown('<div class="name-label">Chatty</div>', unsafe_allow_html=True)
        st.markdown(reply)