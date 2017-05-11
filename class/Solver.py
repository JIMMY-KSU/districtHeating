# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 09:14:00 2017

@author: jpelda
"""

import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import root
import math
import Dependencies as dp
import Balances as bc

Tamb = 5+273.15
v_Pb_set = 5
v_Tb_set = 80+273.15
Tconsumer = 273.15 + 30
Qconsumer = 12000  # [W]
class Solver():
    def __init__(self,nodes_count, elements_count,
                 inzidenzmatrix,
                 inzidenzmatrix_grid,
                 inzidenzmatrix_sink,
                 inzidenzmatrix_source,
                 v_massflow, v_Q,
                 v_T, v_Ta, v_Tb,
                 v_P, v_Pa, v_Pb):

        self.__nodes_count = nodes_count
        self.__elements_count = elements_count

        self.__inzidenzmatrix = np.asarray(inzidenzmatrix)
        self.__inzidenzmatrix_minus = self.__inzidenzmatrix.clip(max=0)
        self.__inzidenzmatrix_minus_T = self.__inzidenzmatrix_minus.T
        self.__inzidenzmatrix_plus = self.__inzidenzmatrix.clip(min=0)
        self.__inzidenzmatrix_plus_T = self.__inzidenzmatrix_plus.T

        self.__inzidenzmatrix_grid = np.asarray(inzidenzmatrix_grid)
        self.__grid_len1dimofInzidenz = self.__inzidenzmatrix_grid.shape[1]
        self.__grid_rangeInInzidenz = slice(0, self.__grid_len1dimofInzidenz)

        self.__inzidenzmatrix_sink = np.asarray(inzidenzmatrix_sink)
        self.__sink_len1dimofInzidenz = self.__inzidenzmatrix_sink.shape[1]
        self.__sink_rangeInInzidenz = slice(self.__grid_len1dimofInzidenz,
                                            self.__grid_len1dimofInzidenz +
                                            self.__sink_len1dimofInzidenz)

        self.__inzidenzmatrix_source = np.asarray(inzidenzmatrix_source)
        self.__source_len1dimofInzidenz = self.__inzidenzmatrix_source.shape[1]
        self.__source_rangeInInzidenz = slice(self.__grid_len1dimofInzidenz+
                                              self.__sink_len1dimofInzidenz,
                                              self.__grid_len1dimofInzidenz +
                                              self.__sink_len1dimofInzidenz +
                                              self.__source_len1dimofInzidenz)

        self.v_massflow = np.asarray(v_massflow)
        self.v_Q = np.asarray(v_Q)
        self.v_T = np.asarray(v_T)
        self.v_Ta = np.asarray(v_Ta)
        self.v_Tb = np.asarray(v_Tb)
        self.v_P = np.asarray(v_P)
        self.v_Pa = np.asarray(v_Pa)
        self.v_Pb = np.asarray(v_Pb)

    def gridCalculation_thermical(self, x):

        i = 0
        j = i + len(self.v_massflow)
        v_massflow = x[i: j]
        i = j

        j = i + len(self.v_P)
        v_P = x[i: j]
        i = j

        j = i + len(self.v_Pa)
        v_Pa = x[i: j]
        i = j

        j = i + len(self.v_Pb)
        v_Pb = x[i: j]
        i = j

        j = i + len(self.v_T)
        v_T = x[i: j]
        i = j

        j = i + len(self.v_Ta)
        v_Ta = x[i: j]
        i = j

        j = i + len(self.v_Tb)
        v_Tb = x[i: j]
        i = j

        j = i + len(self.v_Q)
        v_Q = x[i: j]
        print(v_massflow, v_P, v_Pa, v_Pb, v_T, v_Ta, v_Tb, v_Q)
        '''
        following initialising all balances
        '''
        # mass balance (I * m)
        massBalance = bc.massBalance(self.__inzidenzmatrix, v_massflow)
        massBalance = massBalance[0:len(massBalance)-1]

        # energy balance (I_plus * diag(m)*T^b + I_minus * diag(m)*T^a)
        energyBalance_1 = bc.energyBalance_1(
                self.__inzidenzmatrix_plus, v_massflow, v_Tb,
                self.__inzidenzmatrix_minus, v_Ta)

        # energy balance (-1 * I_minus.T * T - T^a)
        energyBalance_2 = bc.energyBalance_2(
                self.__inzidenzmatrix_minus_T, v_T, v_Ta)

        # impulse balance (-1*I_minus.T*P - P^a)
        impulseBalance_1 = bc.impulseBalance_1(
                self.__inzidenzmatrix_minus_T, v_P, v_Pa)

        # impulse balance I_plus.T*P - P^b
        impulseBalance_2 = bc.impulseBalance_2(
                self.__inzidenzmatrix_plus_T, v_P, v_Pb)

        '''
        following initialising all dependencies
        '''

        producerMassflow = dp.producer_massflow(
            v_massflow[self.__source_rangeInInzidenz],
            v_Ta[self.__source_rangeInInzidenz],
            v_Tb[self.__source_rangeInInzidenz],
            v_Q[self.__source_rangeInInzidenz])

        producerPress = dp.producer_press(
            v_Pb_set, v_Pb[self.__source_rangeInInzidenz])

        producerTemp = dp.producer_temp(
                v_Tb_set, v_Tb[self.__source_rangeInInzidenz])

        pipePress = dp.pipe_press(
                v_Pa[self.__grid_rangeInInzidenz],
                v_Pb[self.__grid_rangeInInzidenz],
                v_massflow[self.__grid_rangeInInzidenz])

        pipeQ = dp.pipe_Q(
                v_Q[self.__grid_rangeInInzidenz],
                v_Ta[self.__grid_rangeInInzidenz],
                v_Tb[self.__grid_rangeInInzidenz],
                Tamb)

        pipeMassflow = dp.pipe_massflow(
                v_massflow[self.__grid_rangeInInzidenz],
                v_Ta[self.__grid_rangeInInzidenz],
                v_Tb[self.__grid_rangeInInzidenz],
                v_Q[self.__grid_rangeInInzidenz])

        consumerMassflow = dp.consumer_massflow(
            v_massflow[self.__sink_rangeInInzidenz],
            v_Ta[self.__sink_rangeInInzidenz],
            v_Tb[self.__sink_rangeInInzidenz],
            v_Q[self.__sink_rangeInInzidenz])

        consumerPress = dp.consumer_press(
                v_Pa[self.__sink_rangeInInzidenz],
                v_Pb[self.__sink_rangeInInzidenz],
                v_massflow[self.__sink_rangeInInzidenz])

        consumerTemp = dp.consumer_temp(
                Tconsumer,
                v_Tb[self.__sink_rangeInInzidenz])

        consumerQ = dp.consumer_Q(
                -5000,
                v_Q[self.__sink_rangeInInzidenz])
#        print(massBalance.shape, energyBalance_1.shape, energyBalance_2.shape,
#              impulseBalance_1.shape, impulseBalance_2.shape, producerMassflow.shape,
#              producerPress.shape, producerTemp.shape, pipeMassflow.shape,
#              pipePress.shape, pipeQ.shape, consumerMassflow.shape,
#              consumerPress.shape, consumerQ.shape, consumerTemp.shape)
        F = np.concatenate((massBalance,
                            energyBalance_1, energyBalance_2,
                            impulseBalance_1, impulseBalance_2,
                            producerMassflow, producerPress, producerTemp,
                            pipeMassflow, pipePress, pipeQ,
                            consumerMassflow, consumerPress, consumerQ,
                            consumerTemp))
        return F

if __name__ == "__main__":
    print('DistrictHeatingSystem run directly')

    inzidenzmatrix = [[1,-1,0,0],[0,1,-1,0],[0,0,1,-1],[-1,0,0,1]]
    inzidenzmatrix_grid = [[-1,0],[1,0],[0,-1],[0,1]]
    inzidenzmatrix_sink = [[0],[-1],[1],[0]]
    inzidenzmatrix_source = [[1],[0],[0],[-1]]

    inzidenzmatrix = np.concatenate((inzidenzmatrix_grid,
                                          inzidenzmatrix_sink,
                                          inzidenzmatrix_source),
                                          axis=1)

    nodes_amount = 4
    elements_amount =4

    v_massflow = [10,10,10,10]
    v_Q = [5000,2,1,-5000]
    v_T = [80+273.15,30+273.15,80+273.15,30+273.15]
    v_Ta = [3,3,3,3]
    v_Tb = [0]*elements_amount
    v_P = [0]*nodes_amount
    v_Pa = [0]*elements_amount
    v_Pb = [0]*elements_amount

    x = np.asarray(v_massflow + v_P + v_Pa + v_Pb + v_T + v_Ta + v_Tb + v_Q)

    solveGrid = Solver(nodes_amount, elements_amount,
                       inzidenzmatrix,
                       inzidenzmatrix_grid,
                       inzidenzmatrix_sink,
                       inzidenzmatrix_source,
                       v_massflow, v_Q, v_T, v_Ta, v_Tb, v_P, v_Pa, v_Pb)

    solution = fsolve(solveGrid.gridCalculation_thermical, x)
    
    massflow = 'Massflow: \t'
    pressure = 'Pressure P: \t'
    pressureA = 'Pressure Pa: \t'
    pressureB = 'Pressure Pb: \t'
    temperature = 'Temperature T: \t'
    temperatureA = 'Temperature Ta: '
    temperatureB = 'Temperature Tb: '
    heatflow = 'Heatflow Q: \t'
    arrayNames = [massflow, pressure, pressureA,
                  pressureB, temperature, temperatureA,
                  temperatureB, heatflow]
    
    i = -1
    j = 1
    for index, item in enumerate(solution):
        j = j + 1
        if index % 4 == 0:
            i = i + 1
            j = 1
        print(str(arrayNames[i]) + str(j) + '  |  ' + str(item))
    
#    print('numbers of unknown variables: ' + str(len(solution)))
#    print('numbers of equations: ' + str(len(gridCalculation_thermical(xGuess, args))))

else:
    print('DistrictHeatingSystem was imported into another module')

