import streamlit as st
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="Tiara Legal Assistance",
    page_icon="⚖️",
    layout="wide"
)

# ---------------- SIDEBAR ----------------

st.sidebar.title("⚖️ Tiara Legal Assistance")
st.sidebar.caption("AI Legal Research Assistant")

mode = st.sidebar.selectbox(
    "Choose Mode",
    [
        "Legal Chat",
        "Quick Section Search",
        "Case Law Research"
    ]
)

st.sidebar.markdown("---")

law_database = st.sidebar.selectbox(
    "Select Law Database",
    [
        "Bharatiya Nyaya Sanhita (BNS)",
        "Bharatiya Nagarik Suraksha Sanhita (BNSS)",
        "Bharatiya Sakshya Adhiniyam (BSA)",
        "Indian Contract Act",
        "Transfer of Property Act",
        "Specific Relief Act",
        "Companies Act",
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
        "Search Legal Section (Example: BNS 103 or Article 21)"
    )

    if section_query:

        with st.spinner("Searching legal section..."):

            system_prompt = f"""
You are an expert Indian legal assistant.

Explain the section clearly.

Structure the answer as:

Section Name
Act Name
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

# ---------------- LEGAL CHAT ----------------

if mode == "Legal Chat":

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask a legal question about Indian law...")

    if prompt:

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        system_prompt = f"""
You are Tiara, an expert Indian legal research assistant.

Law Database Selected: {law_database}

Answer using this format:

Relevant Law
Section Reference
Explanation
Landmark Case Law
Practical Meaning
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

# ---------------- CASE LAW RESEARCH ----------------

if mode == "Case Law Research":

    case_query = st.text_input(
        "Search case law or legal principle"
    )

    if case_query:

        with st.spinner("Searching case law..."):

            system_prompt = """
You are an Indian legal research assistant.

Provide:

Case Name
Court
Year
Legal Principle
Summary
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": case_query}
                ]
            )

            st.write(response.choices[0].message.content)
