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
        # Read specific sheet
        df = pd.read_excel(file, sheet_name='Select')

        # Required columns for options data
        required_columns = {
            'TckrSymb',
            'Asst',
            'XprtnDt',
            'OptnTp',
            'ExrcPric',
            'OptnStyle',
            'Last'
        }

        # Check if all required columns are present
        actual_columns = set(df.columns)
        if not required_columns.issubset(actual_columns):
            missing_cols = required_columns - actual_columns
            print(f"Missing columns: {missing_cols}")
            return False

        # Check data types
        if not pd.api.types.is_numeric_dtype(df['ExrcPric']):
            print("Strike price (ExrcPric) must be numeric")
            return False
        if not pd.api.types.is_numeric_dtype(df['Last']):
            print("Last price must be numeric")
            return False

        return True

    except Exception as e:
        print(f"Validation error: {str(e)}")
        return False