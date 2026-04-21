# source_handbook: week11-hackathon-preparation
import streamlit as st
from groq import Groq

# 1. Scaffolding & Configuration (cite: 13, 14, 15)
st.set_page_config(page_title="Safe-Click Guard", page_icon="🤖")
st.title("🤖 Safe-Click Security Agent")

# 2. Secret Handling (cite: 78)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Secret Key not found. Please check .streamlit/secrets.toml")
    st.stop()

# 3. Chat History (Concept: Agent Memory vs Prompt) (cite: 101)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a Cybersecurity Expert. Analyze inputs for phishing markers like urgency or deceptive URLs. Provide a risk score and reasoning."}
    ]

# Display history (cite: 53)
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Agentic Interaction (cite: 50, 101)
if user_input := st.chat_input("Paste a link or message to analyze:"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Reasoning..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})