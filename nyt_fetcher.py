import os
import requests
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load API key
load_dotenv()
nyt_api_key = os.getenv("NYTIMES_KEY")

# Dates
today_date = datetime.today().strftime('%Y-%m-%d')
one_week_ago = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

def fetch_nyt_articles(query, total_pages=1, delay_seconds=2):

    print(f"Fetching NYT articles for: {query}")

    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        "api-key": nyt_api_key,
        "q": query,
        "begin_date": one_week_ago.replace("-", ""),
        "end_date": today_date.replace("-", ""),
        "page": 0,
    }

    all_articles = []

    for page in range(total_pages):
        params["page"] = page
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("response", {}).get("docs")

        if not isinstance(articles, list):
            print(f"Warning: Unexpected articles format (page {page}):", articles)
            continue
        
        for article in articles:
            all_articles.append({
                "category": query,
                "title": article.get("headline", {}).get("main"),
                "description": article.get("abstract"),
                "publishedAt": article.get("pub_date"),
                "url": article.get("web_url")
            })
        
        if len(articles) < 10:
            break

        

    return all_articles
