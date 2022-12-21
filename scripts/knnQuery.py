import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Get songs from a playlist
df = pd.read_csv('playlists.csv', encoding_errors='ignore', index_col=0, header=0)
dfCopy = df.copy(deep = True)
dfCopy = dfCopy.drop(dfCopy[dfCopy.playlist != 'but my feet in bottega'].index)


# Number of rows and columns
rows, cols = dfCopy.shape
print(f'Number of songs: {rows}')
print(f'Number of attributes per song: {cols}')

# Get a song string search
def getMusicName(elem):
    return f"{elem['artist']} - {elem['name']}"

# Select song and get track info
anySong = dfCopy.loc[15]
anySongName = getMusicName(anySong)
print('name:', anySongName)




# k-Nearest Neighbors (KNN)
def knnQuery(queryPoint, arrCharactPoints, k):
    queryVals = queryPoint.tolist()
    distVals = []
    
    # Copy of dataframe indices and data
    tmp = arrCharactPoints.copy(deep = True)  
    for index, row in tmp.iterrows():
        feat = row.values.tolist()
        
        # Calculate sum of squared differences
        ssd = sum(abs(feat[i] - queryVals[i]) ** 2 for i in range(len(queryVals)))
        
        # Get euclidean distance
        distVals.append(ssd ** 0.5)
        
    tmp['distance'] = distVals
    tmp = tmp.sort_values('distance')
    
    # K closest and furthest points
    return tmp.head(k).index, tmp.tail(k).index


# Execute KNN removing the query point
def querySimilars(df, columns, idx, func, param):
    arr = df[columns].copy(deep = True)
    queryPoint = arr.loc[idx]
    arr = arr.drop([idx])
    return func(queryPoint, arr, param)




######### EXAMPLE 1. KNN Query #########

# Select song and column attributes
songIndex = 6 # query point
columns = ['acousticness', 'danceability', 'energy', 'speechiness', 'valence','tempo']

# Set query parameters
func, param = knnQuery, 3

# Implement query
response = querySimilars(df, columns, songIndex, func, param)

print("---- Query Point ----")
print(getMusicName(df.loc[songIndex]))
print('---- k = 3 similar songs ----')
for track_id in response[0]:
    track_name = getMusicName(df.loc[track_id])
    print(track_name)
print('---- k = 3 nonsimilar songs ----')
for track_id in response[1]:
    track_name = getMusicName(df.loc[track_id])
    print(track_name)
    
##########################################




similar = {} # Similar songs count
nonsimilar = {} # Non-similar songs count

for trackID in df.index:
    response = querySimilars(df, columns, trackID, func, param)

    # Get similar song ids and info
    for similarID in response[0]:
        track = getMusicName(df.loc[similarID])
        if track in similar:
            similar[track] += 1
        else:
            similar[track] = 1

    # Get non-similar song ids and info
    for nonsimilarID in response[1]:
        track = getMusicName(df.loc[nonsimilarID])
        if track in nonsimilar:
            nonsimilar[track] += 1
        else:
            nonsimilar[track] = 1



# Nonsimilar tracks from given playlist
nonsimilar = dict(sorted(nonsimilar.items(), key=lambda item: item[1], reverse=True))
print('---- NON SIMILAR SONG COUNTS ----')
for song, songCount in nonsimilar.items():
    if songCount >= 8:
        print(song, ':', songCount)

# Similar tracks from given playlist
similar = dict(sorted(similar.items(), key=lambda item: item[1], reverse=True))
print('---- SIMILAR SONG COUNTS ----')
for song, song_count in similar.items():
    if song_count >= 8:
        print(song, ':', song_count)
        
