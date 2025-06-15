import argparse
from graph.builder import TradingAgentsGraph
from memory.memory_manager import MemoryManager 

def print_header(step_name: str):
    """Prints a standardized header for each step in the workflow."""
    print("\n" + "="*50)
    print(f"💼 Step: {step_name.replace('_', ' ').title()}")
    print("="*50)

def main(stock_symbol: str):
    """
    The main entry point for the Qwen-Powered Trading Agents application.
    This version streams the output and saves the final analysis to memory.
    """
    print(f"--- Starting Analysis for Stock: {stock_symbol} ---")
    
    # 1. Initialize and build the graph
    graph_builder = TradingAgentsGraph()
    app = graph_builder.build()
    
    # Initialize the memory manager with the embedding model from the graph builder
    memory_manager = MemoryManager(embedding_model=graph_builder.embedding_model)
    
    # 2. Define the initial state for the workflow
    initial_state = {
        "stock_symbol": stock_symbol,
        "analyst_reports": [],
        "investment_plan": "",
        "risk_analysis": "",
        "final_trade_decision": "",
        "debate_rounds": 0,
        "workflow_log": []
    }
    
    # 3. Stream the events and run the graph
    print("\n--- Running Workflow ---")
    final_state = None
    
    for step in app.stream(initial_state):
        node_name = list(step.keys())[0]
        updated_state = list(step.values())[0]
        print_header(node_name)
        if node_name in ["fundamentals_analyst", "news_analyst", "market_analyst", "social_media_analyst", "bull_researcher", "bear_researcher"]:
            if updated_state['analyst_reports']:
                print("Output:\n" + updated_state['analyst_reports'][-1])
        elif node_name == "research_manager":
            if updated_state['investment_plan']:
                 print("Output:\n" + updated_state['investment_plan'])
        elif node_name in ["aggressive_debator", "conservative_debator", "neutral_debator"]:
             if updated_state['risk_analysis']:
                last_report = updated_state['risk_analysis'].split("###")[-1]
                print(f"Output:\n###{last_report.strip()}")
        elif node_name == "risk_manager":
            if updated_state['final_trade_decision']:
                print("Output:\n" + updated_state['final_trade_decision'])
        final_state = updated_state

    # Final Summary
    print_header("Workflow Finished")
    if final_state:
        print("--- Investment Plan ---")
        print(final_state.get('investment_plan', "Not generated.") + "\n")
        print("--- Risk Debate ---")
        print(final_state.get('risk_analysis', "Not generated.") + "\n")
        print("--- FINAL DECISION ---")
        print(final_state.get('final_trade_decision', "Not generated."))
    
    # 4. Save the final state to long-term memory
    if final_state:
        memory_manager.save_analysis(final_state)
    
    print("\n" + "="*50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Qwen-Powered Trading Agents.")
    parser.add_argument("stock_symbol", type=str, help="The stock symbol to analyze (e.g., 'NVDA', 'TSLA').")
    args = parser.parse_args()
    
    main(args.stock_symbol)

