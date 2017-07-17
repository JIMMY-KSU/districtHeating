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
        self.v_producer_Pa_set = self.heatsource.v_producers_Pa
        self.v_producer_Pb_set = self.heatsource.v_producers_Pb
#        self.v_producer_Tb_set = 130+273.15  # [K]
#        self.v_consumer_Tb_set = np.asarray([273.15 + 60] * 3)  # [K]
#        self.v_consumer_Q_set = np.asarray([-75000, -100000, -50000])  # [W]

        
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
        pipeMassflow = dp.pipe_massflow(
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
        consumerMassflow = dp.consumer_massflow(
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
        producerMassflow = dp.producer_massflow(
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
                         pipeMassflow, consumerMassflow, producerMassflow,
                         pipePress, producer_Pb, producer_Pa,
                         consumer_Tb, producer_Tb,
                         pipeQ, consumer_Q))

        return F

    def getGuess(self):
        '''
        vector of massflows by guess
        '''
        v_m = np.zeros(self._elements)
        # massflow
        v_m[self.__I_grid_slice] = np.average(self.heatsink.v_consumers_m)
        v_m[self.__I_sink_slice] = self.heatsink.v_consumers_m
        v_m[self.__I_source_slice] = (np.sum(self.heatsink.v_consumers_m) /
                                       len(self.heatsource.producers()))
        '''
        vector of heatflows by guess
        '''
        v_Q = np.zeros(self._elements)
        # heatflows
        v_Q[self.__I_grid_slice] = 0
        v_Q[self.__I_sink_slice] = self.heatsink.v_consumers_Q
        v_Q[self.__I_source_slice] = (np.sum(self.heatsink.v_consumers_Q) / 
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
        v_Ta[self.__I_sink_slice] = np.average(self.heatsource.v_producers_Tb)
        v_Ta[self.__I_source_slice] = np.sum(self.heatsink.v_consumers_m *
                                            self.heatsink.v_consumers_Tb) /\
                                            np.sum(self.heatsink.v_consumers_m)
        '''temperature Tb'''
        v_Tb[self.__I_sink_slice] = self.heatsink.v_consumers_Tb
        v_Tb[self.__I_source_slice] = self.heatsource.v_producers_Tb

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
        v_Pb[self.__I_source_slice] = np.average(self.heatsource.v_producers_Pb)
        
        arr = np.concatenate((v_m, v_P, v_Pa, v_Pb, v_Q, v_T, v_Ta, v_Tb))

        return arr

    def print_x(self, arr, name):
        v_sprp = self.heatgrid.v_pipes_sprp + [''] * 2*self._elements

        for element, sprp, m, Pa, Pb, Q, Ta, Tb in zip(
                                self.heatgrid.v_pipes_element+\
                                self.heatsink.v_consumers_element+\
                                self.heatsource.v_producers_element,
                                v_sprp,
                                arr[0:self._elements],
                                arr[self._elements + self._nodes:
                                         self._elements*2 + self._nodes],
                                arr[self._elements*2 + self._nodes:
                                         self._elements*3 + self._nodes],
                                arr[self._elements*3 + self._nodes:
                                         self._elements*4 + self._nodes],
                                arr[self._elements*4 + self._nodes*2:
                                         self._elements*5 + self._nodes*2],
                                arr[self._elements*5 + self._nodes*2:
                                         self._elements*6 + self._nodes*2]):
            if sprp != '':
                print("%s: sprp %i Q %11.3f m %9.3f  Ta %3.2f  Tb %3.2f "
                          "Pa %2.3f Pb %2.3f " % (element, sprp,
                                                  Q, m,
                                                  Ta, Tb,
                                                  Pa, Pb))
            elif sprp == '':
                 print("%s: Q %11.3f m %9.3f  Ta %3.2f  Tb %3.2f "
                          "Pa %2.3f Pb %2.3f " % (element,
                                                  Q, m,
                                                  Ta, Tb,
                                                  Pa, Pb))
            

        for element, sprp, P, T in zip(self.heatgrid.v_nodes_element,
                                       self.heatgrid.v_nodes_sprp,
                                 arr[self._elements:
                                     self._elements + self._nodes],
                               arr[self._elements*4 + self._nodes:
                                     self._elements*4 + self._nodes*2]):
            print("%s: sprp %i T %3.2f P %2.3f " % (element, sprp, T, P))
        print("values of %s \t ----> OK\n" % name)

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
    heatsink = HeatSink(heatsink)
    heatsource = HeatSource(heatsource)
    heatgrid = HeatGrid(heatgrid_pipes,
                        heatgrid_nodes,
                        nodeSupply=np.column_stack((
                         heatsource.v_producers_eNode,
                         np.array([None]*len(
                             heatsource.v_producers_eNode)))))
    solver = Solver(heatgrid, heatsink, heatsource)
    guess = solver.getGuess()
    solution = fsolve(solver.gridCalculation, guess)

    solver.print_x(guess, "guess")
    solver.print_x(solution, "solution")

else:
    print("Solver \t\t\t was imported into another module")
