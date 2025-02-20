import pandas as pd

def validate_excel_file(file):
    """
    Validate the uploaded Excel file format and content.
    
    Parameters:
    file: Streamlit uploaded file object
    
    Returns:
    bool: True if file is valid, False otherwise
    """
    try:
        df = pd.read_excel(file)
        
        # Required columns for options data
        required_columns = {
            'symbol',
            'expiry_date',
            'strike',
            'option_type',
            'bid',
            'ask',
            'volume',
            'open_interest'
        }
        
        # Convert actual columns to lowercase for comparison
        actual_columns = {col.lower().strip() for col in df.columns}
        
        # Check if all required columns are present
        if not required_columns.issubset(actual_columns):
            return False
            
        # Check data types
        if not pd.api.types.is_numeric_dtype(df['strike']):
            return False
        if not pd.api.types.is_numeric_dtype(df['bid']):
            return False
        if not pd.api.types.is_numeric_dtype(df['ask']):
            return False
            
        return True
        
    except Exception:
        return False
