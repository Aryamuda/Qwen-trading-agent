# main.py

import argparse
from graph.builder import TradingAgentsGraph

def main(stock_symbol: str):
    """
    The main entry point for the Qwen-Powered Trading Agents application.
    
    Args:
        stock_symbol (str): The stock symbol to analyze (e.g., 'NVDA').
    """
    print(f"--- Starting Analysis for Stock: {stock_symbol} ---")
    
    # 1. Initialize and build the graph
    graph_builder = TradingAgentsGraph()
    app = graph_builder.build()
    
    # 2. Define the initial state for the workflow
    initial_state = {
        "stock_symbol": stock_symbol,
        "analyst_reports": [],
        "investment_plan": None,
        "risk_analysis": None,
        "final_trade_decision": None,
        "debate_rounds": 0,
        "workflow_log": []
    }
    
    # 3. Stream the events and run the graph
    print("\n--- Running Workflow ---")
    final_state = app.invoke(initial_state)
    
    print("\n--- Workflow Finished ---")
    print("Final State:")
    # Pretty print the final state's log
    for i, log_entry in enumerate(final_state['workflow_log']):
        print(f"  {i+1}. {log_entry}")
        
    print(f"\nFinal decision: {final_state.get('final_trade_decision', 'Not reached')}")
    print("-------------------------")


if __name__ == "__main__":
    # Set up argument parser to accept a stock symbol from the command line
    parser = argparse.ArgumentParser(description="Run the Qwen-Powered Trading Agents.")
    parser.add_argument(
        "stock_symbol", 
        type=str, 
        help="The stock symbol to analyze (e.g., 'NVDA', 'TSLA')."
    )
    args = parser.parse_args()
    
    main(args.stock_symbol)

