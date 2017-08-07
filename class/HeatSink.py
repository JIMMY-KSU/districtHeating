#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 12:41:52 2017

@author: johannes
"""
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'function')
import numpy as np

import inspect
import json

from Consumer import Consumer



class HeatSink():
    def __init__(self, tableOfConsumer):
        '''
        input:
            tabelOfConsumer = [] # contains all Consumer of network, \
                allocation Dictionary can be found in Dictionary
        '''
        cp = 4183  # J/(kg*K)
        Ta = 130 + 273.15  # Kelvin
        Tb = 60 + 273.15  # Kelvin
        
        self._instancesConsumer = self.__importConsumer(tableOfConsumer)

        length = len(tableOfConsumer)
        self.v_consumers_index = np.arange(length)
        self.v_consumers_start_x = np.array(tableOfConsumer['start_x'])
        self.v_consumers_start_y = np.array(tableOfConsumer['start_y'])
        self.v_consumers_end_x = np.array(tableOfConsumer['end_x'])
        self.v_consumers_end_y = np.array(tableOfConsumer['end_y'])
        self.v_consumers_sNode = np.array(tableOfConsumer['sNode'])
        self.v_consumers_eNode = np.array(tableOfConsumer['eNode'])
        self.v_consumers_esNode = np.column_stack((self.v_consumers_eNode,
                                                   self.v_consumers_sNode))
        self.v_consumers_profile = np.array(tableOfConsumer['profile'])
        self.v_consumers_average = np.array(tableOfConsumer['average'])
        self.v_consumers_Q = np.array(tableOfConsumer['Q'])
        self.v_consumers_cp = np.array([cp] * length)  # J/(kg*K)
        self.v_consumers_Ta = np.array([Ta] * length)  # Kelvin
        self.v_consumers_Tb = np.array([Tb] * length)  # Kelvin
        # TODO make cp, Ta, Tb function that takes care if cp, Ta and Tb are 
        # given by tableOfConsumer
        self.v_consumers_m = self.__calc_consumers_m(self.v_consumers_Q,
                                                     self.v_consumers_cp,
                                                     self.v_consumers_Ta,
                                                     self.v_consumers_Tb)
        self.v_consumers_Pa = [0] * length
        self.v_consumers_Pb =  [0] * length
        self.v_consumers_element = ['consumer'] * length
        self.__str__()
        print("%i consumer \t----> OK \n" % (len(self.v_consumers_index)))
        self.calcVals = []

    def consumer(self, i=slice(None, None)):
        return self._instancesConsumer[i]

    def averageReturnTemperature(self):
        sumQ = 0
        sumQT = 0
        for i in self.consumer():
            sumQT += i.heat_demand * i.return_temperature
            sumQ += i.heat_demand
        return sumQT / sumQ

    def __calc_consumers_m(self, Q, cp, Ta, Tb):
        arr = Q / (cp * (Tb - Ta))
        return arr
    
    def __consumerProfile(self):
        pass

    def __importConsumer(self, df):
        arr = []
        for index, row in df.iterrows():
            arr.append(Consumer(index, row))
        return arr

    def setCalculations(self):
        attr = self.__dict__
        attr = {item: attr[item] for item in attr if item not in
                ("_instancesConsumer",
                 "__str__",
                 "calcVals")}
        self.calcVals.append(attr)

    def getCalculations(self, i=slice(None,None)):
        return self.calcVals[i]

    def __str__(self):
        index = 0
        for element, i, Q, m, Ta, Tb, Pa, Pb, sNode, eNode in zip(
                self.v_consumers_element,
                self.v_consumers_index,
                self.v_consumers_Q,
                self.v_consumers_m,
                self.v_consumers_Ta,
                self.v_consumers_Tb,
                self.v_consumers_Pa,
                self.v_consumers_Pb,
                self.v_consumers_sNode,
                self.v_consumers_eNode):
            if index < 1:
                print("%s: i %i Q %10.f [W] m %7.3f [m/s] Ta %3.2f [K] "
                      "Tb %3.2f [K] Pa %6.f [Pa] Pb %6.f [Pa] sNode %s"
                      "eNode %s" % (element, i, Q, m, Ta, Tb, Pa, Pb,
                                    sNode, eNode))
                index = index + 1
            else:
                break


if __name__ == "__main__":
    from DataIO import DataIO
    import Dictionary
    print('HeatSink \t\t run directly')
    
    DataIO = DataIO(
                os.path.dirname(os.getcwd()) + os.sep +
                'input' + os.sep + 'TestNetz',
                os.path.dirname(os.getcwd()) + os.sep +
                'output' + os.sep + 'TestNetz')
    heatsink = DataIO.importDBF(
            'WTestNetz.DBF', dtype=Dictionary.STANET_consumer_allocation)

    testSink = HeatSink(heatsink)
    testSink.setCalculations()
    testSink.setCalculations()
    DataIO.exportNumpyArr('Heatsink', testSink.getCalculations())
#    print(calcedValuesArr[0][0][1])
#    print(testSink.saveCalculation())


else:
    print('HeatSink \t\t was imported into another module')