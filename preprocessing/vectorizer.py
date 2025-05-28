import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def analyze_all_categories():
    # This gets the absolute path to the parent folder of preprocessing/
    base_dir = os.path.dirname(os.path.dirname(__file__))
    processed_dir = os.path.join(base_dir, "data", "processed")

    #Go for every file in the specified directory
    for filename in os.listdir(processed_dir):
       
        #Detect if it is a csv file
        if filename.endswith(".csv"):
            path = os.path.join(processed_dir,filename)
            
            #Read the file
            df = pd.read_csv(path)

            #Get category name from filename
            category = filename.replace("_articles.csv", "")
            print(f"\n Category: {category}")

            if "cleaned_text" not in df.columns:
                print("No 'cleaned_text' column found.")
                continue

            print(f"✅ {len(df)} articles found.")

            texts = df["cleaned_text"].dropna().tolist()
            top_keywords = get_top_keywords(texts)

            print(f"🏷️ Top keywords:")
            for word, score in top_keywords:
                print(f"- {word}: {score:.4f}")


def get_top_keywords(texts, top_n=10):
    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_df=0.85, stop_words='english')
    
    # Convert the text list into a TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Get feature names (words)
    feature_names = vectorizer.get_feature_names_out()

    # Sum TF-IDF scores for each word
    scores = tfidf_matrix.sum(axis=0).A1  # convert to 1D list
    word_score_pairs = list(zip(feature_names, scores))

    # Sort by score descending and return top N
    top_keywords = sorted(word_score_pairs, key=lambda x: x[1], reverse=True)[:top_n]
    return top_keywords


def extract_trending_articles():
    # This gets the absolute path to the parent folder of preprocessing/
    base_dir = os.path.dirname(os.path.dirname(__file__))
    processed_dir = os.path.join(base_dir, "data", "processed")
    output_dir = os.path.join(base_dir,"data/trends")

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(processed_dir):
        if filename.endswith(".csv"):
            category = filename.replace("_articles.csv", "")
            path = os.path.join(processed_dir, filename)
            df = pd.read_csv(path)

            if "cleaned_text" not in df.columns:
                continue

            texts = df["cleaned_text"].dropna().tolist()
            top_keywords = get_top_keywords(texts, top_n=10)

            seen_urls = set()
            selected_articles = []

            for keyword, _ in top_keywords:
                matches = df[df["cleaned_text"].str.contains(rf"\b{keyword}\b", case=False, na=False)]
                
                for _, row in matches.iterrows():
                    if row["url"] not in seen_urls:
                        seen_urls.add(row["url"])
                        selected_articles.append({
                            "title": row["title"],
                            "description": row["description"],
                            "publishedAt": row["publishedAt"],
                            "url": row["url"],
                            "category": row["category"],
                            "keyword": keyword
                        })
                    if len(selected_articles) >= 3:
                        break
                if len(selected_articles) >= 3:
                        break
                        
            output_path = os.path.join(output_dir, f"{category}_trending_articles.csv")
            pd.DataFrame(selected_articles).to_csv(output_path, index=False)
            print(f"✅ Saved detailed trending articles for '{category}' to {output_path}")


if __name__ == "__main__":
    analyze_all_categories()