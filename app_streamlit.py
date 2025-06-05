import streamlit as st
from dotenv import load_dotenv
import os
from miriel import Miriel

# --- Config ---
st.set_page_config(
    page_title="CarbonBot",
    page_icon="Carbon Reform Logo.jfif",  # or use .png if that’s your format
    layout="centered"
)

# --- Global Styles ---
st.markdown("""
    <style>
	@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6, p, div, span, label, button {
        font-family: 'DM Sans', sans-serif !important;
    }

    .centered-logo {
        display: flex;
        justify-content: center;
        margin-bottom: 1.2rem;
    }

    .carbon-title {
        text-align: center;
        font-size: 75px;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .carbon-caption {
        text-align: center;
        font-size: 25px !important;
        margin-top: 0;
        color: #666;
    }
    button[kind="secondary"] {
        line-height: 1.2 !important;
        padding-top: 0.35rem !important;
        padding-bottom: 0.35rem !important;
        min-height: auto !important;
    }


    .btn-row {
        display: flex;
        justify-content: center;
        gap: 0.75rem;
        margin-top: 1rem;
    }

    .footer {
        text-align: center;
        font-size: 13px;
        color: #888;
        margin-top: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load API keys ---
load_dotenv()
api_key = st.secrets["MIRIEL_API_KEY"]
project_id = st.secrets["MIRIEL_PROJECT_ID"]
user_id = 90

miriel = Miriel(api_key=api_key)

# --- Session State ---
if "query_input" not in st.session_state:
    st.session_state.query_input = ""
if "submit_from_suggestion" not in st.session_state:
    st.session_state.submit_from_suggestion = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Branding ---
st.markdown('<div class="centered-logo"><img src="https://i.ibb.co/Lz5QyYH6/Carbon-Reform-Logo.jpg" width="140"></div>', unsafe_allow_html=True)
st.markdown('<div class="carbon-title">CarbonBot</div>', unsafe_allow_html=True)
st.markdown('<p class="carbon-caption">Ask anything about Carbon Reform.</p>', unsafe_allow_html=True)

# --- Input field ---
query = st.text_input(" ", value=st.session_state.query_input, key="chat_input", placeholder="Type a question...")

# --- Send & Clear Buttons ---
st.markdown('<div class="btn-row">', unsafe_allow_html=True)
spacer, send_col, clear_col, spacer = st.columns([2.25, 1, 1, 2.25])

with send_col:
    submit = st.button("🚀 Send")

with clear_col:
    clear = st.button("🧹 Clear")
    if clear:
        st.session_state.messages = []
st.markdown('</div>', unsafe_allow_html=True)

# --- Wrap Query ---
def wrap_query(user_input: str) -> str:
    instructions = (
        "You are CarbonBot, an AI assistant for employees at Carbon Reform. "
        "Always give specific names, roles, and documents where possible. "
        "Avoid saying 'ask your manager' or 'contact leadership.' "
        "Refer to specific people like 'Michelle Brancheau-Fogg' when relevant. "
        "Answer only using uploaded documents and respond in natural, human-friendly language."
    )
    return f"{instructions}\n\nUser question: {user_input}"

# --- Query Logic ---
should_submit = submit or st.session_state.get("submit_from_suggestion", False)

if should_submit and query:
    st.session_state.submit_from_suggestion = False
    with st.spinner("🤔 Thinking..."):
        wrapped = wrap_query(query)
        response = miriel.query(wrapped, user_id=user_id, num_results=15)

    with st.expander("📦 Full Response (debug)"):
        st.json(response)

    llm = response.get("results", {}).get("llm_result", "").strip()
    st.markdown("### 💬 Answer")
    if llm:
        st.success(llm)
    else:
        st.error("❌ No LLM result found. Try rewording your question.")

    sources = response.get("results", {}).get("vector_db_results", [])
    if sources:
        st.markdown("### 📄 Sources")
        for src in sources:
            meta = src.get("metadata", {})
            source = meta.get("source", "Unknown Source")
            page = meta.get("page_number", "")
            st.markdown(f"- {source}" + (f" (page {page})" if page else ""))

# --- Suggestions ---
st.markdown("### 💡 Try one of these:")
suggestions = [
    "What is our onboarding process?",
    "Explain our HVAC technology to me like a 5 year old.",
    "How do we plan on reaching $2.5M in revenue?",
]

st.markdown('<div class="suggestion-btns">', unsafe_allow_html=True)
for i in range(0, len(suggestions), 3):
    cols = st.columns(3)
    for j, suggestion in enumerate(suggestions[i:i+3]):
        with cols[j]:
            if st.button(suggestion, key=f"suggestion_{i+j}"):
                st.session_state.query_input = suggestion
                st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown('<div class="footer">Made with ❤️ by the Carbon Reform intern team.</div>', unsafe_allow_html=True)
