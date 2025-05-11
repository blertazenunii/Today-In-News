import csv
from newsapi_fetcher import fetch_newsapi_articles
from nyt_fetcher import fetch_nyt_articles
from guardian_fetcher import fetch_guardian_articles

# Categories for NewsAPI and Guardian (using normal lists)
newsapi_categories = ["business", "sports", "technology", "entertainment", "health"]
guardian_categories = ["business", "sport", "technology", "culture", "lifeandstyle"]
nytapi_categories = ["business", "sports", "technology", "arts", "health"]


all_articles = []
newsapi_all_articles = []
guardianapi_all_articles = []
nytapi_all_articles = []

# Fetch articles from all APIs
for newsapi_category, guardian_category,nytapi_category in zip(newsapi_categories, guardian_categories,nytapi_categories ):
    # NewsAPI
    newsapi_all_articles.extend(fetch_newsapi_articles(newsapi_category, total_pages=1))  # Just 1 page for NewsAPI
    
    # NY Times (if needed)
    nytapi_all_articles.extend(fetch_nyt_articles(nytapi_category))
    
    # Guardian
    guardianapi_all_articles.extend(fetch_guardian_articles(guardian_category))  # Use mapped category for Guardian

# Print NewsAPI articles
print("\n--- NewsAPI Articles ---")
all= 0
newsapi = 0
guardian = 0
nyt = 0

for article in newsapi_all_articles:
    newsapi +=1
    print(f"Category: {article['category']}, Title: {article['title']}")

# Print Guardian articles
print("\n--- Guardian Articles ---")
for article in guardianapi_all_articles:
    guardian +=1
    print(f"Category: {article['category']}, Title: {article['title']}")

# Print NYT articles
print("\n--- NYT Articles ---")
for article in nytapi_all_articles:
    nyt +=1
    print(f"Category: {article['category']}, Title: {article['title']}")

all = newsapi + guardian + nyt
print("All articles count: ", all)