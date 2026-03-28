import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Bird Dashboard", layout="wide")

# ---------------- HELPER FUNCTION ----------------
def get_top_category(series):
    if series.empty:
        return "No Data"
    return series.value_counts().idxmax()

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

# ---------------- KEY INSIGHTS ----------------
st.markdown("### 📌 Key Insights")

top_habitat = get_top_category(filtered_df['habitat'])
top_season = get_top_category(filtered_df['season'])

st.success(f"""
- {top_habitat} habitat shows highest biodiversity  
- Peak activity observed during {top_season} season  
- Certain plots act as biodiversity hotspots  
- Watchlist species require conservation focus  
""")

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🦜 Species", "🌍 Environment"])

# ================= TAB 1 =================
with tab1:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("Habitat Distribution")
    fig = plt.figure(figsize=(8,5))
    filtered_df['habitat'].value_counts().plot(kind='bar')
    plt.xticks(rotation=0)
    st.pyplot(fig)

    st.info(f"👉 {top_habitat} habitat has the highest bird observations.")

    st.subheader("Seasonal Distribution")
    fig = plt.figure(figsize=(8,5))
    filtered_df['season'].value_counts().plot(kind='bar')
    st.pyplot(fig)

    st.info(f"👉 {top_season} season shows peak bird activity.")

    st.subheader("Monthly Trend")
    fig = plt.figure(figsize=(8,5))
    filtered_df['month'].value_counts().sort_index().plot(kind='line', marker='o')
    st.pyplot(fig)

    st.info("👉 Monthly trends help identify peak observation periods.")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 2 =================
with tab2:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("Top 10 Species")
    fig = plt.figure(figsize=(8,5))
    filtered_df['common_name'].value_counts().head(10).plot(kind='bar')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    top_species = get_top_category(filtered_df['common_name'])
    st.info(f"👉 Most frequently observed species is {top_species}.")

    st.subheader("Biodiversity Hotspots")
    hotspots = filtered_df.groupby('plot_name')['scientific_name'].nunique().sort_values(ascending=False).head(10)

    fig = plt.figure(figsize=(8,5))
    hotspots.plot(kind='bar')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    if not hotspots.empty:
        st.info(f"👉 Plot {hotspots.idxmax()} is the top biodiversity hotspot.")

    st.subheader("Observer Analysis")
    fig = plt.figure(figsize=(8,5))
    filtered_df['observer'].value_counts().head(10).plot(kind='bar')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    top_observer = get_top_category(filtered_df['observer'])
    st.info(f"👉 {top_observer} recorded the highest observations.")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 3 =================
with tab3:
    st.markdown('<div class="section">', unsafe_allow_html=True)

    st.subheader("Temperature vs Humidity")
    fig = plt.figure(figsize=(8,5))
    plt.scatter(filtered_df['temperature'], filtered_df['humidity'])
    plt.xlabel("Temperature")
    plt.ylabel("Humidity")
    st.pyplot(fig)

    avg_temp = filtered_df['temperature'].mean()
    avg_hum = filtered_df['humidity'].mean()
    st.info(f"👉 Avg Temp: {avg_temp:.1f}°C | Avg Humidity: {avg_hum:.1f}%")

    st.subheader("Distance Distribution")
    fig = plt.figure(figsize=(8,5))
    filtered_df['distance'].value_counts().plot(kind='bar')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    top_distance = get_top_category(filtered_df['distance'])
    st.info(f"👉 Most birds observed at {top_distance}.")

    st.subheader("Flyover Observations")
    fig = plt.figure(figsize=(8,5))
    filtered_df['flyover_observed'].value_counts().plot(kind='bar')
    st.pyplot(fig)

    top_fly = get_top_category(filtered_df['flyover_observed'])
    st.info(f"👉 Flyover observations are mostly {top_fly}.")

    st.subheader("Watchlist Status")
    fig = plt.figure(figsize=(8,5))
    filtered_df['pif_watchlist_status'].value_counts().plot(kind='bar')
    st.pyplot(fig)

    top_watch = get_top_category(filtered_df['pif_watchlist_status'])
    st.info(f"👉 Majority watchlist status: {top_watch}.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DOWNLOAD ----------------
st.markdown("---")

st.download_button(
    "📥 Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_bird_data.csv"
)
