import pandas as pd
import numpy as np

def process_options_data(df):
    """
    Process the raw options data from Excel file.

    Parameters:
    df (pandas.DataFrame): Raw options data from 'Select' sheet

    Returns:
    pandas.DataFrame: Processed options data
    """
    # Convert column names to our internal format for processing
    df = df.rename(columns={
        'TckrSymb': 'option_ticker',
        'Asst': 'symbol',
        'XprtnDt': 'expiry_date',
        'OptnTp': 'option_type',
        'ExrcPric': 'strike',
        'OptnStyle': 'style',
        'Last': 'last_price'
    })

    # Basic data cleaning
    df['symbol'] = df['symbol'].str.upper()
    df['option_type'] = df['option_type'].str.upper()
    df['style'] = df['style'].str.upper()

    # Convert date format
    df['expiry_date'] = pd.to_datetime(df['expiry_date'])

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
    display_columns = {
        'strike': 'Strike Price',
        'last_price': 'Last Price',
        'style': 'Style',
        'option_ticker': 'Option Ticker'
    }

    calls_df = calls_df[display_columns.keys()].rename(columns=display_columns)
    puts_df = puts_df[display_columns.keys()].rename(columns=display_columns)

    return calls_df, puts_df