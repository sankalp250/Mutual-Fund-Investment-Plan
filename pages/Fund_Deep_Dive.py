# pages/1_📊_Fund_Deep_Dive.py

import streamlit as st
import plotly.express as px
from src.data_ingestion import load_data
from src.analysis_engine import calculate_daily_returns
import config

st.set_page_config(page_title="Fund Deep Dive", page_icon="📊", layout="wide")

price_data, successful_tickers = load_data(
    list(set(config.TICKERS + [config.BENCHMARK_TICKER])),
    config.START_DATE,
    config.END_DATE
)
# This list is now guaranteed to only contain tickers that are in the dataframe
tickers_for_selection = [t for t in successful_tickers if t in config.TICKERS]

st.title("📊 Fund Deep Dive")
st.markdown("Analyze the historical performance and volatility of individual assets.")

# THIS IS THE KEY FIX: Check if we have any assets to show
if not price_data.empty and tickers_for_selection:
    selected_asset = st.sidebar.selectbox(
        "Choose an asset for a detailed view:", options=tickers_for_selection
    )

    # Further check if a valid asset is selected before plotting
    if selected_asset and selected_asset in price_data.columns:
        daily_returns = calculate_daily_returns(price_data)
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Daily Returns Over Time")
            fig_returns = px.line(daily_returns, y=selected_asset, title=f"{selected_asset} Daily Returns", template="plotly_white")
            fig_returns.update_layout(xaxis_title="Date", yaxis_title="Daily Return")
            st.plotly_chart(fig_returns, use_container_width=True)

        with col2:
            st.subheader("Distribution of Daily Returns")
            fig_hist = px.histogram(daily_returns, x=selected_asset, nbins=100, title=f"{selected_asset} Returns Distribution", template="plotly_white")
            fig_hist.update_layout(xaxis_title="Daily Return", yaxis_title="Frequency")
            st.plotly_chart(fig_hist, use_container_width=True)
else:
    st.warning("No assets could be loaded for analysis. Please check app logs or try again later.")