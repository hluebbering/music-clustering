import csv
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from operator import index


# Get songs from a playlist
df = pd.read_csv('data/my_playlist.csv', encoding_errors='ignore', index_col=0, header=0)
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
print('name:', getMusicName(anySong))


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
query_point = 6 # query_point
columns = ['acousticness', 'danceability', 'energy', 'speechiness', 'valence','tempo']

# Set query parameters
func, param = knnQuery, 3

# Implement query
response = querySimilars(df, columns, query_point, func, param)

print("---- Query Point ----")
print(getMusicName(df.loc[query_point]))

print('---- k = 3 similar songs ----')
for track_index in response[0]:
    track_name = getMusicName(df.loc[track_index])
    print(track_name)

print('---- k = 3 nonsimilar songs ----')
for track_index in response[1]:
    track_name = getMusicName(df.loc[track_index])
    print(track_name)
    
    

##########################################

similar_count = {} # Similar songs count
nonsimilar_count = {} # Non-similar songs count

for track_index in df.index:
    response = querySimilars(df, columns, track_index, func, param)
    
    # Get similar songs
    for similar_index in response[0]:
        track = getMusicName(df.loc[similar_index])
        if track in similar_count:
            similar_count[track] += 1
        else:
            similar_count[track] = 1
    # Get non-similar songs
    for nonsimilar_index in response[1]:
        track = getMusicName(df.loc[nonsimilar_index])
        if track in nonsimilar_count:
            nonsimilar_count[track] += 1
        else:
            nonsimilar_count[track] = 1


# Nonsimilar tracks from given playlist
nonsimilar = dict(sorted(nonsimilar_count.items(), key=lambda item: item[1], reverse=True))
print('---- NON SIMILAR SONG COUNTS ----')
for track_name, track_count in nonsimilar.items():
    if track_count >= 8:
        print(track_name, ':', track_count)


# Similar tracks from given playlist
similar = dict(sorted(similar_count.items(), key=lambda item: item[1], reverse=True))
print('---- SIMILAR SONG COUNTS ----')
for track_name, track_count in similar.items():
    if track_count >= 5:
        print(track_name, ':', track_count)
        
