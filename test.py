# CS3
# Angel Rodriguez II
# Lab 6
# Diego Aguirre
# 12-02-2019
# Purpose: The purpose of this lab is to implement kruskal's algorithm and a topological sort algorithm


import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

from lab6 import DisjointSetForest
from lab6 import Edge
from lab6 import GraphAL



graph = GraphAL(4, True, True) # this is the simple graph i am performing the algorithm on
graph.insert_edge(1, 0, 2) # inserting edge
graph.insert_edge(1, 0, 3) # inserting edge
graph.insert_edge(5, 0, 1) # inserting edge
graph.insert_edge(2, 1, 3) # inserting edge
graph.insert_edge(3, 2, 3) # inserting edge

graph3 = GraphAL(9, True, True)
graph3.insert_edge(1, 0, 1)
graph3.insert_edge(1, 4, 0)
graph3.insert_edge(1, 4, 1)
graph3.insert_edge(1, 2, 1)
graph3.insert_edge(1, 5, 1)
graph3.insert_edge(1, 5, 4)
graph3.insert_edge(1, 7, 4)
graph3.insert_edge(1, 8, 7)
graph3.insert_edge(1, 5, 7)
graph3.insert_edge(1, 5, 2)
graph3.insert_edge(1, 6, 5)
graph3.insert_edge(1, 8, 5)
graph3.insert_edge(1, 6, 8)
graph3.insert_edge(1, 6, 3)
graph3.insert_edge(1, 6, 2)
graph3.insert_edge(1, 2, 3)



graph.kruskal() # will show the graph before and after kruskals algorithm
graph3.kruskal() # will show the graph before and after kruskals algorithm

print("----sorted reult from topological graph----")
print(graph.topological_sort())

print("----sorted reult from topological graph3----")
print(graph3.topological_sort())
