# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 16:50:22 2017
@author: jpelda"""

import sys
import os

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

        self._instancesPipe = self.__importPipes(tableOfPipes)
        self._instancesNode = self.__importNodes(tableOfNodes)

        self.v_pipes_index = self.__pipes()[0]
        self.v_pipes_start_x = self.__pipes()[1]
        self.v_pipes_start_y = self.__pipes()[2]
        self.v_pipes_end_x = self.__pipes()[3]
        self.v_pipes_end_y = self.__pipes()[4]
        self.v_pipes_start_node_name = self.__pipes()[5]
        self.v_pipes_end_node_name = self.__pipes()[6]
        self.v_pipes_length = self.__pipes()[7]
        self.v_pipes_diameter_inner = self.__pipes()[8]
        self.v_pipes_diamter_outer = self.__pipes()[9]
        self.v_pipes_start_height = self.__pipes()[10]
        self.v_pipes_end_height = self.__pipes()[11]
        self.v_pipes_roughness = self.__pipes()[12]
        self.v_pipes_sprp = self.__pipes()[13]

        self.v_nodes_index = self.__nodes()[0]
        self.v_nodes_x = self.__nodes()[1]
        self.v_nodes_y = self.__nodes()[2]
        self.v_nodes_name = self.__nodes()[3]
        self.v_nodes_height = self.__nodes()[4]
        self.v_nodes_sprp = self.__nodes()[5]

        self.v_pipes_start_end_node_name = np.column_stack(
                (self.v_pipes_start_node_name, self.v_pipes_end_node_name))
        self.__set_sprp(
                self.__get_sprp(nodeSupply))

        self.__str__()

    def pipes(self, i=slice(None, None)):
        return self._instancesPipe[i]

    def nodes(self, i=slice(None, None)):
        return self._instancesNode[i]

    def __get_sprp(self, nodeSupply):
        '''
        gets an arr of all supply pipes,
        find by class Finder method findAllItems
        '''
        search_list = []
        for item in self.pipes():
            search_list.append(item.start_end_node_name)
        arr = Finder().findAllItems(nodeSupply,
                                    self.v_pipes_start_end_node_name)
        return arr

    def __set_sprp(self, arr):
        '''
        names all Pipes at sp_rp with 1 for supply pipe and 0 for return pipe
        '''
        arr_pipes = self.v_pipes_start_end_node_name

        for index, item in enumerate(arr_pipes):
            for item1 in arr:
                if np.array_equal(item, item1):
                    self.pipes(index).sprp = 1
                    break
                else:
                    self.pipes(index).sprp = 0

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

    def __pipes(self, i=slice(None, None)):
        length = len(self.pipes())
        retarr_index = [0]*length
        retarr_start_x = [0]*length
        retarr_start_y = [0]*length
        retarr_end_x = [0]*length
        retarr_end_y = [0]*length
        retarr_start_node_name = [0]*length
        retarr_end_node_name = [0]*length
        retarr_length = [0]*length
        retarr_diameter_inner = [0]*length
        retarr_diameter_outer = [0]*length
        retarr_start_height = [0]*length
        retarr_end_height = [0]*length
        retarr_roughness = [0]*length
        retarr_sprp = [0]*length
        for index, item in enumerate(self.pipes()):
            retarr_index[index] = item.index
            retarr_start_x[index] = item.start_x
            retarr_start_y[index] = item.start_y
            retarr_end_x[index] = item.end_x
            retarr_end_y[index] = item.end_y
            retarr_start_node_name[index] = item.start_node_name
            retarr_end_node_name[index] = item.end_node_name
            retarr_length[index] = item.length
            retarr_diameter_inner[index] = item.diameter_inner
            retarr_diameter_outer[index] = item.diameter_outer
            retarr_start_height[index] = item.start_height
            retarr_end_height[index] = item.end_height
            retarr_roughness[index] = item.roughness
            retarr_sprp[index] = item.sprp
        return retarr_index, retarr_start_x, retarr_start_y, retarr_end_x,\
            retarr_end_y, retarr_start_node_name, retarr_end_node_name,\
            retarr_length, retarr_diameter_inner, retarr_diameter_outer,\
            retarr_start_height, retarr_end_height, retarr_roughness,\
            retarr_sprp

    def __nodes(self):
        retarr_index = [0]*len(self.nodes())
        retarr_x = [0]*len(self.nodes())
        retarr_y = [0]*len(self.nodes())
        retarr_name = [0]*len(self.nodes())
        retarr_height = [0]*len(self.nodes())
        retarr_sprp = [0]*len(self.nodes())
        for index, item in enumerate(self.nodes()):
            retarr_index[index] = item.index
            retarr_x[index] = item.x
            retarr_y[index] = item.y
            retarr_name[index] = item.name
            retarr_height[index] = item.height
            retarr_sprp[index] = item.sprp
        return retarr_index, retarr_x, retarr_y,\
            retarr_name, retarr_height, retarr_sprp

    def __str__(self):
        for item in self.pipes():
            print("Pipe: RP/SP %s sNode %s eNode %s"
                  % (str(item.sprp),
                     item.start_node_name,
                     item.end_node_name))
        print("%i Pipes ----> OK\n" % (len(self.pipes())))

if __name__ == "__main__":
    from DataIO import DataIO
    import Dictionary

    print('HeatGrid run directly')

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

    testGrid = HeatGrid(heatgrid_pipes, heatgrid_nodes, [["K1017", None]])


else:
    print('HeatGrid was imported into another module')
    sys.path.append(os.getcwd())
#    print(os.getcwd())
