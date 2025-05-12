import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load API key
load_dotenv()
guardian_key = os.getenv("GUARDIAN_KEY")

# Dates
today_date = datetime.today().strftime('%Y-%m-%d')
one_week_ago = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

# Categories
categories = ["business", "sport", "technology", "culture", "lifeandstyle"]

def fetch_guardian_articles(category):
    print(f"\nFetching Guardian articles for: {category}")

    url = "https://content.guardianapis.com/search"
    page = 1
    params = {
        "api-key": guardian_key,
        "section": category,
        "from-date": one_week_ago,
        "to-date": today_date,
        "page": page,
        "page-size": 50,  # Adjust the page size if necessary
        "show-fields": "trailText",
        "order-by": "newest"
    }

    all_articles = []


    response = requests.get(url, params=params)

    # Check if request is successful
    if response.status_code == 400:
        print(f"Bad request for category '{category}'. Response: {response.text}")
        return []

    # Raise for other status errors (e.g., 500, 503, etc.)
    response.raise_for_status()

    data = response.json()
    results = data.get("response", {}).get("results", [])
    
    if not results:
        print(f"No results for '{category}' on page {page}.")
    else:
        for article in results:
            all_articles.append({
                "category": category,
                "title": article.get("webTitle"),
                "description": article.get("fields", {}).get("trailText", ""),
                "publishedAt": article.get("webPublicationDate"),
                "url": article.get("webUrl")
            })

    return all_articles

