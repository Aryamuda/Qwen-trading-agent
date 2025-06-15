import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dataflows.yfin_utils import get_historical_data
import pandas as pd
from stockstats import StockDataFrame as Sdf

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates key technical indicators and adds them to the input DataFrame.
    
    Args:
        df (pd.DataFrame): A DataFrame with historical price data (must contain
                           'open', 'high', 'low', 'close', 'volume' columns).
                           
    Returns:
        The DataFrame with added technical indicator columns (e.g., 'macd', 'rsi_14').
    """
    if df.empty:
        print("Input DataFrame is empty, cannot calculate technical indicators.")
        return df

    print("Calculating technical indicators (MACD, RSI)...")
    try:
        # StockDataFrame expects lowercase column names
        df.columns = [col.lower() for col in df.columns]
        
        # Convert the pandas DataFrame to a StockDataFrame
        stock_df = Sdf.retype(df)
        
        # Calculate Moving Average Convergence Divergence (MACD)
        stock_df.get('macd')
        
        # Calculate Relative Strength Index (RSI) - 14 day is standard
        stock_df.get('rsi_14')
        
        print("Technical indicators calculated successfully.")
        return stock_df

    except Exception as e:
        print(f"An error occurred during technical indicator calculation: {e}")
        # Return the original dataframe on error
        return df

if __name__ == '__main__':

    test_symbol = "TSLA"
    
    # First, get the historical data
    historical_data = get_historical_data(test_symbol, period="3mo")

    if not historical_data.empty:
        # Now, add technical indicators to it
        data_with_indicators = add_technical_indicators(historical_data)
        
        if 'macd' in data_with_indicators.columns:
            print(f"\n--- Data for {test_symbol} with Technical Indicators (last 10 days) ---")
            # Display relevant columns
            print(data_with_indicators[['close', 'macd', 'macds', 'macdh', 'rsi_14']].tail(10))
            print("---------------------------------------------------------------------")
        else:
            print("Failed to add indicators.")
    else:
        print(f"Could not retrieve base data for {test_symbol} to calculate indicators.")

