# source_handbook: week11-hackathon-preparation
import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="Safe Clicq", layout="centered")

# 1. Enhanced Custom UI Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #200a5e 100%);
    }
    
    /* Bolding the 'Paste your link' label */
    label p {
        font-weight: bold !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
    }

    /* Styling the Input Area to prevent collision */
    .stTextArea textarea {
        background-color: white !important;
        color: black !important;
        border-radius: 10px;
        padding: 15px !important;
        line-height: 1.5;
    }

    /* The "Analysis Report" Box: White background, Black text */
    .analysis-box {
        background-color: white;
        color: black;
        padding: 25px;
        border-radius: 12px;
        margin-top: 20px;
        border-left: 10px solid #8a63ff;
    }
    
    /* Ensuring markdown text inside the white box is also black */
    .analysis-box p, .analysis-box li, .analysis-box h3 {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Hero Section
st.markdown("<p style='text-align: center; color: #8a63ff; letter-spacing: 3px; font-size: 0.8rem; font-weight: bold;'>✨ WELCOME TO SAFE CLICQ</p>", unsafe_allow_html=True)
st.markdown("<h1 style='color: white; text-align: center;'>Instantly Analyse, Detect <br> Stay Secured</h1>", unsafe_allow_html=True)

# 3. Input Layer - Using text_area for long messages to avoid collision
user_input = st.text_area("Paste your link or message to analyse", 
                          placeholder="Type or paste your message here...",
                          height=100)

# 4. Logic & Output
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

if user_input:
    with st.spinner("🔍 Analysing..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Professional Cybersecurity Analyst persona. Output markdown."},
                    {"role": "user", "content": user_input}
                ]
            )
            analysis_result = response.choices[0].message.content
            
            # 5. The White Result Box
            st.markdown(f"""
                <div class="analysis-box">
                    <h3 style="color: black !important; margin-top: 0;">Analysis Report:</h3>
                    {analysis_result}
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {e}")
