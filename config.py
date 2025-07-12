# config.py

# --- Main Configuration ---

# Define the list of ticker symbols for the mutual funds/ETFs to analyze.
# We've chosen a diverse mix of US-based ETFs:
# SPY: S&P 500 index - The core US market.
# BND: Total Bond Market - For stability and diversification.
# QQQ: NASDAQ-100 - Tech and growth focused.
# IJS: Small-Cap Value - Represents smaller US companies.
# EFA: International Markets (EAFE) - For global diversification.
TICKERS = [
    "SPY",
    "BND",
    "QQQ",
    "IJS",
    "EFA"
]

# --- Analysis Parameters ---

# Define the start and end dates for downloading the historical data.
# A 10-year period gives a good view of performance across different market cycles.
START_DATE = "2014-01-01"
END_DATE = "2023-12-31"


# --- Portfolio Optimization Parameters ---

# Define the risk-free rate for the Sharpe Ratio calculation.
# This is typically the yield on a long-term government bond.
# We'll use 2% or 0.02 as an approximation.
RISK_FREE_RATE = 0.02

# The number of random portfolios to generate for the Monte Carlo simulation.
# A higher number will give a more precise Efficient Frontier but will take longer to compute.
NUM_PORTFOLIOS = 15000


# --- Benchmark Configuration ---

# Define the ticker symbol for the market benchmark.
# This is used for calculating the Beta of the other assets.
# The S&P 500 (SPY) is a standard choice for a US market benchmark.
BENCHMARK_TICKER = "SPY"
