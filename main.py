from fetchers.news_fetcher import fetch_news
from preprocessing.preprocess_articles import process_all_articles
from preprocessing.vectorizer import analyze_all_categories
from preprocessing.vectorizer import extract_trending_articles
from summarizing.summarize_trends import summarize_trending_articles
from db_tools.write_read_database import write_trends_to_database

def main():
    print("\nStep 1: Fetching fresh news articles...")
    fetch_news()

    print("\nStep 2: Preprocessing articles for trend detection...")
    process_all_articles()
    

    print("\n Step 3: Analyzing trending topics by category...")
    analyze_all_categories()
    
    print("\n Step 4: Saving 3 trending articles per category...")
    extract_trending_articles()

    print("\n Step 5: Generating summaries for trending articles...")
    summarize_trending_articles()

    print("\n Step 6: Writing summarized trends to the PostgreSQL database...")
    write_trends_to_database()


if __name__ == "__main__":
    main()
