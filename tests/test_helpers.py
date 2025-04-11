import pandas as pd
from investment_strategies import helpers


def test_load_sp500_tickers():
    tickers = helpers.load_sp500_tickers()
    assert isinstance(tickers, list)
    assert "AAPL" in tickers  # Apple should always be in S&P 500


def test_simulate_portfolio_with_mock_data():
    data = {
        "Date": pd.date_range("2024-01-01", periods=3),
        "Ticker": ["TEST", "TEST", "TEST"],
        "Investment_Signal": [1.0, 2.0, 1.5],
        "Return_Pct": [0.01, -0.02, 0.03],
    }
    df = pd.DataFrame(data)
    result_df = helpers.simulate_portfolio(df, initial_capital=1000)
    assert not result_df.empty
    assert result_df["Portfolio"].iloc[0] == 1010.0  # first day: 1.0 * 0.01 * 1000
