# source_handbook: week11-hackathon-preparation
import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="Safe Clicq", layout="centered")

# 1. Your Exact UI Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #200a5e 100%);
    }
    label p {
        font-weight: bold !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
    }
    .stTextArea textarea {
        background-color: white !important;
        color: black !important;
        border-radius: 10px;
        padding: 15px !important;
    }
    /* Fixed White Analysis Box */
    .analysis-box {
        background-color: white;
        color: black;
        padding: 25px;
        border-radius: 12px;
        margin-top: 20px;
        border-left: 10px solid #8a63ff;
        min-height: 200px;
    }
    .analysis-box p, .analysis-box li, .analysis-box h3, .analysis-box strong {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.markdown("<p style='text-align: center; color: #8a63ff; letter-spacing: 3px; font-size: 0.8rem; font-weight: bold;'>✨ WELCOME TO SAFE CLICQ</p>", unsafe_allow_html=True)
st.markdown("<h1 style='color: white; text-align: center; font-family: serif;'>Instantly Analyse, Detect <br> Stay Secured</h1>", unsafe_allow_html=True)

# 3. Memory Setup (cite: 101)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a Professional Cybersecurity Analyst. Analyze the input. Be concise. Start with VERDICT and RISK SCORE."}
    ]
if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = "Your analysis will appear here after you paste a link or message..."

# 4. Backend Setup
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. The Input Box (Always stays at the top/middle as per your design)
user_input = st.text_area("Paste your link or message to analyse", 
                          placeholder="Paste here and press Ctrl+Enter to send...",
                          height=100)

# 6. Logic: Update the existing state instead of appending new boxes
if user_input:
    # Only trigger if the input is new
    if "last_input" not in st.session_state or user_input != st.session_state.last_input:
        with st.spinner("🔍 Analysing..."):
            try:
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.last_input = user_input
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages
                )
                
                # Update the SINGLE analysis state
                st.session_state.last_analysis = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": st.session_state.last_analysis})
                
            except Exception as e:
                st.error(f"Error: {e}")

# 7. THE EXACT FORMAT: One single box that changes content
st.markdown(f"""
    <div class="analysis-box">
        <h3 style="margin-top: 0;">Analysis Report:</h3>
        {st.session_state.last_analysis}
    </div>
    """, unsafe_allow_html=True)
