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
        self.v_consumers_start_node_name = self.__consumers()[5]
        self.v_consumers_end_node_name = self.__consumers()[6]
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
        retarr_index = [0]*length
        retarr_start_x = [0]*length
        retarr_start_y = [0]*length
        retarr_end_x = [0]*length
        retarr_end_y = [0]*length
        retarr_start_node_name = [0]*length
        retarr_end_node_name = [0]*length
        retarr_heat_profile = [0]*length
        retarr_heat_average = [0]*length
        retarr_m = [0]*length
        retarr_Q = [0]*length
        retarr_cp = [0]*length
        retarr_Ta = [0]*length
        retarr_Tb = [0]*length

        for index, item in enumerate(self.consumer()):
            retarr_index[index] = item.index
            retarr_start_x = item.start_x
            retarr_start_y = item.start_y
            retarr_end_x = item.end_x
            retarr_end_y = item.end_y
            retarr_start_node_name = item.start_node_name
            retarr_end_node_name = item.end_node_name
            retarr_heat_profile = item.heat_profile
            retarr_heat_average = item.heat_average
            retarr_m = item.m
            retarr_Q = item.Q
            retarr_cp = item.cp
            retarr_Ta = item.Ta
            retarr_Tb = item.Tb
        return retarr_index, retarr_start_x, retarr_start_y, retarr_end_x,\
            retarr_end_y, retarr_start_node_name, retarr_end_node_name,\
            retarr_heat_profile, retarr_heat_average, retarr_m, retarr_Q,\
            retarr_cp, retarr_Ta, retarr_Tb

    def __importConsumer(self, arr):
        retArr = [0]*len(arr)
        for index, item in enumerate(arr):
            retArr[index] = Consumer(item)
        return np.asarray(retArr)

    def __str__(self):
        for item in self.consumer():
            print("Consumer: index %i heatexchanger %s sNode %s eNode %s m %f"
                  % (item.index, item.heat_exchangerModel,
                  item.start_node_name, item.end_node_name, item.m))
        print("%i Consumer  ----> OK \n" % (len(self.consumer())))

if __name__ == "__main__":
    from DataIO import DataIO
    import Dictionary
    print('HeatSink run directly')
    
    DataIO = DataIO(os.path.dirname(os.getcwd()) + os.sep + 'input',
                    os.path.dirname(os.getcwd()) + os.sep + 'output')

    heatsink = DataIO.importDBF(
            'TestNetz' + os.sep + 'WTestNetz.DBF',
            Dictionary.HeatSink_consumer_dtype,
            Dictionary.HeatSink_STANET_consumer_allocation)

    testSink = HeatSink(heatsink)


else:
    print('HeatGrid was imported into another module')