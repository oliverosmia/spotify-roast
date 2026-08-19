import streamlit as st
import json
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Page config
st.set_page_config(page_title="🎵 Spotify Roast", layout="wide", initial_sidebar_state="expanded")

# Custom styling
st.markdown("""
    <style>
    .roast-container {
        background: linear-gradient(135deg, #1DB954 0%, #191414 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-size: 18px;
        line-height: 1.6;
        margin: 20px 0;
        border-left: 5px solid #1ed760;
    }
    .metric-card {
        background: #282828;
        padding: 15px;
        border-radius: 8px;
        color: #1DB954;
        text-align: center;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎵 Spotify Roast - NLP Edition")
st.markdown("*Get roasted by an AI music critic powered by NLP*")

# ============================================================================
# SIDEBAR: Data Selection
# ============================================================================
st.sidebar.header("📥 Data Source")

data_source = st.sidebar.radio(
    "Choose your data source:",
    ["Sample Data", "Upload JSON"]
)

spotify_data = None
username = None

if data_source == "Sample Data":
    sample_option = st.sidebar.selectbox(
        "Select a sample profile:",
        [
            "music_lover_2024 (Balanced)",
            "pop_addict (Pop Heavy)",
            "indie_hipster (Indie Obsessed)",
            "metal_head (Rock/Metal)",
            "kpop_stan (K-Pop Fan)"
        ]
    )
    
    # Load corresponding sample file
    sample_files = {
        "music_lover_2024 (Balanced)": "sample_spotify_data.json",
        "pop_addict (Pop Heavy)": "sample_pop_addict.json",
        "indie_hipster (Indie Obsessed)": "sample_indie_hipster.json",
        "metal_head (Rock/Metal)": "sample_metal_head.json",
        "kpop_stan (K-Pop Fan)": "sample_kpop_stan.json"
    }
    
    try:
        with open(sample_files[sample_option], 'r') as f:
            spotify_data = json.load(f)
            username = spotify_data.get('username', 'Unknown User')
    except FileNotFoundError:
        st.error(f"❌ File not found: {sample_files[sample_option]}")
        st.info("Make sure all sample JSON files are in the same directory as this script.")

else:  # Upload JSON
    uploaded_file = st.sidebar.file_uploader("Upload your Spotify JSON", type="json")
    
    if uploaded_file:
        try:
            spotify_data = json.load(uploaded_file)
            username = spotify_data.get('username', 'Unknown User')
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON file")

# LMStudio connection settings
st.sidebar.header("🔧 LMStudio Settings")
lmstudio_ip = st.sidebar.text_input("LMStudio IP:Port", value="192.168.86.3:1234")
lmstudio_url = f"http://{lmstudio_ip}/v1/chat/completions"

if st.sidebar.checkbox("Test LMStudio Connection"):
    try:
        test_response = requests.post(
            lmstudio_url,
            json={
                "model": "local-model",
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 10
            },
            timeout=5
        )
        if test_response.status_code == 200:
            st.sidebar.success("✅ LMStudio connected!")
        else:
            st.sidebar.error(f"❌ Error: {test_response.status_code}")
    except Exception as e:
        st.sidebar.error(f"❌ Connection failed: {str(e)}")

# ============================================================================
# MAIN CONTENT
# ============================================================================

if spotify_data is None:
    st.warning("👈 Please select or upload Spotify data in the sidebar to begin")
else:
    # Display user info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👤 User", username)
    with col2:
        st.metric("🎵 Top Tracks", len(spotify_data.get('topTracks', [])))
    with col3:
        st.metric("🎸 Genres", len(spotify_data.get('topGenres', [])))
    
    st.divider()
    
    # ============================================================================
    # NER ANALYSIS
    # ============================================================================
    st.header("📊 Part 1: Named Entity Recognition (NER)")
    
    # Extract artist names
    artist_names = [artist['name'] for artist in spotify_data.get('topArtists', [])]
    artist_popularity = {artist['name']: artist['popularity'] for artist in spotify_data.get('topArtists', [])}
    
    # Extract and flatten genres
    all_genres = []
    for artist in spotify_data.get('topArtists', []):
        all_genres.extend(artist.get('genres', []))
    
    genre_counts = Counter(all_genres)
    top_genres = dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:15])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎤 Top 15 Artists")
        artist_df = pd.DataFrame({
            'Artist': artist_names[:15],
            'Popularity': [artist_popularity[a] for a in artist_names[:15]]
        })
        st.dataframe(artist_df.set_index('Artist'), use_container_width=True)
    
    with col2:
        st.subheader("🎭 Top Genres")
        genre_df = pd.DataFrame(
            list(top_genres.items()),
            columns=['Genre', 'Count']
        ).sort_values('Count', ascending=True)
        st.bar_chart(genre_df.set_index('Genre'))
    
    st.divider()
    
    # ============================================================================
    # TF-IDF ANALYSIS
    # ============================================================================
    st.header("🚨 Part 2: TF-IDF Analysis (Guilty Pleasures)")
    
    genre_text = ' '.join(all_genres)
    
    # Baseline corpus
    baseline_corpus = [
        'pop pop pop pop pop synth-pop synth-pop dance-pop',
        'hip hop hip hop r&b trap',
        'rock rock pop rock alternative rock',
    ]
    
    user_corpus = [genre_text]
    
    vectorizer = TfidfVectorizer(max_features=20)
    all_texts = baseline_corpus + user_corpus
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    user_tfidf = tfidf_matrix[-1].toarray()[0]
    
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = dict(zip(feature_names, user_tfidf))
    high_tfidf_genres = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    
    mainstream_genres = set(baseline_corpus[0].split() + baseline_corpus[1].split())
    mainstream_count = len(set(genre_counts.keys()) & mainstream_genres)
    mainstream_pct = (mainstream_count / len(genre_counts)) * 100 if len(genre_counts) > 0 else 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Guilty Pleasures (High TF-IDF)")
        guilty_df = pd.DataFrame(high_tfidf_genres, columns=['Genre', 'TF-IDF Score'])
        st.dataframe(guilty_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("📈 Taste Metrics")
        metrics = {
            "Mainstream Dependency": f"{mainstream_pct:.1f}%",
            "Niche/Alternative": f"{100-mainstream_pct:.1f}%",
            "Unique Genres": len(genre_counts),
            "Total Artists": len(artist_names)
        }
        for metric, value in metrics.items():
            st.metric(metric, value)
    
    st.divider()
    
    # ============================================================================
    # ROAST GENERATION
    # ============================================================================
    st.header("🎤 Part 3: Snarky Roast Generation")
    
    if st.button("🚀 Generate Roast!", key="roast_button"):
        top_5_artists = ', '.join(artist_names[:5])
        top_5_genres = ', '.join([g[0] for g in list(top_genres.items())[:5]])
        guilty_pleasures = ', '.join([g[0] for g in high_tfidf_genres[:3]])
        
        roast_prompt = f"""You are a funny friend who playfully roasts people's music taste. 
Your roasts are witty, self-aware, and make people laugh at themselves while feeling understood.

Their listening profile:
- Top Artists: {top_5_artists}
- Primary Genres: {top_5_genres}
- Guilty Pleasures: {guilty_pleasures}
- Mainstream Dependency: {mainstream_pct:.1f}%

Write a PUNCHY 3-4 sentence roast that:
1. References their actual taste patterns
2. Is playfully teasing (funny, not harsh)
3. Has self-aware humor (makes them laugh at themselves)
4. Is shareable on social media
5. Makes clever observations about their music personality

Keep it punchy and memorable - 3-4 sentences max.

Start the roast:"""
        
        try:
            with st.spinner("🎤 Generating roast from LMStudio..."):
                response = requests.post(
                    lmstudio_url,
                    json={
                        "model": "local-model",
                        "messages": [{"role": "user", "content": roast_prompt}],
                        "temperature": 0.7,
                        "max_tokens": 300
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    roast_text = response.json()['choices'][0]['message']['content']
                    st.markdown(f"<div class='roast-container'>{roast_text}</div>", unsafe_allow_html=True)
                    
                    # Copy button
                    st.text_area("📋 Copy the roast:", value=roast_text, height=120)
                else:
                    st.error(f"❌ LMStudio error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to LMStudio. Make sure it's running!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # ============================================================================
    # VISUALIZATION DASHBOARD
    # ============================================================================
    st.header("📊 Part 4: Visualization Dashboard")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"🎵 Spotify Taste Dashboard - {username}", fontsize=16, fontweight='bold')
    
    # 1. Genre Distribution
    ax1 = axes[0, 0]
    top_10_genres = dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    ax1.barh(list(top_10_genres.keys()), list(top_10_genres.values()), color='#1DB954')
    ax1.set_xlabel('Occurrences')
    ax1.set_title('Top 10 Genres')
    ax1.invert_yaxis()
    
    # 2. Artist Popularity
    ax2 = axes[0, 1]
    top_artists_pop = dict(sorted(artist_popularity.items(), key=lambda x: x[1], reverse=True)[:10])
    ax2.bar(range(len(top_artists_pop)), list(top_artists_pop.values()), color='#1DB954')
    ax2.set_xticks(range(len(top_artists_pop)))
    ax2.set_xticklabels(list(top_artists_pop.keys()), rotation=45, ha='right', fontsize=9)
    ax2.set_ylabel('Popularity Score')
    ax2.set_title('Top 10 Artists - Popularity')
    ax2.set_ylim(75, 100)
    
    # 3. Taste Profile Pie Chart
    ax3 = axes[1, 0]
    taste_labels = ['Pop', 'Hip Hop', 'Alternative/Indie', 'Rock', 'Other']
    taste_values = [
        len([g for g in all_genres if 'pop' in g.lower()]),
        len([g for g in all_genres if 'hip hop' in g.lower() or 'trap' in g.lower()]),
        len([g for g in all_genres if 'indie' in g.lower() or 'alt' in g.lower()]),
        len([g for g in all_genres if 'rock' in g.lower()]),
        len(all_genres) - sum([
            len([g for g in all_genres if 'pop' in g.lower()]),
            len([g for g in all_genres if 'hip hop' in g.lower() or 'trap' in g.lower()]),
            len([g for g in all_genres if 'indie' in g.lower() or 'alt' in g.lower()]),
            len([g for g in all_genres if 'rock' in g.lower()])
        ])
    ]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    ax3.pie([v for v in taste_values if v > 0], 
            labels=[l for l, v in zip(taste_labels, taste_values) if v > 0],
            autopct='%1.1f%%', colors=colors[:len([v for v in taste_values if v > 0])], 
            startangle=90)
    ax3.set_title('Taste Profile Breakdown')
    
    # 4. Scorecard
    ax4 = axes[1, 1]
    ax4.axis('off')
    scorecard_text = "📊 TASTE SCORECARD\n\n"
    
    metrics_dict = {
        "Pop Dependency": mainstream_pct,
        "Alternative Niche": 100 - mainstream_pct,
        "Genre Diversity": min(len(genre_counts) / 20 * 100, 100),
    }
    
    for metric, score in metrics_dict.items():
        bar_length = int(score / 5)
        bar = '█' * bar_length + '░' * (20 - bar_length)
        scorecard_text += f"{metric:<20}\n{bar} {score:.1f}%\n\n"
    
    ax4.text(0.1, 0.9, scorecard_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='#1DB954', alpha=0.2))
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Download dashboard
    buf = plt.savefig('spotify_roast_dashboard.png', dpi=150, bbox_inches='tight')
    with open('spotify_roast_dashboard.png', 'rb') as f:
        st.download_button(
            label="📥 Download Dashboard as PNG",
            data=f,
            file_name=f"spotify_roast_{username}_{datetime.now().strftime('%Y%m%d')}.png",
            mime="image/png"
        )

st.divider()
st.markdown("""
---
**🎵 Spotify Roast NLP Pipeline**
- 🔤 NER: Artist & Genre Extraction
- 📈 TF-IDF: Guilty Pleasure Detection  
- 🤖 LMStudio: Snarky Roast Generation
- 📊 Visualization: Beautiful Dashboard
""")
