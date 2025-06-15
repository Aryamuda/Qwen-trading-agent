import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from graph.state import AgentState
from core.llm_interface import LLMInterface
from dataflows.interface import DataInterface
import pandas as pd

def run_fundamentals_analyst(state: AgentState, llm: LLMInterface) -> AgentState:
    """
    Runs the fundamentals analyst agent. This agent fetches financial data
    and uses the LLM to generate an analysis report.
    
    Args:
        state (AgentState): The current state of the graph.
        llm (LLMInterface): The language model interface to use for analysis.
        
    Returns:
        AgentState: The updated state with the new analysis report.
    """
    stock_symbol = state['stock_symbol']
    print(f"--- Running Fundamentals Analyst for {stock_symbol} ---")
    
    # 1. Fetch data using the unified interface
    data_interface = DataInterface()
    fundamentals = data_interface.get_financial_fundamentals(stock_symbol)
    
    if not fundamentals:
        log_message = f"Fundamentals Analyst: No fundamental data found for {stock_symbol}. Skipping."
        print(log_message)
        state['workflow_log'].append(log_message)
        return state

    # 2. Construct a detailed prompt
    prompt = f"""
    You are a senior financial analyst providing a report on {fundamentals.get('name', stock_symbol)}.
    Based on the following financial data, please generate a concise "Fundamental Analysis Report".

    The report should cover these key areas:
    1.  **Company Profile**: Briefly describe the company's business, industry, and market position.
    2.  **Valuation**: Analyze the market capitalization and share structure. Is it a large-cap, mid-cap, or small-cap stock?
    3.  **Key Metrics**: Comment on the 52-week high/low, and the 50-day and 200-day moving averages. What do these suggest about recent price trends?
    4.  **Overall Conclusion**: Provide a brief, neutral summary of the company's financial health based *only* on the data provided.

    **Financial Data for {stock_symbol}:**
    - Country: {fundamentals.get('country')}
    - Currency: {fundamentals.get('currency')}
    - Exchange: {fundamentals.get('exchange')}
    - Industry: {fundamentals.get('finnhubIndustry')}
    - IPO Date: {fundamentals.get('ipo')}
    - Market Capitalization: {fundamentals.get('marketCapitalization')}
    - Company Name: {fundamentals.get('name')}
    - Ticker: {fundamentals.get('ticker')}
    - Web URL: {fundamentals.get('weburl')}
    - Logo: {fundamentals.get('logo')}
    - 52-Week High: {fundamentals.get('marketCapitalization')} 
    - 52-Week Low: {fundamentals.get('shareOutstanding')}
    - 50-Day Moving Average: {fundamentals.get('marketCapitalization')}
    - 200-Day Moving Average: {fundamentals.get('marketCapitalization')}
    
    Generate the report.
    """

    # 3. Invoke the LLM to get the analysis
    print("Invoking LLM for fundamental analysis...")
    try:
        response = llm.invoke(prompt)
        report = f"## Fundamental Analysis Report for {stock_symbol}\n\n{response}"
        
        # 4. Update the state
        state['analyst_reports'].append(report)
        log_message = f"Fundamentals Analyst: Successfully generated report for {stock_symbol}."
        print(log_message)
        state['workflow_log'].append(log_message)
        
    except Exception as e:
        error_message = f"Fundamentals Analyst: Failed to get analysis from LLM. Error: {e}"
        print(error_message)
        state['workflow_log'].append(error_message)

    return state

