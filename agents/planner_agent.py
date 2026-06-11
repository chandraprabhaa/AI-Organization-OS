from langchain_core.prompts import PromptTemplate
from config.llm import llm_creative

def plan(goal: str, memory_context: str = ""):
    """
    Planner Agent: Breaks down business goal into actionable tasks.
    
    Args:
        goal: The business goal to plan for
        memory_context: Retrieved past plans for context
        
    Returns:
        Structured execution plan
    """
    
    memory_section = f"""
Previous Successful Plans:
{memory_context}

""" if memory_context else ""

    prompt = PromptTemplate(
        input_variables=["goal", "memory"],
        template=f"""{memory_section}You are a Strategic Business Planner in an AI Organization OS.

Your task: Break down the business goal into a comprehensive, actionable execution plan.

Business Goal:
{{goal}}

Generate a detailed plan with:

1. GOAL BREAKDOWN
   - Primary Objective
   - Secondary Objectives
   - Success Criteria

2. EXECUTION PHASES
   - Phase 1: Discovery & Analysis
   - Phase 2: Strategy Development
   - Phase 3: Implementation Planning
   - Phase 4: Validation & Review

3. KEY MILESTONES
   - Critical path items
   - Dependencies
   - Timeline estimates

4. RESOURCE REQUIREMENTS
   - Team skills needed
   - Technology stack
   - Data requirements

5. RISK MITIGATION
   - Potential blockers
   - Mitigation strategies

6. SUCCESS METRICS
   - KPIs to track
   - Measurement methods
   - Target timelines

Provide the plan in a clear, structured format suitable for executive review.
"""
    )

    chain = prompt | llm_creative

    result = chain.invoke({
        "goal": goal,
        "memory": memory_context
    })

    return result.content
