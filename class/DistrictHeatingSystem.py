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
sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'class')
sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'function')

import dependencies as dp 

from DataIO import DataIO
from HeatGrid import HeatGrid
from HeatSink import HeatSink
from HeatSource import HeatSource
from inzidenzmatrix import inzidenzmatrix
from guess import getGuess
from scipy.optimize import root
from gridCalculation import gridCalculation
#from Solver import Solver


class DistrictHeatingSystem():

    def __init__(self, heatgrid_pipes, heatgrid_nodes, heatsink, heatsource):

        self.heatgrid = HeatGrid(heatgrid_pipes, heatgrid_nodes)
        self.heatsink = HeatSink(heatsink)
        self.heatsource = HeatSource(heatsource)

#        self.consumersLocationinMatrix = self.__consumersLocationinMatrix()
#        self.producersLocationinMatrix = self.__producersLocationinMatrix()
#        self.pipesLocationinMatrix = self.__pipesLocationinMatrix()

        self.VMass = self.__VMass()
        self.VTemp = self.__VTemp()
        self.VPres = self.__VPres()
        self.VTa = self.__VTa()
        self.VTb = self.__VTb()
        self.VPa = self.__VPa()
        self.VPb = self.__VPb()
        self._inzidenzmatrix_HeatGrid = self.__inzidenzmatrix_HeatGrid()
        self._inzidenzmatrix_HeatSink = self.__inzidenzmatrix_HeatSink()
        self._inzidenzmatrix_HeatSource = self.__inzidenzmatrix_HeatSource()
        self._inzidenzmatrix = self.__inzidenzmatrix()
        self.__massbilance = self.__massbalance()
        self.__energybalanceTa = self.__energybalance(self.VTa)
        self.__energybalanceTb = self.__energybalance(self.VTb)
        self.__momentumbalancePa = self.__momentumbalancePa(self.VPa)
        self.__momentumbalancePb = self.__momentumbalancePb(self.VPb)

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
        for i in self.heatsink.consumer():
            print(i.heat_demand)
        numberOfNodes = len(self.heatgrid.nodes())
        numberOfPipes = len(self.heatgrid.pipes())
        numberOfSinks = len(self.heatsink.consumer())
        numberOfSources = len(self.heatsource.producer())
        k = numberOfNodes
        v = (numberOfPipes + numberOfSinks + numberOfSources)
        print('Nodes: ', numberOfNodes)
        print('Pipes: ', numberOfPipes)
        print('Sinks: ', numberOfSinks)
        print('Sources: ', numberOfSources)
        print('k:', k)
        print('v:', v)

        solutionRoot = root(
                    gridCalculation,
                    getGuess(self.heatgrid,
                             self.heatsink,
                             self.heatsource),
                    args=[self.heatgrid,
                          self.heatsink,
                          self.heatsource,
                          self._inzidenzmatrix],
                    method='lm')
#        solution = fsolve(
#                    gridCalculation,
#                    getGuess(self.heatgrid,
#                             self.heatsink,
#                             self.heatsource),
#                    args=[self.heatgrid,
#                          self.heatsink,
#                          self.heatsource,
#                          self._inzidenzmatrix])

        for i in solutionRoot:
            print(i)

        solution = solutionRoot['x']
        print('\n', 'Success:', solutionRoot['success'], '\n')
        print('Solution:')
        n = 0
        print('massflow:')
        for i in range(v):
            print('  ', solution[n])
            n += 1

        print('pressure:')
        for i in range(k):
            print('  ', solution[n])
            n += 1

        print('pressure a:')
        for i in range(v):
            print('  ', solution[n])
            n += 1

        print('pressure b:')
        for i in range(v):
            print('  ', solution[n])
            n += 1

        print('tempreature:')
        for i in range(k):
            print('  ', solution[n])
            n += 1

        print('tempreature a:')
        for i in range(v):
            print('  ', solution[n])
            n += 1

        print('tempreature b:')
        for i in range(v):
            print('  ', solution[n])
            n += 1

        print('heatflow:')
        for i in range(v):
            print('  ', solution[n])
            n += 1

        print('läuft!')

        return None

    def __VMass(self):
        '''sets vector massflow of any pipe and consumer and producer'''
        VectorMass = np.asarray([0]*len(self.heatgrid.pipes()))
        return VectorMass

    def __VTemp(self):
        '''sets vector temperature of any node'''
        VectorTemp = np.asarray([0]*len(self.heatgrid.nodes()))
        return VectorTemp

    def __VPres(self):
        '''sets vector pressure of any node'''
        VectorPress = np.asarray([0]*len(self.heatgrid.nodes()))
        return VectorPress

    def __VTa(self):
        '''sets vector temperature of input Temperature of any pipe'''
        VectorTin = np.asarray([0]*len(self.heatgrid.pipes()))
        return VectorTin

    def __VTb(self):
        '''sets vector temperature of output Temperature of any pipe'''
        VectorTout = np.asarray([0]*len(self.heatgrid.pipes()))
        return VectorTout

    def __VPa(self):
        '''sets vector pressure of input pressure of any pipe'''
        VectorPin = np.asarray([0]*len(self.heatgrid.pipes()))
        return VectorPin

    def __VPb(self):
        '''sets vector pressure of output pressure of any pipe'''
        VectorPout = np.asarray([0]*len(self.heatgrid.pipes()))
        return VectorPout

    def __massbalance(self):
        massBalance = self._inzidenzmatrix_HeatGrid * self.VMass
        return massBalance

    def __energybalance(self, T):
        '''sets energy balance of temperature(T):
            T multiplied by diagonal mass vector'''

        energyBalance = np.diag(self.VMass) * T
        return energyBalance

    def __momentumbalancePa(self, P):
        '''sets momentum balance of pressure(P):
            P multiplied by transposed incidencematrix-'''

        operation1 = np.dot(np.transpose(
                    self._inzidenzmatrix_HeatGrid.clip(max=0)), self.VPres)

        momentumbalance = operation1 - P
        return momentumbalance

    def __momentumbalancePb(self, P):
        '''sets momentum balance of pressure(P):
            P multiplied by transposed incidencematrix+'''

        operation1 = np.dot(np.transpose(
                    self._inzidenzmatrix_HeatGrid.clip(min=0)), self.VPres)

        momentumbalance = operation1 - P
        return momentumbalance

if __name__ == "__main__":
    print('DistrictHeatingSystem run directly')
    import sys
    import os

    sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'class')
    sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'function')

    from DataIO import DataIO
    from DistrictHeatingSystem import DistrictHeatingSystem
    import Dictionary
    from Plotter import Plotter
    from matplotlib import pyplot as plt

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
