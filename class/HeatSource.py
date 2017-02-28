# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:55:48 2017

@author: jpelda
"""
from Producer import Producer

class HeatSource():

    def __init__(self, tableOfProducer):

        self._instancesProducer = []
        self.__importProducer(tableOfProducer)
        
    def __importProducer(self, tableOfProducer):
        self._instancesProducer.append(Producer(tableOfProducer))

    def producer(self, i=slice(None,None)):
        return self._instancesProducer[i]

