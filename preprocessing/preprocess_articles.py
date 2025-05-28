import os
import re
import string
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download NLTK data if missing
nltk.download("stopwords")
nltk.download("wordnet")

# Preprocessing tools
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

def process_all_articles():
    # Hardcoded relative paths
    raw_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    processed_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')

    os.makedirs(processed_dir, exist_ok=True)

    for filename in os.listdir(raw_dir):
        if filename.endswith(".csv"):
            raw_path = os.path.join(raw_dir, filename)
            processed_path = os.path.join(processed_dir, filename)

            print(f"Processing: {filename}")
            df = pd.read_csv(raw_path)
            df["cleaned_text"] = df.apply(
                lambda row: clean_text(f"{row.get('title', '')} {row.get('description', '')}"), axis=1
            )
            df.to_csv(processed_path, index=False)
            print(f"Saved cleaned file: {processed_path}")

if __name__ == "__main__":
    process_all_articles()
