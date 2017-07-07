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

        self.v_consumers_index = self.__consumers()[0]
        self.v_consumers_start_x = self.__consumers()[1]
        self.v_consumers_start_y = self.__consumers()[2]
        self.v_consumers_end_x = self.__consumers()[3]
        self.v_consumers_end_y = self.__consumers()[4]
        self.v_consumers_sNode = self.__consumers()[5]
        self.v_consumers_eNode = self.__consumers()[6]
        self.v_consumers_heat_profile = self.__consumers()[7]
        self.v_consumers_heat_average = self.__consumers()[8]
        self.v_consumers_m = self.__consumers()[9]
        self.v_consumers_Q = self.__consumers()[10]
        self.v_consumers_cp = self.__consumers()[11]
        self.v_consumers_Ta = self.__consumers()[12]
        self.v_consumers_Tb = self.__consumers()[13]

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
        retarr = np.zeros(length)
        retarr_str = [0]*length
        retarr_index = retarr
        retarr_start_x = retarr
        retarr_start_y = retarr
        retarr_end_x = retarr
        retarr_end_y = retarr
        retarr_sNode = retarr_str
        retarr_eNode = retarr_str
        retarr_heat_profile = retarr_str
        retarr_heat_average = retarr_str
        retarr_m = retarr
        retarr_Q = retarr
        retarr_cp = retarr
        retarr_Ta = retarr
        retarr_Tb = retarr

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
        for item in self.consumer():
            print("Consumer: index %3i Q %7.0f m %4.1f Tb_set %3.2f Ta_set %3.2f"
                  % (item.index, item.Q, item.m, item.Tb, item.Ta))

        print("%i Consumer \t----> OK \n" % (len(self.consumer())))

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