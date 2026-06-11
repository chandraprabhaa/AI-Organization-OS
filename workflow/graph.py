from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.planner_agent import plan
from agents.ceo_agent import generate_strategy
from agents.research_agent import perform_research
from agents.analyst_agent import AnalystAgent
from agents.qa_agent import qa_review
from agents.critic_agent import critique
from memory.persistent_memory import MemoryManager

class OrganizationState(TypedDict, total=False):
    """Complete workflow state"""
    user_goal: str
    plan: str
    strategy: str
    research: str
    analyst_output: str
    critic_output: str
    qa_output: str
    memory_context: str

# Initialize components
analyst = AnalystAgent()
memory_manager = MemoryManager()

# Node functions with memory injection
def planner_node(state):
    """Planner node with memory context"""
    goal = state["user_goal"]
    
    # Retrieve relevant past plans
    memory_context = memory_manager.search_memory(goal, limit=2, search_type="plans")
    
    result = plan(goal, memory_context)
    state["memory_context"] = memory_context
    
    return {"plan": result}

def ceo_node(state):
    """CEO node using planner output as context"""
    return {"strategy": generate_strategy(state["user_goal"], state.get("plan", ""))}

def research_node(state):
    """Research node using strategy"""
    return {"research": perform_research(state["strategy"])}

def analyst_node(state):
    """Analyst node using research"""
    return {"analyst_output": analyst.run(state["research"])}

def critic_node(state):
    """Critic node - validates analyst output"""
    result = critique(
        goal=state["user_goal"],
        analyst_output=state["analyst_output"],
        research_output=state.get("research", ""),
        strategy=state.get("strategy", "")
    )
    
    # Save critique to memory
    memory_manager.save_memory(
        query=state["user_goal"],
        data=result,
        data_type="critiques"
    )
    
    return {"critic_output": result}

def qa_node(state):
    """QA node - final quality review"""
    result = qa_review(
        business_goal=state["user_goal"],
        plan_output=state.get("plan", ""),
        ceo_output=state.get("strategy", ""),
        research_output=state.get("research", ""),
        analyst_output=state.get("analyst_output", ""),
        critic_output=state.get("critic_output", "")
    )
    
    # Save final report to memory
    memory_manager.save_memory(
        query=state["user_goal"],
        data=result,
        data_type="reports"
    )
    
    return {"qa_output": result}

# Build workflow graph
workflow = StateGraph(OrganizationState)

# Add nodes
nodes = [
    ("planner", planner_node),
    ("ceo", ceo_node),
    ("research", research_node),
    ("analyst", analyst_node),
    ("critic", critic_node),
    ("qa", qa_node),
]

for node_name, node_func in nodes:
    workflow.add_node(node_name, node_func)

# Set entry point
workflow.set_entry_point("planner")

# Add edges (execution flow)
workflow.add_edge("planner", "ceo")
workflow.add_edge("ceo", "research")
workflow.add_edge("research", "analyst")
workflow.add_edge("analyst", "critic")
workflow.add_edge("critic", "qa")
workflow.add_edge("qa", END)

# Compile graph
graph = workflow.compile()
