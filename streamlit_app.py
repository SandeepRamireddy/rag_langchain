import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Must be first Streamlit command
st.set_page_config(
    page_title="SuperB — AI Chat & Document Q&A",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Premium CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    /* ── Global ── */
    html, body, [class*="st-"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Hide default Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Animated background shimmer on main area ── */
    .stApp {
        background: #0a0a0f;
    }

    /* ── Chat messages ── */
    .stChatMessage {
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.06);
        backdrop-filter: blur(12px);
        background: rgba(255,255,255,0.03) !important;
    }

    /* Force readable text in chat area */
    .stChatMessage p,
    .stChatMessage span,
    .stChatMessage li,
    .stChatMessage div,
    .stChatMessage h1,
    .stChatMessage h2,
    .stChatMessage h3,
    .stChatMessage h4 {
        color: #e8eaf6 !important;
    }
    .stChatMessage strong {
        color: #ffffff !important;
    }
    .stChatMessage code {
        color: #c5cae9 !important;
        background: rgba(255,255,255,0.06) !important;
    }
    .stChatMessage a {
        color: #a5b4fc !important;
    }

    /* Main area text readability */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #d1d5db !important;
    }
    .stMarkdown strong {
        color: #f1f5f9 !important;
    }
    .stCaption, .stCaption p {
        color: #94a3b8 !important;
    }

    /* ── Sidebar: deep glass effect ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(165deg, #0d0d1a 0%, #111128 40%, #0f0f20 100%) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.15);
    }
    section[data-testid="stSidebar"] * {
        color: #c8cdf3 !important;
    }

    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a78bfa 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        font-size: 0.9rem;
        width: 100%;
        letter-spacing: 0.02em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45);
    }
    section[data-testid="stSidebar"] .stButton > button:active {
        transform: translateY(0px) scale(0.99);
    }

    /* ── Sidebar brand logo ── */
    .sidebar-brand {
        text-align: center;
        padding: 1.5rem 0 0.5rem;
    }
    .sidebar-brand .logo {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    .sidebar-brand .tagline {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        opacity: 0.5;
        margin-top: 2px;
    }

    /* ── Section headers in sidebar ── */
    .sidebar-section {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        opacity: 0.45;
        margin: 1.5rem 0 0.5rem;
        padding-left: 2px;
    }

    /* ── Status cards: glassmorphism ── */
    .status-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 8px 0;
    }
    .glass-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 14px 16px;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        background: rgba(255,255,255,0.06);
        border-color: rgba(99, 102, 241, 0.25);
        transform: translateY(-1px);
    }
    .glass-card .card-label {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        opacity: 0.5;
    }
    .glass-card .card-value {
        font-size: 1.4rem;
        font-weight: 700;
        margin-top: 4px;
        background: linear-gradient(135deg, #e0e7ff, #c7d2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Pulse dot for live index */
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.3); }
    }
    .pulse-dot {
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 2s ease-in-out infinite;
    }
    .pulse-dot.live { background: #34d399; box-shadow: 0 0 8px rgba(52, 211, 153, 0.5); }
    .pulse-dot.off  { background: #f87171; box-shadow: 0 0 8px rgba(248, 113, 113, 0.3); animation: none; }

    /* ── Hero section ── */
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .hero {
        text-align: center;
        padding: 3rem 0 1.5rem;
    }
    .hero .icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    .hero h1 {
        background: linear-gradient(135deg, #818cf8, #a78bfa, #c084fc, #f472b6, #818cf8);
        background-size: 300% 300%;
        animation: gradientShift 6s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 0.3rem;
    }
    .hero .subtitle {
        color: #64748b;
        font-size: 1.05rem;
        font-weight: 400;
        max-width: 500px;
        margin: 0 auto;
        line-height: 1.5;
    }

    /* ── Feature pills ── */
    .feature-pills {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 1.2rem;
        flex-wrap: wrap;
    }
    .pill {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 100px;
        padding: 6px 16px;
        font-size: 0.78rem;
        color: #a5b4fc;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .pill:hover {
        background: rgba(99, 102, 241, 0.15);
        border-color: rgba(99, 102, 241, 0.4);
    }

    /* ── Answer badge ── */
    .answer-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 100px;
        margin-top: 6px;
        letter-spacing: 0.03em;
    }
    .badge-rag {
        background: rgba(99, 102, 241, 0.12);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.25);
    }
    .badge-generic {
        background: rgba(52, 211, 153, 0.1);
        color: #6ee7b7;
        border: 1px solid rgba(52, 211, 153, 0.25);
    }

    /* ── Expander styling ── */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* ── Divider ── */
    .sidebar-divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin: 1rem 0;
    }

    /* ── File list items ── */
    .file-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 10px;
        margin: 3px 0;
        border-radius: 8px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.05);
        font-size: 0.78rem;
        color: #c8cdf3;
        transition: all 0.2s ease;
    }
    .file-item:hover {
        background: rgba(255,255,255,0.06);
        border-color: rgba(248, 113, 113, 0.3);
    }
    .file-icon {
        font-size: 1rem;
        flex-shrink: 0;
    }
    .file-name {
        flex: 1;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .file-size {
        font-size: 0.65rem;
        opacity: 0.5;
        flex-shrink: 0;
    }

    /* ── Chat input ── */
    .stChatInput {
        border-color: rgba(99, 102, 241, 0.3) !important;
    }
    .stChatInput:focus-within {
        border-color: rgba(99, 102, 241, 0.6) !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Helpers ─────────────────────────────────────────────────────────────────
DATA_DIR = "rag_data"
FAISS_DIR = "faiss_store"


def get_index_status():
    """Check if FAISS index files exist."""
    faiss_path = os.path.join(FAISS_DIR, "faiss.index")
    meta_path = os.path.join(FAISS_DIR, "metadata.pkl")
    return os.path.exists(faiss_path) and os.path.exists(meta_path)


def count_data_files():
    """Count supported files in rag_data/."""
    return len(list_data_files())


def list_data_files():
    """List all supported files in rag_data/."""
    extensions = ["*.pdf", "*.txt", "*.csv", "*.xlsx", "*.docx", "*.json"]
    data_path = Path(DATA_DIR)
    if not data_path.exists():
        return []
    files = []
    for ext in extensions:
        files.extend(data_path.glob(f"**/{ext}"))
    return sorted(files)


@st.cache_resource(show_spinner=False)
def load_rag_search():
    """Load RAGSearch once and cache it across reruns."""
    from src.search import RAGSearch
    return RAGSearch()


def rebuild_index():
    """Rebuild the FAISS index from documents in rag_data/."""
    from src.data_loader import load_all_documents
    from src.vectorstore import FaissVectorStore

    docs = load_all_documents(DATA_DIR)
    if not docs:
        st.sidebar.error("No documents found in `rag_data/`.")
        return False

    store = FaissVectorStore(FAISS_DIR)
    store.build_from_documents(docs)
    # Clear cached RAGSearch so it picks up the new index
    load_rag_search.clear()
    return True


# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown("""
    <div class="sidebar-brand">
        <div class="logo">⚡ SuperB</div>
        <div class="tagline">Intelligent Document Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # Upload section
    st.markdown('<div class="sidebar-section">📁 Document Upload</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload documents",
        accept_multiple_files=True,
        type=["pdf", "txt", "csv", "xlsx", "docx", "json"],
        help="Supported: PDF, TXT, CSV, XLSX, DOCX, JSON",
        label_visibility="collapsed",
    )

    if uploaded_files:
        os.makedirs(DATA_DIR, exist_ok=True)
        saved = 0
        for f in uploaded_files:
            dest = os.path.join(DATA_DIR, f.name)
            with open(dest, "wb") as out:
                out.write(f.getbuffer())
            saved += 1
        st.success(f"✅ {saved} file(s) uploaded")

    # Rebuild button
    st.markdown("")
    if st.button("⚡  Build Knowledge Index", use_container_width=True):
        with st.spinner("Embedding documents & building index..."):
            ok = rebuild_index()
        if ok:
            st.success("✅ Index ready!")
            st.rerun()

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # Status dashboard
    st.markdown('<div class="sidebar-section">📊 System Status</div>', unsafe_allow_html=True)

    n_files = count_data_files()
    idx_ready = get_index_status()

    dot_class = "live" if idx_ready else "off"
    idx_label = "Live" if idx_ready else "Offline"

    st.markdown(
        f"""
        <div class="status-grid">
            <div class="glass-card">
                <div class="card-label">Documents</div>
                <div class="card-value">{n_files}</div>
            </div>
            <div class="glass-card">
                <div class="card-label">Index</div>
                <div class="card-value"><span class="pulse-dot {dot_class}"></span>{idx_label}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not idx_ready:
        st.info("Upload documents and build the index to enable document Q&A.")

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # ── Manage Documents ──
    st.markdown('<div class="sidebar-section">🗂️ Manage Documents</div>', unsafe_allow_html=True)

    data_files = list_data_files()
    if data_files:
        # Map file extensions to icons
        ext_icons = {
            ".pdf": "📕", ".txt": "📝", ".csv": "📊",
            ".xlsx": "📗", ".docx": "📘", ".json": "📋",
        }

        # Multiselect for deletion
        file_options = [f.name for f in data_files]
        files_to_delete = st.multiselect(
            "Select files to remove",
            options=file_options,
            default=[],
            label_visibility="collapsed",
            placeholder="Select files to remove...",
        )

        # Show file list with icons
        for f in data_files:
            icon = ext_icons.get(f.suffix.lower(), "📄")
            size_kb = f.stat().st_size / 1024
            size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"
            st.markdown(
                f'<div class="file-item">'
                f'<span class="file-icon">{icon}</span>'
                f'<span class="file-name">{f.name}</span>'
                f'<span class="file-size">{size_str}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        # Delete button
        if files_to_delete:
            if st.button(
                f"🗑️  Remove {len(files_to_delete)} file(s) & Rebuild",
                use_container_width=True,
                type="primary",
            ):
                # Delete selected files
                deleted = 0
                for fname in files_to_delete:
                    fpath = Path(DATA_DIR) / fname
                    if fpath.exists():
                        fpath.unlink()
                        deleted += 1

                st.success(f"🗑️ Removed {deleted} file(s)")

                # Auto-rebuild if there are remaining files
                remaining = list_data_files()
                if remaining:
                    with st.spinner("Rebuilding index without deleted files..."):
                        rebuild_index()
                    st.success("✅ Index rebuilt!")
                else:
                    # No files left — remove the FAISS index too
                    import shutil
                    if os.path.exists(FAISS_DIR):
                        shutil.rmtree(FAISS_DIR)
                        os.makedirs(FAISS_DIR, exist_ok=True)
                    load_rag_search.clear()
                    st.info("All documents removed. Index cleared.")

                st.rerun()
    else:
        st.caption("No documents uploaded yet.")

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # Clear chat
    st.markdown('<div class="sidebar-section">🧹 Session</div>', unsafe_allow_html=True)
    if st.button("🗑️  Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ── Hero Section ────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <span class="icon">⚡</span>
        <h1>SuperB</h1>
        <div class="subtitle">
            Your intelligent AI assistant — answers general questions instantly
            and searches your documents when you need it.
        </div>
        <div class="feature-pills">
            <span class="pill">💬 General Chat</span>
            <span class="pill">📄 Document Q&A</span>
            <span class="pill">🔍 Smart Routing</span>
            <span class="pill">⚡ Powered by Gemini</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render past messages
for msg in st.session_state.messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "⚡"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("query_type"):
            if msg["query_type"] == "rag":
                st.markdown(
                    '<span class="answer-badge badge-rag">📄 Document Answer</span>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<span class="answer-badge badge-generic">💬 General Answer</span>',
                    unsafe_allow_html=True,
                )
        if msg.get("sources"):
            with st.expander("📄 Retrieved Sources", expanded=False):
                for i, src in enumerate(msg["sources"], 1):
                    st.markdown(f"**Chunk {i}:**")
                    st.code(src[:500], language=None)

# Chat input
if prompt := st.chat_input("Ask SuperB anything..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Generate answer
    with st.chat_message("assistant", avatar="⚡"):
        rag = load_rag_search() if idx_ready else None

        # Classify the query
        if rag:
            with st.spinner("🧠 Understanding your question..."):
                query_type = rag.classify_query(prompt)
        else:
            query_type = "generic"

        if query_type == "rag" and not idx_ready:
            answer = "⚠️ No index found. Please upload documents and click **Build Knowledge Index** in the sidebar first."
            sources = []
            st.warning(answer)
        elif query_type == "rag":
            with st.spinner("🔍 Searching your documents..."):
                # Get raw search results for sources
                results = rag.vectorstore.query(prompt, top_k=3)
                sources = [
                    r["metadata"].get("text", "")
                    for r in results
                    if r["metadata"]
                ]

                # Get LLM summary with context
                answer = rag.search_and_summarize(prompt, top_k=3)

            st.markdown(answer)
            st.markdown(
                '<span class="answer-badge badge-rag">📄 Document Answer</span>',
                unsafe_allow_html=True,
            )

            if sources:
                with st.expander("📄 Retrieved Sources", expanded=False):
                    for i, src in enumerate(sources, 1):
                        st.markdown(f"**Chunk {i}:**")
                        st.code(src[:500], language=None)
        else:
            # Generic question — answer directly without document retrieval
            sources = []
            with st.spinner("⚡ SuperB is thinking..."):
                if rag:
                    answer = rag.answer_generic(prompt)
                else:
                    # No index built yet — use LLM directly for generic answers
                    from langchain.chat_models import init_chat_model
                    llm = init_chat_model("google_genai:gemini-3-flash-preview")
                    answer = llm.invoke([
                        f"You are a helpful, friendly AI assistant named SuperB. Answer the user's question "
                        f"clearly and concisely.\n\nUser question: {prompt}\n\nAnswer:"
                    ]).text()

            st.markdown(answer)
            st.markdown(
                '<span class="answer-badge badge-generic">💬 General Answer</span>',
                unsafe_allow_html=True,
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "query_type": query_type,
    })
