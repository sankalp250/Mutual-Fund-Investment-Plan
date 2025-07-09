# app.py

import streamlit as st
import pandas as pd
import plotly.express as px # NEW: Import the plotly express library

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

**Project Mandates:**
- **Time Series Analysis:** Analyzing historical Net Asset Values (NAVs) and calculating returns.
- **Risk Analysis:** Using key metrics like Standard Deviation, Sharpe Ratio, and Beta to assess risk.

Navigate through the pages in the sidebar to explore the different stages of the analysis.
""")


# --- Data Loading and Display ---

st.header("1. Data Loading")
st.markdown(f"""
We start by loading historical 'Adjusted Close' price data for our chosen assets.
- **Tickers:** `{', '.join(config.TICKERS)}`
- **Time Period:** `{config.START_DATE}` to `{config.END_DATE}`
- **Benchmark:** `{config.BENCHMARK_TICKER}`
""")

# Load data using our function
all_tickers = list(set(config.TICKERS + [config.BENCHMARK_TICKER]))
stock_data = load_data(all_tickers, config.START_DATE, config.END_DATE)


if not stock_data.empty:
    st.success("Data loaded successfully!")
    
    with st.expander("View Raw Historical Data"):
        st.dataframe(stock_data.head())
        
    st.subheader("Historical Performance (Adjusted Close Prices)")
    
    # --- THIS IS THE CHANGED SECTION ---
    # OLD CODE: st.line_chart(stock_data)

    # NEW: Create an interactive Plotly chart with a light theme
    fig = px.line(
        stock_data, 
        x=stock_data.index, 
        y=stock_data.columns,
        title='Asset Price Performance',
        template='plotly_white'  # Use a clean, light theme
    )

    # Improve the layout for clarity
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Adjusted Close Price (USD)',
        legend_title='Tickers',
        height=500 # You can adjust the height of the chart
    )
    
    # Display the Plotly chart in Streamlit, making it expand to the container width
    st.plotly_chart(fig, use_container_width=True)
    # --- END OF CHANGED SECTION ---


    st.info("The data has been loaded and is ready for analysis. Please proceed to the next pages.")

else:
    st.error("Failed to load data. Please check the configurations and your internet connection.")

st.sidebar.success("Select an analysis page above.")