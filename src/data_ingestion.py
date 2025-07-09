# src/data_ingestion.py

import yfinance as yf
import pandas as pd
import streamlit as st
import config

@st.cache_data(show_spinner="Downloading financial data...")
def load_data(tickers, start_date, end_date):
    """
    Downloads historical 'Adjusted Close' prices for a list of tickers
    from Yahoo Finance.
    """
    try:
        # We explicitly set auto_adjust=False to maintain the 'Adj Close' column, which we use.
        # This makes the FutureWarning disappear.
        all_data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)
        
        adj_close_data = all_data['Adj Close']
        
        if adj_close_data.empty:
            st.error("Could not download any data. Check ticker symbols and date range.")
            return pd.DataFrame()
            
        adj_close_data.dropna(axis=1, how='all', inplace=True)

        return adj_close_data

    except Exception as e:
        st.error(f"An error occurred during data download: {e}")
        return pd.DataFrame()

# You can add a small test block to run this file directly and see if it works
if __name__ == '__main__':
    data = load_data(config.TICKERS, config.START_DATE, config.END_DATE)
    
    if not data.empty:
        print("Data loaded successfully!")
        print(data.head())