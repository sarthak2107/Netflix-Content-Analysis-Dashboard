import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Load cleaned data
df = pd.read_csv("netflix_cleaned.csv")

st.title("🎬 Netflix Content Analysis Dashboard")
st.markdown("Analyze Netflix's movie and TV show catalog over time, genre, and country.")

# Filters
type_filter = st.selectbox("Select Type", options=["All"] + df['type'].unique().tolist())
country_filter = st.selectbox("Select Country", options=["All"] + sorted(df['country'].unique().tolist()))

filtered_df = df.copy()
if type_filter != "All":
    filtered_df = filtered_df[filtered_df['type'] == type_filter]
if country_filter != "All":
    filtered_df = filtered_df[filtered_df['country'] == country_filter]

# Charts
col1, col2 = st.columns(2)

with col1:
    type_count = filtered_df['type'].value_counts()
    st.subheader("Content Type Distribution")
    st.bar_chart(type_count)

with col2:
    st.subheader("Content Over Years")
    yearly = filtered_df['year_added'].value_counts().sort_index()
    st.line_chart(yearly)

# Genre breakdown
st.subheader("Top Genres")
all_genres = ','.join(filtered_df['listed_in']).split(',')
from collections import Counter
genre_count = Counter([g.strip() for g in all_genres])
top_genres = pd.DataFrame(genre_count.most_common(10), columns=['Genre', 'Count'])
fig = px.bar(top_genres, x='Count', y='Genre', orientation='h', title='Top 10 Genres')
st.plotly_chart(fig)
