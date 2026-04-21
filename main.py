# source_handbook: week11-hackathon-preparation
import streamlit as st
from groq import Groq
import os

# 1. Page Configuration & Styling (cite: 13, 15)
st.set_page_config(page_title="Safe Clicq", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #200a5e 100%);
    }
    
    /* Bold Labels */
    label p {
        font-weight: bold !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
    }

    /* Input Field Styling */
    .stTextArea textarea {
        background-color: white !important;
        color: black !important;
        border-radius: 10px;
        padding: 15px !important;
    }

    /* Analysis Report Box (White with Black Text) */
    .analysis-box {
        background-color: white;
        color: black;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 8px solid #8a63ff;
    }
    .analysis-box p, .analysis-box li, .analysis-box h3, .analysis-box strong {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Hero Section
st.markdown("<p style='text-align: center; color: #8a63ff; letter-spacing: 3px; font-size: 0.8rem; font-weight: bold;'>✨ WELCOME TO SAFE CLICQ</p>", unsafe_allow_html=True)
st.markdown("<h1 style='color: white; text-align: center;'>Instantly Analyse, Detect <br> Stay Secured</h1>", unsafe_allow_html=True)

# 3. Initialize Session State (Memory) (cite: 101, 118)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    # Initial System Instruction
    st.session_state.messages = [
        {"role": "system", "content": "You are a Professional Cybersecurity Analyst. Analyze links/messages for phishing. Provide a VERDICT, RISK SCORE, and TECHNICAL ANALYSIS. Keep follow-up answers concise."}
    ]

# 4. Backend Setup
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. Display Previous Analysis Reports (The White Boxes)
for message in st.session_state.chat_history:
    role = "User Query" if message["role"] == "user" else "Analysis Report"
    if message["role"] == "assistant":
        st.markdown(f"""
            <div class="analysis-box">
                <h3 style="margin-top:0;">{role}:</h3>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='color: #b0b0b0;'><b>Last Input:</b> {message['content']}</p>", unsafe_allow_html=True)

# 6. Input Layer - Bottom Box for continuous asking
user_input = st.text_area("Paste a link or ask a follow-up question:", 
                          placeholder="Type here and press Ctrl+Enter to send...",
                          height=100)

if user_input:
    # Check if this is the same as the last message to prevent infinite loops on refresh
    if not st.session_state.chat_history or user_input != st.session_state.chat_history[-1]["content"]:
        with st.spinner("🔍 Agent is thinking..."):
            try:
                # Append user message to history
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.chat_history.append({"role": "user", "content": user_input})

                # Generate Response
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages
                )
                
                output = response.choices[0].message.content
                
                # Save assistant response
                st.session_state.messages.append({"role": "assistant", "content": output})
                st.session_state.chat_history.append({"role": "assistant", "content": output})
                
                # Rerun to display the new white box
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")
