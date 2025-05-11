import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load API key from .env
load_dotenv()
api_key = os.getenv("NEWSAPI_KEY")

# Get today's date in YYYY-MM-DD format
today_date = datetime.today().strftime('%Y-%m-%d')

# Calculate the date one week ago
one_week_ago = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

# Set up the API endpoint and parameters
url = "https://newsapi.org/v2/everything"
categories = ["business", "sports", "technology", "entertainment", "health"]
params = {
    "language": "en",  # You can change this to other languages if needed
    "pageSize": 100,    # Max articles per page (up to 100)
    "apiKey": api_key,
    "from": one_week_ago,  # Fetch articles from one week ago
    "to": today_date,  # Fetch articles up until today
}

def fetch_articles_from_category(category, page):
    params["q"] = category   # Use category name as query
    params["page"] = page    # Pagination
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise exception if status is not 200
    return response.json()

def fetch_articles_for_category(category, total_pages):
    all_articles = []
    
    for page_num in range(1, total_pages + 1):
        print(f"Fetching page {page_num} for category: {category}")
        data = fetch_articles_from_category(category, page_num)
        articles = data.get("articles", [])
        all_articles.extend(articles)  # Add articles to the list
        print(f"Page {page_num}: Fetched {len(articles)} articles")
        
        # If there are fewer than the requested articles on a page, stop paginating
        if len(articles) < 100:
            print(f"Less than 100 articles found for {category} on page {page_num}, stopping pagination.")
            break
    
    return all_articles

# Set the number of pages you want to fetch (for more data)
total_pages = 1  # Try fetching up to 10 pages for each category

all_news = {}

for category in categories:
    all_articles = fetch_articles_for_category(category, total_pages)
    all_news[category] = all_articles
    print(f"\nTotal articles fetched for category '{category}': {len(all_articles)}")

# Example: Print titles of the articles fetched for 'sports' category
print("\nExample articles from 'sports' category:")
for i, article in enumerate(all_news['sports'][:5]):  # Print first 5 sports articles
    print(f"{i+1}. {article['title']}")

# Save all articles for each category in a CSV file
import csv

with open("all_articles_last_week.csv", mode="w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Category", "Title", "Description", "Published At", "URL"])

    for category, articles in all_news.items():
        for article in articles:
            writer.writerow([category, article.get("title"), article.get("description"),
                             article.get("publishedAt"), article.get("url")])

print("\nAll articles from the last week saved to all_articles_last_week.csv")
