from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()
api_key = st.secrets["GOOGLE_API_KEY"]
# api_key = os.getenv("GOOGLE_API_KEY")
  

def optimize_portfolio_with_llm(risk_level,optimized_portfolio1,optimized_portfolio2,optimized_portfolio3):
    # Initializing the  LLM
    llm = GoogleGenerativeAI(model="gemini-1.0-pro", google_api_key=api_key)

    template = """
    You are a financial advisor assistant. Based on the user's risk tolerance level suggest the best optimized portfolio.

    Input details:
    - Risk level: {risk_level} (low, medium, or high - indicates the user's tolerance for risk)

    Available portfolios for different risk tolerances:
    - High risk tolerance: {optimized_portfolio1}
    - Medium risk tolerance: {optimized_portfolio2}
    - Low risk tolerance: {optimized_portfolio3}

    Your task:
    - If the risk tolerance level is high, suggest weights from optimized_portfolio1 and explain the reason for choosing markowitz mean variance optimization and tell why markowitz mean variance optimization is best for high risk tolerance.
    - If the risk tolerance level is medium, suggest weights from optimized_portfolio2 and explain the reason for choosing Risk parity optimization and tell why risk parity is best for medium risk tolerance.
    - If the risk tolerance level is low, suggest weights from optimized_portfolio3 and explain the reason for choosing minimum variance optimization and tell why minimum variance optimization is best for low risk tolerance.

    Explain your reasoning for selecting this portfolio based on the user's risk level. Describe how the selected portfolio’s risk-return profile aligns with the specified risk tolerance.

    Output:
    Don't show the inputs
    - Reason for Selection: Explanation of why this portfolio was chosen and how it aligns with the user's risk tolerance level.(Note: give explanation only for the selected risk tolerance level)
    - Explain about the assets and explain if a asset is getting high weightage why it is getting high weightage and if low why it is getting low.
    """

    # -- Defining prompt template --
    prompt = PromptTemplate.from_template(template)
    formatted_prompt = prompt.format(
        risk_level=risk_level,
        optimized_portfolio1=optimized_portfolio1,
        optimized_portfolio2=optimized_portfolio2,
        optimized_portfolio3=optimized_portfolio3
    )
    result = llm.predict(formatted_prompt)
    
    return result
