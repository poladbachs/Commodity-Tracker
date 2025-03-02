import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go
from prophet import Prophet

from data_fetcher import fetch_commodity_price
from data_process import compute_effective_prices
from news_api import get_news_headlines

def forecast_prices(price_data, days=7):
    df = price_data[['Date', 'Close']].copy()
    df.columns = ['ds', 'y']
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=days)
    return model.predict(future)

def main():
    st.set_page_config(
        layout="wide",
        page_title="Commodity Logistics & Price Tracker",
        page_icon=":chart_with_upwards_trend:"
    )
    st.markdown("""
    <style>
    body {
        background-color: #1e1e1e;
        color: #eee;
        font-family: "Segoe UI", sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #2c2c2c;
    }
    .main-title {
        font-size: 2rem; 
        font-weight: 600;
        margin-top: 0;
    }
    .commodity-box {
        background-color: #2c2c2c;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .news-panel {
        background-color: #2c2c2c; 
        border-radius: 8px; 
        padding: 15px; 
        margin-bottom: 20px;
    }
    .news-panel h3 {
        text-align: center; 
        margin-bottom: 10px; 
        color: #fff;
    }
    .news-item {
        background-color: #3a3a3a; 
        border-radius: 6px; 
        margin: 8px 0; 
        padding: 10px;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    .news-item a {
        color: #00c0ff;
        text-decoration: none;
        font-weight: 500;
    }
    .news-item a:hover {
        text-decoration: underline;
    }
    .news-source {
        font-size: 0.8rem;
        color: #ccc;
    }
    .block-container .dataframe table {
        color: #fff !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-title'>Commodity Logistics & Price Tracker</h1>", unsafe_allow_html=True)

    # Dictionary of commodities and corresponding tickers
    commodities = {
        "Crude Oil": "CL=F",   # WTI Crude Oil
        "Gold": "GC=F",       # Gold Futures
        "Copper": "HG=F",     # Copper Futures
        "Silver": "SI=F",     # Silver Futures
        "Steel": "SLX"
    }

    news_search_terms = {
        "Crude Oil": "Crude Oil OPEC",
        "Gold": "Gold precious metals",
        "Copper": "Copper base metals",
        "Silver": "Silver precious metals",
        "Steel": "Steel manufacturing"
    }

    st.sidebar.title("Settings")
    commodity = st.sidebar.selectbox("Select Commodity", list(commodities.keys()), index=0)
    period = st.sidebar.selectbox("Data Period", ["1mo", "3mo", "6mo", "1y"], index=0)
    interval = st.sidebar.selectbox("Data Interval", ["1d", "1wk", "1mo"], index=0)
    freight_factor = st.sidebar.slider("Freight Cost Adjustment", 0.5, 1.5, 1.0, 0.1)

    col_left, col_right = st.columns([3, 1], gap="large")

    with col_left:
        ticker = commodities[commodity]
        st.markdown(f"<h2 style='margin-top:20px;'>{commodity}</h2>", unsafe_allow_html=True)

        price_data = fetch_commodity_price(ticker, period, interval)
        if price_data.empty:
            st.write(f"No data fetched for {commodity}.")
            return

        price_data = price_data.reset_index()
        price_data['Date'] = pd.to_datetime(price_data['Date'])
        price_data['Date_str'] = price_data['Date'].dt.strftime('%Y-%m-%d')

        st.markdown("<div class='commodity-box'>", unsafe_allow_html=True)
        st.markdown("**Recent Price Data**", unsafe_allow_html=True)
        st.dataframe(price_data[['Date_str', 'Close']].tail(), use_container_width=True)

        fig, ax = plt.subplots()
        ax.plot(price_data['Date'], price_data['Close'], label="Close Price", color='#00c0ff')
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        ax.set_xlabel("Date", color='#eee')
        ax.set_ylabel("Price", color='#eee')
        ax.set_title(f"{commodity} Historical Price", color='#fff')
        ax.legend()
        ax.tick_params(colors='#eee')
        fig.patch.set_facecolor('#2c2c2c')
        ax.set_facecolor("#2c2c2c")
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='commodity-box'>", unsafe_allow_html=True)
        st.markdown("**Price Forecast (Next 7 Days)**", unsafe_allow_html=True)
        forecast = forecast_prices(price_data, days=7)
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(
            x=forecast['ds'], y=forecast['yhat'],
            mode='lines', name='Forecast', line=dict(color='#00c0ff')
        ))
        fig_forecast.add_trace(go.Scatter(
            x=forecast['ds'], y=forecast['yhat_upper'],
            mode='lines', name='Upper Conf', line=dict(dash='dash', color='#cccccc')
        ))
        fig_forecast.add_trace(go.Scatter(
            x=forecast['ds'], y=forecast['yhat_lower'],
            mode='lines', name='Lower Conf', line=dict(dash='dash', color='#cccccc')
        ))
        fig_forecast.update_layout(
            title=f"{commodity} Price Forecast",
            xaxis_title="Date",
            yaxis_title="Price",
            plot_bgcolor='#2c2c2c',
            paper_bgcolor='#2c2c2c',
            font=dict(color='#eee')
        )
        st.plotly_chart(fig_forecast, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='commodity-box'>", unsafe_allow_html=True)
        st.markdown("**Effective Price Analysis**", unsafe_allow_html=True)
        routes = ["Route A", "Route B", "Route C", "Route D"]
        effective_data = compute_effective_prices(price_data, routes)
        for entry in effective_data:
            entry["FreightCost"] = round(entry["FreightCost"] * freight_factor, 2)
            entry["EffectivePrice"] = round(entry["CommodityPrice"] + entry["FreightCost"], 2)
        df_effective = pd.DataFrame(effective_data)
        for col in ["FreightCost", "CommodityPrice", "EffectivePrice"]:
            df_effective[col] = df_effective[col].astype(float).round(2)
        st.dataframe(df_effective[['Route', 'FreightCost', 'CommodityPrice', 'EffectivePrice', 'Currency']], use_container_width=True)
        try:
            best_route = df_effective.loc[df_effective['EffectivePrice'].idxmin()]
            st.markdown(f"**Best Route:** {best_route['Route']} at {best_route['EffectivePrice']} {best_route['Currency']}")
        except:
            st.write("Unable to determine best route.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='news-panel'>", unsafe_allow_html=True)
        st.markdown("<h3>Latest News</h3>", unsafe_allow_html=True)
        query = news_search_terms.get(commodity, commodity)
        articles = get_news_headlines(query)
        if articles:
            for art in articles:
                title = art.get("title", "No Title")
                url = art.get("url", "#")
                source = art.get("source", "Unknown Source")
                snippet = art.get("snippet", "")
                st.markdown(
                    f"<div class='news-item'><a href='{url}' target='_blank'>{title}</a><br><span class='news-source'>{source}</span><br><span style='font-size:0.8rem;'>{snippet}</span></div>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown("<div class='news-item'>No news available.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
