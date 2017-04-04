# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 16:22:28 2017

@author: johannes
"""

import sys
import os
import numpy as np
from scipy.optimize import fsolve
sys.path.append(os.getcwd() + os.sep + 'class')
sys.path.append(os.getcwd() + os.sep + 'function')


from DataIO import DataIO
from HeatGrid import HeatGrid
from HeatSink import HeatSink
from HeatSource import HeatSource
from inzidenzmatrix import inzidenzmatrix
from scipy.optimize import fsolve
from Solver import Solver


class DistrictHeatingSystem():

    def __init__(self, heatgrid_pipes, heatgrid_nodes, heatsink, heatsource):

        self.heatgrid = HeatGrid(heatgrid_pipes, heatgrid_nodes)
        self.heatsink = HeatSink(heatsink)
        self.heatsource = HeatSource(heatsource)
        
        self.consumersLocationinMatrix = self.__consumersLocationinMatrix()
        self.producersLocationinMatrix = self.__producersLocationinMatrix()
        self.pipesLocationinMatrix = self.__pipesLocationinMatrix()

        self._inzidenzmatrix_HeatGrid = self.__inzidenzmatrix_HeatGrid()
        self._inzidenzmatrix_HeatSink = self.__inzidenzmatrix_HeatSink()
        self._inzidenzmatrix_HeatSource = self.__inzidenzmatrix_HeatSource()
        self._inzidenzmatrix = np.concatenate((self._inzidenzmatrix_HeatGrid,
                                              self._inzidenzmatrix_HeatSink,
                                              self._inzidenzmatrix_HeatSource),
                                              axis=1)

    def __inzidenzmatrix_HeatGrid(self):
        '''returns an inzidenzmatrix where all elements are displayed 
            (producer, consumer, pipes)'''
        array_col = []

        for item in self.heatgrid.pipes():
            array_col.append(
                             [item.start_node_name,
                              item.end_node_name])
        returnMatrix = inzidenzmatrix(self.heatgrid.nodes_names, array_col,
                              inzidenzmatrix_name = "heatGrid")
        return returnMatrix

    def __inzidenzmatrix_HeatSink(self):

        array_col = []

        for item in self.heatsink.consumer():
            array_col.append(
                             [item.start_node_name,
                              item.end_node_name])

        return inzidenzmatrix(self.heatgrid.nodes_names, array_col,
                              inzidenzmatrix_name = "heatSink")

    def __inzidenzmatrix_HeatSource(self):
        # TODO implement Try and error in case of no loaded\
        # self.heatgrid.nodes_name
        # implement as property as well as other inzidenzmatrixen
        array_col = []
        for item in self.heatsource.producer():
            array_col.append([item.start_node_name,
                              item.end_node_name])

        return inzidenzmatrix(self.heatgrid.nodes_names, array_col,
                               inzidenzmatrix_name = "heatSource")

    def calculateDHS(self):
        edges = np.shape(self._inzidenzmatrix)[1]
        nodes = np.shape(self._inzidenzmatrix)[0]

        v_massflow = [0] * edges
        v_Q = [0] * edges

        v_T = [0] * nodes
        v_Ta = [0] * edges
        v_Tb = [0] * edges

        v_P = [0] * nodes
        v_Pa = [0] * edges
        v_Pb = [0] * edges

        solveGrid = Solver(nodes, edges, self._inzidenzmatrix,
                        self._inzidenzmatrix_HeatGrid,
                        self._inzidenzmatrix_HeatSink,
                        self._inzidenzmatrix_HeatSource,
                        v_massflow,
                        v_Q, v_T, v_Ta, v_Tb,
                        v_P, v_Pa, v_Pb)
        
        solution = fsolve(solveGrid.gridCalculation_thermical, x)
        return solution

    def __consumersLocationinMatrix(self):
        i = 0
        consumerLocationinMatrix = [0]*len(self.heatgrid.nodes_names)

        while i < len(self.heatsink.consumer()):
            consumer_nodename = self.heatsink.consumer(i).start_node_name
            for index, item in enumerate(self.heatgrid.nodes_names):
                if item == consumer_nodename:
                    consumerLocationinMatrix[index] =\
                        consumerLocationinMatrix[index] + 1
            i = i + 1

        return consumerLocationinMatrix

    def __producersLocationinMatrix(self):
        i = 0
        producerLocationinMatrix = [0]*len(self.heatgrid.nodes_names)
        while i < len(self.heatsource.producer()):
            producer_nodename = self.heatsource.producer(i).start_node_name
            for index, item in enumerate(self.heatgrid.nodes_names):
                if item == producer_nodename:
                    producerLocationinMatrix[index] =\
                        producerLocationinMatrix[index] + 1
            i = i + 1

        return producerLocationinMatrix

    def __pipesLocationinMatrix(self):
        i = 0
        pipesLocationinMatrix = [0]*len(self.heatgrid.nodes_names)
        while i < len(self.heatgrid.pipes()):
            pipe_nodename = self.heatgrid.pipes(i).start_node_name
            for index, item in enumerate(self.heatgrid.nodes_names):
                if item == pipe_nodename:
                    pipesLocationinMatrix[index] =\
                        pipesLocationinMatrix[index] + 1
            i = i + 1

        return pipesLocationinMatrix




if __name__ == "__main__":
    print('DistrictHeatingSystem run directly')

    import Dictionary

    DataIO = DataIO(os.path.dirname(os.getcwd()) + os.sep + 'input',
                    os.path.dirname(os.getcwd()) + os.sep + 'output')

    heatgrid_nodes = DataIO.importCSV('Hannover_workshopNet1' +
                                      os.sep + 'heatnet_nodes.csv',
                                      dtypeSource=Dictionary.
                                      HeatGrid_node_dtype,
                                      startrow=1,
                                      columnofdate=None,
                                      dateformat='None')

    heatgrid_pipes = DataIO.importCSV('Hannover_workshopNet1' +
                                      os.sep + 'heatnet_pipes.csv',
                                      dtypeSource=Dictionary.
                                      HeatGrid_pipe_dtype,
                                      startrow=1,
                                      columnofdate=None,
                                      dateformat='None')
    heatsink = DataIO.importCSV('Hannover_workshopNet1' +
                                         os.sep + 'consumer.csv',
                                         dtypeSource=Dictionary.
                                         HeatSink_consumer_dtype,
                                         startrow=1,
                                         columnofdate=None,
                                         dateformat='None')

    heatsource = DataIO.importCSV('Hannover_workshopNet1' +
                                  os.sep + 'producer.csv',
                                  dtypeSource=Dictionary.
                                  HeatSource_producer_dtype,
                                  startrow=1,
                                  columnofdate=None,
                                  dateformat='None')

    DHS1 = DistrictHeatingSystem(heatgrid_pipes, heatgrid_nodes,
                                 heatsink, heatsource)
    DHS1.calculateDHS()

else:
    print('DistrictHeatingSystem was imported into another module')
