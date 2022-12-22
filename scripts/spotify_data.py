import csv
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from operator import index

# Set client id and client secret
client_id = '4cf3afdca2d74dc48af9999b1b7c9c61'
client_secret = 'f6ca08ad37bb41a0afab5ca1dc74b208'

# Spotify authentication token
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


# Get playlist song features and artist info
def playlistTracks(id, artist_id, playlist_id):
    
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
# List of Spotify owned playlists
plLinks = ['https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=3ddeaba6c1fb4aaf',
           'https://open.spotify.com/playlist/37i9dQZF1DX0kbJZpiYdZl?si=6adee497221b41b1',
           'https://open.spotify.com/playlist/37i9dQZF1DX4JAvHpjipBk?si=03e877de87e8476d',
           'https://open.spotify.com/playlist/37i9dQZF1DX11otjJ7crqp?si=1cc221e41e1d4a16',
           'https://open.spotify.com/playlist/37i9dQZF1DWT5MrZnPU1zD?si=77201ffcf60449a3',
           'https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd?si=24cb78119dd44fc0',
           'https://open.spotify.com/playlist/37i9dQZF1DXcRXFNfZr7Tp?si=a2a749e2802e4e1a',
           'https://open.spotify.com/playlist/37i9dQZF1DX2RxBh64BHjQ?si=9503cb431d684f7c']

playlist_ids = []
track_ids = []
artist_ids = []

for link in plLinks:
    uri = link.split("/")[-1].split("?")[0]  
    
    for x1 in sp.playlist_tracks(uri)["items"]:   
        song = x1['track'] 
        
        if song == None:
            continue     
        
        track_ids.append(song["id"])
        artist_ids.append(song["artists"][0]["uri"])
        playlist_ids.append(uri)
        
# Loop over track ids
all_tracks = []
for i in range(len(track_ids2)):
    time.sleep(.5)
    get_features = playlistTracks(track_ids[i], artist_ids[i], playlist_ids[i])
    all_tracks.append(get_features)
    
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



