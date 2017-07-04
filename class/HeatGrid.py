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

from Finder import Finder
from Pipe import Pipe
from Node import Node


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
        arr = self.__setListOfSupplyPipes(
                                    self.__findSupplyAndReturnPipesAndNodes())

        self._instancesPipe_sp = arr[0]
        self._instancesPipe_rp = arr[1]
        
        self._instancesNode = self.__importNodes(tableOfNodes)
        
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
      
    def __findSupplyAndReturnPipesAndNodes(self):
        search_list = []
        for item in self.pipes():
            search_list.append(item.start_end_node_name)
#        print([self.__nodeSupply,0], search_list)
        arr = Finder().findAllItems(self.__nodeSupply, search_list)            
        return arr
        
    def __setListOfSupplyPipes(self, arr):
        arr_sp = []
        arr_rp = []
        for item0 in arr:
            for item1 in self.pipes():
                if item1.start_end_node_name == item0:
                    arr_sp.append(item1)
                else:
                    arr_rp.append(item1)
        return arr_sp, arr_rp
        
        
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
    
#  TODO work for supply return pipe calculation
    for item in testGrid.pipes():
        print("Pipes" + item.sp_rp, item.start_node_name, item.end_node_name)
    
    for index, item in enumerate(testGrid.nodes()):
        if item.sp_rp == "J":
            print(item.sp_rp, item.name, testGrid._instancesPipe_sp[index-1].start_node_name)
    for item in testGrid._instancesPipe_sp:
        print(item.start_end_node_name, item.length)
    
    for index, item in enumerate(testGrid.nodes()):
        if item.sp_rp =="N":
            print(item.sp_rp, item.name, testGrid._instancesPipe_rp[index-1].start_node_name)
        
else:
    print('HeatGrid was imported into another module')
