import sys
import os
from pygooglenews import GoogleNews
import pandas as pd

def get_google_news(query: str, period: str = '7d', top_n: int = 10) -> pd.DataFrame:
    """
    Fetches news articles from Google News based on a search query.
    
    Args:
        query (str): The search term (e.g., 'NVIDIA stock').
        period (str): The time period for the news (e.g., '7d' for 7 days, '1m' for 1 month).
        top_n (int): The number of top news articles to return.
        
    Returns:
        A pandas DataFrame with the news articles, or an empty DataFrame on error.
    """
    print(f"Fetching Google News for query: '{query}'...")
    try:
        gn = GoogleNews(lang='en')
        search_result = gn.search(query, when=period)
        
        if not search_result['entries']:
            print(f"No Google News found for query '{query}'.")
            return pd.DataFrame()

        # Create a list of dictionaries from the search entries
        articles = [
            {
                'title': entry.title,
                'published': pd.to_datetime(entry.published),
                'link': entry.link,
                'source': entry.source['title']
            }
            for entry in search_result['entries']
        ]
        
        # Convert to DataFrame and return the top N articles
        news_df = pd.DataFrame(articles)
        print(f"Successfully fetched {len(news_df)} articles from Google News.")
        return news_df.head(top_n)

    except Exception as e:
        print(f"An error occurred while fetching from Google News: {e}")
        return pd.DataFrame()

if __name__ == '__main__':

    test_query = "BTC/USD"
    news_articles = get_google_news(test_query)

    if not news_articles.empty:
        print(f"\n--- Top Google News for '{test_query}' ---")
        # Set pandas display options to show full content
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.colheader_justify', 'left')
        pd.set_option('display.max_colwidth', 80)
        print(news_articles)
        print("-------------------------------------------------")
    else:
        print(f"Could not retrieve news for '{test_query}'.")

