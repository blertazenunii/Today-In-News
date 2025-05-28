import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load API key
load_dotenv()
newsapi_key = os.getenv("NEWSAPI_KEY")

# Dates
today_date = datetime.today().strftime('%Y-%m-%d')
one_week_ago = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')

def fetch_newsapi_articles(category, total_pages=1):
    
    print(f"Fetching NewsAPI articles for: {category}")


    #Definition of the Http Request
    url = "https://newsapi.org/v2/everything"
    params = {
        "language": "en",
        "pageSize": 100,
        "apiKey": newsapi_key,
        "from": one_week_ago,
        "to": today_date,
        "page": 1,
        "q": category
    }

    
    #Array where the returned articles will be stored
    all_articles = []

    response = requests.get(url, params)
    response.raise_for_status()

    data = response.json()
    articles = data.get("articles", [])

    for article in articles:
        all_articles.append({
            "category": category,
            "title": article.get("title"),
            "description": article.get("description"),
            "publishedAt": article.get("publishedAt"),
            "url": article.get("url")
        })
        if len(articles) < 100:
            break


    return all_articles
