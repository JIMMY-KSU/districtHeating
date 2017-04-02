# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 09:14:00 2017

@author: jpelda
"""

import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import root
import math
from Dependencies import Dependencies as dp

Tamb = 5+273.15
v_Pb_set = 5
v_Tb_set = 80+273.15
Tconsumer = 273.15 + 30
Qconsumer = 273.15 + 80
class Solver():
    def __init__(self,nodes_amount, elements_amount,
                 inzidenzmatrix,
                 inzidensmatrix_grid,
                 inzidenzmatrix_sink,
                 inzidenzmatrix_source,
                 v_massflow, v_Q,
                 v_T, v_Ta, v_Tb,
                 v_P, v_Pa, v_Pb):

        self.__nodes_amount = nodes_amount
        self.__elements_amount = elements_amount

        self.__inzidenzmatrix = inzidenzmatrix
        self.__inzidenzmatrix_minus = self.__inzidenzmatrix.clip(max=0)
        self.__inzidenzmatrix_plus = self.__inzidenzmatrix.clip(min=0)

        self.__inzidenzmatrix_grid = inzidenzmatrix_grid
        self.__elements_location_grid = np.arange(len(inzidenzmatrix_grid))

        self.__inzidenzmatrix_sink = inzidenzmatrix_sink
        self.__elements_location_sink = np.arange(len(inzidenzmatrix_grid) + 1,
                                  len(inzidenzmatrix_grid) + 1 +
                                  len(inzidenzmatrix_sink))

        self.__inzidenzmatrix_source = inzidenzmatrix_source
        self.__elements_location_source = np.arange(len(inzidenzmatrix_grid)+
                                             len(inzidenzmatrix_sink) + 1,
                                             len(inzidenzmatrix_grid) +
                                             len(inzidenzmatrix_sink) + 1 +
                                             len(inzidenzmatrix_source))

        self.v_massflow = np.asarray(v_massflow)
        self.v_Q = np.asarray(v_Q)
        self.v_T = np.asarray(v_T)
        self.v_Ta = np.asarray(v_Ta)
        self.v_Tb = np.asarray(v_Tb)
        self.v_P = np.asarray(v_P)
        self.v_Pa = np.asarray(v_Pa)
        self.v_Pb = np.asarray(v_Pb)
        
        pass
    
    def gridCalculation_thermical(self, x, args):

        i = 0
        v_massflow = x[i: i + len(self.v_massflow)]
        i = i + len(self.v_massflow)
        v_P = x[i: i + len(self.v_P)]
        i = i + len(self.v_P)
        v_Pa = x[i: i + len(self.v_Pa)]
        i = i + len(self.v_Pa)
        v_Pb = x[i: i + len(self.v_Pb)]
        i = i + len(self.v_Pb)
        v_T = x[i: i + len(self.v_T)]
        i = i + len(self.v_T)
        v_Ta = x[i: i + len(self.v_Ta)]
        i = i + len(self.v_Tb)
        v_Tb = x[i: i + len(self.v_Tb)]
        i = i + len(self.v_Tb)
        v_Q = x[i: i + len(self.v_Q)]
    
        F = np.zeros(2 * self.nodes + 6 * self.elements)

        i = 0
        # mass balance M/M
        j = self.nodes
        F[i:i+j] = np.dot(self.inzidenzmatrix, v_massflow)
        i = i+j-1

        # temperature balance TbM/TaM
        #j = self.nodes
        F[i:i+j] = np.dot(
                self.inzidenzmatrix_plus, v_massflow*v_Tb) +\
                np.dot(
                self.inzidenzmatrix_minus, v_massflow*v_Ta)
        i = i+j

        # energy balance T/Ta
        j = self.elements
        F[i:i+j] = np.dot(-1*self.inzidenzmatrix_minus.T, v_T) -\
                          v_Ta
        i = i+j

        # impulse balance P/Pa
        #j=self.elements
        F[i:i+j] = np.dot(-1*self.inzidenzmatrix_minus.T, v_P) - v_Pa
        i = i+j

        # impulse balance P/Pb
        F[i:i+j] = np.dot(self.inzidenzmatrix_plus.T, v_P) - v_Pb
        i = i+j


        F[i:i+len(self.__elements_location_source)] = dp.dependencies_producer_massflow(
                v_massflow[min(self.__elements_location_source):
                           max(self.__elements_location_source)+1],
                v_Ta[min(self.__elements_location_source):
                     max(self.__elements_location_source)+1],
                v_Tb[min(self.__elements_location_source):
                     max(self.__elements_location_source+1)],
                v_Q[min(self.__elements_location_source):
                    max(self.__elements_location_source)+1])
        i = i + len(self.__elements_location_source)

        F[i:i+len(self.__elements_location_source)] = dp.dependencies_producer_press(
                v_Pb_set, v_Pb[min(self.__elements_location_source):
                              max(self.__elements_location_source)+1])
        i = i + len(self.__elements_location_source)
        
        F[i:i+len(self.__elements_location_source)] = dp.dependencies_producer_temp(
                v_Tb_set, v_Tb[min(self.__elements_location_source):
                               max(self.__elements_location_source)+1])
        i = i + len(self.__elements_location_source)
        
        F[i:i+len(self.__elements_location_grid)] = dp.dependencies_pipe_press(
                v_Pa[min(self.__elements_location_grid):
                     max(self.__elements_location_grid)+1],
                v_Pb[min(self.__elements_location_grid):
                     max(self.__elements_location_grid)+1],
                v_massflow[min(self.__elements_location_grid):
                           max(self.__elements_location_grid)+1])
        i = i + len(self.__elements_location_grid)

        F[i:i+len(self.__elements_location_grid)] = dp.dependencies_pipe_Q(
                v_Q[min(self.__elements_location_grid),
                    max(self.__elements_location_grid)+1],
                v_Ta[min(self.__elements_location_grid),
                     max(self.__elements_location_grid)+1],
                v_Tb[min(self.__elements_location_grid),
                     max(self.__elements_location_grid)+1],
                Tamb)
        i = i + len(self.__elements_location_grid)
        
        F[i:i+len(self.__elements_location_grid)] = dp.dependencies_pipe_massflow(
                v_massflow[min(self.__elements_location_grid),
                           max(self.__elements_location_grid)+1],
                v_Ta[min(self.__elements_location_grid),
                     max(self.__elements_location_grid)+1],
                v_Tb[min(self.__elements_location_grid),
                     max(self.__elements_location_grid)+1],
                v_Q[min(self.__elements_location_grid),
                    max(self.__elements_location_grid)+1])
        i = i + len(self.__elements_location_grid)

        F[i:i+len(self.__elements_location_sink)] = dp.dependencies_consumer_massflow(
                v_massflow[min(self.__elements_location_sink),
                           max(self.__elements_location_sink)+1],
                v_Ta[min(self.__elements_location_sink),
                     max(self.__elements_location_sink)+1],
                v_Tb[min(self.__elements_location_sink),
                     max(self.__elements_location_sink)+1],
                v_Q[min(self.__elements_location_sink),
                    max(self.__elements_location_sink)+1])
        i = i + len(self.__elements_location_sink)

        F[i:i+len(self.__elements_location_sink)] = dp.dependencies_consumer_press(
                v_Pa[min(self.__elements_location_sink),
                     max(self.__elements_location_sink)+1],
                v_Pb[min(self.__elements_location_sink),
                     max(self.__elements_location_sink)+1],
                v_massflow[min(self.__elements_location_sink),
                     max(self.__elements_location_sink)+1])
        i = i + len(self.__elements_location_sink)

        F[i:i+len(self.__elements_location_sink)] = dp.dependencies_consumer_temp(
                Tconsumer,
                v_Tb[min(self.__elements_location_sink),
                     max(self.__elements_location_sink)+1])
        i = i + len(self.__elements_location_sink)

        F[i:i+len(self.__elements_location_sink)] = dp.dependencies_consumer_Q(
                Qconsumer,
                v_Q[min(self.__elements_location_sink),
                    max(self.__elements_location_sink)+1])

        return F

if __name__=="__main__":
    print('DistrictHeatingSystem run directly')

    xGuess = np.array((57, 57, 57, 57,  # massflow
                       7, 7, 7, 7,  # pressure
                       7, 7, 7, 7,  # Pa
                       7, 7, 7, 7,  # Pb
                       80+273.15, 80+273.15, 15+273.15, 15+273.15,  # T
                       15+273.15, 80+273.15, 80+273.15, 15+273.15,  # Ta
                       80+273.15, 80+273.15, 15+273.15, 15+273.15,  # Tb
                       12000, 0, -12000, 0  # heatflow
                       ))

    initialValues_heatflow = 12000
    solution = fsolve(gridCalculation_thermical, xGuess, args)
    
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
    
    print('numbers of unknown variables: ' + str(len(solution)))
    print('numbers of equations: ' + str(len(gridCalculation_thermical(xGuess, args))))

else:
    print('DistrictHeatingSystem was imported into another module')

