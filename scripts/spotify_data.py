import csv
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from operator import index

# Set client id and client secret
client_id = 'xxx'
client_secret = 'xxx'

# Spotify authentication token
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


# Get playlist song features and artist info
def playlist_features(id, artist_id, playlist_id):
    
    # Create Spotify API client variables
    meta = sp.track(id)
    audio_features = sp.audio_features(id)
    artist_info = sp.artist(artist_id)
    playlist_info = sp.playlist(playlist_id)

    # Metadata
    name = meta['name']
    track_id = meta['id']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    artist_id = meta['album']['artists'][0]['id']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    # Main artist name, popularity, genre
    artist_pop = artist_info["popularity"]
    artist_genres = artist_info["genres"]

    # Track features
    acousticness = audio_features[0]['acousticness']
    danceability = audio_features[0]['danceability']
    energy = audio_features[0]['energy']
    instrumentalness = audio_features[0]['instrumentalness']
    liveness = audio_features[0]['liveness']
    loudness = audio_features[0]['loudness']
    speechiness = audio_features[0]['speechiness']
    tempo = audio_features[0]['tempo']
    valence = audio_features[0]['valence']
    key = audio_features[0]['key']
    mode = audio_features[0]['mode']
    time_signature = audio_features[0]['time_signature']
    
    # Basic playlist info
    playlist_name = playlist_info['name']

    return [name, track_id, album, artist, artist_id, release_date, length, popularity, 
            artist_pop, artist_genres, acousticness, danceability, 
            energy, instrumentalness, liveness, loudness, speechiness, 
            tempo, valence, key, mode, time_signature, playlist_name]


# Spotify Playlists Data Extraction
playlist_links = ['https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=3ddeaba6c1fb4aaf',
           'https://open.spotify.com/playlist/37i9dQZF1DX0kbJZpiYdZl?si=6adee497221b41b1',
           'https://open.spotify.com/playlist/37i9dQZF1DX4JAvHpjipBk?si=03e877de87e8476d',
           'https://open.spotify.com/playlist/37i9dQZF1DX11otjJ7crqp?si=1cc221e41e1d4a16',
           'https://open.spotify.com/playlist/37i9dQZF1DWT5MrZnPU1zD?si=77201ffcf60449a3',
           'https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd?si=24cb78119dd44fc0',
           'https://open.spotify.com/playlist/37i9dQZF1DXcRXFNfZr7Tp?si=a2a749e2802e4e1a',
           'https://open.spotify.com/playlist/37i9dQZF1DX2RxBh64BHjQ?si=9503cb431d684f7c']

track_ids = []
artist_ids = []
playlist_ids = []

for link in playlist_links:
    playlist_URI = link.split("/")[-1].split("?")[0]
    
    # Iterate over list of tracks in playlist
    for i in sp.playlist_tracks(playlist_URI)["items"]:   
        if i['track'] == None:
            continue          

        track_ids.append(i['track']["id"]) # Extract song id
        artist_ids.append(i['track']["artists"][0]["uri"]) # Extract artist id
        playlist_ids.append(playlist_URI)


# Loop over track ids
all_tracks = []
for i in range(len(track_ids)):
    time.sleep(.5)
    track_feat = playlist_features(track_ids[i], artist_ids[i], playlist_ids[i])
    all_tracks.append(track_feat)


# Create dataframe
spotify_playlists = pd.DataFrame(
    all_tracks, columns=['name', 'track_id', 'album', 'artist', 'artist_id','release_date',
                     'length', 'popularity', 'artist_pop', 'artist_genres',
                     'acousticness', 'danceability', 'energy',
                     'instrumentalness', 'liveness', 'loudness',
                     'speechiness', 'tempo', 'valence', 'key', 'mode',
                     'time_signature', 'playlist'])


# Save to csv file
spotify_playlists.to_csv("data/spotify_playlists.csv", sep=',')
spotify_playlists['playlist'].value_counts()



