from langchain_core.prompts import PromptTemplate
from config.llm import llm
from rag.retriever import get_retriever

def perform_research(strategy: str):
    """
    Research Agent: Conducts market research using RAG-based knowledge base.
    
    Args:
        strategy: The CEO's strategic output
        
    Returns:
        Detailed research report
    """
    
    try:
        # Load retriever from ChromaDB
        retriever = get_retriever()
        
        # Retrieve relevant documents
        docs = retriever.invoke(strategy)
        
        # Combine retrieved chunks with metadata
        context = "\\n\\n".join(
            [f"[Source: {doc.metadata.get('source', 'Unknown')}]\\n{doc.page_content}" 
             for doc in docs]
        ) if docs else "No documents found in knowledge base."
        
    except Exception as e:
        print(f"Warning: Could not retrieve from RAG: {e}")
        context = "Knowledge base unavailable - proceeding with general research."

    prompt = PromptTemplate(
        input_variables=["strategy", "context"],
        template="""You are a professional market research analyst specializing in AI/tech.

Business Strategy:
{strategy}

Knowledge Base Context:
{context}

Conduct comprehensive research and generate a detailed report including:

1. MARKET OVERVIEW
   - Industry landscape
   - Market size and growth
   - Key market players

2. COMPETITIVE ANALYSIS
   - Direct competitors
   - Competitive advantages
   - Market positioning

3. INDUSTRY TRENDS
   - Emerging technologies
   - Market shifts
   - Future outlook

4. OPPORTUNITIES
   - Market gaps
   - Growth vectors
   - Strategic opportunities

5. CHALLENGES & THREATS
   - Market barriers
   - Regulatory considerations
   - Technical challenges

6. KEY FINDINGS
   - Critical insights
   - Data-backed conclusions
   - Recommendations

7. RESEARCH SOURCES
   - Documents consulted
   - Confidence levels
   - Data quality assessment

Use the knowledge base context wherever relevant. If specific data points are unavailable, 
note this clearly and provide general industry insights instead.
"""
    )

    chain = prompt | llm

    result = chain.invoke({
        "strategy": strategy,
        "context": context
    })

    return result.content
