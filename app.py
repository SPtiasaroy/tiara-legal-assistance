import streamlit as st
from openai import OpenAI
import os

# Load API Key from Streamlit secrets
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page setup
st.set_page_config(
    page_title="Tiara Legal Assistance 2.0",
    page_icon="⚖️",
    layout="centered"
)

st.title("⚖️ Tiara Legal Assistance 2.0")
st.write("AI-powered Indian Legal Advisor")

# Legal modes
mode = st.selectbox(
    "Select Legal Mode",
    [
        "Bare Act Explanation",
        "Case Law Research",
        "Legal Advice",
        "Exam Answer Mode"
    ]
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
prompt = st.chat_input("Ask a legal question about Indian law...")

if prompt:
    # Show user message
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    system_prompt = f"""
You are an expert Indian legal assistant.

Mode: {mode}

Always answer using this format:

1. Definition
2. Relevant Section
3. Explanation
4. Landmark Case Law
5. Conclusion

Use simple English and Indian legal references.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ]
    )

    answer = response.choices[0].message.content

    # Show AI message
    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
