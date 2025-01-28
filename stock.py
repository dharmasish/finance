import streamlit as st
import yfinance as yf

# Function to fetch stock data
def get_stock_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    stock_info = stock.info
    current_price = stock_info.get('currentPrice', 'N/A')
    market_cap_usd = stock_info.get('marketCap', 'N/A')
    return current_price, market_cap_usd

# Function to convert USD to INR and round to integer
def usd_to_inr_crore(usd_value):
    if usd_value == 'N/A':
        return 'N/A'
    # Fetch current USD to INR exchange rate
    exchange_rate_data = yf.Ticker("USDINR=X")
    exchange_rate = exchange_rate_data.history(period="1d")['Close'].iloc[-1]
    # Convert market cap to crore INR and round to integer
    market_cap_inr_crore = round((usd_value * exchange_rate) / 10000000)
    return market_cap_inr_crore

# Streamlit app
st.title("Indian Stock Market Dashboard")
st.write("Enter the stock symbols (append `.NS` for NSE) to get the current price and market cap in crore INR.")

# Input for stock symbols
stocks_input = st.text_input("Enter stock symbols (comma-separated):", "RELIANCE.NS, TCS.NS, HDFCBANK.NS, INFY.NS")
stocks = [stock.strip() for stock in stocks_input.split(",")]

# Fetch and display data
if st.button("Get Data"):
    st.write("Fetching data...")
    for stock in stocks:
        current_price, market_cap_usd = get_stock_data(stock)
        if current_price != 'N/A' and market_cap_usd != 'N/A':
            # Convert market cap to crore INR and round to integer
            market_cap_inr_crore = usd_to_inr_crore(market_cap_usd)
            st.write(f"**Stock:** {stock}")
            st.write(f"**Current Price (INR):** ₹{current_price:.2f}")
            st.write(f"**Market Cap (Crore INR):** ₹{market_cap_inr_crore:,} Cr")
            st.write("---")
        else:
            st.write(f"**Stock:** {stock} - Data not available.")