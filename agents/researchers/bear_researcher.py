import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from graph.state import AgentState
from core.llm_interface import LLMInterface

def run_bear_researcher(state: AgentState, llm: LLMInterface) -> AgentState:
    """
    Constructs a bearish investment argument based on the initial analyst reports.
    """
    stock_symbol = state['stock_symbol']
    print(f"--- Running Bear Researcher for {stock_symbol} ---")
    
    reports = "\n\n".join(state['analyst_reports'])
    
    prompt = f"""
    You are a skeptical, bearish financial analyst. Your task is to review the following reports
    for {stock_symbol} and construct a compelling "Bear Case" argument.

    Focus exclusively on the risks, negative aspects, and potential downside revealed in the data.
    Ignore or downplay any positive points.

    **Source Reports:**
    {reports}

    Generate a concise, one-paragraph bear case.
    """
    
    print("Invoking LLM for Bear Case analysis...")
    try:
        response = llm.invoke(prompt)
        report = f"## Bear Case for {stock_symbol}\n\n{response}"
        state['analyst_reports'].append(report)
        log_message = "Bear Researcher: Successfully generated bear case."
        print(log_message)
        state['workflow_log'].append(log_message)
    except Exception as e:
        error_message = f"Bear Researcher: Failed to generate report. Error: {e}"
        print(error_message)
        state['workflow_log'].append(error_message)
        
    return state
