import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import praw
import pandas as pd
from config.default_config import Config

# Reddit Client Initialization
try:
    # Check for all required Reddit API credentials
    if all(os.getenv(key) for key in ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_USER_AGENT']):
        reddit_client = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT'),
            timeout=30  # Increased timeout to 30 seconds to prevent read errors
        )
    else:
        reddit_client = None
        print("Warning: Reddit API credentials not found in .env file. Reddit functions will be disabled.")
except Exception as e:
    reddit_client = None
    print(f"Error initializing PRAW client: {e}")

def get_reddit_sentiment(stock_symbol: str, subreddits: list, limit: int = 10) -> pd.DataFrame:
    """
    Fetches top posts from a list of subreddits that mention a stock symbol.
    
    Args:
        stock_symbol (str): The stock ticker to search for (e.g., 'NVDA').
        subreddits (list): A list of subreddits to search in (e.g., ['wallstreetbets', 'stocks']).
        limit (int): The maximum number of posts to fetch from each subreddit.
        
    Returns:
        A pandas DataFrame with relevant post titles and scores, or an empty DataFrame on error.
    """
    if not reddit_client:
        print("PRAW client not initialized. Cannot fetch Reddit sentiment.")
        return pd.DataFrame()

    print(f"Fetching Reddit sentiment for {stock_symbol} from subreddits: {subreddits}...")
    all_posts = []
    
    try:
        for sub_name in subreddits:
            subreddit = reddit_client.subreddit(sub_name)
            # Search for the stock symbol in the top posts of the subreddit
            for post in subreddit.hot(limit=limit * 5): # Fetch more to filter down
                if len(all_posts) >= limit:
                    break
                if stock_symbol.lower() in post.title.lower() or stock_symbol.lower() in post.selftext.lower():
                    all_posts.append({
                        'subreddit': sub_name,
                        'title': post.title,
                        'score': post.score,
                        'url': post.url
                    })
        
        if not all_posts:
            print(f"No posts found mentioning {stock_symbol}.")
            return pd.DataFrame()

        posts_df = pd.DataFrame(all_posts)
        print(f"Successfully fetched {len(posts_df)} relevant posts from Reddit.")
        return posts_df.head(limit)

    except Exception as e:
        print(f"An error occurred while fetching from Reddit: {e}")
        return pd.DataFrame()

if __name__ == '__main__':

    if not reddit_client:
        print("\nSkipping tests because Reddit client could not be initialized.")
    else:
        test_symbol = "NVDA"
        target_subs = ['stocks']
        
        reddit_posts = get_reddit_sentiment(test_symbol, target_subs)

        if not reddit_posts.empty:
            print(f"\n--- Top Reddit Posts mentioning '{test_symbol}' ---")
            pd.set_option('display.max_colwidth', 80)
            print(reddit_posts)
            print("-------------------------------------------------")
        else:
            print(f"\nCould not retrieve Reddit posts for '{test_symbol}'.")

