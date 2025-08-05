import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import base64
import os
from alpha_vantage.timeseries import TimeSeries
from sklearn.linear_model import LinearRegression
import numpy as np

# Alpha Vantage API key for fetching live stock data
ALPHA_VANTAGE_API_KEY = "ed042842db8b4f528fb3fc9d991f313f"


# Load stock data either from Alpha Vantage or fallback to local CSV if API fails
def load_data(ticker):
    try:
        ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
        df, meta_data = ts.get_daily(symbol=ticker, outputsize='compact')
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        source = "alpha_vantage"  # Indicates data was successfully loaded from the API
    except Exception as e:
        # If API fails, use pre-saved mock data from the local 'mock_data' folder
        st.warning("⚠️ Could not load data from Alpha Vantage. Switching to fallback CSV data.")
        try:
            df = pd.read_csv(f"mock_data/{ticker}.csv", index_col=0, parse_dates=True)
            source = "csv"
        except:
            # If CSV is also missing, return error
            st.error("❌ No local CSV data available either. Please try a different stock ticker symbol.")
            return None, None
    return df, source


# Plot a candlestick chart with 20-day Moving Average using Plotly
def plot_candlestick_chart(df, ticker):
    df["20MA"] = df["Close"].rolling(window=20).mean()

    fig = go.Figure()

    # Add candlestick chart for stock data
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color='green',
        decreasing_line_color='red',
        name='Candlestick'
    ))

    # Add 20-day moving average line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["20MA"],
        line=dict(color='cyan', width=2),
        name="20-Day MA"
    ))

    # Customize layout and appearance
    fig.update_layout(
        title=f"{ticker} Candlestick Chart (Daily)",
        yaxis_title='Stock Price (USD)',
        xaxis_title='Date',
        template='plotly_dark',
        width=1400,
        height=750,
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(color="white")
    )
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)


# Analyze stock trend using Moving Averages (20-day and 50-day)
def analyze_trend(df):
    if df is None:
        return "No data to analyze."
    
    df["20MA"] = df["Close"].rolling(window=20).mean()
    df["50MA"] = df["Close"].rolling(window=50).mean()

    last_close = df["Close"].iloc[-1]
    ma_20 = df["20MA"].iloc[-1]
    ma_50 = df["50MA"].iloc[-1]

    recent_trend = df["20MA"].iloc[-5:].mean() - df["20MA"].iloc[-10:-5].mean()

    # Simple logic to detect upward/downward trend
    if last_close > ma_20 and ma_20 > ma_50 and recent_trend > 0:
        return "✅ Strong upward momentum detected (Price > 20MA > 50MA with upward slope). This may be a good opportunity to invest."
    elif last_close < ma_20 and ma_20 < ma_50 and recent_trend < 0:
        return "❌ The stock shows a downward trend with weakening momentum. It may be best to wait before investing."
    else:
        return "ℹ️ The stock trend is unclear or sideways. Monitoring is recommended before making investment decisions."


# Predict future stock prices using linear regression for the next few days
def predict_future_prices(df, days_ahead=5):
    df = df.copy()
    df["Days"] = np.arange(len(df))  # Add a numerical feature for regression
    X = df[["Days"]]
    y = df["Close"]

    model = LinearRegression()
    model.fit(X, y)

    # Predict prices for future days
    last_day = df["Days"].iloc[-1]
    future_days = np.arange(last_day + 1, last_day + 1 + days_ahead).reshape(-1, 1)
    predicted_prices = model.predict(future_days)

    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=days_ahead)
    prediction_df = pd.DataFrame({
        "Date": future_dates,
        "Predicted Close": predicted_prices
    })

    return prediction_df


# Set animated background for the app using a GIF file
def display_background():
    gif_path = os.path.join(os.path.dirname(__file__), "static", "stock_bg.gif")
    if os.path.exists(gif_path):
        with open(gif_path, "rb") as f:
            gif_base64 = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(f"""
            <style>
                .stApp {{
                    background-image: url("data:image/gif;base64,{gif_base64}");
                    background-size: cover;
                    background-position: center;
                }}
                .css-1dp5vir {{
                    background-color: rgba(0, 0, 0, 0.8) !important;
                }}
                .chart-container {{
                    background-color: rgba(0, 0, 0, 0.9);
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                }}
            </style>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Background GIF not found. Running app without animated background.")



# ========== Streamlit App UI Starts Here ==========
display_background()
st.title("📈 Smart Stock Insight Dashboard")
st.markdown("""
Welcome! Enter a stock ticker (e.g., `AAPL`, `GOOGL`, `TSLA`, `JPM`) to get live data and trend insights. 
If live data isn't available, fallback data will be used.
""")

# User input for stock symbol
ticker = st.text_input("Enter stock ticker symbol:", value="").upper()
if ticker:
    df, data_source = load_data(ticker)
    if df is not None:
        st.subheader(f"📊 Candlestick Chart for {ticker} ({'Live' if data_source == 'alpha_vantage' else 'Cached'})")
        plot_candlestick_chart(df, ticker)

        st.markdown("### 📌 Investment Recommendation")
        recommendation = analyze_trend(df)
        st.success(recommendation)

        st.markdown("### 🕰️ Historical Data Table (Last 30 Days)")
        st.dataframe(df.tail(30))

        st.markdown("### 🔮 Future Price Prediction (Linear Regression)")
        prediction_df = predict_future_prices(df)
        st.dataframe(prediction_df)

        st.line_chart(prediction_df.set_index("Date"))

        st.info("🔁 Want to analyze another stock? Enter a new symbol above.")
    else:
        st.warning("❗ Try another stock. No valid data found for the symbol provided.")
