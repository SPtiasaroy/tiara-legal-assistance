import streamlit as st
from openai import OpenAI
import os

# OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="Tiara Legal Assistance",
    page_icon="⚖️",
    layout="wide"
)

# --------------------------------------------------
# PROFESSIONAL UI + HIDE STREAMLIT ELEMENTS
# --------------------------------------------------

st.markdown("""
<style>

/* Hide Streamlit default UI */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {display: none;}
[data-testid="stDecoration"] {display: none;}
[data-testid="stStatusWidget"] {display: none;}

/* App background */
.stApp {
background: linear-gradient(135deg,#0f172a,#1e293b);
color: white;
font-family: "Segoe UI", sans-serif;
}

/* Title styling */
.title {
font-size:42px;
font-weight:700;
margin-bottom:5px;
}

/* Subtitle */
.subtitle {
font-size:18px;
opacity:0.8;
margin-bottom:25px;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
background-color:#020617;
border-right:1px solid #1e293b;
}

/* Input styling */
input, textarea {
background-color:#1e293b !important;
color:white !important;
border-radius:8px !important;
}

/* Buttons */
button {
border-radius:8px !important;
}

/* Chat container */
[data-testid="stChatMessage"] {
background-color:#1e293b;
padding:10px;
border-radius:10px;
margin-bottom:10px;
}

/* Responsive design (tablet/mobile) */
@media (max-width: 768px) {

.title {
font-size:28px;
}

.subtitle {
font-size:14px;
}

section[data-testid="stSidebar"] {
width:100% !important;
}

}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚖️ Tiara Legal Assistance")
st.sidebar.caption("AI Legal Research Platform")

mode = st.sidebar.selectbox(
    "Choose Mode",
    [
        "Legal Chat",
        "Quick Section Search",
        "Case Law Research",
        "Exam Mode"
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
        "Constitution of India",
        "Family Law (Hindu Law, Muslim Law, Divorce, Maintenance)"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
"""
Tiara helps explore Indian law with:

• Bare Act explanations  
• Section analysis  
• Case law summaries  
• Exam-ready answers
"""
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown('<div class="title">⚖️ Tiara Legal Assistance 2.0</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered Indian Legal Research Assistant</div>', unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# QUICK SECTION SEARCH
# --------------------------------------------------

if mode == "Quick Section Search":

    query = st.text_input(
        "Search Legal Section (Example: BNS 103, IPC 420, Article 21)"
    )

    if query:

        with st.spinner("Searching legal section..."):

            system_prompt = """
You are an expert Indian legal assistant.

Explain the legal provision clearly using:

Section Name
Act Name
Explanation
Punishment / Legal Effect
Example Case Law
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":system_prompt},
                    {"role":"user","content":query}
                ]
            )

            st.write(response.choices[0].message.content)

# --------------------------------------------------
# LEGAL CHAT
# --------------------------------------------------

elif mode == "Legal Chat":

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask a legal question about Indian law...")

    if prompt:

        st.session_state.messages.append({"role":"user","content":prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        system_prompt = f"""
You are Tiara, an expert Indian legal research assistant.

Law database selected: {law_database}

Structure answers with:

Relevant Law
Section Reference
Explanation
Landmark Case Law
Practical Meaning
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

# --------------------------------------------------
# CASE LAW RESEARCH
# --------------------------------------------------

elif mode == "Case Law Research":

    case_query = st.text_input("Search case law or legal principle")

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
                    {"role":"system","content":system_prompt},
                    {"role":"user","content":case_query}
                ]
            )

            st.write(response.choices[0].message.content)

# --------------------------------------------------
# EXAM MODE
# --------------------------------------------------

elif mode == "Exam Mode":

    marks = st.selectbox(
        "Select Answer Length",
        [
            "2 Marks",
            "5 Marks",
            "10 Marks"
        ]
    )

    question = st.text_input("Enter Law Exam Question")

    if question:

        with st.spinner("Preparing exam answer..."):

            system_prompt = f"""
You are an Indian law professor.

Answer the question for a law exam.

Answer length: {marks}

Structure:

Definition
Legal Provision
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
