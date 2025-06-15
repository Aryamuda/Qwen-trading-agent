import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from graph.state import AgentState
from core.llm_interface import LLMInterface
from dataflows.interface import DataInterface
import pandas as pd

def run_market_analyst(state: AgentState, llm: LLMInterface) -> AgentState:
    """
    Runs the market analyst agent. This agent fetches historical price data
    and technical indicators, then uses the LLM to generate a technical analysis report.
    
    Args:
        state (AgentState): The current state of the graph.
        llm (LLMInterface): The language model interface for analysis.
        
    Returns:
        AgentState: The updated state with the new technical analysis report.
    """
    stock_symbol = state['stock_symbol']
    print(f"--- Running Market Analyst for {stock_symbol} ---")

    # 1. Fetch data
    data_interface = DataInterface()
    historical_data = data_interface.get_historical_data(stock_symbol, period="3mo")
    
    if historical_data.empty:
        log_message = f"Market Analyst: No historical data found for {stock_symbol}. Skipping."
        print(log_message)
        state['workflow_log'].append(log_message)
        return state

    data_with_indicators = data_interface.add_technical_indicators(historical_data)

    # 2. Construct a detailed prompt
    recent_data_str = data_with_indicators.tail(15).to_string()
    
    prompt = f"""
    You are a quantitative analyst specializing in technical analysis.
    Your task is to analyze the provided historical stock data for {stock_symbol}
    and generate a "Technical Analysis Report".

    The report must cover:
    1.  **Price Trend**: Analyze the recent price action based on the 'close' prices. Is the trend upwards, downwards, or sideways?
    2.  **MACD Analysis**: Interpret the MACD, signal line ('macds'), and histogram ('macdh'). Is it showing bullish or bearish momentum? Are there any crossovers?
    3.  **RSI Analysis**: Interpret the 14-day RSI ('rsi_14'). Is the stock overbought (above 70), oversold (below 30), or in a neutral range?
    4.  **Overall Conclusion**: Provide a brief, neutral summary of the technical outlook based *only* on the data provided.

    **Recent Data for {stock_symbol}:**
    {recent_data_str}

    Generate the report.
    """

    # 3. Invoke the LLM for analysis
    print("Invoking LLM for market analysis...")
    try:
        response = llm.invoke(prompt)
        report = f"## Technical Analysis Report for {stock_symbol}\n\n{response}"
        
        # 4. Update the state
        state['analyst_reports'].append(report)
        log_message = f"Market Analyst: Successfully generated report for {stock_symbol}."
        print(log_message)
        state['workflow_log'].append(log_message)
        
    except Exception as e:
        error_message = f"Market Analyst: Failed to get analysis from LLM. Error: {e}"
        print(error_message)
        state['workflow_log'].append(error_message)

    return state
