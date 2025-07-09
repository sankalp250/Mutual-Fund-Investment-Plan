# src/analysis_engine.py

import pandas as pd
import numpy as np

def calculate_daily_returns(price_data):
    """
    Calculates the daily percentage returns for each asset.
    """
    daily_returns = price_data.pct_change()
    daily_returns = daily_returns.dropna(axis=0, how='all')
    return daily_returns

def calculate_annualized_volatility(daily_returns):
    """
    Calculates the annualized volatility (standard deviation of returns).
    """
    return daily_returns.std() * np.sqrt(252)

def calculate_sharpe_ratio(daily_returns, risk_free_rate):
    """
    Calculates the Sharpe Ratio for each asset.
    """
    average_daily_return = daily_returns.mean()
    annualized_return = average_daily_return * 252
    annualized_volatility = calculate_annualized_volatility(daily_returns)
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
    return sharpe_ratio

def calculate_beta(asset_returns, benchmark_returns):
    """
    Calculates the Beta of assets relative to a benchmark.
    This version expects 'asset_returns' not to contain the benchmark itself.
    """
    # Combine returns for covariance calculation
    combined = asset_returns.join(benchmark_returns)
    
    # Calculate covariance matrix
    cov_matrix = combined.cov()
    
    # Get benchmark variance
    benchmark_variance = benchmark_returns.var()
    
    # Calculate beta for each asset
    # Select the benchmark's column from the covariance matrix
    cov_vs_benchmark = cov_matrix[benchmark_returns.name]
    beta = cov_vs_benchmark / benchmark_variance
    
    # Drop the benchmark's own beta (which is 1)
    return beta.drop(benchmark_returns.name)