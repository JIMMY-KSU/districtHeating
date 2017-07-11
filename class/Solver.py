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
        self.v_producer_Pa_set = 5  # dont change this, it
                                     # is not yet implemented in the dependecies!
        
        self.v_producer_Pb_set = 2  # dont change this, 
                                    # it is not yet implemented in the dependecies!
        self.v_producer_Tb_set = 130+273.15  # [K]
        self.v_consumer_Tb_set = np.asarray([273.15 + 60] * 3)  # [K]
        self.v_consumer_Q_set = np.asarray([-75000, -100000, -50000])  # [W]


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
                          v_m[self.__I_grid_slice])

        # dependencies for consumer
        consumerMassflow = dp.consumer_massflow(
                                  v_m[self.__I_sink_slice],
                                  v_Ta[self.__I_sink_slice],
                                  v_Tb[self.__I_sink_slice],
                                  v_Q[self.__I_sink_slice])
        consumer_Q = dp.consumer_heatflow(
                                  self.v_consumer_Q_set,
                                  v_Q[self.__I_sink_slice])
        consumer_Tb = dp.consumer_temp(
                                  self.v_consumer_Tb_set,
                                  v_Tb[self.__I_sink_slice])
        consumer_Pb = dp.consumer_press(v_Pa[self.__I_sink_slice],
                                        v_Pb[self.__I_sink_slice],
                                        v_m[self.__I_sink_slice])

        # dependencies for producer
        producerMassflow = dp.producer_massflow(
                                  v_m[self.__I_source_slice],
                                  v_Ta[self.__I_source_slice],
                                  v_Tb[self.__I_source_slice],
                                  v_Q[self.__I_source_slice])
        producer_Tb = dp.producer_temp(
                              self.v_producer_Tb_set,
                              v_Tb[self.__I_source_slice])
        producer_Pb = dp.producer_press(
                          self.v_producer_Pb_set,
                          v_Pb[self.__I_source_slice])


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
#
#        '''
#        vector of massflows by guess
#        '''
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
        v_Q[self.__I_grid_slice] = np.average(heatsink.v_consumers_Q)
        v_Q[self.__I_sink_slice] = heatsink.v_consumers_Q
        v_Q[self.__I_source_slice] = -(np.sum(heatsink.v_consumers_Q) / 
                                       len(heatsource.producer()))

        '''
        vector of temperatures by guess
        '''
        v_T = np.zeros(self.nodes)
        # temperature from node away
        v_Ta = np.zeros(self.edges)
        v_Ta[self.__I_grid_slice] = self.v_producer_Tb_set
        v_Ta[self.__I_sink_slice] = self.v_producer_Tb_set
        v_Ta[self.__I_source_slice] = self.v_producer_Tb_set
        # temperature towards node
        v_Tb = np.zeros(self.edges)
        v_Tb[self.__I_grid_slice] = self.v_producer_Tb_set
        v_Tb[self.__I_sink_slice] = self.v_producer_Tb_set
        v_Tb[self.__I_source_slice] = self.v_producer_Tb_set

        '''
        vector of pressures by guess
        '''
        v_P = np.zeros(self.nodes)
        # pressure from node away
        v_Pa = np.zeros(self.edges)
        v_Pa[self.__I_grid_slice] = self.v_producer_Pa_set
        v_Pa[self.__I_sink_slice] = self.v_producer_Pa_set
        v_Pa[self.__I_source_slice] = self.v_producer_Pa_set
        # pressure towards node
        v_Pb = np.zeros(self.edges)
        v_Pb[self.__I_grid_slice] = self.v_producer_Pb_set
        v_Pb[self.__I_sink_slice] = self.v_producer_Pb_set
        v_Pb[self.__I_source_slice] = self.v_producer_Pb_set
        
        arr = np.concatenate((v_m, v_P, v_Pa, v_Pb, v_Q, v_T, v_Ta, v_Tb))

        return arr
#        pipes_v_m = [1842.5, 614.2, -2763.8, -1842.5, -614.2, 2763.8]
#        consumer_v_m = [921.263, 1228.35, 614.175]
#        producer_v_m = [2764]
#        v_m = pipes_v_m + consumer_v_m + producer_v_m
#    
#        nodes_v_P = [5, 5, 5, 5, 2, 2, 2, 2]
#        v_P = nodes_v_P
#    
#        pipes_v_Pa = [5, 5, 2, 2, 2, 5]
#        consumer_v_Pa = [5, 5, 5]
#        producer_v_Pa = [2]
#        v_Pa = pipes_v_Pa + consumer_v_Pa + producer_v_Pa
#    
#        pipes_v_Pb = [5, 5, 2, 2, 2, 5]
#        consumer_v_Pb = [2, 2, 2]
#        producer_v_Pb = [5]
#        v_Pb = pipes_v_Pb + consumer_v_Pb + producer_v_Pb
#    
#        pipes_v_Q = [0, 0, 0, 0, 0, 0]
#        consumer_v_Q = [-75000, -100000, -50000]
#        producer_v_Q = [225000]
#        v_Q = pipes_v_Q + consumer_v_Q + producer_v_Q
#    
#    
#        nodes_v_T = [130, 130, 130, 130, 60, 60, 60, 60]
#        v_T = nodes_v_T
#    
#        pipes_v_Ta = [130, 130, 60, 60, 60, 130]
#        consumer_v_Ta = [130, 130, 130]
#        producer_v_Ta = [60]
#        v_Ta = pipes_v_Ta + consumer_v_Ta + producer_v_Ta
#        
#        pipes_v_Tb = [130, 130, 60, 60, 60, 130]
#        consumer_v_Tb = [60, 60, 60]
#        producer_v_Tb = [130]
#        v_Tb = pipes_v_Tb + consumer_v_Tb + producer_v_Tb
#        
#        print(len(v_m))
#        print(len(v_P))
#        print(len(v_Pa))
#        print(len(v_Pb))
#        print(len(v_Q))
#        print(len(v_T))
#        print(len(v_Ta))
#        print(len(v_Tb))
#        arr = np.concatenate((v_m, v_P, v_Pa, v_Pb, v_Q, v_T, v_Ta, v_Tb))
#        print(len(arr))
#        return arr


if __name__ == "__main__":
    from DataIO import DataIO
    import Dictionary
    print("Solver \t\t\t run directly \n")

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

    testSolver = Solver(self._inzidenzmatrix,
                               self._inzidenzmatrix_HeatGrid,
                               self._inzidenzmatrix_HeatSink,
                               self._inzidenzmatrix_HeatSource)

    solution = fsolve(testSolver.gridCalculation,
                        Solver_fsolve.getGuess(self.heatgrid,
                                 self.heatsink,
                                 self.heatsource))


    pipes_v_m = [1842.5, 614.2, -2763.8, -1842,5, -614.2, 2763.8]
    consumer_v_m = [921.263, 1228.35, 614.175]
    producer_v_m = [2764]
    v_m = pipes_v_m + consumer_v_m + producer_v_m

    nodes_v_P = [5, 5, 5, 5, 2, 2, 2, 2]
    v_P = nodes_v_P

    pipes_v_Pa = [5, 5, 5, 5]
    consumer_v_Pa = [5, 5, 5]
    producer_v_Pa = [2]
    v_Pa = pipes_v_Pa + consumer_v_Pa + producer_v_Pa

    pipes_v_Pb = [2, 2, 2, 2]
    consumer_v_Pb = [2, 2, 2]
    producer_v_Pb = [5]
    v_Pb = pipes_v_Pb + consumer_v_Pb + producer_v_Pb

    pipes_v_Q = [0, 0, 0, 0, 0, 0]
    consumer_v_Q = [-75000, -100000, -50000]
    producer_v_Q = [225000]
    v_Q = pipes_v_Q + consumer_v_Q + producer_v_Q


    nodes_v_T = [130, 130, 130, 130, 60, 60, 60, 60]
    v_T = nodes_v_T

    pipes_v_Ta = [130, 130, 130]
    consumer_v_Ta = [130, 130, 130,]
    producer_v_Ta = [60]
    v_Ta = pipes_v_Ta + consumer_v_Ta + producer_v_Ta
    
    pipes_v_Tb = [60, 60, 60]
    consumer_v_Tb = [60, 60, 60]
    producer_v_Tb = [130]
    v_Tb = pipes_v_Tb + consumer_v_Tb + producer_v_Tb

    np.concatenate((v_m, v_P, v_Pa, v_Pb, v_Q, v_T, v_Ta, v_Tb))

    
else:
    print("Solver \t\t\t was imported into another module")
