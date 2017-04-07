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

        self._instancesPipe = []
        self._instancesNode = []
        self.__importPipes(tableOfPipes)
        self.__importNodes(tableOfNodes)

        self.nodes_names = self.__nodes_names()

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
            dtypeSource=Dictionary.HeatGrid_node_dtype,
            startrow=1,
            columnofdate=None,
            dateformat='None')
    #  print(heatgrid_nodes['name'])

    heatgrid_pipes = DataIO.importCSV(
            'heatnet_pipes.csv',
            dtypeSource=Dictionary.HeatGrid_pipe_dtype,
            startrow=1,
            columnofdate=None,
            dateformat='None')
    heatgrid = HeatGrid(heatgrid_pipes, heatgrid_nodes)
else:
    print('HeatGrid was imported into another module')
