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

        self.__tableOfConsumer = tableOfConsumer
        self._instancesConsumer = []

        self.__importConsumer()

    def __importConsumer(self):

        for item in self.__tableOfConsumer:
            self._instancesConsumer.append(Consumer(item))


    def consumer(self, i = slice(None,None)):
        return self._instancesConsumer[i]



    def __consumerProfile(self):
        pass
