import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from graph.state import AgentState
from core.llm_interface import LLMInterface

def run_risk_manager(state: AgentState, llm: LLMInterface) -> AgentState:
    """
    Moderates the risk debate and produces the final trade decision.
    """
    stock_symbol = state['stock_symbol']
    print(f"--- Running Risk Manager for {stock_symbol} ---")

    investment_plan = state['investment_plan']
    risk_analysis = state.get('risk_analysis', 'No risk analysis provided.')

    prompt = f"""
    You are the head of risk management at an investment firm. 
    Your decision is final. You have been presented with a final investment plan and two opposing viewpoints from your team.

    Your task is to produce the "Final Trade Decision". The decision must be one of the following four options, exactly as written:
    - **BUY**: The potential reward significantly outweighs the risks.
    - **HOLD**: The situation is uncertain. Monitor for now, but do not commit new capital.
    - **SELL**: The risks significantly outweigh the potential reward.
    - **AVOID**: The asset is too volatile or unpredictable. Do not engage.

    Based on all the information below, choose the single most appropriate action. Provide a brief, one-sentence justification for your choice.

    **Final Investment Plan:**
    {investment_plan}

    **Risk Debate Arguments:**
    {risk_analysis}

    Output only the decision and the single-sentence justification. For example:
    BUY: The strong market position and positive sentiment suggest a high probability of upside.
    """
    
    print("Invoking LLM for final trade decision...")
    try:
        response = llm.invoke(prompt)
        state['final_trade_decision'] = response
        log_message = "Risk Manager: Successfully produced the Final Trade Decision."
        print(log_message)
        state['workflow_log'].append(log_message)
    except Exception as e:
        error_message = f"Risk Manager: Failed to make a final decision. Error: {e}"
        print(error_message)
        state['workflow_log'].append(error_message)
            
    return state
