import streamlit as st
from openai import OpenAI
import os
import pdfplumber

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="Tiara Legal Assistance 2.0",
    page_icon="⚖️",
    layout="centered"
)

st.title("⚖️ Tiara Legal Assistance 2.0")
st.write("AI-powered Indian Legal Advisor")

mode = st.selectbox(
    "Select Legal Mode",
    [
        "Bare Act Explanation",
        "Case Law Research",
        "Legal Advice",
        "Exam Answer Mode",
        "Explain Legal Document"
    ]
)

# Upload PDF if document mode
uploaded_file = None
if mode == "Explain Legal Document":
    uploaded_file = st.file_uploader("Upload Legal PDF", type=["pdf"])

def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask a legal question about Indian law...")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    document_text = ""

    if uploaded_file:
        document_text = read_pdf(uploaded_file)

    system_prompt = f"""
You are an expert Indian legal assistant.

Mode: {mode}

Always answer in this format:

1. Definition
2. Relevant Section
3. Explanation
4. Landmark Case Law
5. Conclusion

If a document is provided, analyze and explain it clearly.
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
        st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
