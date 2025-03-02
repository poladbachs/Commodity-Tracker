import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from data_fetcher import fetch_commodity_price
from data_process import compute_effective_prices

def main():
    st.title("Commodity Logistics & Price Tracker")
    
    st.sidebar.header("Commodity Selection")
    commodities = {
        "Crude Oil [Energy]": "CL=F",
        "Gold [Metals]": "GC=F",
        "Copper [Metals]": "HG=F",
        "Silver [Metals]": "SI=F"
    }
    selected = st.sidebar.multiselect(
        "Select Commodities", 
        list(commodities.keys()), 
        default=["Crude Oil [Energy]"]
    )
    
    period = st.sidebar.selectbox("Data Period", options=["1mo", "3mo", "6mo", "1y"], index=0)
    interval = st.sidebar.selectbox("Data Interval", options=["1d", "1wk", "1mo"], index=0)
    
    routes = ["Route A", "Route B", "Route C", "Route D"]
    
    for commodity in selected:
        ticker = commodities[commodity]
        st.header(f"Commodity Price Data for {commodity}")
        
        price_data = fetch_commodity_price(ticker=ticker, period=period, interval=interval)
        if price_data.empty:
            st.write("No data fetched for ticker:", ticker)
            continue
        
        st.write(price_data)
        
        price_data = price_data.reset_index()  
        
        price_data['Date'] = pd.to_datetime(price_data['Date'])
        
        fig, ax = plt.subplots()
        ax.plot(price_data['Date'], price_data['Close'], label="Close Price")
        
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        
        plt.xticks(rotation=45)
        
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.set_title(f"Historical Price for {commodity}")
        ax.legend()
        st.pyplot(fig)
        
        st.subheader(f"Effective Price Analysis for {commodity}")
        effective_data = compute_effective_prices(price_data, routes)
        effective_df = pd.DataFrame(effective_data)
        
        numeric_cols = ["FreightCost", "CommodityPrice", "EffectivePrice"]
        for col in numeric_cols:
            effective_df[col] = effective_df[col].astype(float).round(2)
        
        st.write(effective_df)
        
        try:
            best_route = effective_df.loc[effective_df['EffectivePrice'].idxmin()]
            st.subheader("Best Route")
            st.write(best_route)
        except Exception as e:
            st.error(f"Error computing effective prices: {e}")

if __name__ == "__main__":
    main()
