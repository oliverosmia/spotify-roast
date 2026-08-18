import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

st.title("Spotify Data Export")

# Your credentials here (you'll add them)
client_id = "a00d8eb147664c60a313beb2a47d759c"
client_secret = "cd1dc9fdbbd542d29f2d78da5a6a12b2"
redirect_uri = "https://spotify-roast.streamlit.app/"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-top-read user-read-recently-played"
))

if st.button("Fetch My Spotify Data"):
    # Fetch data
    st.write("Data fetched!")