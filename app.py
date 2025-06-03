import streamlit as st
from dotenv import load_dotenv
import os
from miriel import Miriel

# Load environment variables
load_dotenv()
api_key = os.getenv("MIRIEL_API_KEY")
project_id = os.getenv("MIRIEL_PROJECT_ID")
user_id = 90  # or change to appropriate user

# Initialize Miriel
miriel = Miriel(api_key=api_key)

# Page config
st.set_page_config(page_title="CarbonBot", page_icon="🌿")
st.title("🌿 CarbonBot")
st.caption("Ask anything about Carbon Reform.")

# Question input
query = st.text_input("Ask a question", placeholder="e.g., Who handles HR at Carbon Reform?")
submit = st.button("Send")

# === Add a wrapper to format the query ===
def wrap_query(user_input: str) -> str:
    instructions = (
        "You are CarbonBot, an AI assistant for employees at Carbon Reform. "
        "Always give specific names, roles, and documents where possible. "
        "Avoid saying 'ask your manager' or 'contact leadership.' "
        "Refer to specific people like 'Michelle Brancheau-Fogg' when relevant. "
        "Answer only using uploaded documents."
    )
    return f"{instructions}\n\nUser question: {user_input}"

# === When the user submits a question ===
if submit and query:
    with st.spinner("Thinking..."):
        wrapped = wrap_query(query)
        response = miriel.query(wrapped, user_id=user_id)

        # Debug section (optional, for dev only)
        with st.expander("📦 Full Response (debug)"):
            st.json(response)

        # Extract answer
        llm = response.get("results", {}).get("llm_result")

        st.markdown("### 💬 Answer")
        if isinstance(llm, str) and llm.strip():
            st.success(llm)
        else:
            st.error("❌ No LLM result found. Try rewording your question.")

        # Optional: Show document sources if available
        sources = response.get("results", {}).get("vector_db_results", [])
        if sources:
            st.markdown("### 📄 Sources")
            for src in sources:
                source = src.get("metadata", {}).get("source", "Unknown Source")
                st.markdown(f"- {source}")
