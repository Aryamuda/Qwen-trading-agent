import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from typing import List, Dict
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

    def get_all_data_for_analyst(self, stock_symbol: str) -> Dict[str, pd.DataFrame | Dict]:
        """
        A high-level method to fetch all necessary data for the initial analysis phase.
        
        Args:
            stock_symbol (str): The stock symbol to analyze.
        
        Returns:
            A dictionary containing all the fetched data, keyed by data type.
        """
        print(f"\n--- Starting Full Data Retrieval for {stock_symbol} via Interface ---")
        
        # 1. Get historical price data
        historical_prices = get_historical_data(stock_symbol, period="1y")
        
        # 2. Add technical indicators to the price data
        if not historical_prices.empty:
            data_with_tech = add_technical_indicators(historical_prices.copy())
        else:
            data_with_tech = pd.DataFrame()

        # 3. Get company news from Finnhub
        company_news = get_company_news(stock_symbol, days=90)
        
        # 4. Get financial fundamentals from Finnhub
        fundamentals = get_financial_fundamentals(stock_symbol)
        
        # 5. Get broader news from Google News
        google_news_results = get_google_news(f"{fundamentals.get('name', stock_symbol)} stock news")
        
        # 6. Get retail sentiment from Reddit
        reddit_posts = get_reddit_sentiment(stock_symbol, subreddits=['stocks', 'wallstreetbets'])

        print("--- Full Data Retrieval Complete ---")
        
        return {
            "historical_data": data_with_tech,
            "company_news": company_news,
            "fundamentals": fundamentals,
            "google_news": google_news_results,
            "reddit_sentiment": reddit_posts
        }

if __name__ == '__main__':

    data_interface = DataInterface()
    test_symbol = "TSLA"
    
    all_data = data_interface.get_all_data_for_analyst(test_symbol)
    
    print(f"\n\n--- Unified Data Report for {test_symbol} ---")
    
    # Check and display a sample of each data type
    for key, value in all_data.items():
        print(f"\n----- {key.replace('_', ' ').title()} -----")
        if isinstance(value, pd.DataFrame):
            if not value.empty:
                print(value.head(3))
            else:
                print("No data found.")
        elif isinstance(value, dict):
            if value:
                # Print first 5 items for brevity
                for i, (k, v) in enumerate(value.items()):
                    if i >= 5: break
                    print(f"{k}: {v}")
            else:
                print("No data found.")
    
    print("\n------------------------------------")

