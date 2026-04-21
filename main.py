# source_handbook: week11-hackathon-preparation
import streamlit as st
from groq import Groq
import os

# 1. Page Config & Professional UI Styling (cite: 13, 15)
st.set_page_config(page_title="Safe Clicq", layout="centered")

st.markdown("""
    <style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #200a5e 100%);
    }
    
    /* Bold White Label for Input */
    [data-testid="stChatInput"] label p {
        font-weight: bold !important;
        color: white !important;
    }

    /* THE FIX: Forcing Assistant Messages to be White Boxes with Black Text */
    [data-testid="stChatMessageAssistant"] {
        background-color: white !important;
        color: black !important;
        border-radius: 12px !important;
        padding: 20px !important;
        border-left: 10px solid #8a63ff !important;
        margin-bottom: 20px !important;
    }
    
    /* Ensuring ALL text inside the assistant box is black and visible */
    [data-testid="stChatMessageAssistant"] p, 
    [data-testid="stChatMessageAssistant"] li,
    [data-testid="stChatMessageAssistant"] strong,
    [data-testid="stChatMessageAssistant"] span {
        color: black !important;
        font-weight: 500 !important;
    }

    /* User Message Styling (Subtle/Dark) */
    [data-testid="stChatMessageUser"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }

    h1 { color: white; text-align: center; font-family: serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. Hero Section
st.markdown("<p style='text-align: center; color: #8a63ff; letter-spacing: 3px; font-size: 0.8rem; font-weight: bold;'>✨ WELCOME TO SAFE CLICQ</p>", unsafe_allow_html=True)
st.markdown("<h1>Instantly Analyse, Detect <br> Stay Secured</h1>", unsafe_allow_html=True)

# 3. Initialize Memory (cite: 101)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a Cybersecurity Analyst. Provide clear verdicts, risk scores, and technical reasons. Output in clear markdown."}
    ]

# 4. Backend Setup
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. Display Conversation History
for message in st.session_state.messages:
    if message["role"] == "system": continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input - Repeats automatically after each response
if prompt := st.chat_input("Paste your link or ask follow-up here..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response (White Box)
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
