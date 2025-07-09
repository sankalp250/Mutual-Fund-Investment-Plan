# 📈 Mutual Fund & ETF Portfolio Analyzer

This Streamlit application is an interactive tool for modern portfolio analysis, designed to help users build a well-balanced investment portfolio based on principles of Modern Portfolio Theory (MPT).

The project simulates the workflow of a financial data analyst, starting from data ingestion and cleaning, moving to exploratory risk & return analysis, and concluding with sophisticated portfolio optimization.

## ✨ Features

- **Multi-Page Interface:** A clean, user-friendly interface with separate pages for each stage of the analysis.
- **Dynamic Data Loading:** Fetches up-to-date historical asset prices from Yahoo Finance (`yfinance`).
- **Time Series Analysis:** Interactive Plotly charts to visualize historical asset performance and daily return volatility.
- **In-Depth Fund Analysis:** A "Deep Dive" page to analyze the return distribution and behavior of individual assets.
- **Comparative Risk Metrics:** A summary dashboard that calculates and compares key metrics across all assets:
  - **Annualized Volatility:** The standard measure of an asset's risk.
  - **Sharpe Ratio:** The crucial measure of risk-adjusted return.
  - **Beta (β):** A measure of volatility relative to a market benchmark (e.g., SPY).
- **Correlation Analysis:** A visual heatmap to assess diversification opportunities between assets.
- **Interactive Portfolio Optimization:** Implements a Monte Carlo simulation to plot the **Efficient Frontier** and identifies two key portfolios:
  1.  **Max Sharpe Ratio Portfolio:** The optimal portfolio for the best risk-adjusted return.
  2.  **Minimum Variance Portfolio:** The safest possible combination of the selected assets.
- **Client-Ready Recommendation:** Presents the optimal portfolio allocation as a clean pie chart and a table of expected performance metrics.

## 🚀 How to Run Locally

To run this application on your local machine, follow these steps:

1.  **Clone the repository (or ensure you have the project folder):**
    ```bash
    git clone https://github.com/sankalp250/Mutual-Fund-Investment-Plan.git
    cd mutual_fund_portfolio_analyzer
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    Your web browser will automatically open with the running application.

## 🛠️ Technologies Used

- **Language:** Python
- **Core Libraries:**
  - `Streamlit`: For building the interactive web application.
  - `Pandas`: For data manipulation and analysis.
  - `NumPy`: For numerical operations and the Monte Carlo simulation.
  - `yfinance`: For downloading financial data.
  - `Plotly`: For creating beautiful, interactive charts.
  - `SciPy`: (Used implicitly by other libraries for statistical functions).
