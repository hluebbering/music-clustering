import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('scripts/playlists.csv',
                 encoding_errors='ignore', index_col=0, header=0)


# Get songs from a playlist
df2 = df.copy(deep=True)
df2 = df2.drop(df2[df2.playlist_name != 'but my feet in bottega'].index)

# Get songs from a playlist
df2 = df.copy(deep=True)
df2 = df2.drop(df2[df2.playlist_name != 'pardon me while I elevate'].index)


#df = df.drop(df[df.score < 50].index)


feature_cols = ['acousticness', 'danceability', 'duration_ms', 'energy',
                'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
                'speechiness', 'tempo', 'time_signature', 'valence',
                'track_name', 'artist_name', 'popularity']

dfSongs = df2[feature_cols]

# Number of rows and columns
rows, cols = dfSongs.shape
print(f'Number of songs: {rows}')
print(f'Number of attributes per song: {cols}')


# Get a Song str search
def getMusicName(elem):
    return f"{elem['artist_name']} - {elem['track_name']}"


# Select song and get track info
# anySong = dfSongs.loc[1]
# anySongName = getMusicName(anySong)
# print('name:', anySongName)


# K-query
def knnQuery(queryPoint, arrCharactPoints, k):

    # Copy of pandas.DataFrame indices and data
    tmp = arrCharactPoints.copy(deep=True)

    query_vals = queryPoint.tolist()
    dist_vals = []

    # Iterate through each row and select
    for index, row in tmp.iterrows():
        feature_vals = row.values.tolist()
        sum_diff_sqr = sum(
            abs(feature_vals[i] - query_vals[i]) ** 2 for i in range(len(query_vals)))

        euc_dist = sum_diff_sqr**0.5
        dist_vals.append(euc_dist)

    # tmp['dist'] = tmp.apply(lambda x: np.linalg.norm(x-queryPoint), axis=1)
    tmp['distance'] = dist_vals
    tmp = tmp.sort_values('distance')

    # return tmp.head(k).index
    return tmp.head(k).index, tmp.tail(k).index

# Execute k-NN removing the 'query point'
def querySimilars(df, columns, idx, func, param):
    arr = df[columns].copy(deep=True)
    queryPoint = arr.loc[idx]
    arr = arr.drop([idx])
    return func(queryPoint, arr, param)



# Selecting song attributes and  query parameters
columns = ['acousticness', 'danceability', 'energy',
           'instrumentalness', 'liveness', 'speechiness', 'valence']

func, param = knnQuery, 3


similar_songs = {}
nonsimilar_songs = {}

for song_index in df2.index:
    
    # Select query point and get song name 
    query_song = dfSongs.loc[song_index]
    query_song_name = getMusicName(query_song)

    # Querying
    response = querySimilars(dfSongs, columns, song_index, func, param)
    similar_ids = response[0]
    nonsimilar_ids = response[1]

    for idx in similar_ids:
        song_name = getMusicName(dfSongs.loc[idx])
        if song_name in similar_songs:
            similar_songs[song_name] += 1
        else:
            similar_songs[song_name] = 1

    for idx in nonsimilar_ids:
        song_name = getMusicName(dfSongs.loc[idx])
        if song_name in nonsimilar_songs:
            nonsimilar_songs[song_name] += 1
        else:
            nonsimilar_songs[song_name] = 1


nonsimilar_songs = dict(sorted(nonsimilar_songs.items(), key=lambda item: item[1], reverse=True))
print('\n', 'NON SIMILAR SONG COUNT')
for song, song_count in nonsimilar_songs.items():
    if song_count >= 15:
        print(song, ':', song_count)


similar_songs = dict(sorted(similar_songs.items(), key=lambda item: item[1], reverse=True))
print('\n', 'SIMILAR SONG COUNT')
for song, song_count in similar_songs.items():
    if song_count >= 6:
        print(song, ':', song_count)
    



# # Selecting song and attributes
# songIndex = 298  # query point, selected song 123
# response = querySimilars(dfSongs, columns, songIndex, func, param)
# responseSimilar = response[0]
# responseNonSimilar = response[1]

# # Select a song and get the song name
# anySongName = getMusicName(dfSongs.loc[songIndex])
# print('\n', '# Query Point:', songIndex, anySongName)

# print('\n', '# Similar songs')
# for idx in responseSimilar:
#     similar_song = getMusicName(dfSongs.loc[idx])
#     print(idx, similar_song)

# print('\n', '# Non-Similar songs')
# for idx in responseNonSimilar:
#     nonsimilar_song = getMusicName(dfSongs.loc[idx])
#     print(idx, nonsimilar_song)