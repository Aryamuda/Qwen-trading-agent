# graph/state.py

from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    """
    Defines the shared state for the trading agent graph. This TypedDict acts as the
    memory that is passed between all the nodes (agents) in the workflow.
    """
    stock_symbol: str
    
    # Data collected by analysts
    analyst_reports: Optional[List[str]]
    
    # Synthesized plans and decisions
    investment_plan: Optional[str]
    risk_analysis: Optional[str]
    final_trade_decision: Optional[str]
    
    # For managing debate rounds
    debate_rounds: int
    
    # A log of all actions taken for debugging and review
    workflow_log: List[str]

