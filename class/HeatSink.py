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
        self._instancesConsumer = self.__importConsumer(tableOfConsumer)

        arr = self.__consumers()
        self.v_consumers_index = np.asarray(arr[0])
        self.v_consumers_start_x = np.asarray(arr[1])
        self.v_consumers_start_y = np.asarray(arr[2])
        self.v_consumers_end_x = np.asarray(arr[3])
        self.v_consumers_end_y = np.asarray(arr[4])
        self.v_consumers_sNode = arr[5]
        self.v_consumers_eNode = arr[6]
        self.v_consumers_heat_profile = arr[7]
        self.v_consumers_heat_average = np.asarray(arr[8])
        self.v_consumers_m = np.asarray(arr[9])
        self.v_consumers_Q = np.asarray(arr[10])
        self.v_consumers_cp = np.asarray(arr[11])
        self.v_consumers_Ta = np.asarray(arr[12])
        self.v_consumers_Tb = np.asarray(arr[13])
        self.v_consumers_Pa = np.asarray(arr[14])
        self.v_consumers_Pb = np.asarray(arr[15])
        self.v_consumers_element = arr[16]

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

    def __consumerProfile(self):
        pass

    def __consumers(self):
        length = len(self.consumer())
        retarr_index = [0]*length
        retarr_start_x = [0]*length
        retarr_start_y = [0]*length
        retarr_end_x = [0]*length
        retarr_end_y = [0]*length
        retarr_sNode = [0]*length
        retarr_eNode = [0]*length
        retarr_heat_profile = [0]*length
        retarr_heat_average = [0]*length
        retarr_m = [0]*length
        retarr_Q = [0]*length
        retarr_cp = [0]*length
        retarr_Ta = [0]*length
        retarr_Tb = [0]*length
        retarr_Pa = [0]*length
        retarr_Pb = [0]*length
        retarr_element = [0]*length

        for index, item in enumerate(self.consumer()):
            retarr_index[index] = item.index
            retarr_start_x[index] = item.start_x
            retarr_start_y[index] = item.start_y
            retarr_end_x[index] = item.end_x
            retarr_end_y[index] = item.end_y
            retarr_sNode[index] = item.sNode
            retarr_eNode[index] = item.eNode
            retarr_heat_profile[index] = item.heat_profile
            retarr_heat_average[index] = item.heat_average
            retarr_m[index] = item.m
            retarr_Q[index] = item.Q
            retarr_cp[index] = item.cp
            retarr_Ta[index] = item.Ta
            retarr_Tb[index] = item.Tb
            retarr_Pa[index] = item.Pa
            retarr_Pb[index] = item.Pb
            retarr_element[index] = item.element
        return retarr_index, retarr_start_x, retarr_start_y, retarr_end_x,\
            retarr_end_y, retarr_sNode, retarr_eNode,\
            retarr_heat_profile, retarr_heat_average, retarr_m, retarr_Q,\
            retarr_cp, retarr_Ta, retarr_Tb,\
            retarr_Pa, retarr_Pb, retarr_element

    def __importConsumer(self, arr):
        retArr = []
        for item in arr:
            retArr.append(Consumer(item))
        return retArr

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
            print("%s: i %i Q %10.f [W] m %7.3f [m/s] Ta %3.2f [K] "
                  "Tb %3.2f [K] Pa %6.f [Pa] Pb %6.f [Pa] sNode %s eNode %s"
                  % (element, i, Q, m, Ta, Tb, Pa, Pb, sNode, eNode))


if __name__ == "__main__":
    from DataIO import DataIO
    import Dictionary
    print('HeatSink \t\t run directly')
    
    DataIO = DataIO(os.path.dirname(os.getcwd()) + os.sep + 'input',
                    os.path.dirname(os.getcwd()) + os.sep + 'output')

    heatsink = DataIO.importDBF(
            'TestNetz' + os.sep + 'WTestNetz.DBF',
            Dictionary.HeatSink_consumer_dtype,
            Dictionary.HeatSink_STANET_consumer_allocation)

    testSink = HeatSink(heatsink)
    testSink.setCalculations()
    testSink.setCalculations()
    DataIO.exportNumpyArr('Heatsink', testSink.getCalculations())
#    print(calcedValuesArr[0][0][1])
#    print(testSink.saveCalculation())


else:
    print('HeatSink \t\t was imported into another module')