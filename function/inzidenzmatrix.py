# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:30:59 2017

@author: jpelda
"""
import numpy as np

def inzidenzmatrix(rows, cols):
    '''
    arranges an inzidenzmatrix for a directed graph for further
    calculations:
                pipes
                f_0  f_1  f_2  f_3
        node 0   1    0    -1   0
        node 1   0    0    1   -1
    Flows towards a node are -1. Flows away from node are 1.
    
    input:
        rows = []
        cols = [[,],[,]] # cols[0] is away from row value -> 1,\
                            cols[1] is towards row value -> -1
    '''
    returnMatrix = np.array(len(rows) * [len(cols)*[0]])
    for index_rows, item_rows in enumerate(rows):

        for index_cols, item_cols in enumerate(cols):

            if item_rows == item_cols[0]:
                returnMatrix[index_rows][index_cols] = 1
            if item_rows == item_cols[1]:
                returnMatrix[index_rows][index_cols] = -1
    for item in returnMatrix:
        print(item)
    return returnMatrix