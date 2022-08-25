import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('scripts/playlists.csv',
                 encoding_errors='ignore', index_col=0, header=0)

feature_cols = ['acousticness', 'danceability', 'duration_ms', 'energy',
                'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
                'speechiness', 'tempo', 'time_signature', 'valence',
                'track_name', 'artist_name', 'popularity']

dfSongs = df[feature_cols]

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

    return tmp.head(k).index

# Execute k-NN removing the 'query point'


def querySimilars(df, columns, idx, func, param):
    arr = df[columns].copy(deep=True)
    queryPoint = arr.loc[idx]
    arr = arr.drop([idx])
    return func(queryPoint, arr, param)


# Selecting song and attributes
songIndex = 193  # query point, selected song
columns = ['acousticness', 'danceability', 'energy',
           'instrumentalness', 'liveness', 'speechiness', 'valence']

# Selecting query parameters
func, param = knnQuery, 3  # k=3

# Querying
response = querySimilars(dfSongs, columns, songIndex, func, param)

# Select a song
anySong = dfSongs.loc[songIndex]
# Get the song name
anySongName = getMusicName(anySong)

# Print
print('# Query Point')
print(songIndex, anySongName)

print('# Similar songs')
for idx in response:
    anySong = dfSongs.loc[idx]
    anySongName = getMusicName(anySong)

    print(idx, anySongName)


#######################################
#######################################
#######################################
#######################################
#######################################
#######################################

name_matrix = dfSongs
X = dfSongs[['danceability', 'energy',
             'key', 'loudness', 'mode', 'speechiness', 'acousticness',
             'instrumentalness', 'liveness', 'valence', 'tempo',
             'time_signature']].copy()
X = np.matrix(X)


def normalize_values(X, use_sigma=True):
    """
    Normalizes the values of X. Can either normalize
    by dividing each feature vector by its respective standard 
    deviation or by the max value in the respective vector.
    Parameters:        
        X: a numpy matrix with dataset of interest
        use_sigma: whether to normalize using sigma
        (True) or by the largest number in the feature 
        vector (False)
    Returns:
        X_normalized: X values normalized based off the 
        decided setting
    """
    m, features = X.shape
    mu = sum(X) / m
    if use_sigma:
        divisor = np.sqrt(sum(np.square(X - mu)) / m)
    else:
        divisor = np.max(X, axis=0)

    # X_normalized
    return np.divide((X-mu), divisor)


X2 = normalize_values(X, use_sigma=False)


def initialize_centroids(X, k):
    """
    Used to select a starting point for centroids. Algorithm
    selects k data points from X and returns the centroid values 
    and location in the index
    paramaters:
        X: a numpy matrix with the dataset of interest
        k: number of centroids to initialize
    Returns:
        centroids, cluster_index
    """
    m, features = X.shape
    initial_centroids = np.random.choice(range(m), k, replace=False)
    centroids = X[initial_centroids]
    cluster_index = np.array(range(k))

    return centroids, cluster_index


# define number of clusters and generate starting point:
k = 40
centroids, cluster_allocation = initialize_centroids(X2, k)


def generate_centroids(X, index_location_of_centroids, k):
    """
    Takes existing allocation of centroids and calculates the
    next centroid value. Specifically, it calculates the average
    location of all X values allocated to each centroid, and 
    returns that as the new centroid.
    Parameters:
        X: a numpy index of values
        index_location_of_centroids: an index of values that 
        indicates which centroid each row in X belongs to
        k: number of centroids

    Returns:
        cluster_each_x_belongs_to: the updated values 
        for index_location_of_centroids
        new_centroids: the new centroid values

    Note: initial_centroids should be organized in order of
    cluster it belongs to (e.g. centroid 0 should correspond
    to initial_centroids[0])
    """
    # Generate variables:
    [m, features] = X.shape
    cluster_each_x_belongs_to = np.array([], dtype='int')
    new_centroids = np.zeros((k, features))

    for i in range(k):
        # get average "location" of each cluster
        new_centroids[i, :] = X[np.where(
            index_location_of_centroids == i), :].mean(axis=1)

    # Generate index value corresponding to the new centroid value
    for row in X:
        distance = np.sum(np.square(row-new_centroids), axis=1)
        # Get the index value of that closest value
        cluster = distance.argmin()
        # Take min distance and assign X value to that cluster
        cluster_each_x_belongs_to = np.append(
            cluster_each_x_belongs_to, cluster)

    return cluster_each_x_belongs_to, new_centroids


def k_means_cost(X, centroid_values, centroid_index_locations):
    """
    Calculates the cost function for the results of the clustering algorithm.
    """
    m, features = X.shape
    # Calculate J cost function
    return 1/m*np.square(X-centroid_values[centroid_index_locations]).sum()


J_list = []

for _ in range(50):
    cluster_allocation, centroids = generate_centroids(
        X2, cluster_allocation, k)
    J = k_means_cost(X2, centroids, cluster_allocation)
    J_list.append(J)

group = name_matrix.loc[cluster_allocation == 1]
# Attach the array containing each songs cluster grouping to the
# original dataset
name_matrix.insert(3, 'cluster_grouping', cluster_allocation)

plt.plot(J_list)
plt.xlabel('Number of iterations')
plt.ylabel('Cost')
# plt.show()

cluster_summary = name_matrix.groupby('cluster_grouping').mean().reset_index()
#grid_widget = qgrid.show_grid(cluster_summary,show_toolbar=True)
# display(grid_widget)
name_matrix[['track_name', 'artist_name', 'cluster_grouping']]
# print(cluster_summary)
