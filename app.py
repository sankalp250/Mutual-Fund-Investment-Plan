# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Import our custom modules
from src.data_ingestion import load_data
import config

# --- Page Configuration ---
st.set_page_config(
    page_title="Mutual Fund Portfolio Analyzer",
    page_icon="💰",
    layout="wide"
)

# --- Main Application ---
st.title("Building a Mutual Fund Investment Plan")

st.markdown("""
This application serves as a powerful tool for financial data analysis, simulating the role of an analyst advising a client on building a well-balanced investment portfolio.
Navigate through the pages in the sidebar to explore the different stages of the analysis.
""")

st.header("1. Data Loading")
st.markdown(f"""
- **Tickers:** `{', '.join(config.TICKERS)}`
- **Time Period:** `{config.START_DATE}` to `{config.END_DATE}`
""")

# --- THIS IS THE FIX ---
# Unpack the tuple returned by load_data
price_data, successful_tickers = load_data(
    list(set(config.TICKERS + [config.BENCHMARK_TICKER])),
    config.START_DATE,
    config.END_DATE
)

if not price_data.empty: # Check the DataFrame, not the tuple
    st.success(f"Data loaded successfully for: {', '.join(successful_tickers)}")
    
    with st.expander("View Raw Historical Data"):
        st.dataframe(price_data.head())
        
    st.subheader("Historical Performance (Adjusted Close Prices)")
    fig = px.line(price_data, x=price_data.index, y=price_data.columns, template='plotly_white')
    fig.update_layout(xaxis_title='Date', yaxis_title='Adjusted Close Price (USD)', legend_title='Tickers')
    st.plotly_chart(fig, use_container_width=True)

    st.info("The data has been loaded and is ready for analysis. Please proceed to the pages in the sidebar.")
else:
    st.error("Failed to load data. Please check configurations, internet connection, and logs.")

st.sidebar.success("Select an analysis page above.")