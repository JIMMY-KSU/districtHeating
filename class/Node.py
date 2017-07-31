# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:17:01 2017

@author: jpelda
"""
import numpy as np

class Node():
    def __init__(self, index, nodeValues):
        self.index = index
        self.x = np.asarray(nodeValues['x'])
        self.y = np.asarray(nodeValues['y'])
        self.name = nodeValues['name']
        self.height = np.asarray(nodeValues['height'], dtype="float32")
        self.sprp = np.asarray(nodeValues['sprp'])
        self.element = "node"