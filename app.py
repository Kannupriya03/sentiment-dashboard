import streamlit as st
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Real-Time Sentiment Analysis Dashboard")

# Sidebar menu
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