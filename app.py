import streamlit as st
from openai import OpenAI
import os
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="Tiara Legal Assistance",
    page_icon="⚖️",
    layout="wide"
)

# ---------------- SIDEBAR ----------------

st.sidebar.title("⚖️ Tiara Legal Assistance")
st.sidebar.caption("Indian Legal Research AI")

mode = st.sidebar.selectbox(
    "Choose Mode",
    [
        "Legal Chat",
        "Bare Act Explanation",
        "Case Law Research",
        "Quick Section Search"
    ]
)

st.sidebar.markdown("---")

law_database = st.sidebar.selectbox(
    "Select Law Database",
    [
        "Indian Penal Code (IPC)",
        "Code of Criminal Procedure (CrPC)",
        "Indian Contract Act",
        "Indian Evidence Act",
        "Constitution of India"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Tiara helps you explore Indian laws, sections and landmark judgments."
)

# ---------------- HEADER ----------------

st.title("⚖️ Tiara Legal Assistance")
st.caption("AI-powered Indian Legal Research Assistant")

# ---------------- QUICK SECTION SEARCH ----------------

if mode == "Quick Section Search":

    section_query = st.text_input(
        "Search Section (Example: IPC 420 or Article 21)"
    )

    if section_query:

        system_prompt = f"""
You are an Indian legal expert.

The user is searching for a legal section.

Explain clearly with this structure:

Section Name
Law Act
Explanation
Punishment / Legal Effect
Example Case Law
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": section_query}
            ]
        )

        st.write(response.choices[0].message.content)

# ---------------- NORMAL LEGAL CHAT ----------------

if mode != "Quick Section Search":

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask a legal question about Indian law")

    if prompt:

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        system_prompt = f"""
You are Tiara, an expert Indian legal research assistant.

Mode: {mode}

Always answer using this structure:

### Relevant Law
Mention the act.

### Section Reference
Mention section numbers.

### Explanation
Explain in simple language.

### Landmark Case Law
Mention famous case law.

### Practical Meaning
Explain what it means in real life.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages
            ]
        )

        answer = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
