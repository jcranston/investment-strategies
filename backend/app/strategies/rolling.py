import pandas as pd
import yfinance as yf


def simulate_rolling(start_date: str, end_date: str, tickers: list) -> dict:
    all_data = yf.download(
        tickers, start=start_date, end=end_date, group_by="ticker", threads=True
    )

    rolling_signals = []
    for ticker in tickers:
        try:
            if ticker not in all_data.columns.levels[0]:
                continue

            df = all_data[ticker].copy()
            df.columns = df.columns.get_level_values(0)
            df["Ticker"] = ticker
            df.dropna(subset=["Open", "Close"], inplace=True)
            df = df.reset_index()

            for i in range(5, len(df) - 5):
                prev_open = df.loc[i - 5, "Open"]
                prev_close = df.loc[i - 1, "Close"]
                change = prev_close - prev_open

                if change < 0:
                    entry_open = df.loc[i, "Open"]
                    exit_index = i + 4
                    if exit_index >= len(df):
                        continue
                    exit_close = df.loc[exit_index, "Close"]
                    return_pct = (exit_close - entry_open) / entry_open

                    signal = {
                        "Date": df.loc[i, "Date"],
                        "Ticker": ticker,
                        "Investment_Signal": abs(change),
                        "Return_Pct": return_pct,
                    }
                    rolling_signals.append(signal)
        except Exception:
            continue

    signal_df = pd.DataFrame(rolling_signals)
    signal_df = signal_df.sort_values("Date")

    initial_capital = 1_000_000
    portfolio_value = initial_capital
    portfolio_over_time = []

    for date, group in signal_df.groupby("Date"):
        buys = group[group["Investment_Signal"] > 0]

        if buys.empty:
            portfolio_over_time.append({"Date": date, "Portfolio": portfolio_value})
            continue

        weights = buys["Investment_Signal"] / buys["Investment_Signal"].sum()
        allocations = portfolio_value * weights
        returns = allocations * buys["Return_Pct"].values
        portfolio_value += returns.sum()
        portfolio_over_time.append({"Date": date, "Portfolio": portfolio_value})

    return {"strategy": "rolling", "portfolio": portfolio_over_time}
