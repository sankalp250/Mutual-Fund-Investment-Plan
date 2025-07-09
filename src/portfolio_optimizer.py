# src/portfolio_optimizer.py

import pandas as pd
import numpy as np

def run_portfolio_optimization(daily_returns, num_portfolios, risk_free_rate):
    """
    Performs a Monte Carlo simulation to find the efficient frontier
    and the optimal portfolio.

    Args:
        daily_returns (pd.DataFrame): Daily returns for the assets.
        num_portfolios (int): The number of random portfolios to generate.
        risk_free_rate (float): The risk-free rate for Sharpe Ratio calc.

    Returns:
        tuple: A tuple containing:
            - A DataFrame of all simulated portfolio results.
            - A Series for the portfolio with the max Sharpe ratio.
            - A Series for the portfolio with the minimum volatility.
    """
    
    # Get the list of assets
    tickers = daily_returns.columns
    
    # Calculate annualized mean returns and the covariance matrix
    mean_returns = daily_returns.mean() * 252
    cov_matrix = daily_returns.cov() * 252

    # Initialize lists to store the results
    results_list = []
    weights_list = []

    for _ in range(num_portfolios):
        # 1. Generate random weights that sum to 1
        weights = np.random.random(len(tickers))
        weights /= np.sum(weights)
        weights_list.append(weights)

        # 2. Calculate portfolio's annualized return, volatility, and Sharpe ratio
        portfolio_return = np.sum(mean_returns * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
        
        # Store results
        results_list.append([portfolio_return, portfolio_volatility, sharpe_ratio])

    # Create a DataFrame of portfolio weights
    weights_df = pd.DataFrame(weights_list, columns=tickers)
    
    # Create a DataFrame of portfolio results
    results_df = pd.DataFrame(results_list, columns=['Return', 'Volatility', 'Sharpe Ratio'])

    # Combine weights and results into a single DataFrame
    all_portfolios_df = pd.concat([results_df, weights_df], axis=1)

    # Find the portfolio with the highest Sharpe ratio (Optimal Portfolio)
    max_sharpe_portfolio = all_portfolios_df.iloc[all_portfolios_df['Sharpe Ratio'].idxmax()]

    # Find the portfolio with the minimum volatility (Minimum Variance Portfolio)
    min_vol_portfolio = all_portfolios_df.iloc[all_portfolios_df['Volatility'].idxmin()]

    return all_portfolios_df, max_sharpe_portfolio, min_vol_portfolio