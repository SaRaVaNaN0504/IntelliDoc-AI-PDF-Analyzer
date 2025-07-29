import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai

# --- Configuration ---
st.set_page_config(
    page_title="IntelliDoc AI",
    page_icon="🧠",
    layout="wide"
)

# --- Enhanced Custom CSS with Colorful Theme ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Root Variables for Dynamic Theme */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --success-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }

    /* Global Background with Animated Gradient */
    .stApp {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Floating Particles Background Effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.3) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }

    /* Stunning Header with Glass Effect */
    .header-banner {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%);
        border-radius: 25px;
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.37),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 3rem 2rem;
        text-align: center;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        animation: slideDown 0.8s ease-out;
    }

    .header-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shine 3s infinite;
        transform: rotate(45deg);
    }

    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        50% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        100% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    }

    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-50px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .header-banner h1 {
        font-weight: 700;
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        position: relative;
        z-index: 1;
    }

    .header-banner p {
        font-size: 1.3rem;
        color: #2d3748;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }

    /* Sidebar Enhancement */
    .css-1d391kg {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0.1) 100%);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2rem 1.5rem;
        animation: slideRight 0.6s ease-out;
    }

    @keyframes slideRight {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }

    /* PDF Upload Area */
    .uploadedFile {
        border: 3px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
        100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
    }

    /* Interactive Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 15px;
        font-size: 1.1rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }

    .stButton > button:active {
        transform: translateY(-1px) scale(0.98);
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    /* Special Button Variants */
    .stButton[data-baseweb="button"][data-testid*="summarize"] > button {
        background: var(--success-gradient);
        box-shadow: 0 4px 15px rgba(67, 233, 123, 0.4);
    }

    .stButton[data-baseweb="button"][data-testid*="download"] > button {
        background: var(--accent-gradient);
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
    }

    /* Response Cards with Glassmorphism */
    .response-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.2) 100%);
        border-radius: 20px;
        box-shadow: 
            0 8px 32px rgba(31, 38, 135, 0.37),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2rem;
        margin: 1.5rem 0;
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }

    .response-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--primary-gradient);
        border-radius: 20px 20px 0 0;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Tab Enhancement */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
        border-radius: 15px;
        padding: 0.5rem;
        backdrop-filter: blur(10px);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #4a5568;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 1rem 2rem;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    /* Input Fields */
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0.1) 100%);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 1rem;
        font-size: 1.1rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        transform: scale(1.02);
    }

    /* Radio Buttons */
    .stRadio > div {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
        border-radius: 15px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }

    /* Success/Error Messages */
    .stSuccess {
        background: var(--success-gradient);
        color: white;
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(67, 233, 123, 0.4);
    }

    .stError {
        background: var(--warning-gradient);
        color: white;
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(250, 112, 154, 0.4);
    }

    .stInfo {
        background: var(--accent-gradient);
        color: white;
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
    }

    /* PDF Icons and Visual Elements */
    .pdf-icon {
        font-size: 4rem;
        background: var(--warning-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 1rem 0;
        animation: bounce 2s infinite;
    }

    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }

    /* Spinner Enhancement */
    .stSpinner > div {
        border-top-color: #667eea !important;
        animation: spin 1s linear infinite;
    }

    /* Progress Enhancement */
    .stProgress > div > div > div {
        background: var(--primary-gradient);
        border-radius: 10px;
    }

    /* Hide Streamlit Branding */
    .css-1rs6os {
        background: transparent;
    }
    
    .css-17eq0hr {
        background: transparent;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* Responsive Design */
    @media (max-width: 768px) {
        .header-banner h1 {
            font-size: 2.5rem;
        }
        .header-banner p {
            font-size: 1.1rem;
        }
    }

    /* Loading Animation */
    .loading-dots {
        display: inline-block;
        position: relative;
        width: 80px;
        height: 80px;
    }
    .loading-dots div {
        position: absolute;
        top: 33px;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background: #667eea;
        animation-timing-function: cubic-bezier(0, 1, 1, 0);
    }
</style>
""", unsafe_allow_html=True)

# --- API Configuration ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error("Error configuring the Generative AI model. Please ensure your GOOGLE_API_KEY is set correctly in secrets.toml.")
    st.stop()

# --- CORE FUNCTIONS ---
def extract_text_from_pdf(file_obj):
    try:
        pdf_document = fitz.open(stream=file_obj.read(), filetype="pdf")
        text = "".join(page.get_text() for page in pdf_document)
        return text
    except Exception as e:
        st.error(f"Error reading the PDF file: {e}")
        return None

def get_gemini_response(prompt, context):
    full_prompt = f"{prompt}\n\nHere is the document context:\n---\n{context}"
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred with the AI model: {e}")
        return None

# --- Enhanced UI Layout ---
st.markdown("""
<div class="header-banner">
    <h1>🧠 IntelliDoc AI</h1>
    <p>Your personal AI assistant for intelligent document analysis</p>
    <div class="pdf-icon">📄✨</div>
</div>
""", unsafe_allow_html=True)

# Sidebar with enhanced styling
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #667eea; font-weight: 700; margin-bottom: 1rem;">📂 Upload Document</h2>
        <div class="pdf-icon">📋</div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload your PDF here", 
        type="pdf", 
        label_visibility="collapsed",
        help="Drag and drop your PDF file here or click to browse"
    )
    
    st.markdown("""
    <div style="margin-top: 2rem; padding: 1rem; background: linear-gradient(135deg, rgba(67, 233, 123, 0.2) 0%, rgba(56, 249, 215, 0.2) 100%); border-radius: 15px; border-left: 4px solid #43e97b;">
        <p style="margin: 0; color: #2d3748; font-weight: 500;">
            🔒 Your document is analyzed securely and is not stored after you close this session.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main content area
if uploaded_file is not None:
    if 'document_text' not in st.session_state or st.session_state.get('file_name') != uploaded_file.name:
        with st.spinner('🔍 Reading and analyzing your PDF...'):
            document_text = extract_text_from_pdf(uploaded_file)
            if document_text:
                st.session_state['document_text'] = document_text
                st.session_state['file_name'] = uploaded_file.name
                # Clear previous summary when a new file is uploaded
                if 'summary' in st.session_state:
                    del st.session_state['summary']
                st.success(f"✅ Successfully processed **{uploaded_file.name}**")
            else:
                st.error("❌ Failed to extract text from the PDF.")
                st.stop()
else:
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; margin: 2rem 0;">
        <div class="pdf-icon" style="font-size: 6rem; margin-bottom: 2rem;">📄</div>
        <h3 style="color: #4a5568; margin-bottom: 1rem;">Welcome to IntelliDoc AI!</h3>
        <p style="color: #718096; font-size: 1.2rem;">Please upload a PDF document using the sidebar to begin your intelligent document analysis journey.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Enhanced tabs with icons
tab1, tab2 = st.tabs(["📄 Intelligent Summarization", "❓ Smart Q&A Assistant"])

with tab1:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #667eea; font-weight: 700;">✨ Generate an Intelligent Summary</h2>
        <p style="color: #718096;">Choose your preferred summary style and let AI do the magic!</p>
    </div>
    """, unsafe_allow_html=True)
    
    summary_type = st.radio(
        "Choose your summary style:",
        ("🎯 Concise Summary", "📚 Section-wise Summary", "• Key Bullet Points"),
        horizontal=True,
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("✨ Generate Summary", key="summarize", use_container_width=True):
            context = st.session_state.get('document_text', '')
            with st.spinner("🎨 Crafting your personalized summary..."):
                prompt_map = {
                    "🎯 Concise Summary": "Generate a concise, easy-to-read summary focusing on the main purpose and conclusions.",
                    "📚 Section-wise Summary": "Provide a summary for each major section. Use markdown headings for section titles.",
                    "• Key Bullet Points": "Extract the most important findings and conclusions as clear, concise bullet points."
                }
                summary = get_gemini_response(prompt_map[summary_type], context)
                if summary:
                    st.session_state['summary'] = summary
    
    if 'summary' in st.session_state:
        st.markdown(f'<div class="response-card">{st.session_state["summary"]}</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.download_button(
                label="📥 Download Summary (.txt)",
                data=st.session_state["summary"],
                file_name=f"{uploaded_file.name.replace('.pdf', '')}_summary.txt",
                mime="text/plain",
                use_container_width=True
            )

with tab2:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #667eea; font-weight: 700;">🤖 Ask Anything About Your Document</h2>
        <p style="color: #718096;">Get instant, intelligent answers from your document!</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_question = st.text_input(
        "💭 Enter your question here:", 
        key="qa_question", 
        placeholder="e.g., What were the main conclusions of the report?",
        label_visibility="collapsed"
    )
    
    if user_question:
        context = st.session_state.get('document_text', '')
        with st.spinner("🔍 Searching for the perfect answer..."):
            prompt = f"Based on the document provided, answer the following question: '{user_question}'. Provide a clear and direct answer. If possible, quote relevant parts of the document to support your answer."
            answer = get_gemini_response(prompt, context)
            if answer:
                st.markdown(f'<div class="response-card">{answer}</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 4rem; padding: 2rem; background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%); border-radius: 20px; backdrop-filter: blur(10px);">
    <p style="color: #718096; margin: 0;">Made with ❤️ using Streamlit & Google Generative AI</p>
</div>
""", unsafe_allow_html=True)