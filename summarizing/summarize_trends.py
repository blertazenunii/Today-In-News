import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
print("KEYKEYKEY: ", openai_key)
client = OpenAI(api_key=openai_key)


def summarize_text(prompt_text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
                {"role": "user", "content": f"Summarize the following article in paragraph with 5-7 sentences:\n\n{prompt_text}"}
            ],
            temperature=0.5,
            max_tokens=120
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error summarizing: {e}")
        return ""

def summarize_trending_articles(trend_dir="data/trends", output_dir="data/final"):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    trend_dir = os.path.join(base_dir, "data", "trends")
    output_dir = os.path.join(base_dir, "data", "final")

    for filename in os.listdir(trend_dir):
        if filename.endswith(".csv"):
            category = filename.replace("_trending_articles.csv", "")
            input_path = os.path.join(trend_dir, filename)

            #Reading the file
            df = pd.read_csv(input_path)

            print(f"\n Summarizing category: {category}")
            summaries = []

            for _, row in df.iterrows():
                combined_text = f"{row['title']}\n{row['description']}"
                summary = summarize_text(combined_text)

                summaries.append({
                    "summary": summary,
                    "title": row["title"],
                    "url": row["url"],
                    "publishedAt": row["publishedAt"],
                    "category": row["category"],
                    "keyword": row["keyword"]
                })

            output_path = os.path.join(output_dir, f"{category}_summary.csv")
            pd.DataFrame(summaries).to_csv(output_path, index=False)
            print(f"Saved summaries to {output_path}")
