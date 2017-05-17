#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 12:41:52 2017

@author: johannes
"""
import os
import sys
from DataIO import DataIO
from Consumer import Consumer
sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'function')

class HeatSink():
    def __init__(self, tableOfConsumer):

        self._instancesOfConsumer = []

        self.__importConsumer(tableOfConsumer)


        self.consumers_m = self.__consumers_m

    def __importConsumer(self, tableOfConsumer):

        for item in tableOfConsumer:
            self._instancesOfConsumer.append(Consumer(item))


    def consumer(self, i = slice(None,None)):
        return self._instancesOfConsumer[i]

    def averageReturnTemperature(self):
        sumQ = 0
        sumQT = 0
        for i in self.consumer():
            sumQT += i.heat_demand * i.return_temperature
            sumQ += i.heat_demand
        return sumQT / sumQ


    def __consumerProfile(self):
        pass

    def __consumers_m(self):
        arr = [0]*len(self.consumer())
        for index, item in enumerate(self.consumer()):
            arr[index] = item.massflow
        return arr
            