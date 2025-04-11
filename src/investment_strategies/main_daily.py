import pandas as pd
from helpers import (
    download_spy_benchmark,
    download_stock_data,
    load_sp500_tickers,
    plot_portfolio_vs_benchmark,
    simulate_portfolio,
)

start_date = "2024-01-01"
end_date = "2024-12-31"
initial_capital = 1_000_000

tickers = load_sp500_tickers()
all_data = download_stock_data(tickers, start_date, end_date)

daily_signals = []

for ticker in tickers:
    try:
        if ticker not in all_data.columns.levels[0]:
            continue

        df = all_data[ticker].copy()
        df.columns = df.columns.get_level_values(0)

        df["Change"] = df["Close"].diff()
        df["Prev_Change"] = df["Change"].shift(1)
        df["Investment_Signal"] = df["Prev_Change"].abs()
        df["Return_Pct"] = (df["Close"].squeeze() - df["Open"].squeeze()) / df[
            "Open"
        ].squeeze()
        df["Ticker"] = ticker

        daily_signals.append(df[["Investment_Signal", "Return_Pct", "Ticker"]])

    except Exception as e:
        print(f"Error processing {ticker}: {e}")

signal_df = pd.concat(daily_signals).dropna().reset_index()
signal_df = signal_df.sort_values(["Date", "Ticker"])

portfolio_df = simulate_portfolio(signal_df, initial_capital)
spy = download_spy_benchmark(start_date, end_date, initial_capital)

final_value = portfolio_df["Portfolio"].iloc[-1]
print(f"\nFinal portfolio value (daily): ${final_value:,.2f}")
print(f"Total return: {(final_value - initial_capital) / initial_capital:.2%}")

plot_portfolio_vs_benchmark(portfolio_df, spy, title="Daily Strategy vs. SPY (2024)")
