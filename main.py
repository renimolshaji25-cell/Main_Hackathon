# source_handbook: week11-hackathon-preparation
import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="Safe Clicq", layout="centered")

# 1. Professional Styling
st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #000000 0%, #200a5e 100%); }
    .analysis-box {
        background-color: white;
        color: black;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 8px solid #8a63ff;
    }
    .analysis-box * { color: black !important; }
    .user-msg { color: #8a63ff; font-weight: bold; margin-top: 10px; }
    label p { font-weight: bold !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Hero Section
st.markdown("<h1 style='color: white; text-align: center;'>🛡️ Safe Clicq Agent</h1>", unsafe_allow_html=True)

# 3. Memory Setup
if "messages" not in st.session_state:
    st.session_state.messages = [] # Only stores the visible chat history

# 4. Backend Setup
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 5. Display History (This builds the "Chat" look)
for chat in st.session_state.messages:
    if chat["role"] == "user":
        st.markdown(f"<p class='user-msg'>You: {chat['content']}</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class='analysis-box'><b>Analysis Report:</b><br>{chat['content']}</div>""", unsafe_allow_html=True)

# 6. The Input Form (The "Fix")
# Using a form with clear_on_submit=True makes it function like a real chatbot
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area("Analyze a new link or ask a follow-up:", placeholder="Paste here...")
    submit_button = st.form_submit_button("Send to Agent")

if submit_button and user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("Analyzing..."):
        try:
            # Construct the full context for Groq
            full_context = [{"role": "system", "content": "You are a professional Cybersecurity Analyst. Be concise."}]
            full_context.extend(st.session_state.messages)
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=full_context
            )
            
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun() # Refresh to show the new message and clear the input box
            
        except Exception as e:
            st.error(f"Error: {e}")
