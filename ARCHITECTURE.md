# AI Organization OS - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         STREAMLIT UI                             │
│  (Home Page | Dashboard | Tabs for all features)                │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW ORCHESTRATION                        │
│              (LangGraph State Machine)                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Planner → CEO → Research → Analyst → Critic → QA      │   │
│  │  (Sequential execution with state passing)             │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────┬──────────────────────────────────┬────────────────┘
               │                                  │
        ┌──────▼──────┐                    ┌─────▼──────┐
        │   AGENTS     │                    │   MEMORY   │
        │  (6 agents)  │                    │  SYSTEM    │
        └──────┬──────┘                    └─────┬──────┘
               │                                  │
    ┌──────────▼──────────┐         ┌────────────▼──────────┐
    │ Planner Agent       │         │ ChromaDB Memory DB    │
    │ CEO Agent           │         │ • Reports             │
    │ Research Agent      │         │ • Critiques           │
    │ Analyst Agent       │         │ • Plans               │
    │ Critic Agent        │         │ • Queries             │
    │ QA Agent            │         └──────────────────────┘
    │                     │
    │ (Each uses Groq)    │
    └────────────┬────────┘
                 │
         ┌───────▼──────────┐
         │   RAG SYSTEM     │
         │ ┌──────────────┐ │
         │ │ Ingest       │ │
         │ │ Chunking     │ │
         │ │ Embeddings   │ │
         │ │ Retrieval    │ │
         │ └──────────────┘ │
         └────────┬─────────┘
                  │
          ┌───────▼──────────┐
          │ ChromaDB RAG DB  │
          │ • Documents      │
          │ • Chunks         │
          │ • Embeddings     │
          └──────────────────┘
```

## Component Architecture

### 1. **UI Layer** (Streamlit)
- `ui/home.py` - Home page with features overview
- `ui/streamlit_ui.py` - Main dashboard with 7 tabs
- `app.py` - Entry point and routing

**Responsibilities:**
- User input collection
- Workflow execution initiation
- Results visualization
- Report export UI

### 2. **Workflow Layer** (LangGraph)
- `workflow/graph.py` - Complete workflow orchestration

**Execution Flow:**
```
Input → Planner → CEO → Research → Analyst → Critic → QA → Output
```

**Features:**
- Sequential agent execution
- State passing between agents
- Error recovery
- Output formatting

### 3. **Agent Layer** (LLM-based)

#### Planner Agent (`agents/planner_agent.py`)
- **Purpose**: Break down goals into execution plans
- **Input**: Business goal
- **Output**: Structured execution plan
- **LLM**: Groq Llama 3.3 70B (creative mode)
- **Prompt**: Strategic planning template

#### CEO Agent (`agents/ceo_agent.py`)
- **Purpose**: Create business strategy
- **Input**: Business goal + Planner context
- **Output**: Strategic direction
- **LLM**: Groq Llama 3.3 70B
- **Prompt**: Executive strategy template

#### Research Agent (`agents/research_agent.py`)
- **Purpose**: Market research using RAG
- **Input**: CEO strategy
- **Output**: Research findings
- **LLM**: Groq Llama 3.3 70B
- **Prompt**: Research analyst template
- **RAG**: Retrieves documents from ChromaDB

#### Analyst Agent (`agents/analyst_agent.py`)
- **Purpose**: Business analysis
- **Input**: Research findings
- **Output**: SWOT, opportunities, risks
- **LLM**: Groq Llama 3.3 70B
- **Prompt**: Business analyst template

#### Critic Agent (`agents/critic_agent.py`)
- **Purpose**: Validation and quality assessment
- **Input**: All previous outputs
- **Output**: Critique with scores
- **LLM**: Groq Llama 3.3 70B
- **Prompt**: Critical reviewer template
- **Functions**: Hallucination detection, evidence validation

#### QA Agent (`agents/qa_agent.py`)
- **Purpose**: Final quality assurance
- **Input**: All outputs
- **Output**: Final QA report
- **LLM**: Groq Llama 3.3 70B
- **Prompt**: QA consultant template
- **Functions**: Consistency checks, readiness assessment

### 4. **Intelligence Layer** (RAG + Memory)

#### RAG System
```
PDF Input → Ingestion → Chunking → Embedding → ChromaDB
                                                    ↓
                              Query → Embedding → Similarity Search
```

**Components:**
- `rag/ingest.py` - Document ingestion
  - PyPDF loader
  - Recursive text splitting
  - Batch embedding

- `rag/retriever.py` - Document retrieval
  - Similarity search
  - K-NN retrieval
  - Score ranking

**Configuration:**
- Chunk size: 1000 chars
- Overlap: 200 chars
- Embedding model: Sentence Transformers (all-MiniLM-L6-v2)
- Retrieval k: 4 documents

#### Memory System
```
Agent Output → Save to Memory → ChromaDB Vector Store
                                        ↓
              Query → Semantic Search → Retrieve Past Similar
```

**Components:**
- `memory/persistent_memory.py` - Memory management
  - Save operations
  - Search operations
  - Retrieval operations
  - Statistics tracking

**Storage:**
- Type: ChromaDB with embeddings
- Collections: reports, critiques, plans, queries
- Index: Local JSON metadata
- Persistence: Disk-based

### 5. **Reporting Layer**

#### Report Generation
- `reports/generator.py` - Report models and formatting
  - Markdown export
  - HTML export
  - Text export
  - Data models

#### PDF Export
- `reports/pdf_export.py` - Professional PDF generation
  - ReportLab implementation
  - Custom styling
  - Table formatting
  - Metadata inclusion

### 6. **Configuration Layer**

#### LLM Configuration (`config/llm.py`)
```python
llm (main)     → Llama 3.3 70B, temp=0.3
llm_fast       → Llama 3.1 8B, temp=0.2 (for speed)
llm_creative   → Llama 3.3 70B, temp=0.7 (for brainstorming)
```

#### System Configuration (`utils/config.py`)
- Paths and directories
- RAG settings
- Memory settings
- LLM settings
- Workflow settings
- Report settings

## Data Flow Diagram

```
┌──────────────┐
│ User Input   │
│ (Goal)       │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Memory Search        │ ◄─────── Search past similar goals
│ (Retrieve Context)   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ WORKFLOW EXECUTION   │
│                      │
│ ┌────────────────┐   │
│ │ Planner        │   │
│ │ Input: Goal    │   │
│ │ Output: Plan   │   │
│ └────────┬───────┘   │
│          │            │
│          ▼            │
│ ┌────────────────┐   │
│ │ CEO            │   │
│ │ Input: Plan    │   │
│ │ Output: Strat  │   │
│ └────────┬───────┘   │
│          │            │
│          ▼            │
│ ┌────────────────┐   │
│ │ Research       │◄──┼─ RAG Retrieval from ChromaDB
│ │ Input: Strat   │   │
│ │ Output: Data   │   │
│ └────────┬───────┘   │
│          │            │
│          ▼            │
│ ┌────────────────┐   │
│ │ Analyst        │   │
│ │ Input: Data    │   │
│ │ Output: Anal   │   │
│ └────────┬───────┘   │
│          │            │
│          ▼            │
│ ┌────────────────┐   │
│ │ Critic         │   │
│ │ Input: All     │   │
│ │ Output: Crit   │   │
│ └────────┬───────┘   │
│          │            │
│          ▼            │
│ ┌────────────────┐   │
│ │ QA             │   │
│ │ Input: All     │   │
│ │ Output: QA     │   │
│ └────────┬───────┘   │
│          │            │
└──────────┼────────────┘
           │
       ┌───┴───┐
       │       │
       ▼       ▼
    Memory  Report
    Save    Gener
    │       │
    ▼       ▼
    ChromaDB     Export
    (Memory)     │
                 ├─ Markdown
                 ├─ HTML
                 ├─ PDF
                 └─ Text
```
