from langgraph.graph import StateGraph, END
from .state import AgentState
from core.llm_interface import QwenLLM
from core.embedding_interface import HuggingFaceEmbedding
from config.default_config import Config

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

    def _placeholder_node(self, state: AgentState):
        """A temporary placeholder node."""
        log = "Executing placeholder node. This will be replaced by actual agent logic."
        print(log)
        state['workflow_log'].append(log)
        return state

    def build(self):
        """
        Constructs the graph by adding nodes and defining the edges between them.
        """
        print("Building the agent workflow graph...")
        
        # For now, we'll create a simple graph with a single placeholder node
        # We will replace this with our actual agents in the next steps.
        self.workflow.add_node("placeholder", self._placeholder_node)
        self.workflow.set_entry_point("placeholder")
        self.workflow.add_edge("placeholder", END)
        
        print("Compiling graph...")
        self.app = self.workflow.compile()
        print("Graph compiled successfully.")
        return self.app

