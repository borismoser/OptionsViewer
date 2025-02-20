import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def process_options_data(df):
    """
    Process the raw options data from Excel file.
    """
    # Convert column names to our internal format
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
    df['expiry_date'] = pd.to_datetime(df['expiry_date'])

    # Shorten option ticker (remove first 4 characters)
    df['short_ticker'] = df['option_ticker'].str[4:]

    return df

def get_date_range_defaults(df):
    """
    Get default date range based on available expiration dates.
    """
    today = pd.Timestamp.now().normalize()
    available_dates = sorted(df['expiry_date'].unique())

    # Find next available date (including today)
    start_date = next((date for date in available_dates if date >= today), available_dates[0])

    # End date is 12 months from start_date
    end_date = start_date + pd.DateOffset(months=12)

    # If end date is beyond last available date, use last available
    if end_date > available_dates[-1]:
        end_date = available_dates[-1]

    return start_date, end_date

def create_matrix_view(df, symbol, start_date=None, end_date=None):
    """
    Create horizontal matrix view with all expiry dates within range.
    """
    # Filter data for selected symbol
    filtered_df = df[df['symbol'] == symbol].copy()

    # Apply date range filter if provided
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['expiry_date'] >= start_date) &
            (filtered_df['expiry_date'] <= end_date)
        ]

    # Get all unique expiry dates and strikes
    expiry_dates = sorted(filtered_df['expiry_date'].unique())
    strikes = sorted(filtered_df['strike'].unique())

    # Initialize the result DataFrame with strike prices
    result_df = pd.DataFrame(strikes, columns=['Strike'])

    # Create column headers
    column_headers = ['Strike']
    for expiry in expiry_dates:
        expiry_str = expiry.strftime('%Y-%m-%d')
        column_headers.extend([f'{expiry_str}', f"{expiry_str}_put"])


    # Process each expiry date
    for expiry in expiry_dates:
        expiry_str = expiry.strftime('%Y-%m-%d')

        # Process calls and puts
        for strike in strikes:
            row_idx = result_df[result_df['Strike'] == strike].index[0]

            # Process call options
            call_data = filtered_df[
                (filtered_df['strike'] == strike) & 
                (filtered_df['option_type'] == 'CALL') &
                (filtered_df['expiry_date'] == expiry)
            ]
            call_value = ''
            if not call_data.empty and call_data['last_price'].iloc[0] > 0:
                ticker = call_data['short_ticker'].iloc[0]
                price = call_data['last_price'].iloc[0]
                call_value = f"{ticker:<6} {price:>6.2f}"

            # Process put options
            put_data = filtered_df[
                (filtered_df['strike'] == strike) & 
                (filtered_df['option_type'] == 'PUT') &
                (filtered_df['expiry_date'] == expiry)
            ]
            put_value = ''
            if not put_data.empty and put_data['last_price'].iloc[0] > 0:
                ticker = put_data['short_ticker'].iloc[0]
                price = put_data['last_price'].iloc[0]
                put_value = f"{ticker:<6} {price:>6.2f}"

            # Add columns for this expiry date
            if expiry_str not in result_df.columns:
                result_df[expiry_str] = ''
                result_df[f"{expiry_str}_put"] = ''

            # Set values
            result_df.at[row_idx, expiry_str] = call_value
            result_df.at[row_idx, f"{expiry_str}_put"] = put_value

    return result_df, column_headers