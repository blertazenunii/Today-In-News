import csv
from newsapi_fetcher import fetch_newsapi_articles
from nyt_fetcher import fetch_nyt_articles
from guardian_fetcher import fetch_guardian_articles
from collections import defaultdict
import os

# Categories for NewsAPI, Guardian and NYT 
newsapi_categories = ["business", "sports", "technology", "entertainment", "health"]
guardian_categories = ["business", "sport", "technology", "culture", "lifeandstyle"]
nytapi_categories = ["business", "sports", "technology", "arts", "health"]


newsapi_all_articles = []
guardianapi_all_articles = []
nytapi_all_articles = []
articles_by_category = defaultdict(list)


# Fetch articles from all APIs
for newsapi_category, guardian_category,nytapi_category in zip(newsapi_categories, guardian_categories,nytapi_categories ):
    # Fetch and store NewsAPI articles
    articles_by_category[newsapi_category].extend(fetch_newsapi_articles(newsapi_category, total_pages=1))

    # Fetch and store NYT articles
    articles_by_category[newsapi_category].extend(fetch_nyt_articles(nytapi_category))

    # Fetch and store Guardian articles
    articles_by_category[newsapi_category].extend(fetch_guardian_articles(guardian_category))


#Writing articles by category to CSV
for category, articles in articles_by_category.items():
    
    # Create the filename based on the category name
    folder_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    filename = os.path.join(folder_path, f"{category.lower().replace(' ', '_')}_articles.csv")

    # Skip empty categories
    if not articles:
        continue

    # Write the articles to the CSV
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
       
        # Write the header
        writer.writerow(["title", "description", "publishedAt", "url", "category"])
        # Write all articles
        for article in articles:
            writer.writerow([article["title"], article["description"], article["publishedAt"], article["url"], category])

    print(f"Saved {len(articles)} articles to {category}.csv")