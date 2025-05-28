import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

def write_trends_to_database():
    
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    today_str = datetime.today().strftime("%Y-%m-%d")

    # Connect to PostgreSQL
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    final_folder = os.path.join(base_dir, "data", "final")

    # Function to create table if it doesn't exist (no UNIQUE constraint)
    def create_table_if_missing(table_name):
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                date DATE,
                title TEXT,
                summary TEXT,
                url TEXT,
                publishedAt TIMESTAMP
            );
        """)
        conn.commit()

    # Process each *_summary.csv file
    for filename in os.listdir(final_folder):
        if filename.endswith("_summary.csv"):
            category = filename.replace("_summary.csv", "")
            table_name = f"{category}_trends"
            file_path = os.path.join(final_folder, filename)

            print(f"\n Processing category: {category}")

            df = pd.read_csv(file_path)
            create_table_if_missing(table_name)

            # Delete existing rows for today's execution date
            cursor.execute(f"DELETE FROM {table_name} WHERE date = %s", (today_str,))
            conn.commit()

            # Insert each summarized row
            for _, row in df.iterrows():
                try:
                    cursor.execute(
                        f"""
                        INSERT INTO {table_name} (date, title, summary, url, publishedAt)
                        VALUES (%s, %s, %s, %s, %s);
                        """,
                        (
                            today_str,  # When the trend was detected
                            row.get("title", ""),
                            row.get("summary", ""),
                            row.get("url", ""),
                            row.get("publishedAt", None),  # Original article's date
                        )
                    )
                except Exception as e:
                    print(f" Failed to insert row: {e}")
            conn.commit()

            print(f" Saved {len(df)} articles to '{table_name}'")

    # Clean up database connection
    cursor.close()
    conn.close()
    print("\n All categories have been written to the database.")


def read_trends_from_database(category, date):
    
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")

    table_name = f"{category}_trends"
    
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()

        query = f"""
            SELECT title, summary, url, publishedAt
            FROM {table_name}
            WHERE date = %s
            ORDER BY publishedAt DESC
        """
        cursor.execute(query, (date,))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows

    except Exception as e:
        print(f" Database read error: {e}")
        return []