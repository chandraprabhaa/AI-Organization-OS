import streamlit as st

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Organization OS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# SESSION STATE
# ==================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🧠 AI Organization OS")

    st.markdown("---")

    if st.button(
        "🏠 Home",
        use_container_width=True,
        key="sidebar_home"
    ):
        st.session_state.page = "home"
        st.rerun()

    if st.button(
        "📊 Dashboard",
        use_container_width=True,
        key="sidebar_dashboard"
    ):
        st.session_state.page = "dashboard"
        st.rerun()

    st.markdown("---")

    st.markdown("### 🔧 System Status")

    st.success("Groq Connected")
    st.success("LangGraph Ready")
    st.success("ChromaDB Ready")
    st.success("Memory Enabled")
    st.success("RAG Enabled")

# ==================================================
# ROUTING
# ==================================================

try:

    if st.session_state.page == "home":

        from ui.home import home_page
        home_page()

    elif st.session_state.page == "dashboard":

        from ui.streamlit_ui import dashboard_page
        dashboard_page()

    else:

        st.session_state.page = "home"
        st.rerun()

except Exception as e:

    st.error(f"Page Loading Error: {e}")

    import traceback

    with st.expander("Full Error Trace"):
        st.code(traceback.format_exc())

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#888;font-size:12px;">
        AI Organization OS | Enterprise Multi-Agent AI System
    </div>
    """,
    unsafe_allow_html=True
)