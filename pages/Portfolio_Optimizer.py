# pages/3_✨_Portfolio_Optimizer.py

import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_ingestion import load_data
from src.analysis_engine import calculate_daily_returns
from src.portfolio_optimizer import run_portfolio_optimization
import config

st.set_page_config(page_title="Portfolio Optimizer", page_icon="✨", layout="wide")

st.title("✨ Portfolio Optimizer")
st.markdown("""
This page uses Modern Portfolio Theory to find an optimal allocation of assets based on a selected risk profile. 
The simulation runs thousands of randomly weighted portfolios to identify the **Efficient Frontier**.
""")

# --- Data Loading and Prep ---
price_data = load_data(config.TICKERS, config.START_DATE, config.END_DATE)
daily_returns = calculate_daily_returns(price_data)

if not daily_returns.empty:
    
    # --- NEW: Client Profile Selector ---
    st.sidebar.header("Select Your Profile")
    risk_profile = st.sidebar.radio(
        "Client Risk Tolerance:",
        options=['Conservative', 'Moderate', 'Aggressive'],
        index=1, # Default to 'Moderate'
        help="""
        - **Conservative:** Aims for the lowest possible risk.
        - **Moderate:** Aims for the highest risk-adjusted return (best 'bang for your buck').
        - **Aggressive:** Aims for the highest possible return, accepting higher risk.
        """
    )
    
    st.sidebar.header("Optimization Settings")
    num_portfolios_input = st.sidebar.number_input(
        "Number of Simulations:", 
        min_value=5000, max_value=50000, value=config.NUM_PORTFOLIOS, step=1000
    )
    
    if st.sidebar.button("Run Optimization", key="run_button"):
        with st.spinner("Finding the optimal portfolios... This may take a moment."):
            all_portfolios, max_sharpe_port, min_vol_port = run_portfolio_optimization(
                daily_returns, num_portfolios_input, config.RISK_FREE_RATE
            )
        
            # --- NEW: Select a portfolio based on the user's profile ---
            if risk_profile == 'Conservative':
                recommended_portfolio = min_vol_port
                profile_header = "Conservative Profile (Lowest Risk)"
            elif risk_profile == 'Aggressive':
                # Find the portfolio with the highest return from all simulations
                recommended_portfolio = all_portfolios.loc[all_portfolios['Return'].idxmax()]
                profile_header = "Aggressive Profile (Highest Return)"
            else: # Moderate
                recommended_portfolio = max_sharpe_port
                profile_header = "Moderate Profile (Best Risk-Adjusted Return)"
            
            st.success("Optimization Complete!")

            # --- CHANGED: Display dynamic results based on profile ---
            st.header(f"Recommendation for: {profile_header}")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.subheader("Recommended Allocation")
                optimal_weights = recommended_portfolio[config.TICKERS][recommended_portfolio[config.TICKERS] > 0.01]
                fig_pie = px.pie(
                    optimal_weights, names=optimal_weights.index, values=optimal_weights.values,
                    title='Recommended Asset Allocation', hole=.3
                )
                fig_pie.update_traces(textinfo='percent+label', textfont_size=14)
                st.plotly_chart(fig_pie, use_container_width=True)

            with col2:
                st.subheader("Portfolio Performance Metrics")
                st.markdown(f"""
                | Metric | Value |
                | :--- | ---: |
                | **Expected Annual Return** | `{recommended_portfolio['Return']:.2%}` |
                | **Expected Annual Volatility** | `{recommended_portfolio['Volatility']:.2%}` |
                | **Sharpe Ratio** | `{recommended_portfolio['Sharpe Ratio']:.2f}` |
                """)
            
            # --- Efficient Frontier Chart (now with a new marker!) ---
            st.header("The Efficient Frontier")
            
            fig_frontier = px.scatter(
                all_portfolios, x='Volatility', y='Return', color='Sharpe Ratio',
                title='Efficient Frontier', template='plotly_white', color_continuous_scale='viridis'
            )
            # Add markers for the standard key portfolios
            fig_frontier.add_scatter(x=[max_sharpe_port['Volatility']], y=[max_sharpe_port['Return']], mode='markers',
                                     marker=dict(color='orange', size=15, symbol='star'), name='Max Sharpe Ratio')
            fig_frontier.add_scatter(x=[min_vol_port['Volatility']], y=[min_vol_port['Return']], mode='markers',
                                     marker=dict(color='blue', size=15, symbol='diamond'), name='Min Volatility')
            
            # NEW: Add a specific marker for the user-selected portfolio profile
            fig_frontier.add_scatter(x=[recommended_portfolio['Volatility']], y=[recommended_portfolio['Return']], mode='markers',
                                     marker=dict(color='red', size=20, symbol='x'), name=f'Your Selected ({risk_profile}) Portfolio')
            st.plotly_chart(fig_frontier, use_container_width=True)
            
    else:
        st.info("Select your risk profile and click 'Run Optimization' to begin.")

else:
    st.warning("Please go to the Homepage to load the data first.")