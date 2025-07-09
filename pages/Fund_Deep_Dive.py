# pages/1_📊_Fund_Deep_Dive.py

import streamlit as st
import plotly.express as px
import pandas as pd

# Import our custom modules
from src.data_ingestion import load_data
from src.analysis_engine import calculate_daily_returns
import config

st.set_page_config(
    page_title="Fund Deep Dive",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Fund Deep Dive")
st.markdown("Analyze the historical performance and volatility of individual assets.")


# --- Data Loading ---
# Note: Thanks to st.cache_data, this will be instant if app.py has already run.
all_tickers = list(set(config.TICKERS + [config.BENCHMARK_TICKER]))
stock_data = load_data(all_tickers, config.START_DATE, config.END_DATE)

# Calculate daily returns for all stocks
daily_returns = calculate_daily_returns(stock_data)

if not stock_data.empty:
    # --- Sidebar for User Input ---
    st.sidebar.header("Select an Asset")
    selected_asset = st.sidebar.selectbox(
        "Choose an asset for a detailed view:",
        options=config.TICKERS
    )
    
    st.header(f"Analysis for: {selected_asset}")

    # --- Display Charts ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Daily Returns Over Time")
        fig_returns = px.line(
            daily_returns,
            x=daily_returns.index,
            y=selected_asset,
            title=f"{selected_asset} Daily Returns",
            template="plotly_white"
        )
        fig_returns.update_layout(xaxis_title="Date", yaxis_title="Daily Return")
        st.plotly_chart(fig_returns, use_container_width=True)

    with col2:
        st.subheader("Distribution of Daily Returns")
        fig_hist = px.histogram(
            daily_returns,
            x=selected_asset,
            nbins=100, # More bins for a detailed view
            title=f"{selected_asset} Returns Distribution",
            template="plotly_white"
        )
        fig_hist.update_layout(xaxis_title="Daily Return", yaxis_title="Frequency")
        st.plotly_chart(fig_hist, use_container_width=True)
else:
    st.warning("Please go to the Homepage to load the data first.")