from dotenv import load_dotenv
import os
import requests

load_dotenv()

def get_news_headlines(commodity):
    API_KEY = os.getenv("NEWS_API_KEY")
    if not API_KEY:
        return ["Error: API key not found. Set the NEWS_API_KEY environment variable."]
    
    commodity_name = commodity.split('[')[0].strip()
    url = f"https://newsapi.org/v2/everything?q={commodity_name}&sortBy=publishedAt&pageSize=5&apiKey={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        results = []
        for art in articles:
            title = art.get("title", "No Title")
            url_link = art.get("url", "#")
            source = art.get("source", {}).get("name", "Unknown Source")
            snippet = art.get("description", "")
            results.append({
                "title": title,
                "url": url_link,
                "source": source,
                "snippet": snippet
            })
        return results
    except Exception as e:
        return [{"title": f"Error fetching news: {e}", "url": "#", "source": "Error", "snippet": ""}]

if __name__ == "__main__":
    headlines = get_news_headlines("Crude Oil [Energy]")
    for h in headlines:
        print(h)