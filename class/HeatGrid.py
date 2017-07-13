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


        arr = self.__pipes()
        self.v_pipes_index = arr[0]
        self.v_pipes_start_x = arr[1]
        self.v_pipes_start_y = arr[2]
        self.v_pipes_end_x = arr[3]
        self.v_pipes_end_y = arr[4]
        self.v_pipes_sNode = arr[5]
        self.v_pipes_eNode = arr[6]
        self.v_pipes_length = np.asarray(arr[7])
        self.v_pipes_diameter_inner = np.asarray(arr[8])
        self.v_pipes_diamter_outer = np.asarray(arr[9])
        self.v_pipes_sHeight = np.asarray(arr[10])
        self.v_pipes_eHeight = np.asarray(arr[11])
        self.v_pipes_roughness = np.asarray(arr[12])
        self.v_pipes_element = arr[13]

        arr = self.__nodes()
        self.v_nodes_index = arr[0]
        self.v_nodes_x = arr[1]
        self.v_nodes_y = arr[2]
        self.v_nodes_name = arr[3]
        self.v_nodes_height = np.asarray(arr[4])
        self.v_nodes_element = arr[5]

        self.v_pipes_seNode = np.column_stack(
                                    (self.v_pipes_sNode, self.v_pipes_eNode))
        seNodes_sprp = self.__get_pipes_sprp(nodeSupply)
        self.v_pipes_sprp = self.__set_pipes_sprp(seNodes_sprp)
        self.v_nodes_sprp = self.__set_nodes_sprp(seNodes_sprp)
        self.__str__()

    def pipes(self, i=slice(None, None)):
        return self._instancesPipe[i]

    def nodes(self, i=slice(None, None)):
        return self._instancesNode[i]

    def __get_pipes_sprp(self, nodeSupply):
        '''
        gets an arr of all supply pipes,
        find by class Finder method findAllItems
        '''
        search_list = []
        for item in self.pipes():
            search_list.append(item.seNode)
        arr = Finder().findAllItems(nodeSupply,
                                    self.v_pipes_seNode)
        return arr

    def __set_pipes_sprp(self, arr):
        '''
        names all pipes at sp_rp with 1 for supply pipe and 0 for return pipe
        '''
        arr_pipes = self.v_pipes_seNode

        for index, item in enumerate(arr_pipes):
            for item1 in arr:
                if np.array_equal(item, item1):
                    self.pipes(index).sprp = 1
                    break
                else:
                    self.pipes(index).sprp = 0

        retarr_sprp = [0]*len(self.pipes())
        for index, item in enumerate(self.pipes()):
            retarr_sprp[index] = item.sprp

        return retarr_sprp

    def __set_nodes_sprp(self, arr):
        '''
        names all nodes at sprp with 1 for supply node and 0 for return node
        '''
        arr_nodes = self.v_nodes_name
        for index, item in enumerate(arr_nodes):
            for item1 in arr:
                if np.array_equal(item, item1[0])\
                    or np.array_equal(item, item1[1]):
                    self.nodes(index).sprp = 1
                    break
                else:
                    self.nodes(index).sprp = 0

        retarr_sprp = [0]*len(self.nodes())
        for index, item in enumerate(self.nodes()):
            retarr_sprp[index] = item.sprp

        return retarr_sprp

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
        retarr_sNode = [0]*length
        retarr_eNode = [0]*length
        retarr_length = [0]*length
        retarr_diameter_inner = [0]*length
        retarr_diameter_outer = [0]*length
        retarr_start_height = [0]*length
        retarr_end_height = [0]*length
        retarr_roughness = [0]*length
        retarr_element = [0]*length
        for index, item in enumerate(self.pipes()):
            retarr_index[index] = item.index
            retarr_start_x[index] = item.start_x
            retarr_start_y[index] = item.start_y
            retarr_end_x[index] = item.end_x
            retarr_end_y[index] = item.end_y
            retarr_sNode[index] = item.sNode
            retarr_eNode[index] = item.eNode
            retarr_length[index] = item.length
            retarr_diameter_inner[index] = item.diameter_inner
            retarr_diameter_outer[index] = item.diameter_outer
            retarr_start_height[index] = item.start_height
            retarr_end_height[index] = item.end_height
            retarr_roughness[index] = item.roughness
            retarr_element[index] = item.element
        return retarr_index, retarr_start_x, retarr_start_y, retarr_end_x,\
            retarr_end_y, retarr_sNode, retarr_eNode,\
            retarr_length, retarr_diameter_inner, retarr_diameter_outer,\
            retarr_start_height, retarr_end_height, retarr_roughness,\
            retarr_element

    def __nodes(self):
        length = len(self.nodes())
        retarr_index = [0]*length
        retarr_x = [0]*length
        retarr_y = [0]*length
        retarr_name = [0]*length
        retarr_height = [0]*length
        retarr_element = [0]*length
        for index, item in enumerate(self.nodes()):
            retarr_index[index] = item.index
            retarr_x[index] = item.x
            retarr_y[index] = item.y
            retarr_name[index] = item.name
            retarr_height[index] = item.height
            retarr_element[index] = item.element
        return retarr_index, retarr_x, retarr_y,\
            retarr_name, retarr_height, retarr_element

    def __str__(self):
        for element, sprp, sNode, eNode, length, diameter_inner,\
            diameter_outer, sprp in zip(self.v_pipes_element, self.v_pipes_sprp,
                                  self.v_pipes_sNode, self.v_pipes_eNode,
                                  self.v_pipes_length,
                                  self.v_pipes_diameter_inner,
                                  self.v_pipes_diamter_outer,
                                  self.v_pipes_sprp):
            print("%s: SP/RP %s sNode %s eNode %s length %4.3f "
                  "diam_outer %4.3f diam_inner %4.3f sprp %s"
                  % (element, str(sprp), sNode, eNode, length, diameter_inner,
                     diameter_outer, sprp))
        print("%i pipes \t----> OK\n" % (len(self.v_pipes_index)))

        for element, name, sprp in zip(self.v_nodes_element,
                              self.v_nodes_name, self.v_nodes_sprp):
            print("%s: name %s sprp %s" % (element, name, sprp))
        print("%i nodes \t----> OK\n" % (len(self.v_nodes_index)))

if __name__ == "__main__":
    from DataIO import DataIO
    import Dictionary

    print('HeatGrid \t\t run directly')

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
    print('HeatGrid \t\t was imported into another module')
    sys.path.append(os.getcwd())
#    print(os.getcwd())
