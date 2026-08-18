import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from datetime import datetime

st.set_page_config(page_title="Spotify Roast - Data Export", layout="wide")

st.title("🎵 Spotify Roast - Data Export")

# Get secrets from Streamlit Cloud
client_id = st.secrets["SPOTIFY_CLIENT_ID"]
client_secret = st.secrets["SPOTIFY_CLIENT_SECRET"]
redirect_uri = "https://spotify-roast.streamlit.app/callback"

# Streamlit caching for Spotify client
@st.cache_resource
def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-top-read user-read-recently-played"
    ))

st.write("Click below to authenticate with Spotify and download your listening data.")

try:
    sp = get_spotify_client()
    
    if st.button("🔐 Authenticate & Fetch My Data"):
        with st.spinner("Fetching your Spotify data..."):
            # Get current user
            user = sp.current_user()
            
            # Get top artists
            top_artists = sp.current_user_top_tracks(limit=50, time_range='all_time')
            
            # Get top tracks
            top_tracks = sp.current_user_top_tracks(limit=50, time_range='all_time')
            
            # Get recently played
            recently_played = sp.current_user_recently_played(limit=50)
            
            # Extract genres from top artists
            top_artists_data = sp.current_user_top_artists(limit=50, time_range='all_time')
            genres = {}
            for artist in top_artists_data['items']:
                for genre in artist.get('genres', []):
                    genres[genre] = genres.get(genre, 0) + 1
            
            # Package data
            spotify_data = {
                "username": user.get('display_name', 'Unknown'),
                "email": user.get('email', 'Unknown'),
                "export_date": datetime.now().isoformat(),
                "topArtists": [
                    {
                        "name": artist['name'],
                        "popularity": artist['popularity'],
                        "genres": artist.get('genres', [])
                    }
                    for artist in top_artists_data['items']
                ],
                "topTracks": [
                    {
                        "name": track['name'],
                        "artist": track['artists'][0]['name'] if track['artists'] else "Unknown",
                        "popularity": track['popularity'],
                        "duration_ms": track['duration_ms']
                    }
                    for track in top_tracks['items']
                ],
                "topGenres": sorted(genres.items(), key=lambda x: x[1], reverse=True),
                "recentlyPlayed": [
                    {
                        "name": item['track']['name'],
                        "artist": item['track']['artists'][0]['name'] if item['track']['artists'] else "Unknown",
                        "played_at": item['played_at']
                    }
                    for item in recently_played['items']
                ]
            }
            
            # Display success
            st.success("✅ Data fetched successfully!")
            
            # Show summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Top Artists", len(spotify_data['topArtists']))
            with col2:
                st.metric("Top Tracks", len(spotify_data['topTracks']))
            with col3:
                st.metric("Unique Genres", len(spotify_data['topGenres']))
            
            # Download as JSON
            json_str = json.dumps(spotify_data, indent=2)
            st.download_button(
                label="📥 Download as JSON",
                data=json_str,
                file_name=f"spotify_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
            # Preview
            st.subheader("📊 Data Preview")
            st.json(spotify_data)

except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.info("Make sure your redirect URI is set correctly in Spotify Developer Dashboard")