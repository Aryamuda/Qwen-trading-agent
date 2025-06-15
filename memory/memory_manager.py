import sys
import os
import chromadb
from datetime import datetime, timezone
from typing import List
import chromadb.utils.embedding_functions as embedding_functions # Wrapper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.embedding_interface import EmbeddingInterface
from graph.state import AgentState
from config.default_config import Config

class MemoryManager:
    """
    Manages the long-term memory of the trading agent system using ChromaDB.
    """
    def __init__(self, embedding_model: EmbeddingInterface):
        """
        Initializes the MemoryManager.
        """
        print("Initializing Memory Manager...")
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_model = embedding_model

        chroma_embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.embedding_model.model_name 
        )
        
        self.collection = self.client.get_or_create_collection(
            name="trading_analyses",
            embedding_function=chroma_embedding_function
        )
        print("Memory Manager initialized successfully.")

    def _format_analysis_for_storage(self, state: AgentState) -> str:
        all_reports = "\n\n---\n\n".join(state.get('analyst_reports', []))
        risk_debate = state.get('risk_analysis', 'No risk debate was conducted.')
        investment_plan = state.get('investment_plan', 'No investment plan was generated.')
        final_decision = state.get('final_trade_decision', 'No final decision was made.')
        
        return f"""
        # Analysis Report for: {state['stock_symbol']}
        # Date: {datetime.now().strftime('%Y-%m-%d')}
        ## Final Decision
        {final_decision}
        ## Investment Plan
        {investment_plan}
        ## Risk Debate
        {risk_debate}
        ## Analyst Reports
        {all_reports}
        """.strip()

    def save_analysis(self, state: AgentState):
        if not state.get('final_trade_decision'):
            print("Memory Manager: Skipping save, as no final decision was reached.")
            return

        print("--- Saving Single Analysis to Long-Term Memory ---")
        document_to_store = self._format_analysis_for_storage(state)
        record_id = f"{state['stock_symbol']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        metadata = {
            "stock_symbol": state['stock_symbol'],
            "final_decision": state['final_trade_decision'].split(':')[0].strip(),
            "date_utc": int(datetime.now(timezone.utc).timestamp())
        }
        
        try:
            self.collection.add(
                documents=[document_to_store],
                metadatas=[metadata],
                ids=[record_id]
            )
            print(f"Successfully saved analysis for {state['stock_symbol']} with ID: {record_id}")
        except Exception as e:
            print(f"Memory Manager: Failed to save analysis to ChromaDB. Error: {e}")

    def save_analyses_in_batches(self, states: List[AgentState], batch_size: int = 100):
        print(f"--- Starting Batch Save of {len(states)} Analyses ---")
        for i in range(0, len(states), batch_size):
            batch = states[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1} with {len(batch)} items...")
            
            documents = [self._format_analysis_for_storage(state) for state in batch]
            metadatas = [
                {
                    "stock_symbol": state['stock_symbol'],
                    "final_decision": state['final_trade_decision'].split(':')[0].strip(),
                    "date_utc": int(datetime.now(timezone.utc).timestamp())
                } for state in batch
            ]
            ids = [f"{state['stock_symbol']}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{j}" for j, state in enumerate(batch)]
            
            try:
                self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
                print(f"Successfully saved batch {i//batch_size + 1}.")
            except Exception as e:
                print(f"Memory Manager: Failed to save batch. Error: {e}")
        
        print("--- Batch Save Complete ---")

    def query_memory(self, query_text: str, n_results: int = 2):
        print(f"\n--- Querying Memory for: '{query_text}' ---")
        try:
            results = self.collection.query(query_texts=[query_text], n_results=n_results)
            if not results or not results.get('documents'):
                print("No relevant memories found.")
                return
            for i, doc in enumerate(results['documents'][0]):
                print(f"\n--- Result {i+1} ---\n{doc[:500]}...")
        except Exception as e:
            print(f"Memory Manager: Failed to query memory. Error: {e}")
