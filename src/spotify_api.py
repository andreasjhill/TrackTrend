import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
#change this whenever you want to change the playlist used
from .config import GLOBAL_TOP_50_PLAYLIST_ID

load_dotenv()

# Set up Spotify API client
#Use Client Credentials
def get_spotify_client():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_top_50_tracks(sp):
    playlist_id = GLOBAL_TOP_50_PLAYLIST_ID  # playlist ID
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    top_tracks = []
    for track in tracks:
        track_info = track['track']
        audio_features = sp.audio_features(track_info['id'])[0]
        
        track_data = {
            'id': track_info['id'],
            'name': track_info['name'],
            'artist': track_info['artists'][0]['name'],
            'popularity': track_info['popularity'],
            'danceability': audio_features['danceability'],
            'energy': audio_features['energy'],
            'key': audio_features['key'],
            'loudness': audio_features['loudness'],
            'mode': audio_features['mode'],
            'speechiness': audio_features['speechiness'],
            'acousticness': audio_features['acousticness'],
            'instrumentalness': audio_features['instrumentalness'],
            'liveness': audio_features['liveness'],
            'valence': audio_features['valence'],
            'tempo': audio_features['tempo'],
            'duration_ms': audio_features['duration_ms'],
            'time_signature': audio_features['time_signature']
        }
        top_tracks.append(track_data)
    
    return top_tracks