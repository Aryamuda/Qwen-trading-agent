# dataflows/interface.py

import sys
import os

# --- Path Fix ---
# Adds the project's root directory to the Python path for direct script testing.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from typing import List, Dict

# Import all our data utility functions
from dataflows.yfin_utils import get_historical_data
from dataflows.finnhub_utils import get_company_news, get_financial_fundamentals
from dataflows.googlenews_utils import get_google_news
from dataflows.stockstats_utils import add_technical_indicators
from dataflows.reddit_utils import get_reddit_sentiment

class DataInterface:
    """
    A unified interface for all data retrieval operations.
    This class abstracts the underlying data sources and provides simple methods
    for agents to call. This adheres to the "Interface Pattern" from the blueprint.
    """
    
    # --- Individual Data Fetching Methods ---
    # These methods allow agents to request only the specific data they need.

    def get_historical_data(self, stock_symbol: str, period: str = "1y") -> pd.DataFrame:
        """Wrapper for the yfin_utils function."""
        return get_historical_data(stock_symbol, period)

    def get_company_news(self, stock_symbol: str, days: int = 30) -> pd.DataFrame:
        """Wrapper for the finnhub_utils news function."""
        return get_company_news(stock_symbol, days)

    def get_financial_fundamentals(self, stock_symbol: str) -> dict:
        """Wrapper for the finnhub_utils fundamentals function."""
        return get_financial_fundamentals(stock_symbol)

    def get_google_news(self, query: str, period: str = '7d', top_n: int = 10) -> pd.DataFrame:
        """Wrapper for the googlenews_utils function."""
        return get_google_news(query, period, top_n)

    def add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Wrapper for the stockstats_utils function."""
        return add_technical_indicators(df)

    def get_reddit_sentiment(self, stock_symbol: str, subreddits: list, limit: int = 10) -> pd.DataFrame:
        """Wrapper for the reddit_utils function."""
        return get_reddit_sentiment(stock_symbol, subreddits, limit)

    # --- High-Level Aggregate Method ---

    def get_all_data_for_analyst(self, stock_symbol: str) -> Dict[str, pd.DataFrame | Dict]:
        """
        A high-level method to fetch all necessary data for the initial analysis phase.
        
        Args:
            stock_symbol (str): The stock symbol to analyze.
        
        Returns:
            A dictionary containing all the fetched data, keyed by data type.
        """
        print(f"\n--- Starting Full Data Retrieval for {stock_symbol} via Interface ---")
        
        historical_prices = self.get_historical_data(stock_symbol, period="1y")
        
        if not historical_prices.empty:
            data_with_tech = self.add_technical_indicators(historical_prices.copy())
        else:
            data_with_tech = pd.DataFrame()

        fundamentals = self.get_financial_fundamentals(stock_symbol)
        
        return {
            "historical_data": data_with_tech,
            "company_news": self.get_company_news(stock_symbol, days=90),
            "fundamentals": fundamentals,
            "google_news": self.get_google_news(f"{fundamentals.get('name', stock_symbol)} stock news"),
            "reddit_sentiment": self.get_reddit_sentiment(stock_symbol, subreddits=['stocks', 'wallstreetbets'])
        }


# How to Use and Test This File
if __name__ == '__main__':
    pass