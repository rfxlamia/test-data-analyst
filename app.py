import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Konfigurasi Halaman Website
st.set_page_config(
    page_title="Spotify Dashboard",
    page_icon="🎵",
    layout="wide"
)

# 2. Judul dan Deskripsi
st.title("🎵 My First Data App: Spotify Analysis")
st.write("Aplikasi ini dibuat menggunakan Python & Streamlit. Data berdasarkan simulasi Spotify dataset.")

# --- LOAD DATA (Simulasi Data Day 3 & 4) ---
@st.cache_data # Biar ngebut, gak load ulang terus
def load_data():
    # Kita bikin data dummy yang mirip dengan hasil cleaning Day 4
    data = {
        'Track': ['Blinding Lights', 'Shape of You', 'Dance Monkey', 'Someone You Loved', 
                  'Sunflower', 'One Dance', 'Stay', 'Believer', 'Closer', 'Starboy'],
        'Artist': ['The Weeknd', 'Ed Sheeran', 'Tones and I', 'Lewis Capaldi', 
                   'Post Malone', 'Drake', 'The Kid LAROI', 'Imagine Dragons', 'The Chainsmokers', 'The Weeknd'],
        'Genre': ['Synthwave', 'Pop', 'Pop', 'Ballad', 
                  'Hip-Hop', 'Hip-Hop', 'Pop', 'Rock', 'EDM', 'R&B'],
        'Streams_Billion': [3.4, 3.3, 2.4, 2.6, 2.5, 2.4, 1.8, 1.7, 2.2, 1.9],
        'Duration_Min': [3.3, 3.9, 3.5, 3.0, 2.6, 2.9, 2.3, 3.4, 4.0, 3.8],
        'Danceability': [51, 82, 82, 50, 75, 79, 59, 77, 75, 68]
    }
    return pd.DataFrame(data)

df = load_data()

# --- SIDEBAR FILTERS (Interaktif) ---
st.sidebar.header("⚙️ Filter Data")

# Filter Genre
selected_genre = st.sidebar.multiselect(
    "Pilih Genre:",
    options=df['Genre'].unique(),
    default=df['Genre'].unique() # Default pilih semua
)

# Filter Streams
min_streams = st.sidebar.slider(
    "Minimum Streams (Billion):",
    min_value=0.0,
    max_value=4.0,
    value=1.5
)

# Filter Dataframe berdasarkan input user
filtered_df = df[
    (df['Genre'].isin(selected_genre)) & 
    (df['Streams_Billion'] >= min_streams)
]

# --- MAIN DASHBOARD (KPI Metrics) ---
# Belajar dari Day 2 (NumPy/Pandas Stats)
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    total_streams = filtered_df['Streams_Billion'].sum()
    st.metric("Total Streams", f"{total_streams:.1f} B")

with col2:
    avg_dance = filtered_df['Danceability'].mean()
    # Handle error kalau data kosong
    if pd.isna(avg_dance): avg_dance = 0 
    st.metric("Avg Danceability", f"{avg_dance:.0f}/100")

with col3:
    top_artist = filtered_df['Artist'].mode()
    if not top_artist.empty:
        st.metric("Top Artist", top_artist[0])
    else:
        st.metric("Top Artist", "-")

# --- VISUALISASI (Matplotlib dari Day 5) ---
st.markdown("---")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 Top Songs by Streams")
    
    # Matplotlib Code (Persis Day 5)
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    # Sort biar grafiknya rapi
    chart_data = filtered_df.sort_values('Streams_Billion', ascending=True)
    
    ax1.barh(chart_data['Track'], chart_data['Streams_Billion'], color='skyblue')
    ax1.set_xlabel("Streams (Billion)")
    ax1.set_title("Lagu Terpopuler")
    
    # Tampilkan di Streamlit
    st.pyplot(fig1)

with col_chart2:
    st.subheader("🎵 Distribution of Duration")
    
    # Histogram Code
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.hist(filtered_df['Duration_Min'], bins=5, color='lightgreen', edgecolor='black')
    ax2.set_xlabel("Duration (Min)")
    ax2.set_ylabel("Count")
    ax2.set_title("Distribusi Durasi Lagu")
    
    st.pyplot(fig2)

# --- MENAMPILKAN DATA RAW ---
st.markdown("---")
st.subheader("📋 Raw Data")
# Checkbox untuk hide/show data
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
