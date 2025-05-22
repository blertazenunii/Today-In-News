from fetchers.news_fetcher import fetch_news
from preprocessing.preprocess_articles import process_all_articles
import os

def main():
    print("\n Step 1: Fetching fresh news articles...")
    fetch_news()

    print("\n Step 2: Preprocessing articles for trend detection...")
    raw_folder = os.path.join("data", "raw")
    processed_folder = os.path.join("data", "processed")
    process_all_articles(raw_folder, processed_folder)

    

if __name__ == "__main__":
    main()
