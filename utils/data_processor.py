import pandas as pd
import numpy as np

def process_options_data(df):
    """
    Process the raw options data from Excel file.
    
    Parameters:
    df (pandas.DataFrame): Raw options data
    
    Returns:
    pandas.DataFrame: Processed options data
    """
    # Ensure all required columns are present
    required_columns = [
        'symbol', 'expiry_date', 'strike', 'option_type',
        'bid', 'ask', 'volume', 'open_interest'
    ]
    
    # Convert column names to lowercase and strip whitespace
    df.columns = [col.lower().strip() for col in df.columns]
    
    # Basic data cleaning
    df['symbol'] = df['symbol'].str.upper()
    df['option_type'] = df['option_type'].str.upper()
    
    # Convert date format
    df['expiry_date'] = pd.to_datetime(df['expiry_date'])
    
    # Calculate mid price
    df['mid_price'] = (df['bid'] + df['ask']) / 2
    
    return df

def create_matrix_view(df, symbol, expiry_date):
    """
    Create matrix view for calls and puts.
    
    Parameters:
    df (pandas.DataFrame): Processed options data
    symbol (str): Selected underlying asset symbol
    expiry_date (datetime): Selected expiry date
    
    Returns:
    tuple: (calls_df, puts_df) Formatted DataFrames for display
    """
    # Filter data
    filtered_df = df[
        (df['symbol'] == symbol) &
        (df['expiry_date'] == expiry_date)
    ]
    
    # Separate calls and puts
    calls_df = filtered_df[filtered_df['option_type'] == 'CALL'].copy()
    puts_df = filtered_df[filtered_df['option_type'] == 'PUT'].copy()
    
    # Sort by strike price
    calls_df = calls_df.sort_values('strike')
    puts_df = puts_df.sort_values('strike')
    
    # Select and rename columns for display
    display_columns = [
        'strike', 'bid', 'ask', 'volume', 'open_interest'
    ]
    
    calls_df = calls_df[display_columns]
    puts_df = puts_df[display_columns]
    
    return calls_df, puts_df
