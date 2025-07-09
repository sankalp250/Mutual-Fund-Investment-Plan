# pages/2_🔬_Risk_and_Return_Analysis.py

import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_ingestion import load_data
from src.analysis_engine import (
    calculate_daily_returns,
    calculate_annualized_volatility,
    calculate_sharpe_ratio,
    calculate_beta
)
import config

st.set_page_config(page_title="Risk & Return Analysis", page_icon="🔬", layout="wide")

price_data, successful_tickers = load_data(
    list(set(config.TICKERS + [config.BENCHMARK_TICKER])),
    config.START_DATE,
    config.END_DATE
)
main_assets = [t for t in successful_tickers if t in config.TICKERS]

st.title("🔬 Risk & Return Analysis")
st.markdown("This page provides a comparative analysis of the selected assets based on key risk and return metrics.")

if not price_data.empty and config.BENCHMARK_TICKER in price_data.columns and main_assets:
    daily_returns = calculate_daily_returns(price_data)
    # THIS IS THE KEY FIX: Use main_assets, not config.TICKERS
    asset_returns = daily_returns[main_assets]
    benchmark_returns = daily_returns[config.BENCHMARK_TICKER]

    volatility = calculate_annualized_volatility(asset_returns)
    sharpe = calculate_sharpe_ratio(asset_returns, config.RISK_FREE_RATE)

    assets_for_beta = asset_returns.drop(columns=[config.BENCHMARK_TICKER], errors='ignore')
    beta_values = calculate_beta(assets_for_beta, benchmark_returns)
    if config.BENCHMARK_TICKER in main_assets:
      beta_values[config.BENCHMARK_TICKER] = 1.0

    summary_df = pd.DataFrame({
        "Annualized Volatility (Std Dev)": volatility,
        "Sharpe Ratio": sharpe,
        "Beta (β)": beta_values
    }).dropna() # Drop any assets that couldn't be calculated

    if not summary_df.empty:
        display_df = summary_df.copy()
        display_df['Annualized Volatility (Std Dev)'] = display_df['Annualized Volatility (Std Dev)'].map('{:.2%}'.format)
        display_df['Sharpe Ratio'] = display_df['Sharpe Ratio'].map('{:.2f}'.format)
        display_df['Beta (β)'] = display_df['Beta (β)'].map('{:.2f}'.format)

        st.header("Comparative Metrics Table")
        st.table(display_df)

        st.header("Asset Correlation Heatmap")
        fig_corr = px.imshow(asset_returns.corr(), text_auto=True, aspect="auto", color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.warning("Could not load sufficient data for analysis. Please check the app logs or try again later.")