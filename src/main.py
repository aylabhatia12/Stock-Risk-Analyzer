import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt


# Portfolio setup
tickers_input = input("Enter stock tickers separated by commas: ")

tickers = [
    ticker.strip().upper()
    for ticker in tickers_input.split(",")
]

weights_input = input("Enter portfolio weights separated by commas: ")

weights = np.array([
    float(weight.strip()) / 100
    for weight in weights_input.split(",")
])


# Check that tickers and weights match
if len(tickers) != len(weights):
    raise ValueError("The number of tickers must match the number of weights.")

# Check that weights add to 100%
if not np.isclose(weights.sum(), 1.0):
    raise ValueError("Portfolio weights must add up to 100%.")


# Store results
annual_returns = []
annual_volatilities = []
daily_returns = {}


# Download and analyze each stock
for ticker in tickers:

    data = yf.download(
        ticker,
        period="1y",
        auto_adjust=True
    )

    prices = data["Close"]

    # Handle yfinance data format
    if len(prices.shape) > 1:
        prices = prices.iloc[:, 0]

    # Calculate daily returns
    returns = prices.pct_change()
    returns = returns.dropna()

    # Annualized return
    average_daily_return = returns.mean()
    annual_return = average_daily_return * 252

    # Annualized volatility
    daily_volatility = returns.std()
    annual_volatility = daily_volatility * np.sqrt(252)

    # Store results
    annual_returns.append(annual_return)
    annual_volatilities.append(annual_volatility)
    daily_returns[ticker] = returns


# Portfolio return
portfolio_return = 0

for i in range(len(tickers)):

    portfolio_return = portfolio_return + (
        weights[i] * annual_returns[i]
    )


# Portfolio volatility
returns_data = np.column_stack([
    daily_returns[ticker]
    for ticker in tickers
])

covariance_matrix = np.cov(
    returns_data,
    rowvar=False
)

portfolio_variance = np.dot(
    weights,
    np.dot(
        covariance_matrix,
        weights
    )
)

portfolio_daily_volatility = np.sqrt(
    portfolio_variance
)

portfolio_annual_volatility = (
    portfolio_daily_volatility * np.sqrt(252)
)


# Sharpe ratio
risk_free_rate = 0.04

sharpe_ratio = (
    portfolio_return - risk_free_rate
) / portfolio_annual_volatility


# Maximum drawdown
portfolio_daily_returns = np.dot(
    returns_data,
    weights
)

portfolio_value = (
    1 + portfolio_daily_returns
).cumprod()

running_max = np.maximum.accumulate(
    portfolio_value
)

drawdown = (
    portfolio_value - running_max
) / running_max

maximum_drawdown = drawdown.min()


# Print individual stock results
print()
print("----- Individual Stock Analysis -----")

for i in range(len(tickers)):

    print()
    print(tickers[i])
    print("Portfolio Weight:", round(weights[i] * 100, 2), "%")
    print("Annualized Return:", round(annual_returns[i] * 100, 2), "%")
    print("Annualized Volatility:", round(annual_volatilities[i] * 100, 2), "%")


# Print portfolio results
print()
print("----- Portfolio Risk Analysis -----")

print(
    "Portfolio Annualized Return:",
    round(portfolio_return * 100, 2),
    "%"
)

print(
    "Portfolio Annualized Volatility:",
    round(portfolio_annual_volatility * 100, 2),
    "%"
)

print(
    "Sharpe Ratio:",
    round(sharpe_ratio, 2)
)

print(
    "Maximum Drawdown:",
    round(maximum_drawdown * 100, 2),
    "%"
)


# Portfolio growth chart
plt.figure(figsize=(10, 6))

plt.plot(portfolio_value)

plt.title("Portfolio Growth Over Time")
plt.xlabel("Trading Days")
plt.ylabel("Portfolio Value ($1 Starting Value)")

plt.grid(True)
plt.show()


# Drawdown chart
plt.figure(figsize=(10, 6))

plt.plot(drawdown)

plt.title("Portfolio Drawdown")
plt.xlabel("Trading Days")
plt.ylabel("Drawdown")

plt.grid(True)
plt.show()


# Risk vs. return chart
plt.figure(figsize=(10, 6))

plt.scatter(
    annual_volatilities,
    annual_returns
)

for i in range(len(tickers)):

    plt.annotate(
        tickers[i],
        (
            annual_volatilities[i],
            annual_returns[i]
        )
    )

plt.title("Risk vs. Return")
plt.xlabel("Annualized Volatility")
plt.ylabel("Annualized Return")

plt.grid(True)
plt.show()