import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

st.title("Spotify Data Export")

# Your credentials here (you'll add them)
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "https://YOUR_USERNAME-spotify-roast.streamlit.app/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-top-read user-read-recently-played"
))

if st.button("Fetch My Spotify Data"):
    # Fetch data
    st.write("Data fetched!")