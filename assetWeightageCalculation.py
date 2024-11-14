import pandas as pd
import yfinance as yf
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt import HRPOpt

# -- Getting Data from Yahoo Finance --
def download_data(tickers):
    df = pd.DataFrame()
    for ticker in tickers:
        data = yf.download(ticker, start="2007-08-01", end="2024-11-09")
        if 'Adj Close' in data.columns:
            df[ticker] = data['Adj Close']
    return df

# -- Portfolio Optimization --
def calculate_optimization(df):
    
    # -- MVO - High sharpe optimization for high risk tolerance
    mu = expected_returns.mean_historical_return(df)  # annual expected returns
    S = risk_models.sample_cov(df)  # covariance matrix
    ef = EfficientFrontier(mu, S)  
    weights = ef.max_sharpe()
    mvo_weights_clean = ef.clean_weights()
    

    # -- Hierarchical risk parity optimization for medium risk tolerance
    hrp = HRPOpt(df.pct_change().dropna())
    risk_parity_weights = hrp.optimize()
    risk_parity_weights_clean = hrp.clean_weights()
    
    
    # -- Minimum variance optimization for low risk tolerance
    ef_mvp = EfficientFrontier(mu, S)
    mvp_weights = ef_mvp.min_volatility()
    mvp_weights_clean = ef_mvp.clean_weights()
    
    
    return mvo_weights_clean, risk_parity_weights_clean, mvp_weights_clean