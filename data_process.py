from freight_api import fetch_freight_cost

def compute_effective_prices(price_data, routes):
    """
    Compute effective commodity prices by adding the simulated freight cost
    to the latest commodity closing price for each route.
    
    Args:
        price_data (pd.DataFrame): Time series data with a 'Close' column.
        routes (list): List of route names (str).
        
    Returns:
        list of dicts: Each dictionary contains route, freight_cost, commodity_price, effective_price, and currency.
    """
    if price_data.empty or 'Close' not in price_data.columns:
        raise ValueError("Invalid price data; must include a 'Close' column.")
        
    latest_price = price_data['Close'].iloc[-1]
    results = []
    for route in routes:
        freight_info = fetch_freight_cost(route)
        freight_cost = freight_info.get("freight_cost", 0)
        effective_price = latest_price + freight_cost
        results.append({
            "Route": route,
            "FreightCost": freight_cost,
            "CommodityPrice": latest_price,
            "EffectivePrice": effective_price,
            "Currency": freight_info.get("currency", "USD")
        })
    return results

if __name__ == "__main__":
    import yfinance as yf
    price_data = yf.download("CL=F", period="1mo", interval="1d")
    routes = ["Route A", "Route B", "Route C", "Route D"]
    effective_data = compute_effective_prices(price_data, routes)
    for data in effective_data:
        print(data)