import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

st.title("Stock Comparison - Normalized Adjusted Close")

# Input for two ticker symbols
col1, col2 = st.columns(2)
with col1:
    ticker1 = st.text_input("Enter first ticker symbol:", key="ticker1")
with col2:
    ticker2 = st.text_input("Enter second ticker symbol:", key="ticker2")

# Period for last 5 years monthly data
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)

if ticker1 and ticker2:
    # Validate and fetch data for ticker 1
    try:
        stock1 = yf.Ticker(ticker1)
        data1 = stock1.history(start=start_date, end=end_date, interval="1mo")
        if data1.empty:
            st.error(f"No data found for {ticker1}. Please check the ticker symbol.")
        else:
            st.success(f"✓ Valid ticker: {ticker1}")
    except:
        st.error(f"Invalid ticker symbol: {ticker1}")
        data1 = None
    
    # Validate and fetch data for ticker 2
    try:
        stock2 = yf.Ticker(ticker2)
        data2 = stock2.history(start=start_date, end=end_date, interval="1mo")
        if data2.empty:
            st.error(f"No data found for {ticker2}. Please check the ticker symbol.")
        else:
            st.success(f"✓ Valid ticker: {ticker2}")
        data2 = stock2.history(start=start_date, end=end_date, interval="1mo")
    except:
        st.error(f"Invalid ticker symbol: {ticker2}")
        data2 = None
    
    # Plot if both tickers have valid data
    if data1 is not None and not data1.empty and data2 is not None and not data2.empty:
        # Normalize adjusted close prices (divide by first value)
        norm_data1 = data1['Close'] / data1['Close'].iloc[0] * 100
        norm_data2 = data2['Close'] / data2['Close'].iloc[0] * 100
        
        # Align dates by reindexing to common dates
        common_index = norm_data1.index.union(norm_data2.index)
        norm_data1 = norm_data1.reindex(common_index).fillna(method='ffill')
        norm_data2 = norm_data2.reindex(common_index).fillna(method='ffill')
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(norm_data1.index, norm_data1.values, linewidth=2, label=f"{ticker1} (Normalized)")
        ax.plot(norm_data2.index, norm_data2.values, linewidth=2, label=f"{ticker2} (Normalized)")
        
        ax.set_title(f"5-Year Performance Comparison: {ticker1} vs {ticker2}", fontsize=16, fontweight='bold')
        ax.set_ylabel("Normalized Adjusted Close (Starting at 100)", fontsize=12)
        ax.set_xlabel("Date", fontsize=12)
        ax.legend(fontsize=12)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig)
        
        # Performance stats
        st.subheader("Performance Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Return", f"{norm_data1.iloc[-1]:.1f}%", f"{norm_data1.iloc[-1]:.1f}%")
        with col2:
            st.metric("Total Return", f"{norm_data2.iloc[-1]:.1f}%", f"{norm_data2.iloc[-1]:.1f}%")
        with col3:
            pct_change1 = ((norm_data1.iloc[-1] - 100) / 100) * 100
            st.metric("Final Value", f"{norm_data1.iloc[-1]:.1f}", f"{pct_change1:.1f}%")
        with col4:
            pct_change2 = ((norm_data2.iloc[-1] - 100) / 100) * 100
            st.metric("Final Value", f"{norm_data2.iloc[-1]:.1f}", f"{pct_change2:.1f}%")
    else:
        st.warning("Please enter valid ticker symbols for both inputs to see the comparison chart.")
else:
    st.info("👆 Enter two valid ticker symbols (e.g., AAPL, MSFT, TSLA) to compare their performance.")
