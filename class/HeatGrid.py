# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 16:50:22 2017
@author: jpelda"""
import sys
import os

sys.path.append(os.getcwd())
print(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'function')
print(os.path.dirname(os.getcwd()) + os.sep + 'function')

from Finder import Finder
from Pipe import Pipe
from Node import Node

import numpy as np


class HeatGrid():

    def __init__(self, tableOfPipes, tableOfNodes,
                 nodeSupply=None, nodeReturn=None):
        '''
        input:
            tableOfPipes = [] # contains all Pipes of network, \
                allocation Dictionary can be found in Dictionary \n
            tableOfNodes = [] # same as tabelOfPipes but for nodes \n
            nodeSupply = [] is given by 
                [[val, None],[val, None], ...], out of this all pipes with
            val and additional numbers are written into pipes_sp\n
            nodeReturn = [] is given by 
                [[val, None], [val, None], ...], out of this all pipes with
                val and additional numbers are written into pipes_rp\n
        '''
        self.__nodeSupply = nodeSupply
        
        self._instancesPipe = self.__importPipes(tableOfPipes)
        
        self.__nameSupplyAndReturnPipesAndNodes(
                self.__findSupplyAndReturnPipesAndNodes())
        
        
        self._instancesNode = self.__importNodes(tableOfNodes)
        self.nodes_names = self.__nodes_names()
        
        self.__str__()

    def pipes(self, i=slice(None, None)):
        return self._instancesPipe[i]

    def pipes_start_end_node_name(self):
        arr = []
        for item in self._instancesPipe:
            arr.append(item.start_end_node_name)
        return arr

    def nodes(self, i=slice(None, None)):
        return self._instancesNode[i]

    def __findSupplyAndReturnPipesAndNodes(self):
        '''
        gets an arr of all supply pipes,
        find by class Finder method findAllItems
        '''
        search_list = []
        for item in self.pipes():
            search_list.append(item.start_end_node_name)
        arr = Finder().findAllItems(self.__nodeSupply, search_list)
        return arr

    def __nameSupplyAndReturnPipesAndNodes(self, arr):
        '''
        names all Pipes at sp_rp with 1 for supply pipe and 0 for return pipe
        '''
        arr_pipes = self.pipes_start_end_node_name()

        for index, item in enumerate(arr_pipes):
            for item1 in arr:
                if item == item1:
                    self.pipes(index).sp_rp = 1
                    break
                else:
                    self.pipes(index).sp_rp = 0

    def __importPipes(self, arr):
        retArr = []
        for item in arr:
            retArr.append(Pipe(item))
        return retArr

    def __importNodes(self, arr):
        retArr = []
        for item in arr:
            retArr.append(Node(item))
        return retArr

    def __nodes_names(self):
        returnArray = [0]*len(self.nodes())
        for index, item in enumerate(self.nodes()):
            returnArray[index] = item.name
        return returnArray

    def __str__(self):
        for item in self.pipes():
            print("Loaded Pipe: RP/SP %s sNode %s eNode %s"
                  % (str(item.sp_rp),
                     item.start_node_name,
                     item.end_node_name))

if __name__ == "__main__":
    print('HeatGrid run directly')
    from DataIO import DataIO
    import Dictionary
    import os

    DataIO = DataIO(os.path.dirname(os.getcwd()) + os.sep + 'input',
                    os.path.dirname(os.getcwd()) + os.sep + 'output')

    heatgrid_nodes = DataIO.importDBF(
        'TestNetz' + os.sep + 'KTestNetz.DBF',
        Dictionary.HeatGrid_node_dtype,
        Dictionary.HeatGrid_STANET_nodes_allocation)

    heatgrid_pipes = DataIO.importDBF(
        'TestNetz' + os.sep + 'STestNetz.DBF',
        Dictionary.HeatGrid_pipe_dtype,
        Dictionary.HeatGrid_STANET_pipes_allocation)
    
    testGrid = HeatGrid(heatgrid_pipes, heatgrid_nodes, [["K1017",None]])


else:
    print('HeatGrid was imported into another module')
    

