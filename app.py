import streamlit as st
import requests
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Kannupriya — Sentiment Dashboard", layout="wide")


NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
# 🔹 Title
st.title("🎬 Real-Time Sentiment Analysis Dashboard")
st.write("Made by Kannupriya ✨")

def fetch_news(query="movies"):
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    articles = data.get("articles", [])
    return articles

# 🔹 News ko Streamlit me show karna
st.subheader("📰 Latest News on Movies")
articles = fetch_news("movies")

for article in articles[:5]:
    st.write("", article["title"], "")
    st.write(article["url"])

from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(texts):
    text = " ".join(texts)
    wordcloud = WordCloud(width=800, height=400, background_color="black").generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

# --- WordCloud after showing news ---
if articles:
    st.subheader("☁ WordCloud of Movie News")
    texts = [article["title"] for article in articles if article["title"]]
    generate_wordcloud(texts)

# --- Sentiment Analysis Section ---
st.subheader("📊 Sentiment Analysis")

option = st.sidebar.selectbox(
    "Choose Analysis Mode",
    ["Single Sentence", "Multiple Sentences"]
)

# --- Single Sentence Analysis ---
if option == "Single Sentence":
    st.subheader("🔹 Single Sentence Analysis")
    text = st.text_input("Enter a sentence:")
    
    if st.button("Analyze"):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        sentiment = "Positive 😀" if polarity > 0 else "Negative 😡" if polarity < 0 else "Neutral 😐"
        st.write("Sentiment:", sentiment)
        st.write("Polarity Score:", polarity)

# --- Multiple Sentences Analysis ---
elif option == "Multiple Sentences":
    st.subheader("🔹 Multiple Sentences Analysis")
    multi_text = st.text_area("Enter multiple sentences (one per line):")
    
    if st.button("Analyze Multiple"):
        lines = multi_text.split("\n")
        results = []
        for line in lines:
            if line.strip():
                blob = TextBlob(line)
                polarity = blob.sentiment.polarity
                results.append({"Sentence": line, "Polarity": polarity})

        df_multi = pd.DataFrame(results)
        st.write(df_multi)

        pos = len(df_multi[df_multi["Polarity"] > 0])
        neg = len(df_multi[df_multi["Polarity"] < 0])
        neu = len(df_multi[df_multi["Polarity"] == 0])

        labels = ["Positive", "Negative", "Neutral"]
        values = [pos, neg, neu]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        st.pyplot(fig)
        st.pyplot(fig)



