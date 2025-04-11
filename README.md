# 🧠 Investment Strategies Simulator

This project explores simple, signal-driven stock trading strategies applied to historical S&P 500 data, simulating how a portfolio would perform under different conditions.

The core idea is to **test if recent price drops predict short-term rebounds** — a basic form of contrarian or mean-reversion strategy. These types of strategies are commonly explored in quantitative finance and behavioral economics, based on the intuition that investors tend to overreact in the short term.

### 📈 What the simulations do:

- **Daily strategy**:
  For each stock in the S&P 500, if the stock **dropped yesterday**, we invest proportionally to the size of that drop at the **next day’s open**, and sell at the **close** of the same day. The strategy repeats this daily across the year.

- **Rolling weekly strategy**:
  For each stock, we scan rolling 5-day windows. If the stock **dropped over the past 5 trading days**, we simulate buying it at the **next day's open** and selling it **five days later**, holding through that recovery window.

Each simulation:
- Reallocates capital dynamically based on signal strength (bigger drop → bigger investment)
- Compounds gains and losses over time
- Benchmarks performance against SPY (the S&P 500 ETF)

---

### 💡 Motivation

These strategies are inspired by real-world observations:
- Stocks often show **mean-reverting behavior** after short-term declines
- Behavioral biases (like panic selling) can create opportunities for reversal
- Simple rules can sometimes outperform complex models — or at least form the foundation for more advanced ones

This project is designed to be:
- **Easy to extend** with new signals
- **Fast to test** different time horizons and asset subsets
- **A springboard** into more sophisticated ideas like stop-loss rules, volatility weighting, or multi-factor models

---

### 🔮 Future directions

Some ideas to expand this project:
- **Filter by sector, volatility, or volume**
- Add **stop-losses** or **profit targets**
- Include **transaction costs**
- Try **momentum-based** or **multi-signal** strategies
- Incorporate **live data** or deploy for paper trading

If you’re curious, quantitative, or just love fiddling with data, this project is meant to be a sandbox for learning, testing, and evolving your own trading ideas.

---

## 🛠️ Getting Started

### 1. 📦 Install [Poetry](https://python-poetry.org/docs/#installation)

If you don't already have Poetry installed, run this:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Make sure it’s available in your terminal:

```bash
poetry --version
```

### 2. 🧬 Clone this repo

```bash
git clone https://github.com/jcranston/investment-strategies.git
cd investment-strategies
```

### 3. 📜 Install dependencies

```bash
poetry install
```

This will create a virtual environment in `.venv/` and install everything you need.


### 4. 🐍 Activate the environment

```bash
poetry shell
```
Now you’re inside the virtual environment. You can run any of the strategy scripts!

## 🚀 Running the Simulations

### 📅 Daily Strategy

This simulates investing in stocks that dropped the previous day, buying at open, and selling at close.

```bash
python src/investment_strategies/main_daily.py
```

You’ll see console output showing:
* Final portfolio value
* Total return
* A plot comparing strategy performance to SPY

💡 This strategy runs from Jan 1 – Dec 31, 2024.

### 🔁 Rolling Weekly Strategy

This simulates investing after a 5-day drop, holding for the next 5 trading days.

```bash
python src/investment_strategies/main_rolling_weekly.py
```

You'll get:
* Final portfolio value
* Return over time
* A plot comparing your strategy to SPY


## 🧪 Project Structure

```
.
├── CONTRIBUTING.md                # Information on contributing to the project
├── LICENSE                        # Software license
├── Makefile                       # Easy commands for executing within the project
├── README.md
├── images/
    ├── daily_strategy_plot.png
    └── rolling_weekly_strategy_plot.png
├── poetry.lock                    # Poetry dependencies file
├── pyproject.toml                 # Poetry config for dependencies
├── pytest.ini                     # Configuration for pytest
├── src/
│   └── investment_strategies/
│       ├── __init__.py
│       └── helpers.py             # Shared logic for downloading, simulating, plotting
│       ├── main_daily.py          # Runs the daily strategy
│       ├── main_rolling_weekly.py # Runs the rolling weekly strategy

├── tests/
    ├── __init__.py
│   └── test_helpers.py            # Tests files
```

## 📊 Example Plots

Run each script to generate these figures. To save them, add this line to the end of each script:

```python
plt.savefig("images/daily_strategy_plot.png")  # or rolling_weekly_strategy_plot.png
```

Create the images folder if needed:

```bash
mkdir -p images
```

## 📌 Requirements

* Python 3.10+
* [Poetry](https://python-poetry.org/)
* Internet connection (for pulling stock data via `yfinance`)

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

## 🙌 Contributions

Pull requests welcome! Please open an issue first to discuss your ideas. See the [future directions](#-future-directions) section for some ideas.

## ✨ Author

Created with love by @jcranston and built with the help of ChatGPT :)
