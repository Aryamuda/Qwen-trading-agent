import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from graph.state import AgentState
from core.llm_interface import LLMInterface

def run_research_manager(state: AgentState, llm: LLMInterface) -> AgentState:
    """
    The entry point for the research and debate phase. It synthesizes analyst
    reports into a coherent investment plan after the debate.
    """
    stock_symbol = state['stock_symbol']
    print(f"--- Running Research Manager for {stock_symbol} ---")

    # Final Task: Synthesize the bull and bear arguments into a final plan.
    if state.get('investment_plan'): # This check ensures it runs after the debate
        all_reports = "\n\n".join(state['analyst_reports'])
        
        prompt = f"""
        You are a senior investment strategist and research manager.
        Your task is to synthesize the following analyst reports, bull case, and bear case 
        into a single, balanced "Final Investment Plan" for {stock_symbol}.

        The plan should have three sections:
        1.  **Summary of Key Findings**: Briefly summarize the most critical points from all the reports (fundamental, technical, news, and social media).
        2.  **Primary Bull Case**: Concisely state the main argument for investing in the stock.
        3.  **Primary Bear Case**: Concisely state the main argument against investing.
        4.  **Final Recommendation**: Based on the synthesis, provide a final investment thesis. This is not a simple buy/sell call, but a reasoned conclusion.

        **Source Reports:**
        {all_reports}

        Generate the "Final Investment Plan".
        """

        print("Invoking LLM to synthesize final investment plan...")
        try:
            response = llm.invoke(prompt)
            state['investment_plan'] = response
            log_message = "Research Manager: Successfully synthesized the Final Investment Plan."
            print(log_message)
            state['workflow_log'].append(log_message)
        except Exception as e:
            error_message = f"Research Manager: Failed to synthesize plan. Error: {e}"
            print(error_message)
            state['workflow_log'].append(error_message)
            
    return state
