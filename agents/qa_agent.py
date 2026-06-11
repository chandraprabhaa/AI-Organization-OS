import time
from langchain_core.prompts import PromptTemplate
from config.llm import llm

def qa_review(
    business_goal: str,
    plan_output: str,
    ceo_output: str,
    research_output: str,
    analyst_output: str,
    critic_output: str
):
    """
    QA Agent: Final quality assurance and report consolidation.
    
    Args:
        business_goal: Original business goal
        plan_output: Planner's execution plan
        ceo_output: CEO's strategy
        research_output: Research findings
        analyst_output: Analyst's analysis
        critic_output: Critic's validation
        
    Returns:
        Final QA report with recommendations
    """
    
    prompt = PromptTemplate(
        input_variables=[
            "business_goal",
            "plan_output",
            "ceo_output",
            "research_output",
            "analyst_output",
            "critic_output"
        ],
        template="""You are a Senior Quality Assurance Business Consultant.

Your responsibility: Ensure all outputs align, are comprehensive, and meet business standards.

Business Goal:
{business_goal}

EXECUTION PLAN:
{plan_output}

CEO STRATEGY:
{ceo_output}

RESEARCH FINDINGS:
{research_output}

ANALYST OUTPUT:
{analyst_output}

CRITIC VALIDATION:
{critic_output}

Perform a comprehensive quality review and generate a final report:

1. EXECUTIVE SUMMARY
   - Overall quality assessment
   - Alignment with goal
   - Ready for implementation? (Yes/No/With Changes)

2. CROSS-DOCUMENT CONSISTENCY
   - Do Plan and Strategy align?
   - Does Research support Strategy?
   - Does Analysis follow Research?
   - Does Critic's concerns addressed?

3. COMPLETENESS ASSESSMENT
   - All required analysis present?
   - All risk areas covered?
   - All opportunities identified?
   - Implementation ready?

4. LOGICAL FLOW VALIDATION
   - Does execution follow logically?
   - Are dependencies clear?
   - Are timelines realistic?
   - Are resources identified?

5. RISK & CONCERN REVIEW
   - Unsolved critic issues
   - Potential implementation blockers
   - Regulatory/compliance gaps
   - Technical feasibility questions

6. MISSING ELEMENTS
   - Critical analyses not covered
   - Important considerations overlooked
   - Data gaps that should be filled
   - Stakeholder perspectives missing

7. IMPROVEMENT ROADMAP
   If NOT ready for implementation:
   - Top 3 items to fix
   - Estimated effort for each
   - Success criteria for each
   
   If ready:
   - Next validation steps
   - Monitoring checkpoints
   - Key decision gates

8. RECOMMENDATIONS FOR EXECUTION
   - Top implementation priorities
   - Resource requirements
   - Timeline adjustments
   - Risk mitigation actions

9. QUALITY METRICS SUMMARY
   Plan Quality: /10
   Strategy Quality: /10
   Research Quality: /10
   Analysis Quality: /10
   Critic Validation: /10
   Overall Package Quality: /10

10. FINAL QA VERDICT
    Status: [APPROVED / APPROVED WITH CHANGES / NEEDS REVISION]
    Confidence: [High / Medium / Low]
    
    If APPROVED: Ready for board presentation and implementation
    If APPROVED WITH CHANGES: Can proceed but with noted modifications
    If NEEDS REVISION: Specific areas must be addressed before use

11. IMPLEMENTATION READINESS CHECKLIST
    ☐ All analysis complete
    ☐ No critical gaps identified
    ☐ Concerns addressed
    ☐ Resources identified
    ☐ Timeline realistic
    ☐ Risks documented
    ☐ KPIs defined
    ☐ Stakeholders aligned

Provide professional, actionable feedback suitable for executive decision-making.
"""
    )

    chain = prompt | llm

    # Retry logic for API stability
    MAX_RETRIES = 3

    for attempt in range(MAX_RETRIES):
        try:
            print(f"QA Agent - Attempt {attempt + 1}/{MAX_RETRIES}")
            
            # Log input sizes for debugging
            print(f"  Plan: {len(plan_output)} chars")
            print(f"  Strategy: {len(ceo_output)} chars")
            print(f"  Research: {len(research_output)} chars")
            print(f"  Analysis: {len(analyst_output)} chars")
            print(f"  Critique: {len(critic_output)} chars")

            result = chain.invoke({
                "business_goal": business_goal,
                "plan_output": plan_output,
                "ceo_output": ceo_output,
                "research_output": research_output,
                "analyst_output": analyst_output,
                "critic_output": critic_output,
            })

            print("QA Agent - Success ✓")
            return result.content

        except Exception as e:
            print(f"QA Agent - Error on attempt {attempt + 1}: {str(e)[:100]}")
            
            if attempt == MAX_RETRIES - 1:
                # Return a fallback QA report
                return f"""
QA REPORT (Generated with Partial Data)

Status: NEEDS REVIEW
Confidence: Low

The QA agent encountered an error generating the full report due to API constraints.
Please review the individual outputs directly:

- Plan: {len(plan_output)} characters generated
- Strategy: {len(ceo_output)} characters generated
- Research: {len(research_output)} characters generated
- Analysis: {len(analyst_output)} characters generated
- Critique: {len(critic_output)} characters generated

Recommendation: Review each agent output independently and conduct manual QA review.
"""
            
            print(f"Retrying in 3 seconds...")
            time.sleep(3)
