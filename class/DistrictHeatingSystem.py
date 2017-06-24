# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 16:22:28 2017

@author: johannes
"""

import sys
import os
import numpy as np
from scipy.optimize import fsolve

sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'class')
print(os.path.dirname(os.getcwd()) + os.sep + 'class')
sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'function')
print(os.path.dirname(os.getcwd()) + os.sep + 'function')

import dependencies as dp 

from DataIO import DataIO
from HeatGrid import HeatGrid
from HeatSink import HeatSink
from HeatSource import HeatSource
from inzidenzmatrix import inzidenzmatrix
from guess import getGuess
from scipy.optimize import root
from Solver import Solver


import logging
logger = logging.getLogger('stackoverflow_rocks')

class DistrictHeatingSystem():
    def __init__(self, heatgrid_pipes, heatgrid_nodes, heatsink, heatsource):
HeatGrid()
        self.heatgrid = HeatGrid(heatgrid_pipes, heatgrid_nodes)
        self.heatsink = HeatSink(heatsink)
        self.heatsource = HeatSource(heatsource)

#        self.consumersLocationinMatrix = self.__consumersLocationinMatrix()
#        self.producersLocationinMatrix = self.__producersLocationinMatrix()
#        self.pipesLocationinMatrix = self.__pipesLocationinMatrix()

        self.v_m = 0
        self.v_T = 0
        self.v_P = 0
        self.v_Ta = 0
        self.v_Tb = 0
        self.v_Pa = 0
        self.v_Pb = 0
        self.v_Q = 0

        self._inzidenzmatrix_HeatGrid = self.__inzidenzmatrix_HeatGrid()
        self._inzidenzmatrix_HeatSink = self.__inzidenzmatrix_HeatSink()
        self._inzidenzmatrix_HeatSource = self.__inzidenzmatrix_HeatSource()
        self._inzidenzmatrix = self.__inzidenzmatrix()

        self.numberOfNodes = len(self.heatgrid.nodes())
        self.numberOfPipes = len(self.heatgrid.pipes())
        self.numberOfSinks = len(self.heatsink.consumer())
        self.numberOfSources = len(self.heatsource.producer())
        self.numberOfElements = (self.numberOfPipes +
                                 self.numberOfSinks +
                                 self.numberOfSources)

        logger.debug("This is a debug log")
        logger.critical("This is critical")
        logger.error("An error occurred")
        logger.info("This is an info log")
        print('Nodes: ', self.numberOfNodes)
        print('Pipes: ', self.numberOfPipes)
        print('Sinks: ', self.numberOfSinks)
        print('Sources: ', self.numberOfSources)
        print('nodes:', self.numberOfNodes)
        print('elements:', self.numberOfElements)

    

        
    def __inzidenzmatrix_HeatGrid(self):
        '''returns an inzidenzmatrix where all elements are displayed 
            (producer, consumer, pipes)'''
        array_col = []

        for item in self.heatgrid.pipes():
            array_col.append(
                             [item.start_node_name,
                              item.end_node_name])

        return inzidenzmatrix(self.heatgrid.nodes_names, array_col,
                              inzidenzmatrix_name="heatGrid")

    def __inzidenzmatrix_HeatSink(self):

        array_col = []

        for item in self.heatsink.consumer():
            array_col.append(
                             [item.start_node_name,
                              item.end_node_name])

        return inzidenzmatrix(self.heatgrid.nodes_names, array_col,
                              inzidenzmatrix_name="heatSink")

    def __inzidenzmatrix_HeatSource(self):
        # TODO implement Try and error in case of no loaded\
        # self.heatgrid.nodes_name
        # implement as property as well as other inzidenzmatrixen
        array_col = []
        for item in self.heatsource.producer():
            array_col.append([item.start_node_name,
                              item.end_node_name])

        return inzidenzmatrix(self.heatgrid.nodes_names, array_col,
                              inzidenzmatrix_name="heatSource")

    def __inzidenzmatrix(self):

        array_col = []

        for item in self.heatgrid.pipes():
            array_col.append(
                             [item.start_node_name,
                              item.end_node_name])

        for item in self.heatsink.consumer():
            array_col.append(
                             [item.start_node_name,
                              item.end_node_name])

        for item in self.heatsource.producer():
            array_col.append([item.start_node_name,
                              item.end_node_name])

        return inzidenzmatrix(self.heatgrid.nodes_names, array_col,
                              inzidenzmatrix_name="all")

    def calculateDHS(self):



#        solutionRoot = root(
#                    gridCalculation,
#                    getGuess(self.heatgrid,
#                             self.heatsink,
#                             self.heatsource),
#                    args=[self.heatgrid,
#                          self.heatsink,
#                          self.heatsource,
#
#                          self._inzidenzmatrix],
#                    method='lm')

#        print('Solution:')
#        n = 0
#        print('massflow:')
#        for i in range(v):
#            print('  ', solution[n])
#            n += 1
#
#        print('pressure:')
#        for i in range(k):
#            print('  ', solution[n])
#            n += 1
#
#        print('pressure a:')
#        for i in range(v):
#            print('  ', solution[n])
#            n += 1
#
#        print('pressure b:')
#        for i in range(v):
#            print('  ', solution[n])
#            n += 1
#
#        print('tempreature:')
#        for i in range(k):
#            print('  ', solution[n])
#            n += 1
#
#        print('tempreature a:')
#        for i in range(v):
#            print('  ', solution[n])
#            n += 1
#
#        print('tempreature b:')
#        for i in range(v):
#            print('  ', solution[n])
#            n += 1
#
#        print('heatflow:')
#        for i in range(v):
#            print('  ', solution[n])
#            n += 1
#
#        print('läuft!')
#        
#        for i in solutionRoot:
#            print(i)
#
#        solution = solutionRoot['x']
#        print('\n', 'Success:', solutionRoot['success'], '\n')

        
        Solver_fsolve = Solver(self._inzidenzmatrix,
                               self._inzidenzmatrix_HeatGrid,
                               self._inzidenzmatrix_HeatSink,
                               self._inzidenzmatrix_HeatSource)
        
        
        solution = fsolve(Solver_fsolve.gridCalculation,
                        getGuess(self.heatgrid,
                                 self.heatsink,
                                 self.heatsource),
                        args=[self.heatgrid,
                              self.heatsink,
                              self.heatsource,
                              self._inzidenzmatrix])

        return None


if __name__ == "__main__":
    print('DistrictHeatingSystem run directly')
    import sys
    import os

    sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'class')
    sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'function')

    import Dictionary

    DataIO = DataIO(
                os.path.dirname(os.getcwd()) + os.sep + 'input',
                os.path.dirname(os.getcwd()) + os.sep + 'output')

    heatgrid_nodes = DataIO.importDBF(
            'TestNetz' + os.sep + 'KTestNetz.DBF',
            Dictionary.HeatGrid_node_dtype,
            Dictionary.HeatGrid_STANET_nodes_allocation)

    heatgrid_pipes = DataIO.importDBF(
            'TestNetz' + os.sep + 'STestNetz.DBF',
            Dictionary.HeatGrid_pipe_dtype,
            Dictionary.HeatGrid_STANET_pipes_allocation)

    heatsink = DataIO.importDBF(
            'TestNetz' + os.sep + 'WTestNetz.DBF',
            Dictionary.HeatSink_consumer_dtype,
            Dictionary.HeatSink_STANET_consumer_allocation)

    heatsource = DataIO.importCSV(
            'TestNetz' + os.sep + 'WTestNetz.csv',
            dtype=Dictionary.HeatSource_producer_dtype,
            startrow=1,
            columnofdate=None,
            dateformat='None')

    DHS1 = DistrictHeatingSystem(
            heatgrid_pipes,
            heatgrid_nodes,
            heatsink,
            heatsource)

    DHS1.calculateDHS()
else:
    print('DistrictHeatingSystem was imported into another module')
