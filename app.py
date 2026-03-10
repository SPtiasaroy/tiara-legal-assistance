import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="Tiara Legal Assistance",
    page_icon="⚖️",
    layout="wide"
)

# ---------------------------
# SIDEBAR
# ---------------------------

st.sidebar.title("⚖️ Tiara Legal Assistance")

mode = st.sidebar.selectbox(
    "Choose Mode",
    [
        "Legal Chat",
        "Quick Section Search",
        "Case Law Research",
        "Exam Mode"
    ]
)

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
        "Constitution of India",
        "Family Law"
    ]
)

st.sidebar.info(
"""
Tiara helps explore Indian law with:

• Bare Acts  
• Sections  
• Case Law  
• Exam answers
"""
)

# ---------------------------
# HEADER
# ---------------------------

st.title("⚖️ Tiara Legal Assistance")
st.caption("AI Powered Indian Legal Research Assistant")

st.divider()

# ---------------------------
# QUICK SECTION SEARCH
# ---------------------------

if mode == "Quick Section Search":

    query = st.text_input(
        "Search Legal Section (Example: BNS 103, IPC 420, Article 21)"
    )

    if query:

        with st.spinner("Searching law..."):

            system_prompt = f"""
You are an expert Indian legal assistant.

Database selected: {law_database}

Explain clearly using:

Relevant Law
Section Reference
Explanation
Case Law
Practical Meaning
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":system_prompt},
                    {"role":"user","content":query}
                ]
            )

            st.write(response.choices[0].message.content)

# ---------------------------
# LEGAL CHAT
# ---------------------------

elif mode == "Legal Chat":

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask a legal question about Indian law")

    if prompt:

        st.session_state.messages.append({"role":"user","content":prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        system_prompt = f"""
You are Tiara, an Indian legal research assistant.

Database: {law_database}

Explain using sections and case law.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":system_prompt},
                *st.session_state.messages
            ]
        )

        answer = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {"role":"assistant","content":answer}
        )

# ---------------------------
# CASE LAW
# ---------------------------

elif mode == "Case Law Research":

    case = st.text_input("Search case law")

    if case:

        with st.spinner("Searching case law..."):

            system_prompt = """
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
                    {"role":"system","content":system_prompt},
                    {"role":"user","content":case}
                ]
            )

            st.write(response.choices[0].message.content)

# ---------------------------
# EXAM MODE
# ---------------------------

elif mode == "Exam Mode":

    marks = st.selectbox(
        "Answer length",
        ["2 Marks","5 Marks","10 Marks"]
    )

    question = st.text_input("Enter law exam question")

    if question:

        with st.spinner("Preparing answer..."):

            system_prompt = f"""
You are a law professor.

Answer length: {marks}

Structure:

Definition
Relevant Section
Case Law
Conclusion
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":system_prompt},
                    {"role":"user","content":question}
                ]
            )

            st.write(response.choices[0].message.content)
