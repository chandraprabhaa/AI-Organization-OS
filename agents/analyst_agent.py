from langchain_core.prompts import PromptTemplate
from config.llm import llm

class AnalystAgent:
    """
    Analyst Agent: Converts research into actionable business analysis.
    """
    
    def run(self, research_output: str):
        """
        Analyze research and produce strategic business analysis.
        
        Args:
            research_output: Output from research agent
            
        Returns:
            Business analysis with SWOT, opportunities, and recommendations
        """
        
        prompt = PromptTemplate(
            input_variables=["research"],
            template="""You are a Senior Business Analyst in an AI Organization OS.

Your task: Analyze the provided research report and generate professional business analysis.

Research Report:
{research}

Generate a comprehensive business analysis including:

1. SWOT ANALYSIS
   Strengths:
   - Internal capabilities
   - Market advantages
   - Resource advantages
   
   Weaknesses:
   - Internal gaps
   - Resource constraints
   - Technical limitations
   
   Opportunities:
   - Market expansion
   - Technology adoption
   - Partnership potential
   
   Threats:
   - Competitive threats
   - Market disruption
   - Regulatory risks

2. MARKET OPPORTUNITIES
   - Size and timeline for each opportunity
   - Required resources
   - Expected ROI
   - Implementation difficulty

3. FINANCIAL ANALYSIS
   - Cost structure
   - Revenue potential
   - Break-even analysis
   - Profitability metrics

4. RISK ANALYSIS
   - Technical risks and mitigation
   - Market risks and mitigation
   - Financial risks and mitigation
   - Operational risks and mitigation

5. COMPETITIVE POSITIONING
   - Market share potential
   - Differentiation strategy
   - Pricing strategy
   - Go-to-market approach

6. STRATEGIC RECOMMENDATIONS
   Short-term Actions (0-3 months):
   - Quick wins
   - Foundation building
   - Team setup
   
   Long-term Strategy (3-12+ months):
   - Market penetration
   - Product evolution
   - Expansion plans
   
   Business Optimization:
   - Efficiency improvements
   - Cost reduction
   - Revenue enhancement

7. METRICS & KPIs
   - Primary success metrics
   - Tracking mechanisms
   - Review frequency

Format as a professional business analysis suitable for board presentation.
"""
        )

        chain = prompt | llm

        result = chain.invoke({"research": research_output})

        return result.content
