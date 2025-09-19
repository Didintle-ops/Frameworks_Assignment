# --- Part 1: Load and Explore Data ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load metadata.csv
df = pd.read_csv("data/metadata.csv")

# Basic exploration
print("Shape:", df.shape)
print(df.info())
print(df.head())

# Missing values
print(df.isnull().sum().sort_values(ascending=False).head(10))

# --- Part 2: Data Cleaning ---
# Convert dates
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year

# Abstract word count (if available)
df['abstract_word_count'] = df['abstract'].astype(str).apply(lambda x: len(x.split()))

# Drop rows without title or year
df = df.dropna(subset=['title', 'year'])

# --- Part 3: Analysis & Visualization ---
# Publications per year
year_counts = df['year'].value_counts().sort_index()
plt.figure(figsize=(8,5))
sns.barplot(x=year_counts.index, y=year_counts.values, palette="viridis")
plt.title("Publications by Year")
plt.xticks(rotation=45)
plt.show()

# Top journals
top_journals = df['journal'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(y=top_journals.index, x=top_journals.values, palette="magma")
plt.title("Top 10 Journals Publishing COVID-19 Papers")
plt.show()

# Word frequency from titles
text = " ".join(df['title'].dropna().astype(str).tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
plt.figure(figsize=(10,6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Word Cloud of Paper Titles")
plt.show()

# Papers by source
source_counts = df['source_x'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(y=source_counts.index, x=source_counts.values, palette="coolwarm")
plt.title("Top 10 Sources of Papers")
plt.show()
