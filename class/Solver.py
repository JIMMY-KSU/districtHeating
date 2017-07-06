# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 14:45:18 2017

@author: narand
"""

import dependencies as dp
import balances as bl
import numpy as np


class Solver():
    def __init__(self, inzidenzmatrix, inzidenzmatrix_grid,
                 inzidenzmatrix_sink, inzidenzmatrix_source):

        self.edges = np.shape(inzidenzmatrix)[1]
        self.nodes = np.shape(inzidenzmatrix)[0]

        '''
        sets up all necessary inzmatrices
        '''
        self.__I = np.asarray(inzidenzmatrix)
        self.__I_minus = self.__I.clip(max=0)
        self.__I_minus_T = self.__I_minus.T
        self.__I_plus = self.__I.clip(min=0)
        self.__I_plus_T = self.__I_plus.T

        self.__I_grid = np.asarray(inzidenzmatrix_grid)
        self.__I_grid_slice = slice(0, self.__I_grid.shape[1])

        self.__I_sink = np.asarray(inzidenzmatrix_sink)
        self.__I_sink_slice = slice(self.__I_grid.shape[1],
                                    self.__I_grid.shape[1] +
                                    self.__I_sink.shape[1])

        self.__I_source = np.asarray(inzidenzmatrix_source)
        self.__I_source_slice = slice(self.__I_grid.shape[1] +
                                      self.__I_sink.shape[1],
                                      self.__I_grid.shape[1] +
                                      self.__I_sink.shape[1] +
                                      self.__I_source.shape[1])

        self.Tamb = 5+273.15  # [K]
        self.producer_v_Pa_set = 10  # dont change this, it
                                     # is not yet implemented in the dependecies!
        
        self.producer_v_Pb_set = 5  # dont change this, 
                                    # it is not yet implemented in the dependecies!
        self.producer_v_Tb_set = 130+273.15  # [K]
        self.consumer_v_Tb_set = 273.15 + 60  # [K]
        self.consumer_v_Q_set = 12000  # [W]


    def gridCalculation(self, x):

        i = 0
        '''
        vector of massflows by solver
        '''
        v_m = x[i: i + self.edges]
        i = i + self.edges
        '''
        vector of pressures by solver
        '''
        v_P = x[i: i + self.nodes]
        i = i + self.nodes
        # pressure from node away
        v_Pa = x[i: i + self.edges]
        i = i + self.edges
        # pressure towards node
        v_Pb = x[i: i + self.edges]
        i = i + self.edges
        '''
        vector of heatflows by solver
        '''
        v_Q = x[i: i + self.edges]
        i = i + self.edges
        '''
        vector of temperatures by solver
        '''
        v_T = x[i: i + self.nodes]
        i = i + self.nodes
        # temperature from node away
        v_Ta = x[i: i + self.edges]
        i = i + self.edges
        # temperature towards node
        v_Tb = x[i: i + self.edges]


        v_Tab = np.zeros_like(v_m)
        v_ma = [1 if i >= 0 else 0 for i in v_m]
        v_mb = [-1 if i < 0 else 0 for i in v_m]

        Iab = np.dot(self.__I_minus, np.diag(v_ma)) +\
            np.dot(self.__I_plus, np.diag(v_mb))

        for index, item in enumerate(v_m):
            if item >= 0:
                v_Tab[index] = v_Ta[index]
            else:
                v_Tab[index] = v_Tb[index]
        '''
        equations of solver
        '''
        # mass balance (I * m)
        massBalance = bl.massBalance(self.__I, v_m)
        massBalance = massBalance[0: self.edges - 1]

        # energy balance 1 (I_plus * diag(m)*T^b + I_minus * diag(m)*T^a)
        energyBalance_1 = bl.energyBalance_1(self.__I_plus, v_m,
                                             v_Tb, self.__I_minus, v_Ta)

        # energy balance 2 (-1 * I_minus.T * T - T^a)
        energyBalance_2 = bl.energyBalance_2(Iab, v_T, v_Tab)

        # impulse balance 1 (-1*I_minus.T*P - P^a)
        impulseBalance_1 = bl.impulseBalance_1(self.__I_minus_T, v_P, v_Pa)

        # impulse balance 2 (I_plus.T*P - P^b)
        impulseBalance_2 = bl.impulseBalance_2(self.__I_plus_T, v_P, v_Pb)
        '''
        constitutive relations
        '''
        # vector of massflow
        pipeMassflow = dp.pipe_massflow(
                                  v_m[self.__I_grid_slice],
                                  v_Ta[self.__I_grid_slice],
                                  v_Tb[self.__I_grid_slice],
                                  v_Q[self.__I_grid_slice])

        consumerMassflow = dp.consumer_massflow(
                                  v_m[self.__I_sink_slice],
                                  v_Ta[self.__I_sink_slice],
                                  v_Tb[self.__I_sink_slice],
                                  v_Q[self.__I_sink_slice])

        producerMassflow = dp.producer_massflow(
                                  v_m[self.__I_source_slice],
                                  v_Ta[self.__I_source_slice],
                                  v_Tb[self.__I_source_slice],
                                  v_Q[self.__I_source_slice])

        pipePress = dp.pipe_press(
                                  v_Pa[self.__I_grid_slice],
                                  v_Pb[self.__I_grid_slice],
                                  v_m[self.__I_grid_slice])

#        producer_Pa = dp.producer_press(
#                                  producer_v_Pa_set,
#                                  v_Pb[self.__I_source_slice])

        producer_Tb = dp.producer_temp(
                              self.producer_v_Tb_set,
                              v_Tb[self.__I_source_slice])

        producer_Pb = dp.producer_press(
                                  self.producer_v_Pb_set,
                                  v_Pa[self.__I_source_slice])

        # temperatur
        consumer_Tb = dp.consumer_temp(
                                  self.consumer_v_Tb_set,
                                  v_Tb[self.__I_sink_slice])

        # heatflow
        pipeQ = dp.pipe_heatflow(
                                  v_Q[self.__I_grid_slice],
                                  v_Ta[self.__I_grid_slice],
                                  v_Tb[self.__I_grid_slice])

        consumer_Q = dp.consumer_heatflow(
                                  self.consumer_v_Q_set,
                                  v_Q[self.__I_sink_slice])

        F = np.concatenate((
                         massBalance,
                         energyBalance_1, energyBalance_2,
                         impulseBalance_1, impulseBalance_2,
                         pipeMassflow, consumerMassflow, producerMassflow,
                         pipePress, producer_Pb,
                         consumer_Tb, producer_Tb,
                         pipeQ, consumer_Q))

        return F

    def getGuess(self, heatgrid, heatsink, heatsource):
        #  TODO update getGuess so it works.

        '''
        vector of massflows by guess
        '''
        v_m = np.zeros(self.edges)
        # massflow
        v_m[self.__I_grid_slice] = -(np.average(heatsink.v_consumers_m))
        v_m[self.__I_sink_slice] = -heatsink.v_consumers_m

        v_m[self.__I_source_slice] = -(np.sum(heatsink.v_consumers_m) /
                                       len(heatsource.producer()))
        '''
        vector of heatflows by guess
        '''
        v_Q = np.zeros(self.edges)
        # heatflows
        v_Q[self.__I_grid_slice] = np.average(heatsink.v_consumers_m)
           #  TODO how to get an array of all heatflows of the consumers?
        v_Q[self.__I_sink_slice] = heatsink.v_consumers_Q
        v_Q[self.__I_source_slice] = -(np.sum(heatsink.v_consumers_m) / 
                                       len(heatsource.producer()))

        '''
        vector of temperatures by guess
        '''
        v_T = np.zeros(self.nodes)
        # temperature from node away
        v_Ta = np.zeros(self.edges)
        v_Ta[self.__I_grid_slice] = self.producer_v_Tb_set
        v_Ta[self.__I_sink_slice] = self.producer_v_Tb_set
        v_Ta[self.__I_source_slice] = self.producer_v_Tb_set
        # temperature towards node
        v_Tb = np.zeros(self.edges)
        v_Tb[self.__I_grid_slice] = self.producer_v_Tb_set
        v_Tb[self.__I_sink_slice] = self.producer_v_Tb_set
        v_Tb[self.__I_source_slice] = self.producer_v_Tb_set

        '''
        vector of pressures by guess
        '''
        v_P = np.zeros(self.nodes)
        # pressure from node away
        v_Pa = np.zeros(self.edges)
        v_Pa[self.__I_grid_slice] = self.producer_v_Pa_set
        v_Pa[self.__I_sink_slice] = self.producer_v_Pa_set
        v_Pa[self.__I_source_slice] = self.producer_v_Pa_set
        # pressure towards node
        v_Pb = np.zeros(self.edges)
        v_Pb[self.__I_grid_slice] = self.producer_v_Pb_set
        v_Pb[self.__I_sink_slice] = self.producer_v_Pb_set
        v_Pb[self.__I_source_slice] = self.producer_v_Pb_set
        print(v_m)
        arr = np.concatenate((v_m, v_P, v_Pa, v_Pb, v_Q, v_T, v_Ta, v_Tb))
        print(arr)
        return arr
