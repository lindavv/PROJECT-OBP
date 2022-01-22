from datetime import datetime, timedelta
import pandas as pd
import os
import math
from collections import namedtuple
from shapely.ops import unary_union
from shapely.geometry import Point, Polygon
import networkx as nx
import numpy as np

Node = namedtuple("node", ["lat", "lon"])
Edge = namedtuple("edge", ["start", "end", "directions", "time", "distance"])

#os.chdir('..')
path_parent = os.path.dirname(os. getcwd())
os.chdir(path_parent)
path = os.getcwd()


with open(path+"/data/paris_map.txt") as file:
    n_nodes, n_edges, n_polygons = map(int, file.readline().split())
    nodes = [Node(*map(float, file.readline().split())) for _ in range(n_nodes)]
    edges = [Edge(*map(int, file.readline().split())) for _ in range(n_edges)]
    polygons = [Polygon(zip(*[map(float, file.readline().split())]*2)) for _ in range(n_polygons)]

def assign_loc(lat,lon,nodes):
    dist = np.sqrt((nodes[:,0]-lat)**2+(nodes[:,1]-lon)**2)
    index = np.argmin(dist)
    return int(index)

# Returns duration between two node indices in minutes
def dist(n1, n2):
    duration = nx.algorithms.shortest_path_length(g, n1.get_location()['node_index'], n2.get_location()['node_index'],
                                                  weight="time")
    return duration / 60

""" -------------Create restaurants dataframe-------------------- """

rests_df = pd.read_csv(path + '/data/restaurants.csv', delimiter = " ")
restaurants_df = np.zeros((42, 3))
paris_nodes = np.array(nodes)
restaurant_indices = []
for i in range(len(rests_df)):
    index = assign_loc(rests_df['lat'][i], rests_df['lon'][i], paris_nodes)
    restaurants_df[i, 0] = paris_nodes[index][0]  # lat
    restaurants_df[i, 1] = paris_nodes[index][1]  # lon
    restaurants_df[i, 2] = int(index)  # index
    restaurant_indices.append(index)
restaurants_df = pd.DataFrame(restaurants_df, columns=['lat', 'lon', 'index'])
rests_df['node'] = restaurants_df['index'].astype(int)

