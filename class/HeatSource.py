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
        
        self.nodes_names = self.__nodes_names()
        
    def __importProducer(self, tableOfProducer):
        self._instancesProducer.append(Producer(tableOfProducer))

    def producer(self, i=slice(None,None)):
        return self._instancesProducer[i]
        
    def __nodes_names(self):
        arr = [[0,0]]*len(self.producer())
        for index, item in enumerate(self.producer()):
            arr[index] = [item.start_node_name, item.end_node_name]
        return arr
