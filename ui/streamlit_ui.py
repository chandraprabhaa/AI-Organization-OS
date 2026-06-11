import streamlit as st
import html
import tempfile
from pathlib import Path
from datetime import datetime

from workflow.graph import graph
from reports.generator import Report, create_report
from reports.pdf_export import PDFReportGenerator
from memory.persistent_memory import MemoryManager
from rag.ingest import ingest_document, get_collection_stats
from rag.retriever import get_retrieval_stats

def dashboard_page():
    """Main dashboard page with all AI OS features"""
    
    # CSS Styling
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    
    h1 {
        color: white !important;
        text-align: center;
        font-size: 2.5em !important;
    }
    
    h2 {
        color: #00ffe7 !important;
        text-align: left !important;
    }
    
    h3 {
        color: #00ffe7 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        color: white;
    }
    
    textarea {
        background-color: rgba(0,0,0,0.45) !important;
        color: white !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        font-size: 16px !important;
    }
    
    textarea::placeholder {
        color: #d0d7da !important;
    }
    
    label {
        color: white !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    
    .stButton button {
        background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
        color: white !important;
        font-size: 18px;
        font-weight: bold;
        border-radius: 14px;
        height: 55px;
        width: 100%;
        border: none;
    }
    
    .stButton button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 20px rgba(0,198,255,0.6);
    }
    
    .card {
        background: rgba(255,255,255,0.08);
        padding: 20px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(15px);
        color: white;
        line-height: 1.7;
        margin-bottom: 20px;
    }
    
    .success-card {
        background: rgba(0, 255, 150, 0.1);
        border: 1px solid rgba(0, 255, 150, 0.3);
    }
    
    .info-card {
        background: rgba(0, 198, 255, 0.1);
        border: 1px solid rgba(0, 198, 255, 0.3);
    }
    
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("<h1>🧠 AI Organization OS Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:#d0d7da; font-size:20px;'>Multi-Agent AI Business Intelligence System</p>",
        unsafe_allow_html=True
    )
    
    # Initialize session state
    if "workflow_result" not in st.session_state:
        st.session_state.workflow_result = None
    if "report" not in st.session_state:
        st.session_state.report = None
    
    # Main tabs
    main_tabs = st.tabs([
        "📌 Execute Workflow",
        "🧠 Planning & Strategy",
        "🔍 Research & Analysis",
        "✅ Validation & QA",
        "📂 Knowledge Base",
        "💾 Memory Dashboard",
        "📄 Reports & Export"
    ])
    
    # ============ TAB 1: Execute Workflow ============
    with main_tabs[0]:
        st.markdown("## Enter Business Goal")
        
        goal = st.text_area(
            "Business Goal",
            placeholder="Example: Build an AI healthcare startup using SaaS model with focus on diagnostic assistance",
            height=150,
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Run Full AI System", use_container_width=True):
                if not goal:
                    st.warning("Please enter a business goal")
                else:
                    with st.spinner("🧠 AI Agents are working... This may take 2-3 minutes..."):
                        try:
                            result = graph.invoke({"user_goal": goal})
                            st.session_state.workflow_result = result
                            st.session_state.report = create_report(result)
                            st.success("✨ Analysis Complete!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        
        with col2:
            if st.button("📚 Use Sample Goal", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
        
        if st.session_state.workflow_result:
            st.markdown("---")
            st.success("Workflow execution completed successfully! Check other tabs for results.")
    
    # ============ TAB 2: Planning & Strategy ============
    with main_tabs[1]:
        if st.session_state.workflow_result:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📋 Execution Plan")
                st.markdown(f"""
                <div class="card info-card">
                {html.escape(st.session_state.workflow_result.get("plan", "No plan generated"))}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 🎯 CEO Strategy")
                st.markdown(f"""
                <div class="card success-card">
                {html.escape(st.session_state.workflow_result.get("strategy", "No strategy generated"))}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Run the workflow first to see planning outputs.")
    
    # ============ TAB 3: Research & Analysis ============
    with main_tabs[2]:
        if st.session_state.workflow_result:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🔍 Market Research")
                st.markdown(f"""
                <div class="card">
                {html.escape(st.session_state.workflow_result.get("research", "No research conducted"))}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 📊 Business Analysis")
                st.markdown(f"""
                <div class="card">
                {html.escape(st.session_state.workflow_result.get("analyst_output", "No analysis generated"))}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Run the workflow first to see research and analysis outputs.")
    
    # ============ TAB 4: Validation & QA ============
    with main_tabs[3]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✔️ Critical Review")
            if st.session_state.workflow_result:
                st.markdown(f"""
                <div class="card">
                {html.escape(st.session_state.workflow_result.get("critic_output", "No critique generated"))}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Run workflow to see critic output.")
        
        with col2:
            st.markdown("### ✅ Quality Assurance")
            if st.session_state.workflow_result:
                st.markdown(f"""
                <div class="card success-card">
                {html.escape(st.session_state.workflow_result.get("qa_output", "No QA review conducted"))}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Run workflow to see QA output.")
    
    # ============ TAB 5: Knowledge Base ============
    with main_tabs[4]:
        st.markdown("## 📚 Knowledge Base Management")
        
        sub_tabs = st.tabs(["Upload PDFs", "Collection Stats", "Retrieval Test"])
        
        with sub_tabs[0]:
            st.markdown("### Upload PDF Documents")
            uploaded_files = st.file_uploader(
                "Upload PDF files",
                type="pdf",
                accept_multiple_files=True,
                help="Upload documents to build your knowledge base"
            )
            
            if uploaded_files and st.button("📥 Ingest Documents"):
                with st.spinner("Ingesting documents..."):
                    for file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            tmp.write(file.getbuffer())
                            tmp_path = tmp.name
                            
                            result = ingest_document(tmp_path)
                            
                            if result.get("status") == "success":
                                st.success(f"✅ {file.name}: {result['chunks']} chunks created")
                            else:
                                st.error(f"❌ {file.name}: {result.get('error')}")
                            
                            Path(tmp_path).unlink()
        
        with sub_tabs[1]:
            st.markdown("### Collection Statistics")
            try:
                stats = get_collection_stats()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Documents in Collection", stats.get("document_count", 0))
                with col2:
                    st.metric("Collection Status", stats.get("status", "unknown").upper())
                
                st.info(f"Embedding Model: Sentence Transformers (all-MiniLM-L6-v2)")
            except Exception as e:
                st.error(f"Could not retrieve stats: {str(e)}")
        
        with sub_tabs[2]:
            st.markdown("### Test Retrieval")
            test_query = st.text_input("Enter a test query to retrieve relevant documents:")
            
            if test_query and st.button("🔎 Test Retrieval"):
                try:
                    from rag.retriever import retrieve_documents
                    results = retrieve_documents(test_query, k=3)
                    
                    st.markdown(f"**Found {len(results)} relevant documents:**")
                    for i, (doc, score) in enumerate(results):
                        with st.expander(f"Result {i+1} (Relevance: {score:.2f})"):
                            st.write(doc.page_content)
                except Exception as e:
                    st.error(f"Retrieval failed: {str(e)}")
    
    # ============ TAB 6: Memory Dashboard ============
    with main_tabs[5]:
        st.markdown("## 💾 Persistent Memory System")
        
        memory_mgr = MemoryManager()
        stats = memory_mgr.get_memory_stats()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Memories", stats.get("total_memories", 0))
        with col2:
            st.metric("Reports Stored", len(stats.get("by_type", {}).get("reports", [])))
        with col3:
            st.metric("Critiques Stored", len(stats.get("by_type", {}).get("critiques", [])))
        
        sub_tabs = st.tabs(["Recent Memories", "Search Memory", "Clear Memory"])
        
        with sub_tabs[0]:
            memory_type = st.selectbox("Memory Type", ["reports", "critiques", "plans", "queries"])
            recent = memory_mgr.get_recent_memories(memory_type, limit=5)
            
            if recent:
                for memory in recent:
                    st.write(f"• {memory['timestamp'][:10]} - {memory['query'][:60]}...")
            else:
                st.info(f"No {memory_type} stored yet")
        
        with sub_tabs[1]:
            search_term = st.text_input("Search memory:")
            if search_term and st.button("🔍 Search"):
                results = memory_mgr.search_memory(search_term, limit=3)
                if results:
                    st.markdown(results)
                else:
                    st.info("No matching memories found")
        
        with sub_tabs[2]:
            if st.button("🗑️ Clear All Memories (Careful!)"):
                memory_mgr.clear_memory()
                st.success("All memories cleared")
    
    # ============ TAB 7: Reports & Export ============
    with main_tabs[6]:
        st.markdown("## 📄 Report Generation & Export")
        
        if st.session_state.report:
            export_format = st.selectbox(
                "Select Export Format",
                ["Markdown", "HTML", "PDF", "Text"],
                help="Choose the format for your report"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if export_format == "Markdown":
                    content = st.session_state.report.to_markdown()
                    st.download_button(
                        "📥 Download Markdown",
                        content,
                        f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        "text/markdown"
                    )
                    with st.expander("Preview Markdown"):
                        st.markdown(content)
                
                elif export_format == "Text":
                    content = st.session_state.report.to_text()
                    st.download_button(
                        "📥 Download Text",
                        content,
                        f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        "text/plain"
                    )
                    with st.expander("Preview Text"):
                        st.text(content[:2000] + "\n...[truncated]")
                
                elif export_format == "HTML":
                    content = st.session_state.report.to_html()
                    st.download_button(
                        "📥 Download HTML",
                        content,
                        f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        "text/html"
                    )
                    st.success("HTML report ready for download")
                
                elif export_format == "PDF":
                    if st.button("🔄 Generate PDF"):
                        with st.spinner("Generating PDF..."):
                            try:
                                generator = PDFReportGenerator()
                                pdf_buffer = generator.generate_pdf(st.session_state.report)
                                
                                st.download_button(
                                    "📥 Download PDF",
                                    pdf_buffer,
                                    f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                    "application/pdf"
                                )
                            except Exception as e:
                                st.error(f"PDF generation failed: {str(e)}")
            
            with col2:
                st.markdown("### Report Summary")
                st.info(f"**Goal:** {st.session_state.report.business_goal[:100]}...")
                st.info(f"**Generated:** {st.session_state.report.timestamp}")
                st.info(f"**Format:** {export_format}")
        
        else:
            st.info("Run the workflow first to generate reports")
