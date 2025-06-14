import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Centralized configuration class for the TradingAgents system.
    
    This class loads settings from environment variables first, falling back to
    default values if they are not set. This allows for easy configuration
s   for different environments (e.g., development, testing, production)
    without changing the codebase.
    """

    # --- 1. Core Intelligence Engine ---
    
    # LLM Configuration
    LLM_MODEL = os.getenv('LLM_MODEL', 'qwen-plus')
    DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY', None) 
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', 0.7))
    LLM_TOP_P = float(os.getenv('LLM_TOP_P', 0.8))
    LLM_MAX_TOKENS = int(os.getenv('LLM_MAX_TOKENS', 1500))

    # Embedding Model Configuration
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')

    # --- 2. API & Dataflow Settings ---
    
    # General API retry settings
    RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', 3))

    # Fallback cache directory for data resilience
    FALLBACK_CACHE_DIR = os.getenv('FALLBACK_CACHE_DIR', 'cache')

    # Finnhub API Key
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', None) # Recommended to be set in .env

    # --- 3. Agent & Graph Settings ---
    
    # Maximum number of debate rounds in the research phase
    MAX_DEBATE_ROUNDS = int(os.getenv('MAX_DEBATE_ROUNDS', 2))



# Verify configuration loading
if __name__ == '__main__':
    print("--- Configuration Loaded ---")
    if Config.DASHSCOPE_API_KEY:
        print(f"DASHSCOPE_API_KEY: Loaded (starts with '{Config.DASHSCOPE_API_KEY[:5]}...')")
    else:
        print("DASHSCOPE_API_KEY: Not found. Please set it in your .env file.")

    if Config.FINNHUB_API_KEY:
        print(f"FINNHUB_API_KEY: Loaded")
    else:
        print("FINNHUB_API_KEY: Not found. Please set it in your .env file.")
        
    print(f"LLM Model: {Config.LLM_MODEL}")
    print(f"Embedding Model: {Config.EMBEDDING_MODEL}")
    print(f"Retry Attempts: {Config.RETRY_ATTEMPTS}")
    print("--------------------------")
