# Smart Stock Insight System - Linear Regression

A lightweight, interactive dashboard for stock price prediction and investment insight generation using a combination of historical data, moving averages, and linear regression. Built with Python and Streamlit, this system is designed to assist users in analyzing stock trends, especially in the absence of live data by falling back on mock datasets.

---

## Objective

The stock market is inherently volatile and influenced by a range of unpredictable factors. This project aims to provide short-term stock price forecasting and trend analysis using simple, interpretable techniques like:

- 20-day and 50-day moving averages (MA20, MA50)
- Linear regression for next-day price prediction
- Candlestick visualization for past trends
- Automated insights based on crossover strategies

---

## Repository Structure

| Folder / File         | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `code/`               | Contains `test.py`, the main Streamlit application script                   |
| `mock_data/`          | Fallback CSV datasets for various stock tickers (e.g., AAPL, TSLA, AMZN)    |
| `screenshots/`        | UI output screenshots of the dashboard and predictions                      |
| `report/`             | Final project report PDF (if included)                                      |
| `README.md`           | This file – complete project documentation                                  |

---

## Future Scope

- Integrate advanced models like LSTM, CNN, or XGBoost for better accuracy
- Add real-time notifications for stock price spikes/dips
- Personalize recommendations based on user-defined watchlists
- Host the platform online for multi-user access
- Add explanations for predictions using XAI techniques

---

## How to Run the App

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/smart-stock-insight-system.git
cd smart-stock-insight-system
