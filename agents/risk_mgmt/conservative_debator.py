import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from graph.state import AgentState
from core.llm_interface import LLMInterface

def run_conservative_debator(state: AgentState, llm: LLMInterface) -> AgentState:
    """
    Analyzes the investment plan from a conservative, capital-preservation perspective.
    """
    stock_symbol = state['stock_symbol']
    print(f"--- Running Conservative Risk Debator for {stock_symbol} ---")
    
    investment_plan = state['investment_plan']
    
    prompt = f"""
    You are a conservative, risk-averse portfolio manager.
    Your primary goal is capital preservation. Review the following "Final Investment Plan" for {stock_symbol}.

    Your task is to write a short, sharp "Conservative Take" that focuses only on the risks.
    Emphasize the potential for losses and highlight any uncertainties or bearish points from the plan.
    Argue why the risks might be too high for a prudent investor.

    **Investment Plan to Analyze:**
    {investment_plan}

    Generate the "Conservative Take".
    """
    
    print("Invoking LLM for Conservative Take...")
    try:
        response = llm.invoke(prompt)
        report = f"### Conservative Take\n{response}"
        
        current_analysis = state.get('risk_analysis') or ''
        state['risk_analysis'] = current_analysis + "\n\n" + report
        
        log_message = "Conservative Debator: Successfully generated its take."
        print(log_message)
        state['workflow_log'].append(log_message)
    except Exception as e:
        error_message = f"Conservative Debator: Failed to generate report. Error: {e}"
        print(error_message)
        state['workflow_log'].append(error_message)
        
    return state
