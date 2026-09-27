import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Choose multiple stocks
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]

# Portfolio weights
weights = np.array([0.25, 0.25, 0.25, 0.25])

# Store annual returns
annual_returns = []

# Store annual volatilities
annual_volatilities = []

# Store daily returns
daily_returns = {}

# Download and analyze each stock
for ticker in tickers:

    data = yf.download(ticker, period="1y")

    # Get closing prices
    prices = data["Close"]

    # Calculate daily returns
    returns = prices.pct_change()
    returns = returns.dropna()

    # Calculate annualized return
    average_daily_return = returns.mean().iloc[0]
    annual_return = average_daily_return * 252

    # Calculate annualized volatility
    daily_volatility = returns.std().iloc[0]
    annual_volatility = daily_volatility * np.sqrt(252)

    # Store results
    annual_returns.append(annual_return)
    annual_volatilities.append(annual_volatility)

    # Store daily returns
    daily_returns[ticker] = returns.iloc[:, 0]


# --------------------------------------------------
# Portfolio Return
# --------------------------------------------------

portfolio_return = 0

for i in range(len(tickers)):
    portfolio_return = portfolio_return + (
        weights[i] * annual_returns[i]
    )


# --------------------------------------------------
# Portfolio Volatility
# --------------------------------------------------

# Create table of daily returns
returns_data = np.column_stack([
    daily_returns[ticker] for ticker in tickers
])

# Calculate covariance matrix
covariance_matrix = np.cov(
    returns_data,
    rowvar=False
)

# Calculate portfolio variance
portfolio_variance = np.dot(
    weights,
    np.dot(covariance_matrix, weights)
)

# Calculate daily portfolio volatility
portfolio_daily_volatility = np.sqrt(
    portfolio_variance
)

# Annualize volatility
portfolio_annual_volatility = (
    portfolio_daily_volatility * np.sqrt(252)
)


# --------------------------------------------------
# Sharpe Ratio
# --------------------------------------------------

risk_free_rate = 0.04

sharpe_ratio = (
    portfolio_return - risk_free_rate
) / portfolio_annual_volatility


# --------------------------------------------------
# Maximum Drawdown
# --------------------------------------------------

# Calculate portfolio daily returns
portfolio_daily_returns = np.dot(
    returns_data,
    weights
)

# Calculate cumulative portfolio value
portfolio_value = (
    1 + portfolio_daily_returns
).cumprod()

# Calculate running maximum
running_max = np.maximum.accumulate(
    portfolio_value
)

# Calculate drawdown
drawdown = (
    portfolio_value - running_max
) / running_max

# Find maximum drawdown
maximum_drawdown = drawdown.min()


# --------------------------------------------------
# Print Results
# --------------------------------------------------

print()
print("----- Individual Stock Analysis -----")

for i in range(len(tickers)):
    print()
    print(tickers[i])
    print("Annualized Return:", round(annual_returns[i] * 100, 2), "%")
    print("Annualized Volatility:", round(annual_volatilities[i] * 100, 2), "%")


print()
print("----- Portfolio Risk Analysis -----")
print("Portfolio Annualized Return:", round(portfolio_return * 100, 2), "%")
print("Portfolio Annualized Volatility:", round(portfolio_annual_volatility * 100, 2), "%")
print("Sharpe Ratio:", round(sharpe_ratio, 2))
print("Maximum Drawdown:", round(maximum_drawdown * 100, 2), "%")
# --------------------------------------------------
# Portfolio Growth Chart
# --------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(portfolio_value)

plt.title("Portfolio Growth Over Time")
plt.xlabel("Trading Days")
plt.ylabel("Portfolio Value ($1 Starting Value)")

plt.grid(True)
plt.show()


# --------------------------------------------------
# Drawdown Chart
# --------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(drawdown)

plt.title("Portfolio Drawdown")
plt.xlabel("Trading Days")
plt.ylabel("Drawdown")

plt.grid(True)
plt.show()


# --------------------------------------------------
# Risk vs. Return Chart
# --------------------------------------------------

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