import streamlit as st
import requests
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Kannupriya — Sentiment Dashboard", layout="wide")

# 🔑 Load API key from Streamlit Secrets (safe method)
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]

# ------------------ TITLE ------------------
st.title("🎬 Real-Time Sentiment Analysis Dashboard")
st.write("Made by *Kannupriya ✨*")

# ------------------ FUNCTION: Fetch News ------------------
def fetch_news(query="movies"):
    """
    Fetch latest news articles from NewsAPI based on a query.
    """
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Return empty list if request fails
    if data.get("status") != "ok":
        return []
    return data.get("articles", [])

# ------------------ SHOW LATEST NEWS ------------------
st.subheader("📰 Latest News on Movies")
articles = fetch_news("movies")

if articles:
    for article in articles[:5]:  # show only first 5 articles
        st.write("👉", article["title"])
        st.write(article["url"])
else:
    st.warning("⚠ No news available right now (API limit may have been reached).")

# ------------------ FUNCTION: WordCloud ------------------
def generate_wordcloud(texts):
    """
    Generate and display a WordCloud from a list of texts.
    """
    text = " ".join(texts)
    wordcloud = WordCloud(width=800, height=400, background_color="black").generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

# --- WordCloud Section ---
if articles:
    st.subheader("☁ WordCloud of Movie News")
    texts = [article["title"] for article in articles if article["title"]]
    if texts:
        generate_wordcloud(texts)

# ------------------ SENTIMENT ANALYSIS ------------------
st.subheader("📊 Sentiment Analysis")

# Sidebar selection
option = st.sidebar.selectbox(
    "Choose Analysis Mode",
    ["Single Sentence", "Multiple Sentences"]
)

# --- Single Sentence Analysis ---
if option == "Single Sentence":
    st.subheader("🔹 Single Sentence Analysis")
    text = st.text_input("Enter a sentence:")
    
    if st.button("Analyze"):
        if text.strip():
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            sentiment = "Positive 😀" if polarity > 0 else "Negative 😡" if polarity < 0 else "Neutral 😐"
            
            st.success(f"*Sentiment:* {sentiment}")
            st.info(f"*Polarity Score:* {polarity}")
        else:
            st.error("⚠ Please enter some text before analyzing.")

# --- Multiple Sentences Analysis ---
elif option == "Multiple Sentences":
    st.subheader("🔹 Multiple Sentences Analysis")
    multi_text = st.text_area("Enter multiple sentences (one per line):")
    
    if st.button("Analyze Multiple"):
        if multi_text.strip():
            lines = multi_text.split("\n")
            results = []
            for line in lines:
                if line.strip():
                    blob = TextBlob(line)
                    polarity = blob.sentiment.polarity
                    results.append({"Sentence": line, "Polarity": polarity})

            df_multi = pd.DataFrame(results)
            st.write("📋 Sentiment Results:", df_multi)

            # Count sentiments
            pos = len(df_multi[df_multi["Polarity"] > 0])
            neg = len(df_multi[df_multi["Polarity"] < 0])
            neu = len(df_multi[df_multi["Polarity"] == 0])

            labels = ["Positive", "Negative", "Neutral"]
            values = [pos, neg, neu]

            # Pie Chart
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct="%1.1f%%")
            st.pyplot(fig)
        else:
            st.error("⚠ Please enter some text before analyzing.")

# ------------------ SIDEBAR: About ------------------
st.sidebar.markdown("## About this App")
st.sidebar.info(
    "🎬 This is a Real-Time Sentiment Analysis Dashboard built with Streamlit. "
    "It fetches latest movie news using NewsAPI, generates a WordCloud of trending keywords, "
    "and performs sentiment analysis (single & multiple sentences) using TextBlob. \n\n"
    "👩‍💻 Built with ❤ by [Kannupriya](https://github.com/Kannupriya03)"
)





