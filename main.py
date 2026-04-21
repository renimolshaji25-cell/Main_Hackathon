# source_handbook: week11-hackathon-preparation
import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="Safe Clicq", layout="centered")

# 1. THE INJECTION: This targets the actual background of the whole page
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #200a5e 100%);
    }
    /* This targets the chat input text specifically */
    .stChatInput textarea {
        color: black !important;
    }
    h1 { color: white !important; text-align: center; font-family: serif; font-size: 3.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Hero Section
st.markdown("<p style='text-align: center; color: #8a63ff; letter-spacing: 3px; font-weight: bold; font-size: 0.8rem;'>✨ WELCOME TO SAFE CLICQ</p>", unsafe_allow_html=True)
st.markdown("<h1>Instantly Analyse, Detect <br> Stay Secured</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #b0b0b0; text-align: center; font-style: italic; font-size: 1.2rem;'>Share your site link or message to Analyse Phishing</p>", unsafe_allow_html=True)

# 3. State Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Backend
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. THE FIX: Displaying messages with INLINE HTML STYLES
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"<span style='color: white !important;'>{message['content']}</span>", unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            # We wrap the AI response in a custom DIV with forced white bold text
            st.markdown(f"""
                <div style="color: white !important; font-weight: bold !important; font-size: 1.1rem !important; border-left: 5px solid #8a63ff; padding-left: 15px;">
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)

# 6. Repeating Chat Input
if prompt := st.chat_input("Paste your link or ask follow-up here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Analysis Logic
    with st.spinner("🔍 Analysing..."):
        try:
            # Create a history for the AI that includes the system prompt
            api_messages = [{"role": "system", "content": "You are a Cybersecurity Analyst. Be bold and direct."}] + st.session_state.messages
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=api_messages
            )
            full_response = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
