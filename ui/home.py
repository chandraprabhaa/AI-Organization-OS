import streamlit as st

def home_page():
    """Home page with feature overview and launch button"""
    
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    
    h1, h2, h3 {
        color: #00ffe7 !important;
    }
    
    .feature-card {
        background: rgba(255,255,255,0.08);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(0,198,255,0.3);
        backdrop-filter: blur(15px);
        margin: 10px 0;
    }
    
    .feature-card h3 {
        margin-top: 0;
    }
    
    .stButton button {
        background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
        color: white !important;
        font-size: 20px;
        font-weight: bold;
        border-radius: 14px;
        height: 60px;
        width: 100%;
        border: none;
        margin-top: 20px;
    }
    
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(0,198,255,0.8);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main title
    st.markdown(
        "<h1 style='text-align:center; font-size:3em;'>🧠 AI Organization OS</h1>",
        unsafe_allow_html=True
    )
    
    st.markdown(
        "<h2 style='text-align:center;'>Enterprise Multi-Agent + RAG + Memory Platform</h2>",
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Feature overview in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>🤖 Active Agents</h3>
        <ul>
        <li><strong>Planner:</strong> Break down goals into execution plans</li>
        <li><strong>CEO:</strong> Create strategic direction</li>
        <li><strong>Research:</strong> Conduct market research with RAG</li>
        <li><strong>Analyst:</strong> Analyze findings and opportunities</li>
        <li><strong>Critic:</strong> Validate outputs and detect hallucinations</li>
        <li><strong>QA:</strong> Final quality assurance and consolidation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3>🔍 Intelligence Layer</h3>
        <ul>
        <li><strong>PDF Upload:</strong> Import documents into knowledge base</li>
        <li><strong>Chunking:</strong> Automatic document segmentation</li>
        <li><strong>Embeddings:</strong> Sentence Transformers for semantic search</li>
        <li><strong>ChromaDB:</strong> Vector database persistence</li>
        <li><strong>RAG Retrieval:</strong> Intelligent context retrieval</li>
        <li><strong>Smart Memory:</strong> Persistent memory system</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
        <h3>📄 Reporting Layer</h3>
        <ul>
        <li><strong>Executive Reports:</strong> Comprehensive business analysis</li>
        <li><strong>Multi-Format Export:</strong> Markdown, HTML, PDF, Text</li>
        <li><strong>Validation Scores:</strong> Quality metrics from Critic</li>
        <li><strong>Memory Integration:</strong> Learn from past analyses</li>
        <li><strong>Real-time Dashboard:</strong> Monitor workflow progress</li>
        <li><strong>PDF Export:</strong> Professional report generation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key features
    st.markdown("<h2>✨ Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Complete AI Workflow**
        - Automated multi-agent analysis pipeline
        - Each agent has specific expertise
        - Sequential execution with context passing
        - Real-time progress updates
        
        **💾 Persistent Memory**
        - ChromaDB-backed memory system
        - Stores all reports and analyses
        - Intelligent memory retrieval
        - Learn from past decisions
        
        **🔬 Advanced RAG**
        - PDF document ingestion
        - Semantic chunking
        - Vector similarity search
        - Source tracking and attribution
        """)
    
    with col2:
        st.markdown("""
        **📊 Professional Reporting**
        - Multiple export formats
        - Rich HTML formatting
        - PDF generation with reportlab
        - Executive summary + detailed analysis
        
        **🛡️ Quality Assurance**
        - Critic agent validates outputs
        - Hallucination detection
        - Evidence quality scoring
        - Cross-validation of results
        
        **⚡ Groq Integration**
        - Fast, reliable LLM inference
        - Llama 3.3 70B model
        - Automatic error recovery
        - Production-ready architecture
        """)
    
    st.markdown("---")
    
    # How it works
    st.markdown("<h2>🔄 How It Works</h2>", unsafe_allow_html=True)
    
    workflow_steps = """
    1. **User Input** → You provide a business goal
    2. **Planner** → Breaks goal into execution plan
    3. **CEO** → Creates strategic direction
    4. **Research** → Conducts market research with RAG
    5. **Analyst** → Analyzes research findings
    6. **Critic** → Validates quality and detects hallucinations
    7. **QA** → Final quality review and consolidation
    8. **Export** → Generate professional reports in multiple formats
    """
    
    st.info(workflow_steps)
    
    # Launch button
    st.markdown("---")
    
    if st.button("🚀 Launch AI Organization OS Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()
    
    # Technical stack
    st.markdown("---")
    st.markdown("<h3>🛠️ Technical Stack</h3>", unsafe_allow_html=True)
    
    tech_stack = """
    - **LLM**: Groq (Llama 3.3 70B)
    - **Workflow Engine**: LangGraph
    - **RAG Framework**: LangChain
    - **Vector Database**: ChromaDB
    - **Embeddings**: Sentence Transformers
    - **UI**: Streamlit
    - **PDF Export**: ReportLab
    - **Python**: 3.8+
    """
    
    col1, col2 = st.columns(2)
    with col1:
        st.code(tech_stack, language="markdown")
    
    with col2:
        st.markdown("""
        **Project Structure**
        - agents/ → 6 specialized agents
        - workflow/ → LangGraph orchestration
        - rag/ → Document ingestion & retrieval
        - memory/ → Persistent memory system
        - reports/ → Report generation
        - ui/ → Streamlit dashboard
        - config/ → LLM & system config
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#d0d7da; font-size:12px;'>"
        "AI Organization OS v1.0 | "
        "Multi-Agent Enterprise AI System | "
        "© 2026"
        "</p>",
        unsafe_allow_html=True
    )
