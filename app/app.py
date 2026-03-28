import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Bird Dashboard", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}
.big-title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    color: #FFFFFF;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(135deg, #1f4037, #99f2c8);
    color: black;
    text-align: center;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
}
.section {
    margin-top: 30px;
    padding: 20px;
    border-radius: 15px;
    background-color: #161B22;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/processed/merged_data.csv")

# ---------------- TITLE ----------------
st.markdown('<div class="big-title">🐦 Bird Species Analysis Dashboard</div>', unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔍 Filters")

habitat = st.sidebar.multiselect("Habitat", df['habitat'].unique(), default=df['habitat'].unique())
season = st.sidebar.multiselect("Season", df['season'].unique(), default=df['season'].unique())
species = st.sidebar.multiselect("Species", df['common_name'].dropna().unique())
observer = st.sidebar.multiselect("Observer", df['observer'].dropna().unique())

# ---------------- FILTER ----------------
filtered_df = df[(df['habitat'].isin(habitat)) & (df['season'].isin(season))]

if species:
    filtered_df = filtered_df[filtered_df['common_name'].isin(species)]

if observer:
    filtered_df = filtered_df[filtered_df['observer'].isin(observer)]

# ---------------- KPI CARDS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="card">📊<br><b>Total Observations</b><br>{len(filtered_df)}</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="card">🦜<br><b>Unique Species</b><br>{filtered_df["scientific_name"].nunique()}</div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="card">📍<br><b>Total Locations</b><br>{filtered_df["plot_name"].nunique()}</div>', unsafe_allow_html=True)

# ---------------- INSIGHTS ----------------
st.markdown("### 📌 Key Insights")
st.success("""
- Forest habitats have higher biodiversity  
- Monsoon season shows peak bird activity  
- Certain plots are biodiversity hotspots  
- Watchlist species require urgent conservation  
""")

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🦜 Species", "🌍 Environment"])

# ---------- TAB 1 ----------
with tab1:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("Habitat Distribution")
    fig = plt.figure(figsize=(8,5))
    filtered_df['habitat'].value_counts().plot(kind='bar')
    plt.xticks(rotation=0)
    st.pyplot(fig)

    st.subheader("Seasonal Distribution")
    fig = plt.figure(figsize=(8,5))
    filtered_df['season'].value_counts().plot(kind='bar')
    st.pyplot(fig)

    st.subheader("Monthly Trend")
    fig = plt.figure(figsize=(8,5))
    filtered_df['month'].value_counts().sort_index().plot(kind='line', marker='o')
    st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- TAB 2 ----------
with tab2:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("Top 10 Species")
    fig = plt.figure(figsize=(8,5))
    filtered_df['common_name'].value_counts().head(10).plot(kind='bar')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Biodiversity Hotspots")
    hotspots = filtered_df.groupby('plot_name')['scientific_name'].nunique().sort_values(ascending=False).head(10)
    fig = plt.figure(figsize=(8,5))
    hotspots.plot(kind='bar')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Observer Analysis")
    fig = plt.figure(figsize=(8,5))
    filtered_df['observer'].value_counts().head(10).plot(kind='bar')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- TAB 3 ----------
with tab3:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("Temperature vs Humidity")
    fig = plt.figure(figsize=(8,5))
    plt.scatter(filtered_df['temperature'], filtered_df['humidity'])
    plt.xlabel("Temperature")
    plt.ylabel("Humidity")
    st.pyplot(fig)

    st.subheader("Distance Distribution")
    fig = plt.figure(figsize=(8,5))
    filtered_df['distance'].value_counts().plot(kind='bar')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Flyover Observations")
    fig = plt.figure(figsize=(8,5))
    filtered_df['flyover_observed'].value_counts().plot(kind='bar')
    st.pyplot(fig)

    st.subheader("Watchlist Status")
    fig = plt.figure(figsize=(8,5))
    filtered_df['pif_watchlist_status'].value_counts().plot(kind='bar')
    st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DOWNLOAD ----------------
st.markdown("---")
st.download_button("📥 Download Data", filtered_df.to_csv(index=False), "filtered_data.csv")