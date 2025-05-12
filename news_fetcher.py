import csv
from newsapi_fetcher import fetch_newsapi_articles
from nyt_fetcher import fetch_nyt_articles
from guardian_fetcher import fetch_guardian_articles

# Categories for NewsAPI, Guardian and NYT 
newsapi_categories = ["business", "sports", "technology", "entertainment", "health"]
guardian_categories = ["business", "sport", "technology", "culture", "lifeandstyle"]
nytapi_categories = ["business", "sports", "technology", "arts", "health"]


newsapi_all_articles = []
guardianapi_all_articles = []
nytapi_all_articles = []

# Fetch articles from all APIs
for newsapi_category, guardian_category,nytapi_category in zip(newsapi_categories, guardian_categories,nytapi_categories ):
    # NewsAPI
    newsapi_all_articles.extend(fetch_newsapi_articles(newsapi_category, total_pages=1))  
    
    # NY Times (if needed)
    nytapi_all_articles.extend(fetch_nyt_articles(nytapi_category))
    
    # Guardian
    guardianapi_all_articles.extend(fetch_guardian_articles(guardian_category))  

# Print details about fetched articles
total_articles_count = len(newsapi_all_articles) + len(nytapi_all_articles)+ len(guardianapi_all_articles)
print("Total number of articles fetched from NEWSAPI:", len(newsapi_all_articles))
print("Total number of articles fetched from NYTAPI:", len(nytapi_all_articles))
print("Total number of articles fetched from GUARDIANAPI:", len(guardianapi_all_articles))
print("Total articles fetched: ", total_articles_count)