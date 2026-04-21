# source_handbook: week11-hackathon-preparation
import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="Safe Clicq", layout="centered")

# 1. THE ULTIMATE CSS OVERRIDE: This forces EVERY element to be Bold White
st.markdown("""
    <style>
    /* Background Gradient */
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #200a5e 100%);
    }
    
    /* Header & Titles */
    h1 { color: white !important; text-align: center; font-family: serif; font-size: 3.5rem !important; }
    .second-title { color: #b0b0b0 !important; text-align: center; font-style: italic; font-size: 1.2rem; }

    /* THE ATOMIC FIX: Forcing Assistant messages to show BOLD WHITE text */
    div[data-testid="stChatMessageAssistant"] {
        background-color: rgba(48, 16, 122, 0.8) !important; /* Dark Purple Box */
        border: 2px solid #8a63ff !important;
        border-radius: 15px !important;
    }

    /* Target every single piece of text inside the Assistant box */
    div[data-testid="stChatMessageAssistant"] p, 
    div[data-testid="stChatMessageAssistant"] li, 
    div[data-testid="stChatMessageAssistant"] strong, 
    div[data-testid="stChatMessageAssistant"] div,
    div[data-testid="stChatMessageAssistant"] span {
        color: #FFFFFF !important;
        font-weight: 900 !important; /* Ultra Bold */
        font-size: 1.1rem !important;
        -webkit-text-fill-color: white !important; /* Force for Chrome/Edge */
    }

    /* Bold Label for Input */
    .stChatInputContainer textarea {
        color: black !important;
    }
    label { color: white !important; font-weight: bold !important; }

    </style>
    """, unsafe_allow_html=True)

# 2. Hero Section (Exact Layout)
st.markdown("<p style='text-align: center; color: #8a63ff; letter-spacing: 3px; font-weight: bold; font-size: 0.8rem;'>✨ WELCOME TO SAFE CLICQ</p>", unsafe_allow_html=True)
st.markdown("<h1>Instantly Analyse, Detect <br> Stay Secured</h1>", unsafe_allow_html=True)
st.markdown("<p class='second-title'>Share your site link or message to Analyse Phishing</p>", unsafe_allow_html=True)

# 3. State & Backend
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a Cybersecurity Analyst. Be direct."}]

api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 4. Display History
for message in st.session_state.messages:
    if message["role"] == "system": continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Repeating Input Box
if prompt := st.chat_input("Paste your link or ask follow-up here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Analysing..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
