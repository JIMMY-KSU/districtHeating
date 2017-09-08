7# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 14:45:18 2017

@author: narand
"""
import os
import sys
sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'function')
import dependencies as dp
import numpy as np
from inzidenzmatrix import inzidenzmatrix
import time
from scipy.optimize import root
from scipy.linalg import solve

class Solver():
    def __init__(self, heatgrid, heatsink, heatsource):

        self.heatgrid = heatgrid
        self.heatsink = heatsink
        self.heatsource = heatsource
        self._inzidenzmatrix_HeatGrid = self.__inzidenzmatrix_HeatGrid()
        self._inzidenzmatrix_HeatSink = self.__inzidenzmatrix_HeatSink()
        self._inzidenzmatrix_HeatSource = self.__inzidenzmatrix_HeatSource()
        #TODO calculate inzidenzmatrix outof previous inzidenzmatrizen with np.hstack
        self._inzidenzmatrix = self.__inzidenzmatrix()
        self._elements = np.shape(self._inzidenzmatrix)[1]
        self._nodes = np.shape(self._inzidenzmatrix)[0]

        '''
        sets up all necessary inzmatrices
        '''
        self.myslice = slice(1,1000)
        self.__I = np.asarray(self._inzidenzmatrix)
        self.__I_minus = self.__I.clip(max=0)
        self.__I_minus_T = self.__I_minus.T
        self.__I_plus = self.__I.clip(min=0)
        self.__I_plus_T = self.__I_plus.T

        self.__I_grid = np.asarray(self._inzidenzmatrix_HeatGrid)
        self.__I_grid_slice = slice(0, self.__I_grid.shape[1])

        self.__I_sink = np.asarray(self._inzidenzmatrix_HeatSink)
        self.__I_sink_slice = slice(self.__I_grid.shape[1],
                                    self.__I_grid.shape[1] +
                                    self.__I_sink.shape[1])

        self.__I_source = np.asarray(self._inzidenzmatrix_HeatSource)
        self.__I_source_slice = slice(self.__I_grid.shape[1] +
                                      self.__I_sink.shape[1],
                                      self.__I_grid.shape[1] +
                                      self.__I_sink.shape[1] +
                                      self.__I_source.shape[1])

        self.slice_v_m, self.slice_v_P, self.slice_v_Pa,\
            self.slice_v_Pb, self.slice_v_Q, self.slice_v_T,\
            self.slice_v_Ta, self.slice_v_Tb = self.__xSlicesOfVectors()

        self.Tamb = 5+273.15  # [K]
        self.cp = 4182  # J/(kg*K)
        self.v_pipes_resistivity = self.heatgrid.v_pipes_resistivity

        self.v_Zeta = 0.2
        self.rho = 1000
        self.g = 9.81
        self.v_producer_Pa_set = self.heatsource.v_producers_Pa
        self.v_producer_Pb_set = self.heatsource.v_producers_Pb
#        self.run = 0
        self.solver_i = 0

        self.getGuessFirstRun = 1  # if this value is 1, then the guess is
# calculated, otherwise guess comes from the former calculated values
# from heatsink, heatsource and heatgrid.

    def __inzidenzmatrix_HeatGrid(self):
        '''
        returns an inzidenzmatrix of HeatGrid, where pipes are col
        and nodes are row
        '''
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

        try:
            arr_col = np.vstack((
                    self.heatgrid.v_pipes_esNode,
                    self.heatsink.v_consumers_esNode,
                    self.heatsource.v_producers_esNode))

        except ValueError:
            print("Error in __inzidenzmatrix")

        inzMatrix = inzidenzmatrix(self.heatgrid.v_nodes_name, arr_col,
                                   inzidenzmatrix_name="all")

        return inzMatrix

    def gridCalculation(self, x):
        '''
        alternative for np.dot(a,b) whould be a@b but it is not faster:
            10000000 iterations with np.dot(a,b) = 8.7978 sec
            10000000 iterations with a@b = 13.8919 sec
        '''
        print('\r' + str(self.solver_i), end='')
        self.solver_i = self.solver_i + 1

#        if self.run == 20:
#            sec = 30
#            while sec > 0:
#                print("\rpause of %i sec" %sec, end=' ')
#
#                time.sleep(1)    # pause 5.5 seconds
#                sec = sec - 1
#            self.run = 0
#        self.run = self.run + 1
        '''
        vector of massflows by solver
        '''
        v_m = x[self.slice_v_m]

        '''
        vector of pressures by solver
        '''
        v_P = x[self.slice_v_P]
        # pressure from node away
        v_Pa = x[self.slice_v_Pa]
        # pressure towards node
        v_Pb = x[self.slice_v_Pb]

        '''
        vector of heatflows by solver
        '''
        v_Q = x[self.slice_v_Q]

        '''
        vector of temperatures by solver
        '''
        v_T = x[self.slice_v_T]
        # temperature from node away
        v_Ta = x[self.slice_v_Ta]
        # temperature towards node
        v_Tb = x[self.slice_v_Tb]

        v_m_ceiled = np.ceil(v_m)
        v_ma = v_m_ceiled.clip(min=0, max=1)
        v_m_floored = np.floor(v_m)
        v_mb = v_m_floored.clip(min=-1, max=0)

        Iab = np.dot(self.__I_minus, np.diag(v_ma)) +\
            np.dot(self.__I_plus, np.diag(v_mb))

        v_Tab = v_Ta * v_ma
        v_Tab = v_Tab + v_Tb * (v_mb * -1)

        '''
        ########
        balances
        ########
        '''
        '''
        mass balance (I * m)
        '''
    #    print('massbalance %s' %type(v_m))
        massBalance = np.dot(self.__I, v_m)
        massBalance = massBalance[0: len(massBalance) - 1]

        '''
        energy balance 1 (I_plus * diag(m)*T^b + I_minus * diag(m)*T^a)
        '''
        energyBalance_1 = np.dot(self.__I_plus, np.dot(np.diag(v_m), v_Tb)) +\
            np.dot(self.__I_minus, np.dot(np.diag(v_m), v_Ta))

        '''
        energy balance (I_ab.T * v_T + v_Tab)
        '''
        energyBalance_2 = np.dot(np.transpose(Iab), v_T) + v_Tab
#        energyBalance_2 = np.dot(-1*np.transpose(self.__I_minus), v_T) - v_Ta

        '''
        impulse balance (-1*I_minus.T*P - P^a)
        '''
        impulseBalance_1 = np.dot(self.__I_minus_T, v_P) + v_Pa

        '''
        impulse balance I_plus.T*P - P^b
        '''
        impulseBalance_2 = np.dot(self.__I_plus_T, v_P) - v_Pb

        '''
        ######################
        constitutive relations
        ######################
        '''
        '''
        dependencies for pipes
        '''
        # massflow
        massflows = v_m * self.cp * (v_Tb - v_Ta) - v_Q

        # heatflow
        pipeQ = self.v_pipes_resistivity * (self.Tamb - (
            v_Ta[self.__I_grid_slice] + v_Tb[self.__I_grid_slice]) / 2)\
            - v_Q[self.__I_grid_slice]

        # pressure
        pipePress = (v_Pa[self.__I_grid_slice] - v_Pb[self.__I_grid_slice]) *\
            100000 - self.v_Zeta * v_m[self.__I_grid_slice] *\
            abs(v_m[self.__I_grid_slice]) + self.rho * self.g *\
            (self.heatgrid.v_pipes_sHeight -
             self.heatgrid.v_pipes_eHeight)

        '''
        dependencies for consumer
        '''
        # heatflow
        consumer_Q = self.heatsink.v_consumers_Q - v_Q[self.__I_sink_slice]
        # temperature
        consumer_Tb = self.heatsink.v_consumers_Tb -\
            v_Tb[self.__I_sink_slice]

        '''
        dependencies for producer
        '''
        # temperature
        producer_Tb = self.heatsource.v_producers_Tb -\
            v_Tb[self.__I_source_slice]
        # pressure
        producer_Pb = dp.producer_press(
                          self.v_producer_Pb_set,
                          v_Pb[self.__I_source_slice])
        producer_Pa = dp.producer_press(
                            self.v_producer_Pa_set,
                            v_Pa[self.__I_source_slice])

        F = np.concatenate((
                         massBalance,
                         energyBalance_1, energyBalance_2,
                         impulseBalance_1, impulseBalance_2,
                         massflows,
                         pipePress, producer_Pb, producer_Pa,
                         consumer_Tb, producer_Tb,
                         pipeQ, consumer_Q))

        return F

    def getGuess(self):
        print("Getting guess for solver")
        if self.getGuessFirstRun is 1:

            '''
            vector of massflows by guess in the first run
            '''
            v_m = np.zeros(self._elements)
            # massflow
#            val = np.sum(-self.__I_sink *
#                                  self.heatsink.v_consumers_m, axis=1)
#            print(val)
#            iMatrix = iMatrix[:, [self.__I_grid_slice, self.__I_source_slice]]
#            ''' The pseudo-inverse of a matrix A, denoted A^+, is defined as:
#            “the matrix that ‘solves’ [the least-squares problem] Ax = b,”
#            i.e., if \bar{x} is said solution, then A^+ is that matrix such
#            that \bar{x} = A^+b.'''
            iMatrix_pseudo = np.linalg.pinv(np.hstack((self.__I_grid,
                                                       self.__I_source)))
            v_m_guess = v_m
            v_m_guess[self.__I_sink_slice] = self.heatsink.v_consumers_m
            v_m = np.dot(iMatrix_pseudo, v_m_guess)

#            print(val)
#            print(iMatrix_pseudo)
            print(v_m)
#            v_m = np.hstack((v_m[self.__I_grid_slice], v_))
#            print('Matrix:')
#            print(iMatrix_pseudo)
#            print('val')
#            print(val)
#            print('v_m')
#            print(v_m)

#            v_m[self.__I_grid_slice] = np.average(self.heatsink.v_consumers_m)
#            v_m[self.__I_sink_slice] = self.heatsink.v_consumers_m
#            v_m[self.__I_source_slice] = (np.sum(self.heatsink.v_consumers_m) /
#                                          len(self.heatsource.producers()))

            '''
            vector of temperatures by guess
            '''
            v_T = np.zeros(self._nodes)
            v_Ta = np.zeros(self._elements)
            v_Tb = np.zeros(self._elements)

            '''set guess temperature for supply and return pipes'''
            for index, item in enumerate(self.heatgrid.v_nodes_sprp):

                try:
                    if item == 1:
                        v_T[index] = np.average(self.heatsource.v_producers_Tb)
                    elif item == 0:
                        v_T[index] = np.sum(self.heatsink.v_consumers_Tb *
                                            self.heatsink.v_consumers_m) /\
                                            np.sum(self.heatsink.v_consumers_m)
                except ValueError:
                    print("Guess for temperature of nodes failed!")

            '''set guess temperature for supply and return pipes'''
            for index, item in enumerate(self.heatgrid.v_pipes_sprp):

                try:
                    if item == 1:
                        v_Ta[self.__I_grid_slice][index] =\
                            np.average(self.heatsource.v_producers_Tb)
                        v_Tb[self.__I_grid_slice][index] =\
                            v_Ta[self.__I_grid_slice][index]

                    elif item == 0:
                        v_Ta[self.__I_grid_slice][index] =\
                             np.sum(self.heatsink.v_consumers_Tb *
                                    self.heatsink.v_consumers_m) /\
                             np.sum(self.heatsink.v_consumers_m)
                        v_Tb[self.__I_grid_slice][index] =\
                            v_Ta[self.__I_grid_slice][index]
                except ValueError:
                    print("Guess for temperature of pipes failed!")

            '''temperature Ta'''
            v_Ta[self.__I_sink_slice] = np.average(
                    self.heatsource.v_producers_Tb)
            v_Ta[self.__I_source_slice] = np.sum(
                    self.heatsink.v_consumers_m *
                    self.heatsink.v_consumers_Tb) /\
                np.sum(self.heatsink.v_consumers_m)
            '''temperature Tb'''
            v_Tb[self.__I_sink_slice] = self.heatsink.v_consumers_Tb
            v_Tb[self.__I_source_slice] = self.heatsource.v_producers_Tb

            '''
            vector of heatflows by guess
            '''
            v_Q = np.zeros(self._elements)
            # heatflows
            v_Q[self.__I_grid_slice] = self.v_pipes_resistivity * (
                    self.Tamb - v_Ta[self.__I_grid_slice])
            v_Q[self.__I_sink_slice] = self.heatsink.v_consumers_Q
            v_Q[self.__I_source_slice] = np.abs(
                    (np.sum(self.heatsink.v_consumers_Q) /
                     len(self.heatsource.producers())))

            '''
            vector of pressures by guess
            '''
            v_P = np.zeros(self._nodes)

            v_Pa = np.zeros(self._elements)
            v_Pb = np.zeros(self._elements)

            '''set guess temperature for supply and return nodes'''
            for index, item in enumerate(self.heatgrid.v_nodes_sprp):
                try:
                    if item == 1:
                        v_P[index] = np.average(self.heatsource.v_producers_Pb)
                    elif item == 0:
                        v_P[index] = np.average(self.heatsource.v_producers_Pa)
                except ValueError:
                    print("Guess for pressure of nodes faile!")

            '''set guess temperature for supply and return pipes'''
            for index, item in enumerate(self.heatgrid.v_pipes_sprp):
                try:
                    if item == 1:
                        v_Pa[self.__I_grid_slice][index] =\
                            np.average(self.heatsource.v_producers_Pb)
                        v_Pb[self.__I_grid_slice][index] =\
                            v_Pa[self.__I_grid_slice][index]
                    elif item == 0:
                        v_Pa[self.__I_grid_slice][index] =\
                            np.average(self.heatsource.v_producers_Pa)
                        v_Pb[self.__I_grid_slice][index] =\
                            v_Pa[self.__I_grid_slice][index]
                except ValueError:
                    print("Guess for pressure of pipes failed!")

            # pressure Pa
            v_Pa[self.__I_sink_slice] = np.average(
                                        self.heatsource.v_producers_Pb)
            v_Pa[self.__I_source_slice] = self.heatsource.v_producers_Pa
            # pressure Pb
            v_Pb[self.__I_sink_slice] = np.average(
                                        self.heatsource.v_producers_Pa)
            v_Pb[self.__I_source_slice] = np.average(
                    self.heatsource.v_producers_Pb)

        elif self.getGuessFirstRun is 0:
            v_m = self.heatgrid.v_pipes_m +\
                self.heatsink.v_consumers_m +\
                self.heatsource.v_producers_m
            v_P = self.heatgrid.v_nodes_P
            v_Pa = self.heatgrid.v_pipes_Pa +\
                self.heatsink.v_consumers_Pa +\
                self.heatsource.v_producers_Pa
            v_Pb = self.heatgrid.v_pipes_Pb +\
                self.heatsink.v_consumers_Pb +\
                self.heatsource.v_producers_Pb
            v_Q = self.heatgrid.v_pipes_Q +\
                self.heatsink.v_consumers_Q +\
                self.heatsource.v_producers_Q
            v_T = self.heatgrid.v_nodes_T
            v_Ta = self.heatgrid.v_pipes_Ta +\
                self.heatsink.v_consumers_Ta +\
                self.heatsource.v_producers_Ta
            v_Tb = self.heatgrid.v_pipes_Tb +\
                self.heatsink.v_consumers_Tb +\
                self.heatsource.v_producers_Tb
#        for item in v_m:
#            print('????????????? v_m %f \n'%item)
#        for item in v_P:
#            print('????????????? v_P %f \n'%item)
#        for item in v_Pa:
#            print('????????????? v_Pa %f \n'%item)
#        for item in v_Pb:
#            print('????????????? v_Pb %f \n'%item)
#        for item in v_Q:
#            print('????????????? v_Q %f \n'%item)
#        for item in v_T:
#            print('????????????? v_T %f \n'%item)
#        for item in v_Ta:
#            print('????????????? v_Ta %f \n'%item)
#        for item in v_Tb:
#            print('????????????? v_Tb %f \n'%item)

        x = np.concatenate((v_m, v_P, v_Pa, v_Pb, v_Q, v_T, v_Ta, v_Tb))

#        print("Guess for solver \t----> OK")
        return x

    def __xSlicesOfVectors(self):
        '''
        Set slices that split x into v_m, v_P ... .
        '''
        i = 0
        slice_v_m = slice(0, i + self._elements)
        i = i + self._elements
        slice_v_P = slice(i, i + self._nodes)
        i = i + self._nodes
        slice_v_Pa = slice(i, i + self._elements)
        i = i + self._elements
        slice_v_Pb = slice(i, i + self._elements)
        i = i + self._elements

        slice_v_Q = slice(i, i + self._elements)
        i = i + self._elements

        slice_v_T = slice(i, i + self._nodes)
        i = i + self._nodes
        slice_v_Ta = slice(i, i + self._elements)
        i = i + self._elements
        slice_v_Tb = slice(i, i + self._elements)
        i = i + self._elements

        return slice_v_m, slice_v_P, slice_v_Pa, slice_v_Pb, slice_v_Q,\
            slice_v_T, slice_v_Ta, slice_v_Tb

    def __xToSingleVectorsAndVectorsToElementtypes(self, x):
        '''
        Splits the solver vextor x into its parts v_m, v_P, v_Pa etc
        input: x
        output: v_m, v_P, v_Pa, v_Pb, v_Q, v_T, v_Ta, v_Tb
        '''
        v_m = x[self.slice_v_m]
        v_P = x[self.slice_v_P]
        v_Pa = x[self.slice_v_Pa]
        v_Pb = x[self.slice_v_Pb]

        v_Q = x[self.slice_v_Q]

        v_T = x[self.slice_v_T]
        v_Ta = x[self.slice_v_Ta]
        v_Tb = x[self.slice_v_Tb]

        pipe_m = v_m[self.__I_grid_slice]
        pipe_Pa = v_Pa[self.__I_grid_slice]
        pipe_Pb = v_Pb[self.__I_grid_slice]
        pipe_Ta = v_Ta[self.__I_grid_slice]
        pipe_Tb = v_Tb[self.__I_grid_slice]
        pipe_Q = v_Q[self.__I_grid_slice]

        consumer_m = v_m[self.__I_sink_slice]
        consumer_Pa = v_Pa[self.__I_sink_slice]
        consumer_Pb = v_Pb[self.__I_sink_slice]
        consumer_Ta = v_Ta[self.__I_sink_slice]
        consumer_Tb = v_Tb[self.__I_sink_slice]
        consumer_Q = v_Q[self.__I_sink_slice]

        producer_m = v_m[self.__I_source_slice]
        producer_Pa = v_Pa[self.__I_source_slice]
        producer_Pb = v_Pb[self.__I_source_slice]
        producer_Ta = v_Ta[self.__I_source_slice]
        producer_Tb = v_Tb[self.__I_source_slice]
        producer_Q = v_Q[self.__I_source_slice]

        v_P = v_P
        v_T = v_T

        return pipe_m, pipe_Pa, pipe_Pb, pipe_Q, pipe_Ta, pipe_Tb,\
            consumer_m, consumer_Pa, consumer_Pb, consumer_Q, consumer_Ta,\
            consumer_Tb, producer_m, producer_Pa, producer_Pb, producer_Q,\
            producer_Ta, producer_Tb, v_P, v_T

    def save_x(self, x):

        pipe_m, pipe_Pa, pipe_Pb, pipe_Q, pipe_Ta, pipe_Tb,\
            consumer_m, consumer_Pa, consumer_Pb, consumer_Q, consumer_Ta,\
            consumer_Tb, producer_m, producer_Pa, producer_Pb, producer_Q,\
            producer_Ta, producer_Tb, v_P, v_T =\
            self.__xToSingleVectorsAndVectorsToElementtypes(x)

        self.heatgrid.v_pipes_m = pipe_m
        self.heatgrid.v_pipes_Q = pipe_Q
        self.heatgrid.v_pipes_Ta = pipe_Ta
        self.heatgrid.v_pipes_Tb = pipe_Tb
        self.heatgrid.v_pipes_Pa = pipe_Pa
        self.heatgrid.v_pipes_Pb = pipe_Pb

        self.heatgrid.v_nodes_P = v_P
        self.heatgrid.v_nodes_T = v_T

        self.heatsink.v_consumers_m = consumer_m
        self.heatsink.v_consumers_Q = consumer_Q
        self.heatsink.v_consumers_Ta = consumer_Ta
        self.heatsink.v_consumers_Tb = consumer_Tb
        self.heatsink.v_consumers_Pa = consumer_Pa
        self.heatsink.v_consumers_Pb = consumer_Pb

        self.heatsource.v_producers_m = producer_m
        self.heatsource.v_producers_Q = producer_Q
        self.heatsource.v_producers_Ta = producer_Ta
        self.heatsource.v_producers_Tb = producer_Tb
        self.heatsource.v_producers_Pa = producer_Pa
        self.heatsource.v_producers_Pb = producer_Pb
        self.getGuessFirstRun = 0
#   TODO save_x for pipes, plus how to print pretty.

    def print_x(self, x, name, amount_pipes=1, amount_nodes=1,
                amount_consumer=1, amount_producer=1):
        '''
        prints x from Solver
        input: arr = x
               name = guess or solution or another name for values of x
        output: print(x)
        '''

        pipe_m, pipe_Pa, pipe_Pb, pipe_Q, pipe_Ta, pipe_Tb,\
            consumer_m, consumer_Pa, consumer_Pb, consumer_Q, consumer_Ta,\
            consumer_Tb, producer_m, producer_Pa, producer_Pb, producer_Q,\
            producer_Ta, producer_Tb, v_P, v_T =\
            self.__xToSingleVectorsAndVectorsToElementtypes(x)

        index = amount_pipes
        i = 0
        for element, sNode, eNode, sprp, m, Pa, Pb, Q, Ta, Tb in zip(
                                self.heatgrid.v_pipes_element,
                                self.heatgrid.v_pipes_sNode,
                                self.heatgrid.v_pipes_eNode,
                                self.heatgrid.v_pipes_sprp,
                                pipe_m, pipe_Pa, pipe_Pb, pipe_Q,
                                pipe_Ta, pipe_Tb):
            if i < index:
                print("%s \t %s --> %s\t: sprp %i Q %11.3f [W] m %7.3f [m/s] Ta %3.2f [K] "
                      "Tb %3.2f [K] Pa %6.f [Pa] Pb %6.f [Pa]" % (
                                                  element, sNode, eNode,
                                                  sprp,
                                                  Q, m,
                                                  Ta, Tb,
                                                  Pa, Pb))
                i = i + 1
            else:
                break
        index = amount_consumer
        i = 0
        for element, sNode, eNode, m, Pa, Pb, Q, Ta, Tb in zip(
                                self.heatsink.v_consumers_element,
                                self.heatsink.v_consumers_sNode,
                                self.heatsink.v_consumers_eNode,
                                consumer_m, consumer_Pa, consumer_Pb,
                                consumer_Q, consumer_Ta, consumer_Tb):
            if i < index:
                print("%s %s --> %s\t: \t Q %11.3f [W] m %7.3f [m/s] Ta %3.2f [K] "
                      "Tb %3.2f [K] Pa %6.f [Pa] Pb %6.f [Pa]" % (
                                                  element,
                                                  sNode,
                                                  eNode,
                                                  Q, m,
                                                  Ta, Tb,
                                                  Pa, Pb))
                i = i + 1
            else:
                break
        index = amount_producer
        i = 0
        for element, sNode, eNode, m, Pa, Pb, Q, Ta, Tb in zip(
                                self.heatsource.v_producers_element,
                                self.heatsource.v_producers_sNode,
                                self.heatsource.v_producers_eNode,
                                producer_m, producer_Pa, producer_Pb,
                                producer_Q, producer_Ta, producer_Tb):

            if i < index:
                print("%s %s --> %s\t: \t Q %11.3f [W] m %7.3f [m/s] Ta %3.2f [K] "
                      "Tb %3.2f [K] Pa %6.f [Pa] Pb %6.f [Pa]" % (
                                                  element,
                                                  sNode,
                                                  eNode,
                                                  Q, m,
                                                  Ta, Tb,
                                                  Pa, Pb))
                i = i + 1
            else:
                break

        index = amount_nodes
        i = 0
        for element, name_nodes, sprp, P, T in zip(
                                       self.heatgrid.v_nodes_element,
                                       self.heatgrid.v_nodes_name,
                                       self.heatgrid.v_nodes_sprp,
                                       v_P, v_T):
            if i < index:
                print("%s \t %s\t\t: sprp %i T %11.3f [K]"
                      " P %7.f [Pa]" % (element, name_nodes, sprp, T, P))
                i = i + 1
            else:
                break
        print("values of %s \t ----> OK\n" % name)


if __name__ == "__main__":
    import os
    from DataIO import DataIO
    import Dictionary
    from Plotter import Plotter
    from HeatGrid import HeatGrid
    from HeatSink import HeatSink
    from HeatSource import HeatSource
    from scipy.optimize import fsolve
    print('DistrictHeatingSystem \t run directly \n')

    DataIO = DataIO(
                os.path.dirname(os.getcwd()) + os.sep +
                'input' + os.sep + 'TestNetze' + os.sep + 'TestNetz_einEinspeiser',
                os.path.dirname(os.getcwd()) + os.sep +
                'output' + os.sep + 'TestNetze' + os.sep +
                'TestNetz_einEinspeiser')

    heatgrid_nodes = DataIO.importDBF(
            'KTestNetz.DBF', dtype=Dictionary.STANET_nodes_allocation)

    heatgrid_pipes = DataIO.importDBF(
            'STestNetz.DBF', dtype=Dictionary.STANET_pipes_allocation)
    
    heatsink = DataIO.importDBF(
            'WTestNetz.DBF', dtype=Dictionary.STANET_consumer_allocation)
    
    heatsink_profiles_Q = None
#    heatsink = DataIO.importCSV(
#            'TestNetz_consumer.csv', dtype=Dictionary.STANET_consumer_allocation)

#    heatsink_profiles_Q = DataIO.importCSV(
#            'consumers_profile_Q.csv')
    heatsource = DataIO.importCSV(
            'WTestNetz.csv', dtype=Dictionary.STANET_producer_allocation,
            delimiter=';', header=0)

    heatsink = HeatSink(heatsink, tableOfProfiles=heatsink_profiles_Q)
    heatsource = HeatSource(heatsource)
    heatgrid = HeatGrid(heatgrid_pipes,
                        heatgrid_nodes,
                        nodeSupply=np.column_stack((
                         heatsource.v_producers_eNode,
                         np.array([None]*len(
                             heatsource.v_producers_eNode)))))
    solver = Solver(heatgrid, heatsink, heatsource)

    print('----> Get guess for equations.')
    guess = solver.getGuess()

    solver.print_x(guess, "guess",
                   amount_pipes=len(heatgrid.pipes()),
                   amount_nodes=len(heatgrid.nodes()),
                   amount_producer=len(heatsource.producers()),
                   amount_consumer=len(heatsink.consumer()))
    print('----> Solve equations.')
    startTime = time.clock()
#    solution = fsolve(solver.gridCalculation, guess)
    solution_root = root(solver.gridCalculation, guess, method='lm')

    solution = solution_root.x
    print(time.clock() - startTime)

#    solver.print_x(solution, "solution")
    solver.print_x(solution, "solution", amount_pipes=18, amount_nodes=18,
                   amount_consumer=4, amount_producer=2)
    solver.save_x(solution)
    print(solution_root.success)
    print(solution_root.message)
    Solver_plotter = Plotter()
#    Solver_plotter.plot_graph(solver.heatgrid.v_nodes_name,
#                              solver.heatgrid.v_pipes_esNode)
    print(solver.heatsource.v_producers_end_x, solver.heatsource.v_producers_end_y,
          solver.heatsource.v_producers_start_x, solver.heatsource.v_producers_start_y,
          solver.heatsource.v_producers_m)
    fig = Solver_plotter.plot_DHS(
            v_pipes_start_x=solver.heatgrid.v_pipes_start_x,
            v_pipes_start_y=solver.heatgrid.v_pipes_start_y,
            v_pipes_end_x=solver.heatgrid.v_pipes_end_x,
            v_pipes_end_y=solver.heatgrid.v_pipes_end_y,
            v_pipes_Q=np.abs(solver.heatgrid.v_pipes_m),
            v_nodes_x=solver.heatgrid.v_nodes_x,
            v_nodes_y=solver.heatgrid.v_nodes_y,
            v_consumers_start_x=solver.heatsink.v_consumers_start_x,
            v_consumers_start_y=solver.heatsink.v_consumers_start_y,
            v_consumers_end_x=solver.heatsink.v_consumers_end_x,
            v_consumers_end_y=solver.heatsink.v_consumers_end_y,
            v_consumers_Q=np.abs(solver.heatsink.v_consumers_m),
            v_producers_start_x=solver.heatsource.v_producers_start_x,
            v_producers_start_y=solver.heatsource.v_producers_start_y,
            v_producers_end_x=solver.heatsource.v_producers_end_x,
            v_producers_end_y=solver.heatsource.v_producers_end_y,
            v_producers_Q=np.abs(solver.heatsource.v_producers_m))
    DataIO.exportFig('test_solver', fig)
    DataIO.exportNumpyArr('test_einEinspeiser_heatgrid',
                          solver.heatgrid.getCalculations)
else:
    print("Solver \t\t\t was imported into another module")

    
#    performance check clip vs [i for i in ...]
#    clip = 0.00346
#    [i for i in...] = 0.0858 (mean @ array 4000, 10 * 100)
    
#    arr_plus = np.array([1]*2000)
#    arr_minus = np.array([-1]*2000)
#    arr = np.concatenate((arr_plus, arr_minus))
#    mytime = []
#    y = 0
#    while y < 10:
#        startTime = time.clock()
#        i = 0
#        while i < 100:
#            arr_ceiled = np.ceil(arr)
#            test = arr_ceiled.clip(min=0)
##            test = [1 if i >= 0 else 0 for i in arr]
#            i = i + 1
#        mytime.append(time.clock() - startTime)
#        y = y + 1
#    print('clip' + str(np.mean(mytime)))

#    performance check variable, class.variable
#    variable = 0.537 sec (mean @ 10 * 1000000)
#    class.variable = 0.580 sec (mean @ 10 * 1000000)
#    arr = np.array([10]*100000)
#    myslice = slice(1,1000)
#    mytime = []
#    y = 0
#    while y < 10:
#        startTime = time.clock()
#        i = 0
#        while i < 1000000:
#            test = arr[myslice]
#            test = arr[solver.myslice]
#            test = test[solver.myslice]
#            i = i + 1
#        mytime.append(time.clock() - startTime)
#        y = y + 1
#    print(np.mean(mytime))

#    performance check function, class.function, direct:
#    dependencies by class.function: 0.642 sec (mean @ 10 * 1000000)
#    dependencies by dp.function (functions stored in other file): 0.620 sec
#    (mean @ 10 * 1000000)
#    dependencies written direct in function F of fsolve: 0.1775 sec
#    (mean @ 10 * 1000000)
#    mytime = []
#    y = 0
#    while y < 10:
#        startTime = time.clock()
#        i = 0
#        while i < 1000000:
#            test = dp.consumer_massflow(1,2,3,4)
##            test = 1 * 4182 * (3 - 2) - 4
#            i = i + 1
#        mytime.append(time.clock() - startTime)
#        y = y + 1
#
#    print(np.mean(mytime))
    
#        def __del_DeadEnds(self):
#        '''
#        deletes all dead ends in a network
#        output: inzidenzmatrix with zeros for elments that are dead ends.
#        '''
#        
#        print("Deletion of all dead ends")
#        
#        print(self._inzidenzmatrix)
#        print('\n')
#        Inzidenzmatrix = self._inzidenzmatrix
#
#        index = Inzidenzmatrix.shape[1]
#        i = 0
#        I_row_deleted = [] 
#        I_col_deleted = []
#        while i < index:
#            I_abs = np.abs(Inzidenzmatrix)
#            I_row_sum = np.sum(I_abs, axis=1)
#            I_row_index = np.where(I_row_sum == 1)
#            for val in I_row_index[0]:
#                Inzidenzmatrix[val] = 0
##                if val.size is not 0:
##                    print('deleted node: ' + str(
##                            self.heatgrid.nodes(val).name))
#            I_row_deleted.append(I_row_index[0])
#
#            I_col_sum = np.sum(I_abs, axis=0)
#            I_col_index = np.where(I_col_sum == 1)
#            for val in I_col_index[0]:
#                Inzidenzmatrix[:, val] = 0
##                if val.size is not 0:
##                    print('deleted edges: ' + str(
#                #            self.heatgrid.pipes(val).esNode))
#            I_col_deleted.append(I_col_index[0])
#            i = i + 1
#
#            if not (I_row_index and I_col_index):
#                break
#
#        self._inzidenzmatrix = Inzidenzmatrix
#        self.heatgrid
#        print(self._inzidenzmatrix)
#        print('\n')