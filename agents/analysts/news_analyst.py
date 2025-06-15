import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from graph.state import AgentState
from core.llm_interface import LLMInterface
from dataflows.interface import DataInterface
import pandas as pd

def run_news_analyst(state: AgentState, llm: LLMInterface) -> AgentState:
    """
    Runs the news analyst agent. This agent fetches company and general news,
    and uses the LLM to generate a summarized report with a sentiment score.
    
    Args:
        state (AgentState): The current state of the graph.
        llm (LLMInterface): The language model interface for analysis.
        
    Returns:
        AgentState: The updated state with the new news analysis report.
    """
    stock_symbol = state['stock_symbol']
    print(f"--- Running News Analyst for {stock_symbol} ---")
    
    # 1. Fetch data
    data_interface = DataInterface()
    company_name = data_interface.get_financial_fundamentals(stock_symbol).get('name', stock_symbol)
    
    company_news = data_interface.get_company_news(stock_symbol)
    google_news = data_interface.get_google_news(f"{company_name} stock")
    
    if company_news.empty and google_news.empty:
        log_message = f"News Analyst: No news found for {stock_symbol}. Skipping."
        print(log_message)
        state['workflow_log'].append(log_message)
        return state

    # 2. Combine and format news headlines for the prompt
    all_headlines = []
    if not company_news.empty:
        all_headlines.extend(f"- {h} (Source: {s})" for h, s in zip(company_news['headline'], company_news['source']))
    if not google_news.empty:
        all_headlines.extend(f"- {h} (Source: {s})" for h, s in zip(google_news['title'], google_news['source']))
    
    news_string = "\n".join(all_headlines)

    # 3. Construct a detailed prompt
    prompt = f"""
    You are a financial news analyst. Your task is to analyze the following recent news headlines related to {company_name} ({stock_symbol})
    and provide a "News Analysis Report".

    The report must contain two parts:
    1.  **Summary**: A brief, one-paragraph summary of the key themes and events found in the news.
    2.  **Overall Sentiment**: A single-word sentiment rating. Choose from: **Positive**, **Negative**, or **Neutral**.

    **Recent News Headlines:**
    {news_string}

    Generate the report based *only* on the headlines provided.
    """

    # 4. Invoke the LLM for analysis
    print("Invoking LLM for news analysis...")
    try:
        response = llm.invoke(prompt)
        report = f"## News Analysis Report for {stock_symbol}\n\n{response}"
        
        # 5. Update the state
        state['analyst_reports'].append(report)
        log_message = f"News Analyst: Successfully generated report for {stock_symbol}."
        print(log_message)
        state['workflow_log'].append(log_message)
        
    except Exception as e:
        error_message = f"News Analyst: Failed to get analysis from LLM. Error: {e}"
        print(error_message)
        state['workflow_log'].append(error_message)

    return state
