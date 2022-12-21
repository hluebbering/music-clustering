import csv
from operator import index
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

# Set client id and client secret
client_id = '4cf3afdca2d74dc48af9999b1b7c9c61'
client_secret = 'f6ca08ad37bb41a0afab5ca1dc74b208'

# Spotify authentication
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)




# Get playlist song features and artist info
def playlistTracks(id, artist_ids):
    meta = sp.track(id)
    features = sp.audio_features(id)
    artist_info = sp.artist(artist_ids)

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
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    valence = features[0]['valence']
    key = features[0]['key']
    mode = features[0]['mode']
    time_signature = features[0]['time_signature']

    return [name, track_id, album, artist, artist_id, release_date, length, popularity, 
            artist_pop, artist_genres, acousticness, danceability, 
            energy, instrumentalness, liveness, loudness, speechiness, 
            tempo, valence, key, mode, time_signature]
            



# Spotify playlist url
playlist_link = "https://open.spotify.com/playlist/4lSykOrQfnAiCgtHKVudTT"
playlist_link = "https://open.spotify.com/playlist/1nvpVNmzL7Vi1pXcQEiaLx?si=a62187de23924f4c"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

# Extract song ids and artists from playlist
track_ids = [x1["track"]["id"]
             for x1 in sp.playlist_tracks(playlist_URI)["items"]]
artist_uris = [x2["track"]["artists"][0]["uri"]
               for x2 in sp.playlist_tracks(playlist_URI)["items"]]


# Loop over track ids
tracks = []
for i in range(len(track_ids)):
    time.sleep(.5)
    track = playlistTracks(track_ids[i], artist_uris[i])
    tracks.append(track)
    
    
# Save the playlist name for each song
playlist_name = sp.user_playlist(user = None, playlist_id = playlist_URI, fields="name")
for x in tracks:
    x.append(playlist_name['name'])
    
    
# Create dataframe
df = pd.DataFrame(
    tracks, columns=['name', 'track_id', 'album', 'artist', 'artist_id','release_date',
                     'length', 'popularity', 'artist_pop', 'artist_genres',
                     'acousticness', 'danceability', 'energy',
                     'instrumentalness', 'liveness', 'loudness',
                     'speechiness', 'tempo', 'valence', 'key', 'mode',
                     'time_signature', 'playlist'])
# Save to csv file
df.to_csv("spotify.csv", sep=',')


