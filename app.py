import streamlit as st
from datetime import date
from fetchers.news_fetcher import fetch_news
from preprocessing.preprocess_articles import process_all_articles
from preprocessing.vectorizer import analyze_all_categories
from summarizing.summarize_trends import summarize_trending_articles
from db_tools.write_read_database import write_trends_to_database, read_trends_from_database

# Page settings
st.set_page_config(page_title="Today In News", layout="wide")
st.title("🗞️ Today in News - Daily Trend Detection")

# Step 1: Run pipeline only once
if "pipeline_done" not in st.session_state:
    with st.status("⚙️ Running pipeline... Please wait...", expanded=True) as status:
        st.write("🔄 Fetching fresh news...")
        fetch_news()

        st.write("🔄 Preprocessing articles...")
        process_all_articles()

        st.write("🔄 Detecting trending topics...")
        analyze_all_categories()

        st.write("🔄 Summarizing articles...")
        summarize_trending_articles()

        st.write("🔄 Saving to database...")
        write_trends_to_database()

        status.update(label="✅ All steps completed!", state="complete", expanded=False)

    st.session_state.pipeline_done = True

# Step 2: UI for viewing by date and category
st.subheader("Explore Trending News")

# Date selection at the top
selected_date = st.date_input("Select a date", value=date.today())

# Step 3: Tabs per category
categories = ["business", "sports", "technology", "entertainment", "health"]
tabs = st.tabs([cat.capitalize() for cat in categories])

for tab, category in zip(tabs, categories):
    with tab:
        st.write(f"🗂️ Showing trends for **{category}** on {selected_date}")
        rows = read_trends_from_database(category, selected_date)

        if not rows:
            st.warning("No trending articles found for this date.")
        else:
            for title, summary, url, published_at in rows:
                st.markdown(f"### {title}")
                st.markdown(f"**Published:** {published_at}")
                st.markdown(summary)
                st.markdown(f"[🔗 Read Full Article]({url})")
                st.markdown("---")
