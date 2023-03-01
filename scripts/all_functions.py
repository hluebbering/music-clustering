import csv
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from operator import index

# Set client id and client secret
# Spotify authentication token
# client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
# sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
sp = spotipy.Spotify()
# Read csv file into pandas dataframe
df = pd.read_csv(
 "scripts/data/my_playlist.csv", encoding_errors="ignore", index_col=0, header=0
)


# Get a song string search
def getMusicName(elem):
    return f"{elem['artist']} - {elem['name']}"


# K-nearest neighbors algorithm
def knnQuery(queryPoint, arrCharactPoints, k):
    queryVals = queryPoint.tolist()
    distVals = []

    # Copy of dataframe indices and data
    tmp = arrCharactPoints.copy(deep=True)
    for index, row in tmp.iterrows():
        feat = row.values.tolist()

        # Calculate sum of squared differences
        ssd = sum(abs(feat[i] - queryVals[i]) ** 2 for i in range(len(queryVals)))

        # Get euclidean distance
        distVals.append(ssd**0.5)

    tmp["distance"] = distVals
    tmp = tmp.sort_values("distance")

    # K closest and furthest points
    return tmp.head(k).index, tmp.tail(k).index


# Execute KNN removing the query point
def querySimilars(df, columns, idx, func, param):
    arr = df[columns].copy(deep=True)
    queryPoint = arr.loc[idx]
    arr = arr.drop([idx])
    return func(queryPoint, arr, param)
