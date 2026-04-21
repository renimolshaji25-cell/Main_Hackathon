# source_handbook: week11-hackathon-preparation
import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="Safe Clicq", layout="centered")

# 1. THE BRUTE FORCE CSS: Defining our own custom result box
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #200a5e 100%);
    }
    
    /* Custom Analysis Box - High Contrast */
    .result-container {
        background-color: rgba(255, 255, 255, 0.1); /* Subtle box background */
        border: 2px solid #8a63ff;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0px;
    }

    /* FORCING BOLD WHITE TEXT - No exceptions */
    .result-text {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        line-height: 1.6;
        display: block;
    }

    /* Header Styling */
    h1 { color: white !important; text-align: center; font-family: serif; font-size: 3.5rem !important; margin-bottom: 0px; }
    .second-title { color: #b0b0b0 !important; text-align: center; font-style: italic; font-size: 1.2rem; margin-bottom: 30px; }
    
    /* Chat Input Styling */
    .stChatInput textarea {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Hero Section
st.markdown("<p style='text-align: center; color: #8a63ff; letter-spacing: 3px; font-weight: bold; font-size: 0.8rem;'>✨ WELCOME TO SAFE CLICQ</p>", unsafe_allow_html=True)
st.markdown("<h1>Instantly Analyse, Detect <br> Stay Secured</h1>", unsafe_allow_html=True)
st.markdown("<p class='second-title'>Share your site link or message to Analyse Phishing</p>", unsafe_allow_html=True)

# 3. State Management
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 4. Backend
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. Display History using our Custom Class
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"<p style='color: #8a63ff; font-weight: bold;'>User:</p><p style='color: white;'>{chat['content']}</p>", unsafe_allow_html=True)
    else:
        # This is where we force the Bold White visibility
        st.markdown(f"""
            <div class="result-container">
                <span class="result-text">
                    <strong>ANALYSIS REPORT:</strong><br><br>
                    {chat['content']}
                </span>
            </div>
            """, unsafe_allow_html=True)

# 6. Chat Input
if prompt := st.chat_input("Paste your link or ask follow-up here..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    with st.spinner("🔍 Analysing..."):
        try:
            # Build history for Groq
            messages = [{"role": "system", "content": "You are a professional Cyber Analyst. Be direct and clear."}]
            for c in st.session_state.chat_history:
                messages.append(c)
                
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages
            )
            
            answer = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()
            
        except Exception as e:
            st.error(f"System Error: {e}")
