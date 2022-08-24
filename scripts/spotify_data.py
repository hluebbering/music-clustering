import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

# Spotify Authentication - without user
client_credentials_manager = SpotifyClientCredentials(
    client_id='4cf3afdca2d74dc48af9999b1b7c9c61', client_secret='f6ca08ad37bb41a0afab5ca1dc74b208')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_link = "https://open.spotify.com/playlist/4lSykOrQfnAiCgtHKVudTT"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

# Track Ids and Artist Info
track_ids = [x1["track"]["id"]
             for x1 in sp.playlist_tracks(playlist_URI)["items"]]
artist_uris = [x2["track"]["artists"][0]["uri"]
               for x2 in sp.playlist_tracks(playlist_URI)["items"]]





def playlistTracks(id, artist_ids):
    meta = sp.track(id)
    features = sp.audio_features(id)
    artist_info = sp.artist(artist_ids)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    # Main artist name, popularity, genre
    artist_pop = artist_info["popularity"]
    artist_genres = artist_info["genres"]

    # Track features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']

    return [name, album, artist, release_date, length,
            popularity, artist_pop, artist_genres,
            acousticness, danceability, energy,
            instrumentalness, liveness, loudness,
            speechiness, tempo, time_signature]


# loop over track ids
tracks = []
for i in range(len(track_ids)):
    time.sleep(.5)
    track = playlistTracks(track_ids[i], artist_uris[i])
    tracks.append(track)

# create dataset
df = pd.DataFrame(
    tracks, columns=['name', 'album', 'artist', 'release_date',
                     'length', 'popularity', 'artist_pop', 'artist_genres',
                     'acousticness', 'danceability', 'energy',
                     'instrumentalness', 'liveness', 'loudness',
                     'speechiness', 'tempo', 'time_signature'])
df.to_csv("spotify.csv", sep=',')
