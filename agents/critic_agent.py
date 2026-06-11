from langchain_core.prompts import PromptTemplate
from config.llm import llm

def critique(goal: str, analyst_output: str, research_output: str = "", strategy: str = ""):
    """
    Critic Agent: Validates outputs for quality, accuracy, and hallucinations.
    
    Args:
        goal: The original business goal
        analyst_output: The analyst's output to validate
        research_output: Research context for validation
        strategy: CEO strategy for cross-validation
        
    Returns:
        Critical analysis with validation score and recommendations
    """
    
    prompt = PromptTemplate(
        input_variables=["goal", "analyst_output", "research", "strategy"],
        template="""You are a Critical Validation Expert and Quality Assurance Specialist.

Your role: Critically evaluate the analyst output for accuracy, logic, and hallucination risk.

Original Business Goal:
{goal}

Strategy (for context):
{strategy}

Research Foundation (for context):
{research}

Analyst Output to Validate:
{analyst_output}

Perform rigorous validation and generate a critical review including:

1. LOGICAL CONSISTENCY CHECK
   - Are conclusions logically sound?
   - Are cause-effect relationships valid?
   - Are assumptions explicit and reasonable?

2. EVIDENCE VALIDATION
   - Are claims supported by evidence?
   - Are data points correctly cited?
   - Is reasoning transparent?

3. HALLUCINATION RISK ASSESSMENT
   - Identify unsupported claims (0-10 score)
   - Flag suspicious assertions
   - Note missing evidence

4. COMPLETENESS AUDIT
   - Missing analysis areas
   - Incomplete arguments
   - Overlooked considerations

5. QUALITY SCORING
   Strategic Alignment: /10
   - How well does analysis align with goal?
   
   Evidence Quality: /10
   - Strength of supporting evidence
   
   Logical Rigor: /10
   - Quality of reasoning
   
   Actionability: /10
   - Can recommendations be executed?
   
   Comprehensiveness: /10
   - Coverage of important areas

6. SPECIFIC CRITIQUES
   - Strengths of the analysis
   - Weaknesses and gaps
   - Contradictions if any
   - Over-generalizations

7. HALLUCINATION FINDINGS
   - Suspicious claims
   - Unverified assertions
   - Potential factual errors
   - Risk level (Low/Medium/High)

8. IMPROVEMENT SUGGESTIONS
   - How to strengthen arguments
   - Data to verify
   - Analysis to add
   - Logic to clarify

9. FINAL VERDICT
   Quality Rating: [Poor/Fair/Good/Excellent]
   Confidence Level: [Low/Medium/High]
   Ready for Use: [Yes/No/With Caveats]

10. EXECUTIVE SUMMARY
    - Key validation finding
    - Main concern (if any)
    - Recommendation

Be rigorous and critical. Flag weak points clearly. Provide specific, actionable feedback.
"""
    )

    chain = prompt | llm

    result = chain.invoke({
        "goal": goal,
        "analyst_output": analyst_output,
        "research": research_output,
        "strategy": strategy
    })

    return result.content
