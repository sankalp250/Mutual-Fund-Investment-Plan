# pages/2_🔬_Risk_and_Return_Analysis.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Import our custom modules
from src.data_ingestion import load_data
from src.analysis_engine import (
    calculate_daily_returns,
    calculate_annualized_volatility,
    calculate_sharpe_ratio,
    calculate_beta
)
import config

st.set_page_config(page_title="Risk & Return Analysis", page_icon="🔬", layout="wide")

st.title("🔬 Risk & Return Analysis")
st.markdown("""
This page provides a comparative analysis of the selected assets based on key risk and return metrics.
""")

# --- Data Loading and Processing ---
all_tickers = list(set(config.TICKERS + [config.BENCHMARK_TICKER]))
price_data = load_data(all_tickers, config.START_DATE, config.END_DATE)
daily_returns = calculate_daily_returns(price_data)

if not daily_returns.empty:
    asset_returns = daily_returns[config.TICKERS]
    benchmark_returns_series = daily_returns[config.BENCHMARK_TICKER]

    # --- Calculate Metrics ---
    volatility = calculate_annualized_volatility(asset_returns)
    sharpe = calculate_sharpe_ratio(asset_returns, config.RISK_FREE_RATE)
    
    assets_for_beta = asset_returns.drop(columns=[config.BENCHMARK_TICKER], errors='ignore')
    beta_values = calculate_beta(assets_for_beta, benchmark_returns_series)
    beta_values[config.BENCHMARK_TICKER] = 1.0
    
    # --- Create Summary DataFrame ---
    summary_df = pd.DataFrame({
        "Annualized Volatility (Std Dev)": volatility,
        "Sharpe Ratio": sharpe,
        "Beta (β)": beta_values
    })
    
    # --- Create Pre-Formatted DataFrame for Display ---
    display_df = summary_df.copy()
    display_df['Annualized Volatility (Std Dev)'] = display_df['Annualized Volatility (Std Dev)'].map('{:.2%}'.format)
    display_df['Sharpe Ratio'] = display_df['Sharpe Ratio'].map('{:.2f}'.format)
    display_df['Beta (β)'] = display_df['Beta (β)'].map('{:.2f}'.format)
    display_df.sort_index(inplace=True)

    st.header("Comparative Metrics Table")

    # --- THE FINAL FIX: Using st.table() ---
    # This renders a static table that is guaranteed not to vibrate.
    st.table(display_df)
    # --- END OF FINAL FIX ---
    
    # --- Correlation Analysis ---
    st.header("Asset Correlation Heatmap")
    correlation_matrix = asset_returns.corr()
    
    fig_corr = px.imshow(
        correlation_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='RdYlGn',
        title="Correlation Between Asset Daily Returns"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

else:
    st.warning("Please go to the Homepage to load the data first.")