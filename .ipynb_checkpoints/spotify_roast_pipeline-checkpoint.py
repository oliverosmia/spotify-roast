# Spotify Roast - NLP Pipeline
# Run this in Jupyter Lab in your NLP environment
# Make sure LMStudio is running on http://127.0.0.1:1234

import json
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================================
# PART 1: LOAD SPOTIFY DATA
# ============================================================================
print("=" * 80)
print("SPOTIFY ROAST NLP PIPELINE")
print("=" * 80)

# Load sample Spotify data
with open('sample_spotify_data.json', 'r') as f:
    spotify_data = json.load(f)

username = spotify_data['username']
print(f"\n👤 User: {username}")
print(f"📊 Top Artists: {len(spotify_data['topArtists'])}")
print(f"🎵 Top Tracks: {len(spotify_data['topTracks'])}")
print(f"🎸 Genres: {len(spotify_data['topGenres'])}")

# ============================================================================
# PART 2: NAMED ENTITY RECOGNITION (NER) - Extract Artist Names & Genres
# ============================================================================
print("\n" + "=" * 80)
print("PART 1: NAMED ENTITY RECOGNITION (NER)")
print("=" * 80)

# Extract artist names
artist_names = [artist['name'] for artist in spotify_data['topArtists']]
artist_popularity = {artist['name']: artist['popularity'] for artist in spotify_data['topArtists']}

# Extract and flatten genres
all_genres = []
for artist in spotify_data['topArtists']:
    all_genres.extend(artist.get('genres', []))

genre_counts = Counter(all_genres)
top_genres = dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:15])

print(f"\n✨ Top 15 Artists:")
for i, artist in enumerate(artist_names[:15], 1):
    print(f"  {i}. {artist} (popularity: {artist_popularity[artist]})")

print(f"\n🎭 Top Genres Extracted:")
for genre, count in list(top_genres.items())[:10]:
    print(f"  • {genre}: {count} occurrences")

# ============================================================================
# PART 3: TF-IDF ANALYSIS - Find Guilty Pleasures & Niche Tastes
# ============================================================================
print("\n" + "=" * 80)
print("PART 2: TF-IDF ANALYSIS (Guilty Pleasures Detection)")
print("=" * 80)

# Create genre frequency vector for this user
genre_text = ' '.join(all_genres)

# Baseline "popular music" corpus (what mainstream listeners like)
baseline_corpus = [
    'pop pop pop pop pop synth-pop synth-pop dance-pop',  # Baseline: lots of pop
    'hip hop hip hop r&b trap',  # Baseline: mainstream hip hop
    'rock rock pop rock alternative rock',  # Baseline: mainstream rock
]

# Add user's genre profile
user_corpus = [genre_text]

# TF-IDF to find what's unusual about their taste
vectorizer = TfidfVectorizer(max_features=20)
all_texts = baseline_corpus + user_corpus
tfidf_matrix = vectorizer.fit_transform(all_texts)
user_tfidf = tfidf_matrix[-1].toarray()[0]

# Get feature names and their TF-IDF scores
feature_names = vectorizer.get_feature_names_out()
tfidf_scores = dict(zip(feature_names, user_tfidf))
high_tfidf_genres = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:5]

print(f"\n🚨 Guilty Pleasures (High TF-IDF = Unusual taste):")
for genre, score in high_tfidf_genres:
    print(f"  • {genre}: {score:.3f} (niche factor)")

mainstream_genres = set(baseline_corpus[0].split() + baseline_corpus[1].split())
niche_genres = set(genre for genre, _ in high_tfidf_genres)

# Count intersection properly
mainstream_count = len(set(genre_counts.keys()) & mainstream_genres)
niche_count = len(niche_genres)

print(f"\n📊 Taste Profile:")
print(f"  Mainstream genres: {mainstream_count}")
print(f"  Niche/Alternative: {niche_count}")
mainstream_pct = (mainstream_count / len(genre_counts)) * 100
print(f"  Mainstream dependency: {mainstream_pct:.1f}%")

# ============================================================================
# PART 4: BUILD ROAST PROMPT & SEND TO LMSTUDIO
# ============================================================================
print("\n" + "=" * 80)
print("PART 3: GENERATING SNARKY ROAST via LMStudio")
print("=" * 80)

# Build context for LMStudio
top_5_artists = ', '.join(artist_names[:5])
top_5_genres = ', '.join([g[0] for g in list(top_genres.items())[:5]])
guilty_pleasures = ', '.join([g[0] for g in high_tfidf_genres[:3]])

roast_prompt = f"""You are a snarky music critic with a sharp, witty sense of humor. 
Your job is to roast someone's Spotify taste in an entertaining, funny way (not mean-spirited).

Here's their listening profile:
- Top Artists: {top_5_artists}
- Primary Genres: {top_5_genres}
- Guilty Pleasure Genres: {guilty_pleasures}
- Mainstream Dependency: {mainstream_pct:.1f}%
- Total Unique Tracks: {len(spotify_data['topTracks'])}

Write a 3-4 sentence roast that is:
1. Funny and snarky (like a music journalist)
2. References their actual listening habits
3. Self-aware and not mean-spirited
4. Ends with one witty observation

Start the roast now:"""

print(f"\n🎤 Sending roast prompt to LMStudio...")
print(f"   Target: http://127.0.0.1:1234/v1/chat/completions")

# Call LMStudio API
try:
    response = requests.post(
        "http://192.168.86.3:1234/v1/chat/completions",
        json={
            "model": "local-model",  # LMStudio accepts any model name
            "messages": [
                {
                    "role": "user",
                    "content": roast_prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 300
        },
        timeout=30
    )
    
    if response.status_code == 200:
        roast_text = response.json()['choices'][0]['message']['content']
        print(f"\n✅ ROAST GENERATED!")
        print(f"\n" + "=" * 80)
        print("🎵 YOUR SPOTIFY ROAST 🎵")
        print("=" * 80)
        print(f"\n{roast_text}\n")
    else:
        print(f"❌ LMStudio error: {response.status_code}")
        print(f"   Response: {response.text}")
        roast_text = "LMStudio offline - using fallback roast..."
        
except requests.exceptions.ConnectionError:
    print(f"❌ Cannot connect to LMStudio at http://127.0.0.1:1234")
    print(f"   Make sure LMStudio Local Server is running!")
    roast_text = "LMStudio connection failed"
except Exception as e:
    print(f"❌ Error: {str(e)}")
    roast_text = f"Error generating roast: {str(e)}"

# ============================================================================
# PART 5: VISUALIZATION - SCORECARD BREAKDOWN
# ============================================================================
print("\n" + "=" * 80)
print("PART 4: VISUALIZATION & SCORECARD")
print("=" * 80)

# Create scorecard metrics
metrics = {
    "Pop Dependency": mainstream_pct,
    "Alternative Niche": 100 - mainstream_pct,
    "Genre Diversity": min(len(top_genres) / 20 * 100, 100),
    "Indie/Alt Taste": (len([g for g in all_genres if 'indie' in g or 'alt' in g]) / len(all_genres) * 100),
    "Hip Hop Affinity": (len([g for g in all_genres if 'hip hop' in g]) / len(all_genres) * 100),
}

print(f"\n📊 SPOTIFY ROAST SCORECARD:")
print(f"\n{'Metric':<25} {'Score':>10} {'Status':>15}")
print("-" * 50)
for metric, score in metrics.items():
    status = "🔴 High" if score > 70 else "🟡 Medium" if score > 40 else "🟢 Low"
    print(f"{metric:<25} {score:>9.1f}% {status:>15}")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(f"🎵 Spotify Roast Dashboard - {username}", fontsize=16, fontweight='bold')

# 1. Genre Distribution (Top 10)
ax1 = axes[0, 0]
top_10_genres = dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:10])
ax1.barh(list(top_10_genres.keys()), list(top_10_genres.values()), color='#1DB954')
ax1.set_xlabel('Occurrences')
ax1.set_title('Top 10 Genres in Your Library')
ax1.invert_yaxis()

# 2. Artist Popularity
ax2 = axes[0, 1]
top_artists_pop = dict(sorted(artist_popularity.items(), key=lambda x: x[1], reverse=True)[:10])
ax2.bar(range(len(top_artists_pop)), list(top_artists_pop.values()), color='#1DB954')
ax2.set_xticks(range(len(top_artists_pop)))
ax2.set_xticklabels(list(top_artists_pop.keys()), rotation=45, ha='right')
ax2.set_ylabel('Popularity Score')
ax2.set_title('Top 10 Artists - Popularity')
ax2.set_ylim(75, 100)

# 3. Taste Profile Pie Chart
ax3 = axes[1, 0]
taste_labels = ['Mainstream\nPop', 'Hip Hop', 'Alternative/Indie', 'Rock', 'Other']
taste_values = [
    len([g for g in all_genres if 'pop' in g]),
    len([g for g in all_genres if 'hip hop' in g or 'trap' in g]),
    len([g for g in all_genres if 'indie' in g or 'alt' in g]),
    len([g for g in all_genres if 'rock' in g]),
    len(all_genres) - sum([
        len([g for g in all_genres if 'pop' in g]),
        len([g for g in all_genres if 'hip hop' in g or 'trap' in g]),
        len([g for g in all_genres if 'indie' in g or 'alt' in g]),
        len([g for g in all_genres if 'rock' in g])
    ])
]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
ax3.pie(taste_values, labels=taste_labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax3.set_title('Your Taste Profile Breakdown')

# 4. Scorecard
ax4 = axes[1, 1]
ax4.axis('off')
scorecard_text = "📊 ROAST SCORECARD\n\n"
for metric, score in metrics.items():
    bar_length = int(score / 5)
    bar = '█' * bar_length + '░' * (20 - bar_length)
    scorecard_text += f"{metric:<20}\n{bar} {score:.1f}%\n\n"

ax4.text(0.1, 0.9, scorecard_text, transform=ax4.transAxes, fontsize=10,
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('spotify_roast_dashboard.png', dpi=150, bbox_inches='tight')
print(f"\n✅ Dashboard saved as 'spotify_roast_dashboard.png'")
plt.show()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("✨ PIPELINE COMPLETE ✨")
print("=" * 80)
print(f"\n✅ Files generated:")
print(f"   • spotify_roast_dashboard.png (visualization)")
print(f"\n🎤 Ready to demo on Thursday!")
print(f"\nTo use your real Spotify data:")
print(f"   1. Download your Spotify JSON")
print(f"   2. Replace 'sample_spotify_data.json' with your file")
print(f"   3. Run this script again")
print(f"\n" + "=" * 80)
