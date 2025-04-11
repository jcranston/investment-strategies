import pandas as pd
from helpers import (
    download_spy_benchmark,
    download_stock_data,
    load_sp500_tickers,
    plot_simple_portfolio,
    simulate_portfolio,
)

start_date = "2023-12-15"
end_date = "2024-12-31"
initial_capital = 1_000_000

tickers = load_sp500_tickers()
all_data = download_stock_data(tickers, start_date, end_date)

rolling_signals = []

for ticker in tickers:
    try:
        if ticker not in all_data.columns.levels[0]:
            continue

        df = all_data[ticker].copy()
        df.columns = df.columns.get_level_values(0)
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

                rolling_signals.append(
                    {
                        "Date": df.loc[i, "Date"],
                        "Ticker": ticker,
                        "Investment_Signal": abs(change),
                        "Return_Pct": return_pct,
                    }
                )

    except Exception as e:
        print(f"Error processing {ticker}: {e}")

signal_df = pd.DataFrame(rolling_signals).sort_values("Date")

portfolio_df = simulate_portfolio(signal_df, initial_capital)
spy = download_spy_benchmark(start_date, end_date, initial_capital)

final_value = portfolio_df["Portfolio"].iloc[-1]
print(f"\nFinal portfolio value (rolling weekly): ${final_value:,.2f}")
print(f"Total return: {(final_value - initial_capital) / initial_capital:.2%}")

plot_simple_portfolio(portfolio_df, spy, title="Rolling Weekly Strategy vs. SPY (2024)")
