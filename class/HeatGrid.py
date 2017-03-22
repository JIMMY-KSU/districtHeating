# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 16:50:22 2017
@author: jpelda"""

from Pipe import Pipe
from Node import Node


class HeatGrid():

    def __init__(self, tableOfPipes, tableOfNodes):
        '''
        input:
            tableOfPipes = [] # contains all Pipes of network, \
                allocation Dictionary can be found in Dictionary
            tableOfNodes = [] # same as tabelOfPipes but for nodes
            SP = '' # name in imported tables for supply line
            RP = '' # name in imported tables for return line
        '''
        self.__tableOfPipes = tableOfPipes
        self.__tableOfNodes = tableOfNodes
        self._instancesPipe = []
        self._instancesNode = []
        self.__importPipes()
        self.__importNodes()

        self.nodes_names = self.__nodes_names()

    def __importPipes(self):

        for item in self.__tableOfPipes:

            self._instancesPipe.append(Pipe(item))

    def __importNodes(self):
        for item in self.__tableOfNodes:

            self._instancesNode.append(Node(item))

    def pipes(self, i=slice(None, None)):
        return self._instancesPipe[i]
    
    def nodes(self, i=slice(None, None)):
        return self._instancesNode[i]

    def __nodes_names(self):
        returnArray = [0]*len(self.nodes())
        for index, item in enumerate(self.nodes()):
            returnArray[index] = item.name
        return returnArray
    
if __name__=="__main__":
    print('HeatGrid is being run directly')
else:
    print('HeatGrid is being imported into another module')
