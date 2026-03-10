import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="Tiara Legal Assistance",
    page_icon="⚖️",
    layout="wide"
)

# -------------------------
# CLEAN UI
# -------------------------

st.markdown("""
<style>

.stApp {
background-color:#f9fafb;
font-family: "Segoe UI", sans-serif;
}

.block-container{
max-width:1100px;
padding-top:2rem;
}

h1{
text-align:center;
font-size:42px;
color:#111827;
}

.subtitle{
text-align:center;
color:#6b7280;
margin-bottom:30px;
}

[data-testid="stChatMessage"]{
background:white;
border:1px solid #e5e7eb;
padding:14px;
border-radius:12px;
}

textarea, input{
border-radius:10px !important;
border:1px solid #e5e7eb !important;
}

section[data-testid="stSidebar"]{
background:white;
border-right:1px solid #e5e7eb;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("⚖️ Tiara Legal")

mode = st.sidebar.selectbox(
"Mode",
[
"Legal Chat",
"Legal Search",
"Case Law",
"Exam Mode"
]
)

law_database = st.sidebar.selectbox(
"Law Database",
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
Tiara helps research Indian law:

• Bare Acts  
• Sections  
• Case Law  
• Exam answers
"""
)

# -------------------------
# HEADER
# -------------------------

st.title("⚖️ Tiara Legal Assistance")
st.markdown('<p class="subtitle">AI Powered Indian Legal Research</p>', unsafe_allow_html=True)

st.divider()

# -------------------------
# LEGAL SEARCH
# -------------------------

if mode == "Legal Search":

    query = st.text_input("Search Indian law")

    if query:

        with st.spinner("Searching law..."):

            system_prompt = f"""
You are an Indian legal research assistant.

Database: {law_database}

Provide:

Relevant Law
Section
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

# -------------------------
# LEGAL CHAT
# -------------------------

elif mode == "Legal Chat":

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask a legal question")

    if prompt:

        st.session_state.messages.append({"role":"user","content":prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        system_prompt = f"""
You are an expert Indian legal assistant.

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

# -------------------------
# CASE LAW
# -------------------------

elif mode == "Case Law":

    case = st.text_input("Search case law")

    if case:

        with st.spinner("Searching case law..."):

            system_prompt = """
Provide:

Case Name
Court
Year
Legal Principle
Short summary
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":system_prompt},
                    {"role":"user","content":case}
                ]
            )

            st.write(response.choices[0].message.content)

# -------------------------
# EXAM MODE
# -------------------------

elif mode == "Exam Mode":

    marks = st.selectbox("Answer length",["2 Marks","5 Marks","10 Marks"])

    question = st.text_input("Law exam question")

    if question:

        with st.spinner("Writing answer..."):

            system_prompt = f"""
Answer like a law professor.

Length: {marks}

Structure:

Definition
Relevant section
Case law
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
