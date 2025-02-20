import streamlit as st
import pandas as pd
from utils.data_processor import process_options_data, create_matrix_view
from utils.validators import validate_excel_file

# Page configuration
st.set_page_config(
    page_title="Options Data Viewer",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.title("Options Data Viewer")
    st.markdown("### Upload and analyze stock options data")

    # File upload section
    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx', 'xls'])

    if uploaded_file:
        try:
            # Validate the uploaded file
            if not validate_excel_file(uploaded_file):
                st.error("Invalid file format. Please ensure your Excel file contains the required columns in the 'Select' sheet.")
                st.markdown("""
                Required columns:
                - TckrSymb (Option Ticker)
                - Asst (Underlying Asset)
                - XprtnDt (Expiration Date)
                - OptnTp (Option Type)
                - ExrcPric (Strike Price)
                - OptnStyle (Option Style)
                - Last (Last Price)
                """)
                return

            # Read and process the data
            df = pd.read_excel(uploaded_file, sheet_name='Select')
            processed_data = process_options_data(df)

            # Filters
            st.markdown("### Data Filters")
            col1, col2 = st.columns(2)

            with col1:
                selected_symbol = st.selectbox(
                    "Select Underlying Asset",
                    options=sorted(processed_data['symbol'].unique())
                )

            with col2:
                expiry_dates = sorted(processed_data[
                    processed_data['symbol'] == selected_symbol
                ]['expiry_date'].unique())

                selected_expiry = st.selectbox(
                    "Select Expiry Date",
                    options=expiry_dates
                )

            # Create and display matrix view
            calls_df, puts_df = create_matrix_view(
                processed_data,
                selected_symbol,
                selected_expiry
            )

            # Display matrices side by side
            st.markdown("### Options Matrix View")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Calls")
                st.dataframe(
                    calls_df.style.format({
                        'Strike Price': '${:.2f}',
                        'Last Price': '${:.2f}'
                    }).set_properties(**{
                        'text-align': 'center'
                    })
                )

            with col2:
                st.markdown("#### Puts")
                st.dataframe(
                    puts_df.style.format({
                        'Strike Price': '${:.2f}',
                        'Last Price': '${:.2f}'
                    }).set_properties(**{
                        'text-align': 'center'
                    })
                )

        except Exception as e:
            st.error(f"An error occurred while processing the file: {str(e)}")

    else:
        st.info("Please upload an Excel file to begin analysis.")

if __name__ == "__main__":
    main()