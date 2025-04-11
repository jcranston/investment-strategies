import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf


def load_sp500_tickers():
    return pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0][
        "Symbol"
    ].tolist()


def download_stock_data(tickers, start_date, end_date):
    print("Downloading data...")
    return yf.download(
        tickers, start=start_date, end=end_date, group_by="ticker", threads=True
    )


def download_spy_benchmark(start_date, end_date, initial_capital):
    spy = yf.download("SPY", start=start_date, end=end_date, threads=False)
    if isinstance(spy.columns, pd.MultiIndex):
        spy.columns = spy.columns.get_level_values(0)
    spy = spy[["Close"]].copy()
    spy = spy.rename(columns={"Close": "SPY_Close"})
    spy["Benchmark"] = spy["SPY_Close"] / spy["SPY_Close"].iloc[0] * initial_capital
    return spy


def simulate_portfolio(signal_df, initial_capital):
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

    portfolio_df = pd.DataFrame(portfolio_over_time).set_index("Date")
    return portfolio_df


def plot_portfolio_vs_benchmark(
    portfolio_df, benchmark_df, title="Portfolio vs. Benchmark"
):
    plot_df = portfolio_df.join(benchmark_df[["Benchmark"]], how="inner")
    plot_df["Daily Change (%)"] = plot_df["Portfolio"].pct_change() * 100

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(14, 10), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )

    ax1.plot(
        plot_df.index, plot_df["Portfolio"], label="Strategy Portfolio", linewidth=2
    )
    ax1.plot(
        plot_df.index,
        plot_df["Benchmark"],
        label="SPY Benchmark",
        linestyle="--",
        linewidth=1.5,
    )
    ax1.fill_between(plot_df.index, plot_df["Portfolio"], alpha=0.2)

    ax1.set_title(title, fontsize=16)
    ax1.set_ylabel("Portfolio Value ($)")
    ax1.legend()
    ax1.grid(True)

    ax2.plot(plot_df.index, plot_df["Daily Change (%)"], color="tab:gray")
    ax2.axhline(0, color="black", linewidth=0.5)
    ax2.set_title("Daily % Change in Portfolio Value")
    ax2.set_ylabel("% Change")
    ax2.set_xlabel("Date")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()


def plot_simple_portfolio(
    portfolio_df, benchmark_df=None, title="Portfolio Value Over Time"
):
    plt.figure(figsize=(12, 6))
    plt.plot(
        portfolio_df.index,
        portfolio_df["Portfolio"],
        label="Strategy Portfolio",
        linewidth=2,
    )
    plt.fill_between(portfolio_df.index, portfolio_df["Portfolio"], alpha=0.2)
    if benchmark_df is not None:
        plt.plot(
            benchmark_df.index,
            benchmark_df["Benchmark"],
            label="SPY Benchmark",
            linestyle="--",
            linewidth=1.5,
        )
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
