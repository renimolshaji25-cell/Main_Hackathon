# source_handbook: week11-hackathon-preparation
import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="Safe Clicq", layout="centered")

# 1. THE BULLETPROOF CSS: Forces Bold White text for the AI analysis
st.markdown("""
    <style>
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #200a5e 100%);
    }
    
    /* Header Styling */
    h1 { 
        color: white; 
        text-align: center; 
        font-family: 'Times New Roman', serif; 
        font-size: 3.5rem !important;
        margin-bottom: 0px;
    }
    .second-title {
        color: #b0b0b0; 
        text-align: center; 
        font-style: italic; 
        font-size: 1.2rem;
        margin-bottom: 40px;
    }

    /* THE FIX: Target the Assistant message box and force Bold White text */
    [data-testid="stChatMessageAssistant"] {
        background-color: rgba(255, 255, 255, 0.1) !important; /* Slight transparency for style */
        border-radius: 15px !important;
        padding: 20px !important;
        border-left: 5px solid #8a63ff !important;
    }

    /* FORCING ALL TEXT TO BOLD WHITE */
    [data-testid="stChatMessageAssistant"] * {
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-family: sans-serif !important;
        font-size: 1.05rem !important;
    }

    /* Chat Input Styling */
    .stChatInputContainer label {
        color: white !important;
        font-weight: bold !important;
    }
    
    /* User message box */
    [data-testid="stChatMessageUser"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Hero Section
st.markdown("<p style='text-align: center; color: #8a63ff; letter-spacing: 3px; font-weight: bold; font-size: 0.8rem;'>✨ WELCOME TO SAFE CLICQ</p>", unsafe_allow_html=True)
st.markdown("<h1>Instantly Analyse, Detect <br> Stay Secured</h1>", unsafe_allow_html=True)
st.markdown("<p class='second-title'>Share your site link or message to Analyse Phishing</p>", unsafe_allow_html=True)

# 3. State Management
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a Cybersecurity Analyst. Provide a clear VERDICT and REASONING. Use bullet points."}
    ]

# 4. Backend
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. Display Conversation History
for message in st.session_state.messages:
    if message["role"] == "system": continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input
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
