# pages/3_✨_Portfolio_Optimizer.py

import streamlit as st
import plotly.express as px
from src.data_ingestion import load_data
from src.analysis_engine import calculate_daily_returns
from src.portfolio_optimizer import run_portfolio_optimization
import config

st.set_page_config(page_title="Portfolio Optimizer", page_icon="✨", layout="wide")

# Use only the main tickers for optimization, not the benchmark
price_data, successful_tickers = load_data(config.TICKERS, config.START_DATE, config.END_DATE)

st.title("✨ Portfolio Optimizer")
st.markdown("This page uses Modern Portfolio Theory to find an optimal allocation of assets...")

if not price_data.empty:
    daily_returns = calculate_daily_returns(price_data)
    
    st.sidebar.header("Select Your Profile")
    risk_profile = st.sidebar.radio(
        "Client Risk Tolerance:", ['Conservative', 'Moderate', 'Aggressive'], index=1
    )
    st.sidebar.header("Optimization Settings")
    num_portfolios = st.sidebar.number_input(
        "Number of Simulations:", 5000, 50000, config.NUM_PORTFOLIOS, 1000
    )

    if st.sidebar.button("Run Optimization", key="run_button"):
        with st.spinner("Finding optimal portfolios..."):
            all_portfolios, max_sharpe, min_vol = run_portfolio_optimization(
                daily_returns, num_portfolios, config.RISK_FREE_RATE
            )
            
            if risk_profile == 'Conservative':
                recommended_portfolio, header = min_vol, "Conservative (Lowest Risk)"
            elif risk_profile == 'Aggressive':
                recommended_portfolio, header = all_portfolios.loc[all_portfolios['Return'].idxmax()], "Aggressive (Highest Return)"
            else:
                recommended_portfolio, header = max_sharpe, "Moderate (Best Risk-Adjusted)"

        st.success("Optimization Complete!")
        st.header(f"Recommendation for: {header}")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Recommended Allocation")
            weights = recommended_portfolio[successful_tickers][recommended_portfolio[successful_tickers] > 0.01]
            fig_pie = px.pie(weights, names=weights.index, values=weights.values, hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)
        with col2:
            st.subheader("Performance Metrics")
            st.markdown(f"| Metric | Value |\n|:---|---:|\n|**Expected Return**|`{recommended_portfolio['Return']:.2%}`|\n|**Expected Volatility**|`{recommended_portfolio['Volatility']:.2%}`|\n|**Sharpe Ratio**|`{recommended_portfolio['Sharpe Ratio']:.2f}`|")
        
        st.header("Efficient Frontier")
        fig_frontier = px.scatter(all_portfolios, x='Volatility', y='Return', color='Sharpe Ratio', template='plotly_white')
        fig_frontier.add_scatter(x=[recommended_portfolio['Volatility']], y=[recommended_portfolio['Return']], mode='markers', marker=dict(color='red', size=20, symbol='x'), name='Your Portfolio')
        st.plotly_chart(fig_frontier, use_container_width=True)
    else:
        st.info("Select your risk profile and click 'Run Optimization' to begin.")
else:
    st.warning("Data could not be loaded for optimization. Please check logs.")