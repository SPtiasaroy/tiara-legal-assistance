import streamlit as st
from openai import OpenAI
import os
import pdfplumber

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="Tiara Legal Assistance",
    page_icon="⚖️",
    layout="wide"
)

# Sidebar
st.sidebar.title("⚖️ Tiara Legal Assistance")
st.sidebar.write("AI Legal Advisor for Indian Law")

mode = st.sidebar.selectbox(
    "Choose Mode",
    [
        "Legal Chat",
        "Bare Act Explanation",
        "Case Law Research",
        "Legal Advice",
        "Explain Legal Document"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Tiara helps you understand Indian law with sections, case laws and explanations."
)

# Main title
st.title("⚖️ Tiara Legal Assistance 2.0")
st.caption("AI-powered Indian Legal Research Assistant")

# Upload PDF
uploaded_file = None
if mode == "Explain Legal Document":
    uploaded_file = st.file_uploader("Upload Legal Document", type=["pdf"])

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask a legal question about Indian law...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    document_text = ""

    if uploaded_file:
        document_text = read_pdf(uploaded_file)

    system_prompt = f"""
You are Tiara, an expert Indian legal assistant.

Mode: {mode}

Always answer using this structure:

### Definition
Explain the legal concept.

### Relevant Section
Mention Indian law sections.

### Explanation
Explain clearly.

### Landmark Case Law
Mention important case law.

### Conclusion
Give a short summary.
"""

    user_input = prompt

    if document_text:
        user_input += f"\n\nDocument Content:\n{document_text}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages,
            {"role": "user", "content": user_input}
        ]
    )

    answer = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
