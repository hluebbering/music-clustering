import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import cluster, decomposition

songs = pd.read_csv('data/my_playlist.csv', encoding_errors='ignore', index_col=0, header=0)

labels = songs.values[:,0]
X = songs.values[:,10:22]

kmeans = cluster.AffinityPropagation(preference=-200)
kmeans.fit(X)

predictions = {}
for p,n in zip(kmeans.predict(X),labels):
    if not predictions.get(p):
        predictions[p] = []
        
    predictions[p] += [n]

for p in predictions:
    print("Category",p)
    print("-----")
    for n in predictions[p]:
        print(n)
    print("")
