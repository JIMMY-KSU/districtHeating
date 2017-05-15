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
        self.producer_v_Tb_set = 80+273.15  # [K]
        self.consumer_v_Tb_set = 273.15 + 30  # [K]
        self.consumer_v_Q_set = 12000  # [W]

        '''
        vector of massflows
        '''
        v_m = [0] * self.edges

        '''
        vector of heatflows
        '''
        v_Q = [0] * self.edges

        '''
        vector of temperatures
        '''
        v_T = [0] * self.nodes
        # temperature from node away
        v_Ta = [0] * self.edges
        # temperature towards node
        v_Tb = [0] * self.edges

        '''
        vector of pressures
        '''
        v_P = [0] * self.nodes
        # pressure from node away
        v_Pa = [0] * self.edges
        # pressure towards node
        v_Pb = [0] * self.edges

    def gridCalculation(self, x):

        i = 0
        v_m = x[i: i + self.edges]
        i = i + self.edges

        v_P = x[i: i + self.nodes]
        i = i + self.nodes
        v_Pa = x[i: i + self.edges]
        i = i + self.edges

        v_Pb = x[i: i + self.edges]
        i = i + self.edges

        v_T = x[i: i + self.nodes]
        i = i + self.nodes

        v_Ta = x[i: i + self.edges]
        i = i + self.edges

        v_Tb = x[i: i + self.edges]
        i = i + self.edges

        v_Q = x[i: i + self.edges]

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

    def getGuess(heatgrid, heatsink, heatsource):
#  TODO update getGuess so it works.

    averageReturnTemperature = heatsink.averageReturnTemperature()

    guess = np.zeros(6*self.edges + 2*self.nodes)
    n = 0

    # massflow
    v_m = 
    guess[n] = 0.51
    n += 1
    guess[n] = 0.17
    n += 1
    guess[n] = 0.765
    n += 1
    guess[n] = 0.51
    n += 1
    guess[n] = 0.17
    n += 1
    guess[n] = 0.765
    n += 1

    for index, item in enumerate(heatsink.consumer()):
        # TODO make cp variable
        guess[n] = (item.heat_demand*(-1)) / (4182 * (heatsource.producer(0).supply_temperature-item.return_temperature))
        n += 1

    for index, item in enumerate(heatsource.producer()):
        guess[n] = 0.765
        n += 1

    # pressure
    for index, item in enumerate(heatgrid.nodes()):
        if item.SP_RP == 'J':
            guess[n] = heatsource.producer(0).supply_pressure
        elif item.SP_RP == 'N':
            guess[n] = heatsource.producer(0).return_pressure
        else:
            guess[n] = heatsource.producer(0).return_pressure
            print('No value for SP_RP for', item.name, '!')
        n += 1

    # pressure a
    for indexPipe, itemPipe in enumerate(heatgrid.pipes()):
        for indexNode, itemNode in enumerate(heatgrid.nodes()):
            if itemPipe.start_node_name == itemNode.name:
                if itemNode.SP_RP == 'J':
                    guess[n] = heatsource.producer(0).supply_pressure
                elif itemNode.SP_RP == 'N':
                    guess[n] = heatsource.producer(0).return_pressure
                else:
                    guess[n] = heatsource.producer(0).return_pressure
                    print('No value for SP_RP for', item.name, '!')
        n += 1

    for index, item in enumerate(heatsink.consumer()):
        guess[n] = heatsource.producer(0).supply_pressure
        n += 1

    for index, item in enumerate(heatsource.producer()):
        guess[n] = heatsource.producer(0).return_pressure
        n += 1

    # pressure b
    for indexPipe, itemPipe in enumerate(heatgrid.pipes()):
        for indexNode, itemNode in enumerate(heatgrid.nodes()):
            if itemPipe.end_node_name == itemNode.name:
                if itemNode.SP_RP == 'J':
                    guess[n] = heatsource.producer(0).supply_pressure
                elif itemNode.SP_RP == 'N':
                    guess[n] = heatsource.producer(0).return_pressure
                else:
                    guess[n] = heatsource.producer(0).return_pressure
                    print('No value for SP_RP for', item.name, '!')
        n += 1

    for index, item in enumerate(heatsink.consumer()):
        guess[n] = heatsource.producer(0).return_pressure
        n += 1

    for index, item in enumerate(heatsource.producer()):
        guess[n] = heatsource.producer(0).supply_pressure
        n += 1

    # temperature
    for index, item in enumerate(heatgrid.nodes()):
        if item.SP_RP == 'J':
            guess[n] = heatsource.producer(0).supply_temperature
        elif item.SP_RP == 'N':
            guess[n] = averageReturnTemperature
        else:
            guess[n] = heatsource.producer(0).supply_temperature
            print('No value for SP_RP for', item.name, '!')
        print(guess[n])
        n += 1

    # temperature a
    for indexPipe, itemPipe in enumerate(heatgrid.pipes()):
        for indexNode, itemNode in enumerate(heatgrid.nodes()):
            if itemPipe.start_node_name == itemNode.name:
                if itemNode.SP_RP == 'J':
                    guess[n] = heatsource.producer(0).supply_temperature
                elif itemNode.SP_RP == 'N':
                    guess[n] = averageReturnTemperature
                else:
                    guess[n] = heatsource.producer(0).supply_temperature
                    print('No value for SP_RP for', item.name, '!')
        print(guess[n])
        n += 1

    for index, item in enumerate(heatsink.consumer()):
        guess[n] = heatsource.producer(0).supply_temperature
        n += 1

    for index, item in enumerate(heatsource.producer()):
        guess[n] = averageReturnTemperature
        n += 1

    # temperature b
    for indexPipe, itemPipe in enumerate(heatgrid.pipes()):
        for indexNode, itemNode in enumerate(heatgrid.nodes()):
            if itemPipe.end_node_name == itemNode.name:
                if itemNode.SP_RP == 'J':
                    guess[n] = heatsource.producer(0).supply_temperature
                elif itemNode.SP_RP == 'N':
                    guess[n] = averageReturnTemperature
                else:
                    guess[n] = heatsource.producer(0).supply_temperature
                    print('No value for SP_RP for', item.name, '!')
        print(guess[n])
        n += 1

    for index, item in enumerate(heatsink.consumer()):
        guess[n] = item.return_temperature
        n += 1

    for index, item in enumerate(heatsource.producer()):
        guess[n] = heatsource.producer(0).supply_temperature
        n += 1

    # heatflow
    for index, item in enumerate(heatgrid.pipes()):
        guess[n] = -1
        n += 1

    for index, item in enumerate(heatsink.consumer()):
        guess[n] = item.heat_demand
        n += 1

    for index, item in enumerate(heatsource.producer()):
        guess[n] = 225000
        n += 1

    return guess
