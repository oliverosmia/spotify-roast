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

st.write("Click below to authenticate with Spotify and download your listening data.")

try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-top-read user-read-recently-played"
    ))
    
    if st.button("🔐 Authenticate & Fetch My Data"):
        with st.spinner("Fetching your Spotify data..."):
            # Get current user
            user = sp.current_user()
            
            # Get top artists
            top_artists_data = sp.current_user_top_artists(limit=50, time_range='all_time')
            
            # Get top tracks
            top_tracks = sp.current_user_top_tracks(limit=50, time_range='all_time')
            
            # Get recently played
            recently_played = sp.current_user_recently_played(limit=50)
            
            # Extract genres
            genres = {}
            for artist in top_artists_data['items']:
                for genre in artist.get('genres', []):
                    genres[genre] = genres.get(genre, 0) + 1
            
            # Package data
            spotify_data = {
                "username": user.get('display_name', 'Unknown'),
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
                        "popularity": track['popularity']
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
            
            st.success("✅ Data fetched!")
            
            # Download
            json_str = json.dumps(spotify_data, indent=2)
            st.download_button(
                label="📥 Download as JSON",
                data=json_str,
                file_name=f"spotify_data.json",
                mime="application/json"
            )

except Exception as e:
    st.error(f"❌ Error: {str(e)}")