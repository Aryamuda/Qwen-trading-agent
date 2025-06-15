import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from graph.state import AgentState
from core.llm_interface import LLMInterface

def run_aggressive_debator(state: AgentState, llm: LLMInterface) -> AgentState:
    """
    Analyzes the investment plan from an aggressive, profit-focused perspective.
    """
    stock_symbol = state['stock_symbol']
    print(f"--- Running Aggressive Risk Debator for {stock_symbol} ---")
    
    investment_plan = state['investment_plan']
    
    prompt = f"""
    You are an aggressive, high-risk, high-reward trader.
    Your sole focus is on maximizing profit potential. Review the following "Final Investment Plan" for {stock_symbol}.

    Your task is to write a short, sharp "Aggressive Take" that focuses only on the upside.
    Emphasize the potential for significant gains and disregard or minimize the stated risks.
    Argue why the potential rewards strongly outweigh any downside.

    **Investment Plan to Analyze:**
    {investment_plan}

    Generate the "Aggressive Take".
    """
    
    print("Invoking LLM for Aggressive Take...")
    try:
        response = llm.invoke(prompt)
        report = f"### Aggressive Take\n{response}"
        
        current_analysis = state.get('risk_analysis') or ''
        state['risk_analysis'] = current_analysis + "\n\n" + report
        
        log_message = "Aggressive Debator: Successfully generated its take."
        print(log_message)
        state['workflow_log'].append(log_message)
    except Exception as e:
        error_message = f"Aggressive Debator: Failed to generate report. Error: {e}"
        print(error_message)
        state['workflow_log'].append(error_message)
        
    return state
