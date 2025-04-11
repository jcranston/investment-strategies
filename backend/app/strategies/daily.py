import pandas as pd
import yfinance as yf


def simulate_daily(start_date: str, end_date: str, tickers: list) -> dict:
    all_data = yf.download(
        tickers, start=start_date, end=end_date, group_by="ticker", threads=True
    )

    daily_signals = []
    for ticker in tickers:
        try:
            if ticker not in all_data.columns.levels[0]:
                continue

            df = all_data[ticker].copy()
            df.columns = df.columns.get_level_values(0)
            df["Ticker"] = ticker
            df["Change"] = df["Close"].diff()
            df["Prev_Change"] = df["Change"].shift(1)
            df["Buy"] = df["Prev_Change"] < 0
            df["Investment_Signal"] = df["Prev_Change"].abs()
            df["Return_Pct"] = (df["Close"] - df["Open"]) / df["Open"]
            daily_signals.append(df[["Ticker", "Investment_Signal", "Return_Pct"]])
        except Exception:
            continue

    signal_df = pd.concat(daily_signals)
    signal_df.reset_index(inplace=True)
    signal_df = signal_df.sort_values(["Date", "Ticker"])

    initial_capital = 1_000_000
    portfolio_value = initial_capital
    portfolio_over_time = []

    for date, group in signal_df.groupby("Date"):
        buys = group.dropna(subset=["Investment_Signal", "Return_Pct"])
        buys = buys[buys["Investment_Signal"] > 0]

        if buys.empty:
            portfolio_over_time.append({"Date": date, "Portfolio": portfolio_value})
            continue

        weights = buys["Investment_Signal"] / buys["Investment_Signal"].sum()
        allocations = portfolio_value * weights
        returns = allocations * buys["Return_Pct"].values
        portfolio_value += returns.sum()
        portfolio_over_time.append({"Date": date, "Portfolio": portfolio_value})

    return {"strategy": "daily", "portfolio": portfolio_over_time}
