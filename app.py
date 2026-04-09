import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Siva Indian Stock Live", layout="wide")
st.title("📈 Siva's Real-Time Market Dashboard")

# Fetch Data
def get_data():
    nifty = yf.Ticker("^NSEI").history(period="1d", interval="5m")
    crude = yf.Ticker("CL=F").history(period="1d")['Close'].iloc[-1]
    usd_inr = yf.Ticker("INR=X").history(period="1d")['Close'].iloc[-1]
    return nifty, crude, usd_inr

try:
    nifty_df, crude_p, usd_p = get_data()
    last_price = nifty_df['Close'].iloc[-1]

    st.sidebar.header("Global Indicators")
    st.sidebar.metric("Crude Oil", f"${crude_p:.2f}")
    st.sidebar.metric("USD / INR", f"₹{usd_p:.2f}")

    st.subheader("Market Signal")
    score = 0
    if crude_p < 85: score += 50
    if usd_p < 84: score += 50

    if score >= 100:
        st.success("🎯 SIGNAL: CALL ENTRY (Bullish)")
    elif score == 50:
        st.warning("⚠️ SIGNAL: NEUTRAL (Wait)")
    else:
        st.error("🎯 SIGNAL: PUT ENTRY (Bearish)")

    st.line_chart(nifty_df['Close'])
    st.write(f"Current Nifty Price: **{last_price:.2f}**")

except Exception as e:
    st.error("Data is loading or Market is Closed...")
