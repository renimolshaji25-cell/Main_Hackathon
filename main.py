# source_handbook: week11-hackathon-preparation
import streamlit as st
from groq import Groq
import os

# 1. Page Configuration & Custom UI Styling (cite: 13, 15)
st.set_page_config(page_title="Safe Clicq", layout="centered")

# Custom CSS to match the 'Safe Clicq' Dark/Purple Gradient Theme
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #200a5e 100%);
    }
    
    /* Typography Styling */
    h1 {
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-text {
        color: #b0b0b0;
        text-align: center;
        font-style: italic;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    .welcome-text {
        text-align: center; 
        color: #8a63ff; 
        letter-spacing: 3px; 
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    /* Input Field Styling */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: black !important;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Result Area Styling */
    .stTextArea > div > div > textarea {
        background-color: #f0f2f6 !important;
        color: #1a1a1a !important;
        border-radius: 8px;
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Hero Section (Matches your Safe Clicq design)
st.markdown("<p class='welcome-text'>✨ WELCOME TO SAFE CLICQ</p>", unsafe_allow_html=True)
st.markdown("<h1>Instantly Analyse, Detect <br> Stay Secured</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Share your site link or message to Analyse Phishing</p>", unsafe_allow_html=True)

# 3. Backend Logic - Agentic Reasoning Configuration (cite: 78, 101)
# Secure Key Retrieval (Works locally with secrets.toml and on Cloud)
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("🔑 Error: GROQ_API_KEY not found in Secrets. Deployment halted.")
    st.stop()

client = Groq(api_key=api_key)

# 4. User Interaction Layer
user_input = st.text_input("Paste your link or message to analyse", placeholder="e.g., http://secure-login-bank.com")

if user_input:
    with st.spinner("🔍 Performing Security Triage..."):
        try:
            # Professional Cybersecurity Analyst Persona (Groundedness Check)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are an expert Cybersecurity Analyst for 'Safe Clicq'. 
                        Analyze the user's input for phishing markers, typosquatting, and urgency.
                        Structure your response exactly as follows:
                        1. **VERDICT**: (BOLD RED for MALICIOUS, BOLD GREEN for SAFE)
                        2. **RISK SCORE**: (X/10)
                        3. **TECHNICAL ANALYSIS**: (Brief bullet points explaining your reasoning)
                        4. **ACTIONABLE ADVICE**: (One sentence on what the user should do next)
                        Keep it professional, direct, and fact-based."""
                    },
                    {"role": "user", "content": user_input}
                ]
            )
            
            analysis_result = response.choices[0].message.content
            
            # Display result in the styled output box
            st.markdown("### Analysis Report:")
            st.info(analysis_result)
            
        except Exception as e:
            st.error(f"⚠️ System Error: {str(e)}")

# 5. Footer Branding
st.markdown("---")
st.markdown("<p style='font-size: 0.7rem;'>© 2026 Safe Clicq | Built for Hackathon Readiness</p>", unsafe_allow_html=True)
