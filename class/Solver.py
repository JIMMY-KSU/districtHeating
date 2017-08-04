# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 14:45:18 2017

@author: narand
"""

import dependencies as dp
import balances as bl
import numpy as np
from inzidenzmatrix import inzidenzmatrix


class Solver():
    def __init__(self, heatgrid, heatsink, heatsource):

        self.heatgrid = heatgrid
        self.heatsink = heatsink
        self.heatsource = heatsource
        self._inzidenzmatrix_HeatGrid = self.__inzidenzmatrix_HeatGrid()
        self._inzidenzmatrix_HeatSink = self.__inzidenzmatrix_HeatSink()
        self._inzidenzmatrix_HeatSource = self.__inzidenzmatrix_HeatSource()
        self._inzidenzmatrix = self.__inzidenzmatrix()
        self._elements = np.shape(self._inzidenzmatrix)[1]
        self._nodes = np.shape(self._inzidenzmatrix)[0]
#        print(self._inzidenzmatrix)
#        print(self._inzidenzmatrix_HeatGrid)
#        print(self._inzidenzmatrix_HeatSink)
#        print(self._inzidenzmatrix_HeatSource)
        '''
        sets up all necessary inzmatrices
        '''
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

        self.Tamb = 5+273.15  # [K]
        self.cp = 4182 #  J/(kg*K)
        self.k = 1
        self.A = 1
        self.v_producer_Pa_set = self.heatsource.v_producers_Pa
        self.v_producer_Pb_set = self.heatsource.v_producers_Pb

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

    def gridCalculation(self, x):
        '''
        vector of massflows by solver
        '''
        i = 0

        v_m = x[i: i + self._elements]
        i = i + self._elements
        '''
        vector of pressures by solver
        '''
        v_P = x[i: i + self._nodes]
        i = i + self._nodes
        # pressure from node away
        v_Pa = x[i: i + self._elements]
        i = i + self._elements
        # pressure towards node
        v_Pb = x[i: i + self._elements]
        i = i + self._elements
        '''
        vector of heatflows by solver
        '''
        v_Q = x[i: i + self._elements]
        i = i + self._elements
        '''
        vector of temperatures by solver
        '''
        v_T = x[i: i + self._nodes]
        i = i + self._nodes
        # temperature from node away
        v_Ta = x[i: i + self._elements]
        i = i + self._elements
        # temperature towards node
        v_Tb = x[i: i + self._elements]

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
        massBalance = massBalance[0: len(massBalance) - 1]

        # energy balance 1 (I_plus * diag(m)*T^b + I_minus * diag(m)*T^a)
        energyBalance_1 = bl.energyBalance_1(self.__I_plus, v_m,
                                             v_Tb, self.__I_minus, v_Ta)

        # energy balance 2 (-1 * I_minus.T * T - T^a)
        energyBalance_2 = bl.energyBalance_2(Iab, v_T, v_Tab)
#        energyBalance_2 = bl.energyBalance_2(self.__I_minus_T, v_T, v_Ta)
        # impulse balance 1 (-1*I_minus.T*P - P^a)
        impulseBalance_1 = bl.impulseBalance_1(self.__I_minus_T, v_P, v_Pa)

        # impulse balance 2 (I_plus.T*P - P^b)
        impulseBalance_2 = bl.impulseBalance_2(self.__I_plus_T, v_P, v_Pb)
        '''
        constitutive relations
        '''
        # dependencies for pipes
        pipe_m = dp.pipe_massflow(
                                  v_m[self.__I_grid_slice],
                                  v_Ta[self.__I_grid_slice],
                                  v_Tb[self.__I_grid_slice],
                                  v_Q[self.__I_grid_slice])
        pipeQ = dp.pipe_heatflow(
                          v_Q[self.__I_grid_slice],
                          v_Ta[self.__I_grid_slice],
                          v_Tb[self.__I_grid_slice])
        pipePress = dp.pipe_press(
                          v_Pa[self.__I_grid_slice],
                          v_Pb[self.__I_grid_slice],
                          v_m[self.__I_grid_slice],
                          self.heatgrid.v_pipes_sHeight,
                          self.heatgrid.v_pipes_eHeight)

        # dependencies for consumer
        consumer_m = dp.consumer_massflow(
                                  v_m[self.__I_sink_slice],
                                  v_Ta[self.__I_sink_slice],
                                  v_Tb[self.__I_sink_slice],
                                  v_Q[self.__I_sink_slice])
        consumer_Q = dp.consumer_heatflow(
                                  self.heatsink.v_consumers_Q,
                                  v_Q[self.__I_sink_slice])
        consumer_Tb = dp.consumer_temp(
                                  self.heatsink.v_consumers_Tb,
                                  v_Tb[self.__I_sink_slice])

        # dependencies for producer
        producer_m = dp.producer_massflow(
                                  v_m[self.__I_source_slice],
                                  v_Ta[self.__I_source_slice],
                                  v_Tb[self.__I_source_slice],
                                  v_Q[self.__I_source_slice])
        producer_Tb = dp.producer_temp(
                              self.heatsource.v_producers_Tb,
                              v_Tb[self.__I_source_slice])
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
                         pipe_m, consumer_m, producer_m,
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
            v_m[self.__I_grid_slice] = np.average(self.heatsink.v_consumers_m)
            v_m[self.__I_sink_slice] = self.heatsink.v_consumers_m
            v_m[self.__I_source_slice] = (np.sum(self.heatsink.v_consumers_m) /
                                          len(self.heatsource.producers()))

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
            v_Q[self.__I_grid_slice] = self.k * self.A * (
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
            v_Pa[self.__I_sink_slice] = np.average(self.heatsource.v_producers_Pb)
            v_Pa[self.__I_source_slice] = self.heatsource.v_producers_Pa
            # pressure Pb
            v_Pb[self.__I_sink_slice] = np.average(self.heatsource.v_producers_Pa)
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

        arr = np.concatenate((v_m, v_P, v_Pa, v_Pb, v_Q, v_T, v_Ta, v_Tb))
        print("Guess for solver \t----> OK")
        return arr

    def __xToSingleVectors(self, x):
        '''
        Splits the solver vextor x into its parts v_m, v_P, v_Pa etc
        input: x
        output: v_m, v_P, v_Pa, v_Pb, v_Q, v_T, v_Ta, v_Tb
        '''
        v_m = x[0:self._elements]

        v_P = x[self._elements:self._elements + self._nodes]
        v_Pa = x[self._elements + self._nodes:self._elements*2 + self._nodes]
        v_Pb = x[self._elements*2 + self._nodes:
                   self._elements*3 + self._nodes]

        v_Q = x[self._elements*3 + self._nodes:
                  self._elements*4 + self._nodes]

        v_T = x[self._elements*4 + self._nodes:
                  self._elements*4 + self._nodes*2]
        v_Ta = x[self._elements*4 + self._nodes*2:
                   self._elements*5 + self._nodes*2]
        v_Tb = x[self._elements*5 + self._nodes*2:
                   self._elements*6 + self._nodes*2]
        
        return v_m, v_P, v_Pa, v_Pb, v_Q, v_T, v_Ta, v_Tb
        
    def save_x(self, x):
        v_m, v_P, v_Pa, v_Pb, v_Q, v_T, v_Ta, v_Tb = self.__xToSingleVectors(x)

        self.heatgrid.v_pipes_m = v_m[self.__I_grid_slice]
        self.heatgrid.v_pipes_Q = v_Q[self.__I_grid_slice]
        self.heatgrid.v_pipes_Ta = v_Ta[self.__I_grid_slice]
        self.heatgrid.v_pipes_Tb = v_Tb[self.__I_grid_slice]
        self.heatgrid.v_pipes_Pa = v_Pa[self.__I_grid_slice]
        self.heatgrid.v_pipes_Pb = v_Pb[self.__I_grid_slice]

        self.heatgrid.v_nodes_P = v_P
        self.heatgrid.v_nodes_T = v_T

        self.heatsink.v_consumers_m = v_m[self.__I_sink_slice]
        self.heatsink.v_consumers_Q = v_Q[self.__I_sink_slice]
        self.heatsink.v_consumers_Ta = v_Ta[self.__I_sink_slice]
        self.heatsink.v_consumers_Tb = v_Tb[self.__I_sink_slice]
        self.heatsink.v_consumers_Pa = v_Pa[self.__I_sink_slice]
        self.heatsink.v_consumers_Pb = v_Pb[self.__I_sink_slice]

        self.heatsource.v_producers_m = v_m[self.__I_source_slice]
        self.heatsource.v_producers_Q = v_Q[self.__I_source_slice]
        self.heatsource.v_producers_Ta = v_Ta[self.__I_source_slice]
        self.heatsource.v_producers_Tb = v_Tb[self.__I_source_slice]
        self.heatsource.v_producers_Pa = v_Pa[self.__I_source_slice]
        self.heatsource.v_producers_Pb = v_Pb[self.__I_source_slice]
        self.getGuessFirstRun = 0
#   TODO save_x for pipes, plus how to print pretty.

    def print_x(self, x, name):
        '''
        prints x from Solver
        input: arr = x
               name = guess or solution or another name for values of x
        output: print(x)
        '''
        v_sprp = self.heatgrid.v_pipes_sprp + [''] * 2*self._elements
        v_m, v_P, v_Pa, v_Pb, v_Q, v_T, v_Ta, v_Tb = self.__xToSingleVectors(x)
        for element, sprp, m, Pa, Pb, Q, Ta, Tb in zip(
                                self.heatgrid.v_pipes_element +
                                self.heatsink.v_consumers_element +
                                self.heatsource.v_producers_element,
                                v_sprp,
                                v_m, v_Pa, v_Pb, v_Q, v_Ta, v_Tb):
            if sprp != '':
                print("%s: sprp %i \t Q %11.3f [W] m %7.3f [m/s] Ta %3.2f [K] "
                      "Tb %3.2f [K] Pa %6.f [Pa] Pb %6.f [Pa]" % (
                                                  element, sprp,
                                                  Q, m,
                                                  Ta, Tb,
                                                  Pa, Pb))
            elif sprp == '':
                print("%s: \t Q %11.3f [W] m %7.3f [m/s] Ta %3.2f [K] "
                      "Tb %3.2f [K] Pa %6.f [Pa] Pb %6.f [Pa]" % (
                                                  element,
                                                  Q, m,
                                                  Ta, Tb,
                                                  Pa, Pb))

        for element, name_nodes, sprp, P, T in zip(
                                       self.heatgrid.v_nodes_element,
                                       self.heatgrid.v_nodes_name,
                                       self.heatgrid.v_nodes_sprp,
                                       v_P, v_T):
            print("%s %s: sprp %i \t\t\t\t\t\t T %3.2f [K] \t\t P %6.f [Pa]"
                  % (element, name_nodes, sprp, T, P))
        print("values of %s \t ----> OK\n" % name)

    def checkDHSForDeadEnds(self):
        I = np.array([[0,-1,0,1],[0,1,-1,0],[0,0,1,-1],
                   [-1,0,0,1],[0,0,0,1],[0,0,0,0]])
        index = I.shape[1]
        i = 0
        while i < index:

            I_abs = np.abs(self._inzidenzmatrix)
            

            I_row_sum = np.sum(I_abs, axis=1)
            I_row_index = np.where(I_row_sum == 1)
            for val in I_row_index:
                I[val] = 0
        
            I_col_sum = np.sum(I_abs, axis=0)
            I_col_index = np.where(I_col_sum == 1)
            
            for val in I_col_index:
                I[:,val] = 0
            i = i + 1
            if not (I_row_index and I_col_index):
                break





if __name__ == "__main__":
    import os
    from DataIO import DataIO
    import Dictionary
    from HeatGrid import HeatGrid
    from HeatSink import HeatSink
    from HeatSource import HeatSource
    from scipy.optimize import fsolve
    print('DistrictHeatingSystem \t run directly \n')

    DataIO = DataIO(
                os.path.dirname(os.getcwd()) + os.sep +
                'input' + os.sep + 'TestNetz',
                os.path.dirname(os.getcwd()) + os.sep +
                'output' + os.sep + 'TestNetz')

    heatgrid_nodes = DataIO.importDBF(
            'KTestNetz.DBF', dtype=Dictionary.STANET_nodes_allocation)

    heatgrid_pipes = DataIO.importDBF(
            'STestNetz.DBF', dtype=Dictionary.STANET_pipes_allocation)

    heatsink = DataIO.importDBF(
            'WTestNetz.DBF', dtype=Dictionary.STANET_consumer_allocation)

    heatsource = DataIO.importCSV(
            'WTestNetz.csv', dtype=Dictionary.STANET_producer_allocation,
            delimiter='\t', header=0)

    heatsink = HeatSink(heatsink)
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
    
    solver.print_x(guess, "guess")
    print('----> Solve equations.')
    solution = fsolve(solver.gridCalculation, guess)

    solver.print_x(solution, "solution")
    solver.save_x(solution)

else:
    print("Solver \t\t\t was imported into another module")
