import yfinance as yf
import pandas as pd

def get_historical_data(stock_symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetches historical market data for a given stock symbol from Yahoo Finance.
    
    Args:
        stock_symbol (str): The stock ticker symbol (e.g., 'NVDA').
        period (str): The time period for the data (e.g., '1d', '5d', '1mo', '1y', '5y', 'max').
        
    Returns:
        A pandas DataFrame containing the historical data (OHLC, Volume),
        or an empty DataFrame if the symbol is invalid or an error occurs.
    """
    print(f"Fetching '{period}' historical data for {stock_symbol} from Yahoo Finance...")
    try:
        ticker = yf.Ticker(stock_symbol)
        hist_data = ticker.history(period=period)
        
        if hist_data.empty:
            print(f"Warning: No data found for symbol '{stock_symbol}'. It might be an invalid ticker.")
            return pd.DataFrame()
            
        print(f"Successfully fetched data for {stock_symbol}.")
        # Ensure the index is just the date, not datetime, for cleaner merging later
        hist_data.index = hist_data.index.date
        return hist_data
        
    except Exception as e:
        print(f"An error occurred while fetching data for {stock_symbol}: {e}")
        return pd.DataFrame()

if __name__ == '__main__':

    test_symbol = "AAPL"
    nvda_data = get_historical_data(test_symbol, period="1mo")
    
    if not nvda_data.empty:
        print(f"\n--- Historical Data for {test_symbol} (last 5 days) ---")
        print(nvda_data.tail())
        print("-------------------------------------------------")
    else:
        print(f"\nCould not retrieve data for {test_symbol}.")
        
    # Test with an invalid symbol
    test_invalid_symbol = "INVALIDTICKERXYZ"
    invalid_data = get_historical_data(test_invalid_symbol)
    if invalid_data.empty:
        print(f"\nSuccessfully handled invalid ticker: {test_invalid_symbol}")

