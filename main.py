# source_handbook: week11-hackathon-preparation
import streamlit as st
from groq import Groq
import os

# 1. Page Config & Professional UI Styling (cite: 13, 15)
st.set_page_config(page_title="Safe Clicq", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #200a5e 100%);
    }
    
    /* Styling the Chat Messages */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        margin-bottom: 10px;
    }

    /* Making the Assistant (Analysis) Box White with Black Text */
    [data-testid="stChatMessageAssistant"] {
        background-color: white !important;
        color: black !important;
        border-left: 8px solid #8a63ff;
    }
    
    [data-testid="stChatMessageAssistant"] p, 
    [data-testid="stChatMessageAssistant"] li,
    [data-testid="stChatMessageAssistant"] strong {
        color: black !important;
    }

    /* Header Styling */
    h1 { color: white; text-align: center; font-family: serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. Hero Section
st.markdown("<p style='text-align: center; color: #8a63ff; letter-spacing: 3px; font-size: 0.8rem; font-weight: bold;'>✨ WELCOME TO SAFE CLICQ</p>", unsafe_allow_html=True)
st.markdown("<h1>Instantly Analyse, Detect <br> Stay Secured</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #b0b0b0; text-align: center; font-style: italic;'>Your conversational security assistant</p>", unsafe_allow_html=True)

# 3. Initialize Memory (cite: 101)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a Cybersecurity Analyst. Provide clear verdicts, risk scores, and technical reasons. Stay professional."}
    ]

# 4. Backend Setup
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. Display Chat History (The Repeating Conversation)
for message in st.session_state.messages:
    if message["role"] == "system": continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input - This repeats after every message automatically
if prompt := st.chat_input("Paste your link or ask a follow-up question here..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
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
            except Exception as e:
                st.error(f"Error: {e}")
