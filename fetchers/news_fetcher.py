import csv
import os
from collections import defaultdict
from newsapi_fetcher import fetch_newsapi_articles
from nyt_fetcher import fetch_nyt_articles
from guardian_fetcher import fetch_guardian_articles

def fetch_news():
    # Categories for NewsAPI, Guardian and NYT 
    newsapi_categories = ["business", "sports", "technology", "entertainment", "health"]
    guardian_categories = ["business", "sport", "technology", "culture", "lifeandstyle"]
    nytapi_categories = ["business", "sports", "technology", "arts", "health"]

    articles_by_category = defaultdict(list)

    # Fetch articles from all APIs
    for newsapi_category, guardian_category, nytapi_category in zip(newsapi_categories, guardian_categories, nytapi_categories):
        # Fetch and store NewsAPI articles
        articles_by_category[newsapi_category].extend(fetch_newsapi_articles(newsapi_category, total_pages=1))

        # Fetch and store NYT articles
        articles_by_category[newsapi_category].extend(fetch_nyt_articles(nytapi_category))

        # Fetch and store Guardian articles
        articles_by_category[newsapi_category].extend(fetch_guardian_articles(guardian_category))

    # Writing articles by category to CSV in data/raw/
    for category, articles in articles_by_category.items():
        folder_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
        os.makedirs(folder_path, exist_ok=True)

        filename = os.path.join(folder_path, f"{category.lower().replace(' ', '_')}_articles.csv")

        if not articles:
            continue

        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["title", "description", "publishedAt", "url", "category"])
            for article in articles:
                writer.writerow([
                    article["title"], 
                    article["description"], 
                    article["publishedAt"], 
                    article["url"], 
                    category
                ])

        print(f"Saved {len(articles)} articles to {filename}")

# For testing or standalone execution
if __name__ == "__main__":
    fetch_news()
