import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(page_title="CORD-19 Data Explorer", layout="wide")

# Title
st.title("📊 CORD-19 Data Explorer")
st.write("Interactive exploration of COVID-19 research papers using the CORD-19 metadata dataset.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/metadata.csv")
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    df = df.dropna(subset=['title', 'year'])
    return df

df = load_data()

# Sidebar filters
year_range = st.slider("Select year range", int(df['year'].min()), int(df['year'].max()), (2020, 2021))
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(20))

# Publications over time
st.subheader("Publications Over Time")
year_counts = filtered_df['year'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x=year_counts.index, y=year_counts.values, ax=ax, palette="viridis")
ax.set_title("Number of Publications by Year")
st.pyplot(fig)

# Top journals
st.subheader("Top Journals")
top_journals = filtered_df['journal'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(y=top_journals.index, x=top_journals.values, ax=ax, palette="magma")
ax.set_title("Top 10 Journals")
st.pyplot(fig)

# Word cloud
st.subheader("Word Cloud of Paper Titles")
text = " ".join(filtered_df['title'].dropna().astype(str).tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
fig, ax = plt.subplots(figsize=(10,6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)
