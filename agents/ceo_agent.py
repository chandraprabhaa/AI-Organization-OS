from langchain_core.prompts import PromptTemplate
from config.llm import llm

def generate_strategy(user_goal: str, plan_context: str = ""):
    """
    CEO Agent: Creates business strategy based on planning output.
    
    Args:
        user_goal: The overall business goal
        plan_context: The planner's output for context
        
    Returns:
        Executive strategy document
    """
    
    context_section = f"""
Based on the following execution plan:
{plan_context}

""" if plan_context else ""

    prompt = PromptTemplate(
        input_variables=["goal"],
        template=f"""{context_section}You are the CEO of an AI organization.

Your responsibility: Create a comprehensive business strategy that aligns with organizational goals.

Business Goal:
{{goal}}

Develop a strategic document that includes:

1. EXECUTIVE SUMMARY
   - Vision statement
   - Strategic direction
   - Expected outcomes

2. MARKET POSITIONING
   - Competitive advantage
   - Market opportunities
   - Target market segments

3. BUSINESS STRATEGY
   - Value proposition
   - Revenue model
   - Growth strategy

4. ORGANIZATIONAL ALIGNMENT
   - Key stakeholders
   - Cross-functional dependencies
   - Team structure requirements

5. RESOURCE ALLOCATION
   - Budget considerations
   - Team assignments
   - Technology investments

6. STRATEGIC TIMELINE
   - Quarter-by-quarter milestones
   - Key decision points
   - Review checkpoints

7. SUCCESS CRITERIA
   - Strategic KPIs
   - Financial metrics
   - Operational metrics

Format as an executive-level strategic plan document.
"""
    )

    chain = prompt | llm

    result = chain.invoke({"goal": user_goal})

    return result.content
