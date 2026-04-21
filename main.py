# source_handbook: week11-hackathon-preparation
import streamlit as st
from groq import Groq
import os

# 1. Page Config & Custom Styling (cite: 13, 15)
st.set_page_config(page_title="Safe Clicq", layout="centered")

# Custom CSS to match your UI design
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #30107a 100%);
    }
    h1 {
        color: white;
        font-family: 'Serif';
        text-align: center;
        font-size: 3rem !important;
    }
    p {
        color: #b0b0b0;
        text-align: center;
        font-style: italic;
    }
    .stTextInput > div > div > input {
        background-color: white !important;
        color: black !important;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Header Section
st.markdown("<p style='text-align: center; color: #8a63ff; letter-spacing: 2px;'>✨ WELCOME TO SAFE CLICQ</p>", unsafe_allow_html=True)
st.markdown("<h1>Instantly Analyse, Detect <br> Stay Secured</h1>", unsafe_allow_html=True)
st.markdown("<p>Share your site link or message to Analyse Phishing</p>", unsafe_allow_html=True)

# 3. Backend Logic (Groq Agent)
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("Missing GROQ_API_KEY!")
    st.stop()

client = Groq(api_key=api_key)

# 4. Input Fields
user_input = st.text_input("Paste your link or message to analyse", placeholder="Type here...")

if user_input:
    with st.spinner("Analysing..."):
        try:
            # Agentic Reasoning (cite: 101)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert. Provide a concise safety verdict and explain 'why' to a non-technical user (like a grandma)."},
                    {"role": "user", "content": user_input}
                ]
            )
            verdict = response.choices[0].message.content
            
            # Output Box matching your UI
            st.text_area("Find our Analysis Here:", value=verdict, height=200)
            
        except Exception as e:
            st.error(f"Error: {e}")
