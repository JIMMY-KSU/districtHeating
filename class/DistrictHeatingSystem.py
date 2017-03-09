# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 16:22:28 2017

@author: johannes
"""

import sys
import os
import numpy as np

sys.path.append(os.getcwd() + os.sep + 'class')
sys.path.append(os.getcwd() + os.sep + 'function')

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
        
        self.consumersLocationinMatrix = self.__consumersLocationinMatrix()
        self.producersLocationinMatrix = self.__producersLocationinMatrix()
        self.pipesLocationinMatrix = self.__pipesLocationinMatrix()
        
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
        array_consumer = np.zeros([len(self.__inzidenzmatrix_HeatSink), 1])

        for i in range(len(self.heatsink.consumer())):
            array_consumer += self.__inzidenzmatrix_HeatSink[0:len(
                                self.__inzidenzmatrix_HeatSink), i:(i + 1)] * \
                                self.heatsink.consumer(i).flow

        return np.dot(np.linalg.pinv(
                np.concatenate((
                        self.__inzidenzmatrix_HeatGrid,
                        self.__inzidenzmatrix_HeatSource),
                        axis=1)) , array_consumer)
    def simulateDHS(self):

        VMass = np.asarray()

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
                    self._inzidenzmatrix_HeatGrid.clip(max=0)),self.VPres)

        momentumbalance = operation1 - P
        return momentumbalance
    
    def __momentumbalancePb(self, P):
        '''sets momentum balance of pressure(P):
            P multiplied by transposed incidencematrix+'''

        operation1 = np.dot(np.transpose(
                    self._inzidenzmatrix_HeatGrid.clip(min=0)),self.VPres)

        momentumbalance = operation1 - P
        return momentumbalance