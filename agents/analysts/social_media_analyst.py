import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from graph.state import AgentState
from core.llm_interface import LLMInterface
from dataflows.interface import DataInterface
import pandas as pd

def run_social_media_analyst(state: AgentState, llm: LLMInterface) -> AgentState:
    """
    Runs the social media analyst agent. This agent fetches Reddit posts and uses
    the LLM to determine the overall retail investor sentiment.
    
    Args:
        state (AgentState): The current state of the graph.
        llm (LLMInterface): The language model interface for analysis.
        
    Returns:
        AgentState: The updated state with the new social media analysis report.
    """
    stock_symbol = state['stock_symbol']
    print(f"--- Running Social Media Analyst for {stock_symbol} ---")

    # 1. Fetch data
    data_interface = DataInterface()
    reddit_posts = data_interface.get_reddit_sentiment(
        stock_symbol, 
        subreddits=['wallstreetbets', 'stocks', 'investing']
    )
    
    if reddit_posts.empty:
        log_message = f"Social Media Analyst: No Reddit posts found for {stock_symbol}. Skipping."
        print(log_message)
        state['workflow_log'].append(log_message)
        return state

    # 2. Construct a detailed prompt
    post_titles = "\n".join(f"- {title}" for title in reddit_posts['title'])
    
    prompt = f"""
    You are a market sentiment analyst specializing in social media trends.
    Your task is to analyze the following Reddit post titles mentioning {stock_symbol}
    and generate a "Social Media Sentiment Report".

    The report must contain two parts:
    1.  **Sentiment Summary**: Briefly describe the general attitude of retail investors towards the stock based on the post titles. Is it hype, fear, general discussion, or something else?
    2.  **Overall Sentiment**: A single-word sentiment rating. Choose from: **Very Bullish**, **Bullish**, **Neutral**, **Bearish**, or **Very Bearish**.

    **Recent Reddit Post Titles:**
    {post_titles}

    Generate the report based *only* on the titles provided.
    """

    # 3. Invoke the LLM for analysis
    print("Invoking LLM for social media analysis...")
    try:
        response = llm.invoke(prompt)
        report = f"## Social Media Sentiment Report for {stock_symbol}\n\n{response}"
        
        # 4. Update the state
        state['analyst_reports'].append(report)
        log_message = f"Social Media Analyst: Successfully generated report for {stock_symbol}."
        print(log_message)
        state['workflow_log'].append(log_message)
        
    except Exception as e:
        error_message = f"Social Media Analyst: Failed to get analysis from LLM. Error: {e}"
        print(error_message)
        state['workflow_log'].append(error_message)

    return state
