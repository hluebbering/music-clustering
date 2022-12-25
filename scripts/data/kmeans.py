"""
* Name: Hannah Luebbering
* Date: 07/23/2022
* CSE 160, Summer 2022
* Homework 4
* Description: Designed and implemented a k-means clustering algorithm 
  for a given list of data points and dictionary of centroids.
* Collaboration: N/A
"""

import utils  # noqa: F401, do not remove if using a Mac
import matplotlib.pyplot as plt  # noqa: E402
import os  # noqa: E402
import math  # noqa: E402
from utils import converged, plot_2d, plot_centroids, assert_equals, \
    read_data, load_centroids, write_centroids_tofile  # noqa: E402
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
    
# ----------------------------------------------------------
# Part 1. Implementing K-means clustering


# Calculating Euclidean distances
def euclidean_distance(point1, point2):
    """
    Calculate the Euclidean distance between two data points.

    Arguments:
        point1: a non-empty list of floats representing a data point
        point2: a non-empty list of floats representing a data point

    Returns: the Euclidean distance between two data points

    Example:
        Code:
            point1 = [1.1, 1, 1, 0.5]
            point2 = [4, 3.14, 2, 1]
            print(euclidean_distance(point1, point2))
        Output:
            3.7735394525564456
    """
    
    # Sum of squared difference between coordinates
    sum_of_squares = 0
    
    # Number of dimensions
    for n in range(len(point1)):
        
        a_n = point1[n]
        b_n = point2[n]
        
        sum_of_squares += (a_n - b_n) ** 2
    
    # Square root of sum of squared difference
    return sum_of_squares ** 0.5



# Assigning data points to closest centroids
def get_closest_centroid(point, centroids_dict):
    """
    Find the closest centroid given a data point using the
    euclidean_distance function implemented above.

    Arguments:
        point: a list of floats representing a data point
        centroids_dict: a dictionary representing the centroids where
                        the keys are strings of centroid names and
                        the values are lists of centroid locations

    Returns: the key name (a string) of the closest centroid to the data point

    Example:
        Code:
            point = [0, 0, 0, 0]
            centroids_dict = {"centroid1": [1, 1, 1, 1],
                            "centroid2": [2, 2, 2, 2]}
            print(get_closest_centroid(point, centroids_dict))
        Output:
            centroid1
    """
    
    min_distance = 0
    
    # Setting key-value pair
    for centroid_name in centroids_dict.keys():
        
        # Access centroid value from key name
        centroid_location = centroids_dict[centroid_name]

        # Get euclidean distance between datapoint and centroid
        new_distance = euclidean_distance(point, centroid_location)

        # Find smallest euclidean distance
        if min_distance == 0 or new_distance < min_distance:
            # Update closest distance and corresponding centroid name
            min_distance = new_distance
            closest_centroid = centroid_name

    # Key name of closest centroid to the data point
    return closest_centroid
        


# Update assignment of points to centroids
def update_assignment(list_of_points, centroids_dict):
    """
    Assign all data points to closest centroids using implemented
    get_closest_centroid function above. Should return a new
    dictionary, not modify any passed in parameters.

    Arguments:
        list_of_points: a list of lists representing all data points
        centroids_dict: a dictionary representing the centroids where the keys
                        are strings (centroid names) and the values are lists
                        of centroid locations

    Returns: a new dictionary whose keys are the centroids' key names and
             values are lists of points that belong to the centroid. If a
             given centroid does not have any data points closest to it,
             do not include the centroid in the returned dictionary

    Example:
        Code:
            list_of_points = [[1.1, 1, 1, 0.5], [4, 3.14, 2, 1], [0, 0, 0, 0]]
            centroids_dict = {"centroid1": [1, 1, 1, 1],
                            "centroid2": [2, 2, 2, 2]}

            print(update_assignment(list_of_points, centroids_dict))
        Output:
            {'centroid1': [[1.1, 1, 1, 0.5], [0, 0, 0, 0]],
             'centroid2': [[4, 3.14, 2, 1]]}
    """
    
    # Create a new empty dictionary
    new_dict = {}
    for datapoint in list_of_points:
        
        # For each datapoint, determine closest centroid
        centroid_name = get_closest_centroid(datapoint, centroids_dict) 

        # Setting key-value pair
        if centroid_name in new_dict:
            # Append datapoint to list for centroid key name
            new_dict[centroid_name] += [datapoint]
        else:
            # Start new list of points for centroid key name
            new_dict[centroid_name] = [datapoint]

    return new_dict


# Find the average of a cluster
def mean_of_points(list_of_points):
    """
    Calculate mean of a given group of data points. 

    Arguments:
        list_of_points: a list of lists representing a group of data points

    Returns: a list of floats as the mean of the given data points

    Example:
        Code:
            list_of_points = [[1.1, 1, 1, 0.5], [4, 3.14, 2, 1], [0, 0, 0, 0]]
            print(mean_of_points(list_of_points))
        Output:
            [1.7, 1.3800000000000001, 1.0, 0.5]
    """
    
    # Number of data points in list
    num_points = len(list_of_points)
    
    # Create new list
    avg_location = []
    
    # Index n-dimensional points
    n = 0
    while n < len(list_of_points[1]):
        
        # Add data points' components in each dimension
        sum_n = 0
        for datapoint in list_of_points:
            sum_n += datapoint[n]
        
        # Append mean (float) of given datapoint to list
        avg_location += [sum_n / num_points]
        
        n += 1
    

    return avg_location

    
    
    

    


# Update centroid to be the average of the clusters
def update_centroids(assignment_dict):
    """
    Update centroid locations as the mean of all data points that belong
    to the cluster using the mean_of_points function. 
    This function should return a new dictionary, not modify any
    passed in parameters.

    Arguments:
        assignment_dict: a dictionary whose keys are the centroids' key
                         names and values are lists of points that belong
                         to the centroid. It is the dictionary
                         returned by update_assignment function.

    Returns: A new dictionary representing the updated centroids. If a
             given centroid does not have any data points closest to it,
             do not include the centroid in the returned dictionary.

    Example:
        Code:
            assignment_dict = {'centroid1': [[1.1, 1, 1, 0.5], [0, 0, 0, 0]],
                            'centroid2': [[4, 3.14, 2, 1]]}
            print(update_centroids(assignment_dict))
        Output:
          {'centroid1': [0.55, 0.5, 0.5, 0.25],
           'centroid2': [4.0, 3.14, 2.0, 1.0]}
    """
    
    # New dictionary representing updated centroids
    new_dict = {}
    
    for centroid_name in assignment_dict.keys():
        
        # Mean of all datapoints that belong to the cluster
        points_list = assignment_dict[centroid_name]
        cluster_average = mean_of_points(points_list)
        
        # Set key-value pair for new dictionary
        new_dict[centroid_name] = cluster_average
    
    return new_dict
        

# ----------------------------------------------------------
# HELPER FUNCTIONS


def setup_data_centroids():
    """
    Creates are returns data for testing k-means methods.

    Returns: list_of_points, a list of data points
             centroids_dict1, two 4D centroids
             centroids_dict2, two 4D centroids
    """

    #######################################################
    # You do not need to change anything in this function #
    #######################################################

    list_of_points = [
        [-1.01714716,  0.95954521,  1.20493919,  0.34804443],
        [-1.36639346, -0.38664658, -1.02232584, -1.05902604],
        [1.13659605, -2.47109085, -0.83996912, -0.24579457],
        [-1.48090019, -1.47491857, -0.6221167,  1.79055006],
        [-0.31237952,  0.73762417,  0.39042814, -1.1308523],
        [-0.83095884, -1.73002213, -0.01361636, -0.32652741],
        [-0.78645408,  1.98342914,  0.31944446, -0.41656898],
        [-1.06190687,  0.34481172, -0.70359847, -0.27828666],
        [-2.01157677,  2.93965872,  0.32334723, -0.1659333],
        [-0.56669023, -0.06943413,  1.46053764,  0.01723844]
    ]
    centroids_dict1 = {
        "centroid1": [0.1839742, -0.45809263, -1.91311585, -1.48341843],
        "centroid2": [-0.71767545, 1.2309971, -1.00348728, -0.38204247],
    }
    centroids_dict2 = {
        "centroid1": [0.1839742, -0.45809263, -1.91311585, -1.48341843],
        "centroid2": [10, 10, 10, 10],
    }
    return list_of_points, centroids_dict1, centroids_dict2


# ----------------------------------------------------------
# TESTS


    #######################################################
    # You do not need to change anything in this function #
    #######################################################

    test_euclidean_distance()
    test_get_closest_centroid()
    test_update_assignment()
    test_mean_of_points()
    test_update_centroids()
    print("all tests passed.")


def main_2d(data, init_centroids):
    #######################################################
    # You do not need to change anything in this function #
    #######################################################
    centroids = init_centroids
    old_centroids = None
    step = 0
    while not converged(centroids, old_centroids):
        # save old centroid
        old_centroids = centroids
        # new assignment
        assignment_dict = update_assignment(data, old_centroids)
        # update centroids
        centroids = update_centroids(assignment_dict)
        # plot centroid
        fig = plot_2d(assignment_dict, centroids)
        plt.title(f"step{step}")
        fig.savefig(os.path.join("results", "2D", f"step{step}.png"))
        plt.clf()
        step += 1
    print(f"K-means converged after {step} steps.")
    return centroids


def main_mnist(data, init_centroids):
    #######################################################
    # You do not need to change anything in this function #
    #######################################################
    centroids = init_centroids
    # plot initial centroids
    plot_centroids(centroids, "init")
    old_centroids = None
    step = 0
    while not converged(centroids, old_centroids):
        # save old centroid
        old_centroids = centroids
        # new assignment
        assignment_dict = update_assignment(data, old_centroids)
        # update centroids
        centroids = update_centroids(assignment_dict)
        step += 1
    print(f"K-means converged after {step} steps.")
    # plot final centroids
    plot_centroids(centroids, "final")
    return centroids


if __name__ == "__main__":
    # main_test()

    # data, label = read_data("data/data_2d.csv")
    # init_c = load_centroids("data/2d_init_centroids.csv")
    # final_c = main_2d(data, init_c)
    # write_centroids_tofile("2d_final_centroids.csv", final_c)
    

    # Load MNIST dataset instead of the 2D points
    #data, label = read_data("data/mnist.csv")
    #init_c = load_centroids("data/mnist_init_centroids.csv")
    #final_c = main_mnist(data, init_c)
    #write_centroids_tofile("mnist_final_centroids.csv", final_c)

    # Spotify Authentication - without user
    
    dimensions = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'key',
              'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']
    centroids = dict()
    fname = 'scripts/playlists.csv'
    with open(fname) as f:
        
        reader = csv.DictReader(f)
        for row in reader:
            track = row['track_id']
            dim_point = []
            for dim in dimensions:
                dim_point.append(row[dim])
            centroids[track] = dim_point
    #print(centroids)
    centroid_values = np.asarray(list(centroids.values()))
    #print(centroid_values)
    
    data = []
    label = []
    with open(fname, newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        for r in reader:
            label.append(r['track_id'])
            dim_point = []
            
            for dim in dimensions:
                dim_point.append(r[dim])
            data.append(list(map(float, dim_point)))
    #print(data)
    
    xx=main_mnist(data, centroids)
                
    
    #np.savetxt('scripts/playlist_centroids.csv', centroid_values, delimiter=',')
                
            
            #centroids[f"centroid{i}"] = list(map(float, r))
    #return centroids

    



