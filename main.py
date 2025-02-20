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

            # Asset selection
            st.markdown("### Select Asset")
            selected_symbol = st.selectbox(
                "Select Underlying Asset",
                options=sorted(processed_data['symbol'].unique())
            )

            # Create and display matrix view
            matrix_df, headers = create_matrix_view(processed_data, selected_symbol)

            # Display the matrix
            st.markdown("### Options Matrix")
            st.markdown(f"**{selected_symbol}**")

            # Format the strike price column
            matrix_df['Strike'] = matrix_df['Strike'].apply(lambda x: f"{x:.2f}")

            # Display the matrix with custom formatting
            st.dataframe(
                matrix_df,
                column_config={
                    "Strike": st.column_config.TextColumn(
                        "Strike",
                        width="small",
                    ),
                    **{col: st.column_config.TextColumn(
                        col,
                        width="medium",
                    ) for col in matrix_df.columns if col != "Strike"}
                },
                hide_index=True
            )

        except Exception as e:
            st.error(f"An error occurred while processing the file: {str(e)}")

    else:
        st.info("Please upload an Excel file to begin analysis.")

if __name__ == "__main__":
    main()