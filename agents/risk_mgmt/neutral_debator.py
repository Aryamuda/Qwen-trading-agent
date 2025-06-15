import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from graph.state import AgentState
from core.llm_interface import LLMInterface

def run_neutral_debator(state: AgentState, llm: LLMInterface) -> AgentState:
    """
    Analyzes the investment plan from a balanced, neutral perspective.
    """
    stock_symbol = state['stock_symbol']
    print(f"--- Running Neutral Risk Debator for {stock_symbol} ---")
    
    investment_plan = state['investment_plan']
    
    prompt = f"""
    You are a neutral, balanced portfolio strategist.
    Your task is to provide a "Balanced Take" on the following "Final Investment Plan" for {stock_symbol}.

    Objectively weigh the potential upside against the highlighted risks.
    Provide a rational perspective that acknowledges both sides of the argument without leaning heavily in either direction.
    What is the most reasonable, middle-ground perspective?

    **Investment Plan to Analyze:**
    {investment_plan}

    Generate the "Balanced Take".
    """
    
    print("Invoking LLM for Balanced Take...")
    try:
        response = llm.invoke(prompt)
        report = f"### Balanced Take\n{response}"
        
        current_analysis = state.get('risk_analysis') or ''
        state['risk_analysis'] = current_analysis + "\n\n" + report
        
        log_message = "Neutral Debator: Successfully generated its take."
        print(log_message)
        state['workflow_log'].append(log_message)
    except Exception as e:
        error_message = f"Neutral Debator: Failed to generate report. Error: {e}"
        print(error_message)
        state['workflow_log'].append(error_message)
        
    return state
