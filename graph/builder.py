from langgraph.graph import StateGraph, END
from functools import partial

from .state import AgentState
from core.llm_interface import QwenLLM
from core.embedding_interface import HuggingFaceEmbedding
from config.default_config import Config

# Import all agents
from agents.analysts.fundamentals_analyst import run_fundamentals_analyst
from agents.analysts.news_analyst import run_news_analyst
from agents.analysts.market_analyst import run_market_analyst
from agents.analysts.social_media_analyst import run_social_media_analyst
from agents.researchers.bull_researcher import run_bull_researcher
from agents.researchers.bear_researcher import run_bear_researcher
from agents.managers.research_manager import run_research_manager
from agents.risk_mgmt.aggressive_debator import run_aggressive_debator
from agents.risk_mgmt.conservative_debator import run_conservative_debator
from agents.risk_mgmt.neutral_debator import run_neutral_debator  
from agents.managers.risk_manager import run_risk_manager

class TradingAgentsGraph:
    """
    Master orchestrator for the multi-agent trading analysis workflow.
    """
    
    def __init__(self):
        """Initializes the models and the graph."""
        print("Initializing Core Intelligence Engine...")
        self.llm = QwenLLM(
            model=Config.LLM_MODEL,
            api_key=Config.DASHSCOPE_API_KEY,
            temperature=Config.LLM_TEMPERATURE,
            top_p=Config.LLM_TOP_P,
            max_tokens=Config.LLM_MAX_TOKENS
        )
        self.embedding_model = HuggingFaceEmbedding(model_name=Config.EMBEDDING_MODEL)
        print("Core Intelligence Engine Initialized.")
        
        self.workflow = StateGraph(AgentState)
        self.app = None

    def build(self):
        """
        Constructs the graph by adding nodes and defining the edges between them.
        """
        print("Building the agent workflow graph...")
        
        # Callable nodes for all agents
        fundamentals_analyst_node = partial(run_fundamentals_analyst, llm=self.llm)
        news_analyst_node = partial(run_news_analyst, llm=self.llm)
        market_analyst_node = partial(run_market_analyst, llm=self.llm)
        social_media_analyst_node = partial(run_social_media_analyst, llm=self.llm)
        bull_researcher_node = partial(run_bull_researcher, llm=self.llm)
        bear_researcher_node = partial(run_bear_researcher, llm=self.llm)
        research_manager_node = partial(run_research_manager, llm=self.llm)
        aggressive_debator_node = partial(run_aggressive_debator, llm=self.llm)
        conservative_debator_node = partial(run_conservative_debator, llm=self.llm)
        neutral_debator_node = partial(run_neutral_debator, llm=self.llm) # New node
        risk_manager_node = partial(run_risk_manager, llm=self.llm)

        # Add all agent nodes to the graph
        self.workflow.add_node("fundamentals_analyst", fundamentals_analyst_node)
        self.workflow.add_node("news_analyst", news_analyst_node)
        self.workflow.add_node("market_analyst", market_analyst_node)
        self.workflow.add_node("social_media_analyst", social_media_analyst_node)
        self.workflow.add_node("bull_researcher", bull_researcher_node)
        self.workflow.add_node("bear_researcher", bear_researcher_node)
        self.workflow.add_node("research_manager", research_manager_node)
        self.workflow.add_node("aggressive_debator", aggressive_debator_node)
        self.workflow.add_node("conservative_debator", conservative_debator_node)
        self.workflow.add_node("neutral_debator", neutral_debator_node) # New node added
        self.workflow.add_node("risk_manager", risk_manager_node)
        
        # Define the full workflow
        self.workflow.set_entry_point("fundamentals_analyst")
        
        # 1. Analyst Team runs in sequence
        self.workflow.add_edge("fundamentals_analyst", "news_analyst")
        self.workflow.add_edge("news_analyst", "market_analyst")
        self.workflow.add_edge("market_analyst", "social_media_analyst")
        
        # 2. Investment Debate Team runs
        self.workflow.add_edge("social_media_analyst", "bull_researcher")
        self.workflow.add_edge("bull_researcher", "bear_researcher")
        
        # 3. Research Manager synthesizes the investment plan
        self.workflow.add_edge("bear_researcher", "research_manager")
        
        # 4. Risk Management Team runs
        self.workflow.add_edge("research_manager", "aggressive_debator")
        self.workflow.add_edge("aggressive_debator", "conservative_debator")
        self.workflow.add_edge("conservative_debator", "neutral_debator") # New edge
        
        # 5. Risk Manager makes the final decision
        self.workflow.add_edge("neutral_debator", "risk_manager") # New edge
        
        # 6. End of the workflow
        self.workflow.add_edge("risk_manager", END)
        
        print("Compiling graph...")
        self.app = self.workflow.compile()
        print("Graph compiled successfully.")
        return self.app
