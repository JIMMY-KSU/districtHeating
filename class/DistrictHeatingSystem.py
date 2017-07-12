# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 16:22:28 2017

@author: johannes
"""

import sys
import os
import numpy as np
from scipy.optimize import fsolve

#sys.path.append(os.getcwd())
#print(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'function')
#print(os.path.dirname(os.getcwd()) + os.sep + 'function')

import dependencies as dp 

from HeatGrid import HeatGrid
from HeatSink import HeatSink
from HeatSource import HeatSource
from inzidenzmatrix import inzidenzmatrix
from scipy.optimize import root
from Solver import Solver


import logging
logger = logging.getLogger('stackoverflow_rocks')

class DistrictHeatingSystem():
    def __init__(self, heatgrid_pipes, heatgrid_nodes, heatsink, heatsource):

        self.heatsink = HeatSink(heatsink)
        self.heatsource = HeatSource(heatsource)
        self.heatgrid = HeatGrid(heatgrid_pipes,
                                 heatgrid_nodes,
                                 nodeSupply=np.column_stack((
                                     self.heatsource.v_producers_eNode,
                                     np.array([None]*len(
                                         self.heatsource.v_producers_eNode)))))

#        self.consumersLocationinMatrix = self.__consumersLocationinMatrix()
#        self.producersLocationinMatrix = self.__producersLocationinMatrix()
#        self.pipesLocationinMatrix = self.__pipesLocationinMatrix()

        self._inzidenzmatrix_HeatGrid = self.__inzidenzmatrix_HeatGrid()
        self._inzidenzmatrix_HeatSink = self.__inzidenzmatrix_HeatSink()
        self._inzidenzmatrix_HeatSource = self.__inzidenzmatrix_HeatSource()
        self._inzidenzmatrix = self.__inzidenzmatrix()
        
        self._nodes = len(self._inzidenzmatrix)
        self._elements = len(self._inzidenzmatrix[0])


#        logger.debug("This is a debug log")
#        logger.critical("This is critical")
#        logger.error("An error occurred")
#        logger.info("This is an info log")

    def __inzidenzmatrix_HeatGrid(self):
        '''returns an inzidenzmatrix of HeatGrid, where pipes are col
        and nodes are row'''
        array_col = []
        try:
            for item in self.heatgrid.pipes():
                array_col.append(
                                 [item.sNode,
                                  item.eNode])
        except ValueError:
            print("Error in __inzidenzmatrix_HeatGrid, no heatgrid loaded?")
        return inzidenzmatrix(self.heatgrid.v_nodes_name, array_col,
                              inzidenzmatrix_name="heatGrid")

    def __inzidenzmatrix_HeatSink(self):
        '''returns an inzidenzmatrix of HeatSink, where consumer are col
        and nodes are row'''
        array_col = []
        try:
            for item in self.heatsink.consumer():
                array_col.append(
                                 [item.sNode,
                                  item.eNode])
        except ValueError:
            print("Error in __inzidenzmatrix_HeatSink, no heatsink loaded?")
        return inzidenzmatrix(self.heatgrid.v_nodes_name, array_col,
                              inzidenzmatrix_name="heatSink")

    def __inzidenzmatrix_HeatSource(self):
        '''returns an inzidenzmatrix of HeatSource, where producer are col
        and nodes are row'''
        array_col = []
        try:
            for item in self.heatsource.producers():
                array_col.append([item.sNode,
                                  item.eNode])
        except ValueError:
            print("Error in __inzidenzmatrix_HeatSource, \
                  no heatsource loaded?")
        return inzidenzmatrix(self.heatgrid.v_nodes_name, array_col,
                              inzidenzmatrix_name="heatSource")

    def __inzidenzmatrix(self):
        '''returns an inzidenzmatrix of HeatGrid, HeatSink and HeatSource,\
        where all elements are col and nodes are row'''
        array_col = []
        try:
            for item in self.heatgrid.pipes():
                array_col.append(
                                 [item.sNode,
                                  item.eNode])

            for item in self.heatsink.consumer():
                array_col.append(
                                 [item.sNode,
                                  item.eNode])

            for item in self.heatsource.producers():
                array_col.append([item.sNode,
                                  item.eNode])
        except ValueError:
            print("Error in __inzidenzmatrix")
        return inzidenzmatrix(self.heatgrid.v_nodes_name, array_col,
                              inzidenzmatrix_name="all")

    def calculateDHS(self):
        print("---->\tstart to calculate heatgrid\n")
        Solver_fsolve = Solver(self._inzidenzmatrix,
                               self._inzidenzmatrix_HeatGrid,
                               self._inzidenzmatrix_HeatSink,
                               self._inzidenzmatrix_HeatSource)

        solution = fsolve(Solver_fsolve.gridCalculation,
                        Solver_fsolve.getGuess(self.heatgrid,
                                 self.heatsink,
                                 self.heatsource))
        
        Solver_fsolve.print_x(self.heatgrid, self.heatsink, self.heatsource,
                              Solver_fsolve.getGuess(self.heatgrid,
                                                     self.heatsink,
                                                     self.heatsource), "guess")
        Solver_fsolve.print_x(self.heatgrid, self.heatsink, self.heatsource,
                              solution, "solution")

        return None


if __name__ == "__main__":
    from DataIO import DataIO
    import Dictionary
    print('DistrictHeatingSystem \t run directly \n')


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
    print('DistrictHeatingSystem \t was imported into another module')
