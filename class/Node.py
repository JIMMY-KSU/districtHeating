# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:17:01 2017

@author: jpelda
"""


class Node():
    def __init__(self, nodeValues):
        self.index = nodeValues['index']
        self.x = nodeValues['x']
        self.y = nodeValues['y']
        self.name = nodeValues['name']
        self.height = nodeValues['height']
        self.SP_RP = nodeValues['SP_RP']