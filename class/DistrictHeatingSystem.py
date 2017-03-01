# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 16:22:28 2017

@author: johannes
"""

import sys
import os
import inspect

sys.path.append(os.getcwd() + os.sep + 'class')
print(sys.path.append(os.getcwd() + os.sep + 'function'))

from DataIO import DataIO
from HeatGrid import HeatGrid
from HeatSink import HeatSink
from HeatSource import HeatSource
from inzidenzmatrix import inzidenzmatrix
import Dictionary


class DistrictHeatingSystem():

    def __init__(self, heatgrid_pipes, heatgrid_nodes, heatsink, heatsource):

        self.heatgrid = HeatGrid(heatgrid_pipes, heatgrid_nodes)
        self.heatsink = HeatSink(heatsink)
        self.heatsource = HeatSource(heatsource)

        self.__inzidenzmatrix_HeatGrid = self.__inzidenzmatrix_HeatGrid()
        self.__inzidenzmatrix_HeatSink = self.__inzidenzmatrix_HeatSink()
        self.__inzidenzmatrix_HeatSource = self.__inzidenzmatrix_HeatSource()

    def calculateDHS():
        pass

    def __inzidenzmatrix_HeatGrid(self):

        array_col = []

        for item in self.heatgrid.pipes():
            array_col.append(
                             [item.start_node_name,
                              item.end_node_name])

        return inzidenzmatrix(self.heatgrid.nodes_name, array_col)

    def __inzidenzmatrix_HeatSink(self):

        array_col = []

        for item in self.heatsink.consumer():
            array_col.append(
                             [item.start_node_name,
                              item.end_node_name])

        return inzidenzmatrix(self.heatgrid.nodes_name, array_col)

    def __inzidenzmatrix_HeatSource(self):
        # TODO implement Try and error in case of no loaded\
        # self.heatgrid.nodes_name
        array_col = []

        for item in self.heatsource.producer():
            array_col.append([item.start_node_name,
                              item.end_node_name])

        return inzidenzmatrix(self.heatgrid.nodes_name, array_col)
