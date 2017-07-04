# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 16:50:22 2017
@author: jpelda"""
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'class')
print(os.path.dirname(os.getcwd()) + os.sep + 'class')
sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'function')
print(os.path.dirname(os.getcwd()) + os.sep + 'function')

from Pipe import Pipe
from Node import Node
import findAdditionalElements


class HeatGrid():

    def __init__(self, tableOfPipes, tableOfNodes,
                 producersSupplyNode=None, producersReturnNode=None):
        '''
        input:
            tableOfPipes = [] # contains all Pipes of network, \
                allocation Dictionary can be found in Dictionary \n
            tableOfNodes = [] # same as tabelOfPipes but for nodes \n
            producersSupplyNode = [] is given by 
                [[val, None],[val, None], ...], out of this all pipes with
            val and additional numbers are written into pipes_sp\n
            producersRetrunNode = [] is given by 
                [[val, None], [val, None], ...], out of this all pipes with
                val and additional numbers are written into pipes_rp\n
        '''

        self._instancesPipe = []
        self._instancesNode = []
        self.__importPipes(tableOfPipes)
        self.__importNodes(tableOfNodes)
        print(self._instancesPipe)
        print(self._instancesNode)
        print(self._instancesPipe[1].start_)
        self.nodes_names = self.__nodes_names()

#    def pipes_sp(self):
#        return findAdditionalElements(
#                producersSupplyNode,
#                [self.pipes(i).start_x, self.pipes(i).end_x])
        
    
    def pipes_rp(self):
        pass
    
    def pipes(self, i=slice(None, None)):
        return self._instancesPipe[i]

    def nodes(self, i=slice(None, None)):
        return self._instancesNode[i]

    def __importPipes(self, arr):
        for item in arr:
            self._instancesPipe.append(Pipe(item))

    def __importNodes(self, arr):
        for item in arr:
            self._instancesNode.append(Node(item))

    def __nodes_names(self):
        returnArray = [0]*len(self.nodes())
        for index, item in enumerate(self.nodes()):
            returnArray[index] = item.name
        return returnArray

if __name__ == "__main__":
    print('HeatGrid run directly')
    from DataIO import DataIO
    import Dictionary
    import os

    DataIO = DataIO(os.path.dirname(os.getcwd()) + os.sep + 'input',
                    os.path.dirname(os.getcwd()) + os.sep + 'output')

    heatgrid_nodes = DataIO.importCSV(
            'heatnet_nodes.csv',
            dtype=Dictionary.HeatGrid_node_dtype,
            startrow=1,
            columnofdate=None,
            dateformat='None')
    #  print(heatgrid_nodes['name'])

    heatgrid_pipes = DataIO.importCSV(
            'heatnet_pipes.csv',
            dtype=Dictionary.HeatGrid_pipe_dtype,
            startrow=1,
            columnofdate=None,
            dateformat='None')
    heatgrid = HeatGrid(heatgrid_pipes, heatgrid_nodes)

#  TODO work for supply return pipe calculation
    arr = heatgrid.pipes()
    firstNodeOfSupply = 1
    arrOfNumbersOfSupplyPipes = []
    i = 0
    while i < len(arr):
        print(arr[i].end_node_name)
        print(arr[i].start_node_name)
        
        if arr[i].start_node_name == "1":
            arrOfNumbersOfSupplyPipes.append(i)
        j = 0
        while j < len(arr):
            if arr[i].end_node_name == arr[j].start_node_name:
                arrOfNumbersOfSupplyPipes.append(i)
            j = j + 1
        i = i + 1
    print(arrOfNumbersOfSupplyPipes)
else:
    print('HeatGrid was imported into another module')
