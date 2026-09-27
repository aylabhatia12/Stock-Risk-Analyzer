# Stock Risk Analyzer

A Python-based quantitative finance tool for analyzing historical stock performance and portfolio risk.

## Overview

This project analyzes a portfolio of stocks using historical market data. It calculates individual stock returns and volatility, then evaluates the overall portfolio using several risk metrics.

The project uses:

* Python
* NumPy
* Pandas
* Matplotlib
* SciPy
* yfinance

## Features

* Downloads historical stock market data
* Calculates daily stock returns
* Calculates annualized returns
* Calculates annualized volatility
* Calculates portfolio return
* Calculates portfolio volatility using a covariance matrix
* Calculates the Sharpe ratio
* Calculates maximum drawdown
* Visualizes portfolio growth
* Visualizes portfolio drawdown
* Visualizes individual stock risk versus return

## Portfolio

The current portfolio contains four stocks with equal 25% weights:

* AAPL
* MSFT
* GOOGL
* AMZN

## Example Results

Using the downloaded one-year historical data:

| Metric                          |  Result |
| ------------------------------- | ------: |
| Portfolio Annualized Return     |  24.26% |
| Portfolio Annualized Volatility |  20.69% |
| Sharpe Ratio                    |    0.98 |
| Maximum Drawdown                | -16.71% |

Individual stock results:

| Stock | Annualized Return | Annualized Volatility |
| ----- | ----------------: | --------------------: |
| AAPL  |            32.53% |                24.52% |
| MSFT  |             7.03% |                32.80% |
| GOOGL |            38.83% |                31.77% |
| AMZN  |            18.65% |                34.46% |

## Visualizations

The program generates three visualizations:

1. **Portfolio Growth Over Time** — shows the cumulative value of the portfolio starting from $1.
2. **Portfolio Drawdown** — shows declines from previous portfolio peaks.
3. **Risk vs. Return** — compares annualized volatility and annualized return for each stock.

## How to Run

Clone the repository and navigate into the project:

```bash
cd Stock-Risk-Analyzer
```

Create and activate a virtual environment:

```bash
py -3.11 -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

Run the program:

```powershell
python src/main.py
```

## Project Structure

```text
Stock-Risk-Analyzer/
├── src/
│   └── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Financial Metrics

### Annualized Return

The average daily return is multiplied by 252, representing the approximate number of trading days in a year.

### Annualized Volatility

Daily volatility is multiplied by the square root of 252 to estimate annualized volatility.

### Portfolio Volatility

Portfolio volatility is calculated using the covariance matrix of the individual stocks:

```text
Portfolio Variance = wᵀΣw
```

where `w` represents the portfolio weights and `Σ` represents the covariance matrix.

### Sharpe Ratio

The Sharpe ratio measures historical return relative to portfolio volatility using an assumed 4% risk-free rate:

```text
Sharpe Ratio = (Portfolio Return - Risk-Free Rate) / Portfolio Volatility
```

### Maximum Drawdown

Maximum drawdown measures the largest historical decline from a previous portfolio peak.

## Disclaimer

This project is for educational and analytical purposes. The results are based on historical market data and should not be interpreted as financial advice or predictions of future performance.
