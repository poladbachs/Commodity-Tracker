import yfinance as yf

def fetch_commodity_price(ticker="CL=F", period="1mo", interval="1d"):
    """
    Fetch historical commodity price data from Yahoo Finance.
    
    Args:
        ticker (str): Commodity ticker (default: "CL=F" for WTI Crude Oil).
        period (str): Data period (default: "1mo").
        interval (str): Data interval (default: "1d").
        
    Returns:
        pd.DataFrame: Historical data DataFrame.
    """
    data = yf.download(ticker, period=period, interval=interval)
    return data

if __name__ == "__main__":
    data = fetch_commodity_price()
    print(data.head())