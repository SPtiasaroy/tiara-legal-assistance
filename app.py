import streamlit as st
import os
from openai import OpenAI

# Load API key from environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="Tiara Legal Assistance 2.0",
    page_icon="⚖️",
)

# Title
st.title("⚖️ Tiara Legal Assistance 2.0")
st.write("AI-powered Indian Legal Advisor")

# Legal Mode Selector
mode = st.selectbox(
    "Select Legal Mode",
    [
        "Bare Act Explanation",
        "General Legal Advice",
        "Case Law Summary"
    ]
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# Chat input
user_input = st.chat_input("Ask a legal question about Indian law...")

if user_input:

    # Show user message
    st.chat_message("user").write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    try:

        system_prompt = f"""
You are Tiara Legal Assistance 2.0.

You specialize in Indian law.

Mode selected: {mode}

Provide answers in:
• Simple English
• Point wise explanation
• Mention relevant legal sections
• Mention landmark case laws if applicable
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

        answer = response.choices[0].message.content

        # Display AI response
        st.chat_message("assistant").write(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:
        st.error(f"Error: {e}")