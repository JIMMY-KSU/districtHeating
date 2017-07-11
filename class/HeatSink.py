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
        self.v_consumers_index = arr[0]
        self.v_consumers_start_x = arr[1]
        self.v_consumers_start_y = arr[2]
        self.v_consumers_end_x = arr[3]
        self.v_consumers_end_y = arr[4]
        self.v_consumers_sNode = arr[5]
        self.v_consumers_eNode = arr[6]
        self.v_consumers_heat_profile = arr[7]
        self.v_consumers_heat_average = arr[8]
        self.v_consumers_m = np.asarray(arr[9])
        self.v_consumers_Q = np.asarray(arr[10])
        self.v_consumers_cp = np.asarray(arr[11])
        self.v_consumers_Ta = np.asarray(arr[12])
        self.v_consumers_Tb = np.asarray(arr[13])


        self.__str__()

    def consumer(self, i = slice(None,None)):
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
        for item in self.consumer():
            print(item.index, item.Q)

        for index, item in enumerate(self.consumer()):
            retarr_index[index] = item.index
            retarr_start_x[index] = item.start_x
            retarr_start_y[index] = item.start_y
            retarr_end_x[index] = item.end_x
            retarr_end_y[index] = item.end_y
            retarr_sNode[index]= item.sNode
            retarr_eNode[index] = item.eNode
            retarr_heat_profile[index] = item.heat_profile
            retarr_heat_average[index] = item.heat_average
            retarr_m[index] = item.m
            retarr_Q[index] = item.Q
            retarr_cp[index] = item.cp
            retarr_Ta[index] = item.Ta
            retarr_Tb[index] = item.Tb
        return retarr_index, retarr_start_x, retarr_start_y, retarr_end_x,\
            retarr_end_y, retarr_sNode, retarr_eNode,\
            retarr_heat_profile, retarr_heat_average, retarr_m, retarr_Q,\
            retarr_cp, retarr_Ta, retarr_Tb

    def __importConsumer(self, arr):
        retArr = []
        for item in arr:
            retArr.append(Consumer(item))
        return retArr

    def __str__(self):
        for i, Q, m, Tb, Ta in zip(self.v_consumers_index, self.v_consumers_Q,
                                   self.v_consumers_m, self.v_consumers_Tb,
                                   self.v_consumers_Ta):
            print("Consumer: index %3i Q %7.0f m %4.1f Tb %3.2f Ta %3.2f"
                  % (i, Q, m, Tb, Ta))

        print("%i Consumer \t----> OK \n" % (len(self.v_consumers_index)))

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


else:
    print('HeatSink \t\t was imported into another module')