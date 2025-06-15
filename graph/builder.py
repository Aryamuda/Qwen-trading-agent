from langgraph.graph import StateGraph, END
from functools import partial

from .state import AgentState
from core.llm_interface import QwenLLM
from core.embedding_interface import HuggingFaceEmbedding
from config.default_config import Config

# Analyst agents
from agents.analysts.fundamentals_analyst import run_fundamentals_analyst
from agents.analysts.news_analyst import run_news_analyst
from agents.analysts.market_analyst import run_market_analyst
from agents.analysts.social_media_analyst import run_social_media_analyst

class TradingAgentsGraph:
    """
    Master orchestrator for the multi-agent trading analysis workflow.
    
    This class initializes the core components (LLM, embedding model) and
    constructs the LangGraph workflow with all the defined agent nodes and logical edges.
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
        
        # Create callable nodes for our agents by binding the LLM instance
        fundamentals_analyst_node = partial(run_fundamentals_analyst, llm=self.llm)
        news_analyst_node = partial(run_news_analyst, llm=self.llm)
        market_analyst_node = partial(run_market_analyst, llm=self.llm)
        social_media_analyst_node = partial(run_social_media_analyst, llm=self.llm)
        
        # Add the agent nodes to the graph
        self.workflow.add_node("fundamentals_analyst", fundamentals_analyst_node)
        self.workflow.add_node("news_analyst", news_analyst_node)
        self.workflow.add_node("market_analyst", market_analyst_node)
        self.workflow.add_node("social_media_analyst", social_media_analyst_node)
        
        # Define the workflow edges
        
        # Set the entry point
        self.workflow.set_entry_point("fundamentals_analyst")
        
        # Define the sequential flow of the analyst team
        self.workflow.add_edge("fundamentals_analyst", "news_analyst")
        self.workflow.add_edge("news_analyst", "market_analyst")
        self.workflow.add_edge("market_analyst", "social_media_analyst")
        
        # The Social Media Analyst is the final step for now
        self.workflow.add_edge("social_media_analyst", END)
        
        print("Compiling graph...")
        self.app = self.workflow.compile()
        print("Graph compiled successfully.")
        return self.app
