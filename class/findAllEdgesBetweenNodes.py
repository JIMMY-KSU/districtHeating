#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 18:08:43 2017

@author: johannes
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import igraph

adjacency_matrix = np.array([[-1,1,0,0],
                             [1,0,0,-1],
                             [0,-1,1,0],
                             [0,-1,0,1],
                             [0,0,1,-1],
                             [1,0,-1,0]])
adjacency_matrix = adjacency_matrix.T

adjacency_matrix_abs = np.abs(adjacency_matrix)
rows, cols = np.where(adjacency_matrix_abs
                      == 1)
edges = zip(rows.tolist(), cols.tolist())
g = nx.Graph()
g.add_edges_from(edges)

nx.draw_networkx(g)
plt.show()

for path in nx.all_simple_paths(g, source=0,
                                target=3):
    print(path)
    
path_between_generator = nx.all_simple_paths(g,
                        source=0, target=3)

nodes_between_set = {node for path in path_between_generator 
                     for node in path}
print(nodes_between_set)
sg = g.subgraph(nodes_between_set)
nx.draw_networkx(sg)
plt.show()
