![Image](https://github.com/user-attachments/assets/9958fdd9-5e52-4d2d-9b93-bed472eb5c40)
# Commodity Logistics & Price Tracker

## Overview
Commodity Logistics & Price Tracker is a high-performance demo tool for commodity trading firms. It provides real-time analysis of commodity prices, simulated freight costs, route logistics, effective price computation, and live news integration—all in one interactive dashboard.

---

## 📺 Demo
![Image](https://github.com/user-attachments/assets/5134d9da-ef52-4699-944d-8e3cb331a68d)

---

## 📌 How It Works
- **Real-Time Price Data:** Retrieves historical prices for energy and metals using Yahoo Finance.
- **Simulated Freight Cost:** Generates realistic freight cost data with an adjustable factor.
- **Effective Price Analysis:** Combines commodity prices with freight costs to determine optimal shipping routes.
- **Price Forecasting:** Predicts future prices (next 7 days) using Facebook Prophet model.
- **Commodity News Integration:** Fetches and displays relevant news headlines with sources and snippets via NewsAPI.org.
- **Dashboard Visualization:** Displays all data and insights in a modern, interactive Streamlit UI.

## 🛠️ Tech Stack
| Technology      | Purpose                                |
|-----------------|----------------------------------------|
| **Python**      | Core programming language              |
| **Streamlit**   | Interactive dashboard/UI               |
| **Pandas**      | Data manipulation                      |
| **yfinance**    | Commodity price data retrieval         |
| **Facebook Prophet**     | Time series forecasting       |
| **Plotly**      | Interactive forecasting charts         |
| **Matplotlib**  | Historical price charting              |
| **NewsAPI**     | Live news headlines integration        |
| **NumPy**       | Numeric operations                     |

## 🔧 Setup & Installation

```bash
# Clone the repository
git clone https://github.com/YourUsername/commodities_tracker.git
cd commodities_tracker

# Install dependencies
pip install -r requirements.txt

# News API Key
In news_api.py, replace "YOUR_NEWS_API_KEY" with your actual NewsAPI.org API key.

# Commodity Tickers
Customize commodity tickers in dashboard.py if needed.

```
## Running the Project
```bash
# Launch the Streamlit dashboard
streamlit run dashboard.py
```
