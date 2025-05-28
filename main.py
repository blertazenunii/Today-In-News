from fetchers.news_fetcher import fetch_news
from preprocessing.preprocess_articles import process_all_articles

def main():
    print("\nStep 1: Fetching fresh news articles...")
    fetch_news()

    print("\nStep 2: Preprocessing articles for trend detection...")
    process_all_articles()

    

if __name__ == "__main__":
    main()
