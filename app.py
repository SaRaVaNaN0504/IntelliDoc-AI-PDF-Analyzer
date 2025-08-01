# app.py

import streamlit as st
from pdf_utils import extract_text_from_pdf
from gemini_utils import summarize_text, ask_question

# --- Page Configuration ---
st.set_page_config(page_title="IntelliDoc AI", layout="wide", page_icon="🧠")

# --- Load Custom CSS ---
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("style.css not found. Please ensure the file is in the same directory.")

# --- UI Layout ---
st.markdown("""
<div class="title-card">
    <div class="title">🧠 IntelliDoc AI</div>
    <div class="subtitle">Your AI Assistant for Smart Document Analysis</div>
</div>
""", unsafe_allow_html=True)

# Sidebar for file uploading
with st.sidebar:
    st.header("Upload Your Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    st.info("Your document is processed securely and is never stored.")

# --- Main Application Logic ---
if uploaded_file:
    # Use session_state to store data across reruns for efficiency
    if 'pdf_text' not in st.session_state or st.session_state.get('file_name') != uploaded_file.name:
        with st.spinner("Extracting text from your PDF... Please wait."):
            st.session_state['pdf_text'] = extract_text_from_pdf(uploaded_file)
            st.session_state['file_name'] = uploaded_file.name
            # Clear previous results when a new file is uploaded
            if 'summary' in st.session_state:
                del st.session_state['summary']
            if 'answer' in st.session_state:
                del st.session_state['answer']
        st.success("Text extracted successfully!")

    if st.session_state.get('pdf_text'):
        # --- Summarization Section ---
        st.markdown("### 📚 Document Summary")
        summary_option = st.radio(
            "Choose summary type:",
            ("Concise", "Detailed", "Bullet Points"),
            horizontal=True,
            label_visibility="collapsed"
        )
        if st.button(f"Generate {summary_option} Summary"):
            with st.spinner(f"Generating your {summary_option.lower()} summary..."):
                summary = summarize_text(st.session_state['pdf_text'], summary_option)
                st.session_state['summary'] = summary
        
        # --- CRITICAL FIX IMPLEMENTED HERE ---
        if 'summary' in st.session_state:
            # The summary is now passed directly into the markdown f-string
            st.markdown(f'<div class="response-card">{st.session_state["summary"]}</div>', unsafe_allow_html=True)
            st.download_button("📥 Download Summary", st.session_state['summary'], file_name="summary.txt")

        # --- Question-Answering Section ---
        st.markdown("---")
        st.markdown("### ❓ Ask a Question")
        user_question = st.text_input("Type your question about the document:", placeholder="e.g., What were the main conclusions?")
        
        if st.button("Get Answer"):
            if user_question:
                with st.spinner("Searching for the answer..."):
                    answer = ask_question(st.session_state['pdf_text'], user_question)
                    st.session_state['answer'] = answer
            else:
                st.warning("Please enter a question first.")
        
        # --- CRITICAL FIX IMPLEMENTED HERE ---
        if 'answer' in st.session_state:
            # The answer is also passed directly into the markdown f-string
            st.markdown(f'<div class="response-card">{st.session_state["answer"]}</div>', unsafe_allow_html=True)
else:
    # Welcome message when no file is uploaded
    st.info("Please upload a PDF document using the sidebar to get started.")