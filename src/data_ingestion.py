# src/data_ingestion.py

import yfinance as yf
import pandas as pd
import streamlit as st
import config

@st.cache_data(show_spinner="Downloading financial data...")
def load_data(tickers, start_date, end_date):
    """
    Downloads historical 'Adjusted Close' prices and returns a list
    of the tickers that were successfully downloaded.
    
    Returns:
        tuple: A tuple containing:
            - pandas.DataFrame: The price data.
            - list: The list of tickers successfully loaded.
    """
    try:
        all_data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)
        
        if all_data.empty:
            st.error("Could not download any data. Check tickers and date range.")
            return pd.DataFrame(), []
            
        adj_close_data = all_data['Adj Close']
        adj_close_data.dropna(axis=1, how='all', inplace=True)

        # The new, crucial part: return the list of columns that actually exist.
        successful_tickers = adj_close_data.columns.tolist()
        
        return adj_close_data, successful_tickers

    except Exception as e:
        st.error(f"An error occurred during data download: {e}")
        return pd.DataFrame(), []