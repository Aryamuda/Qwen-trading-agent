import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import finnhub
import pandas as pd
from datetime import datetime, timedelta
from config.default_config import Config

# Finnhub Client Initialization 
try:
    if Config.FINNHUB_API_KEY:
        finnhub_client = finnhub.Client(api_key=Config.FINNHUB_API_KEY)
    else:
        finnhub_client = None
        print("Warning: FINNHUB_API_KEY not found. Finnhub functions will be disabled.")
except Exception as e:
    finnhub_client = None
    print(f"Error initializing Finnhub client: {e}")

def get_company_news(stock_symbol: str, days: int = 30) -> pd.DataFrame:
    """
    Fetches company news for a given stock symbol from Finnhub.
    
    Args:
        stock_symbol (str): The stock ticker symbol (e.g., 'NVDA').
        days (int): The number of past days to fetch news for.
        
    Returns:
        A pandas DataFrame containing recent news articles,
        or an empty DataFrame if the API key is not set or an error occurs.
    """
    if not finnhub_client:
        print("Finnhub client not initialized. Cannot fetch company news.")
        return pd.DataFrame()

    print(f"Fetching recent news for {stock_symbol} from Finnhub...")
    try:
        # Calculate the date range for the news query
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        news_list = finnhub_client.company_news(stock_symbol, _from=start_date, to=end_date)
        
        if not news_list:
            print(f"No news found for {stock_symbol} in the last {days} days.")
            return pd.DataFrame()
        
        # Convert the list of news articles into a DataFrame for easier analysis
        news_df = pd.DataFrame(news_list)
        # Convert timestamp to a readable date format
        news_df['datetime'] = pd.to_datetime(news_df['datetime'], unit='s').dt.date
        print(f"Successfully fetched {len(news_df)} news articles for {stock_symbol}.")
        return news_df[['datetime', 'headline', 'source', 'summary']]
        
    except Exception as e:
        print(f"An error occurred while fetching news for {stock_symbol}: {e}")
        return pd.DataFrame()

def get_financial_fundamentals(stock_symbol: str) -> dict:
    """
    Fetches key financial metrics and fundamentals for a stock.
    
    Args:
        stock_symbol (str): The stock ticker symbol.

    Returns:
        A dictionary containing the company's financial profile,
        or an empty dictionary if an error occurs.
    """
    if not finnhub_client:
        print("Finnhub client not initialized. Cannot fetch fundamentals.")
        return {}

    print(f"Fetching financial fundamentals for {stock_symbol} from Finnhub...")
    try:
        profile = finnhub_client.company_profile2(symbol=stock_symbol)
        if not profile:
            print(f"Warning: No financial profile found for {stock_symbol}.")
            return {}
        
        print(f"Successfully fetched fundamentals for {stock_symbol}.")
        return profile

    except Exception as e:
        print(f"An error occurred while fetching fundamentals for {stock_symbol}: {e}")
        return {}

if __name__ == '__main__':

    if not finnhub_client:
        print("\nSkipping tests because Finnhub client could not be initialized.")
    else:
        test_symbol = "NVDA"
        
        # Test fetching news
        news = get_company_news(test_symbol)
        if not news.empty:
            print(f"\n--- Recent News for {test_symbol} (first 5) ---")
            print(news.head())
            print("---------------------------------------------")
        
        # Test fetching fundamentals
        fundamentals = get_financial_fundamentals(test_symbol)
        if fundamentals:
            print(f"\n--- Fundamentals for {test_symbol} ---")
            print(f"Name: {fundamentals.get('name')}")
            print(f"Industry: {fundamentals.get('finnhubIndustry')}")
            print(f"Market Cap: {fundamentals.get('marketCapitalization')}")
            print("--------------------------------------")
