# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 16:50:22 2017
@author: jpelda"""

import sys
import os

from Finder import Finder
from Pipe import Pipe
from Node import Node
import time
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


        length = len(tableOfPipes)
        self.v_pipes_index = np.arange(length)
        self.v_pipes_start_x = np.array(tableOfPipes['start_x'])
        self.v_pipes_start_y = np.array(tableOfPipes['start_y'])
        self.v_pipes_end_x = np.array(tableOfPipes['end_x'])
        self.v_pipes_end_y = np.array(tableOfPipes['end_y'])
        self.v_pipes_sNode = np.array(tableOfPipes['sNode'])
        self.v_pipes_eNode = np.array(tableOfPipes['eNode'])
        self.v_pipes_length = np.array(tableOfPipes['length'])
        self.v_pipes_diameter_inner = np.array(tableOfPipes['diameter_inner'])
#        self.v_pipes_diameter_middleinner = tableOfPipes['diameter_middleinner']
#        self.v_pipes_diameter_middleouter = tableOfPipes['diameter_middleouter']
        self.v_pipes_diamter_outer = np.array(tableOfPipes['diameter_outer'])
        self.v_pipes_sHeight = np.array(tableOfPipes['start_height'])
        self.v_pipes_eHeight = np.array(tableOfPipes['end_height'])
        self.v_pipes_roughness = np.array(tableOfPipes['roughness'])
#        
#        self.v_pipes_conductivity_inner = tableOfPipes['conductivity_inner']
#        self.v_pipes_conductivity_middle = tableOfPipes['conductivity_middle']
#        self.v_pipes_conductivity_outer = tableOfPipes['conductivity_outer']

        self.v_pipes_element = ['pipe'] * length
        self.v_pipes_Q = np.array([0.0] * length)
        self.v_pipes_m = np.array([0.0] * length)
        self.v_pipes_Ta = np.array([0.0] * length)
        self.v_pipes_Tb = np.array([0.0] * length)
        self.v_pipes_Pa = np.array([0.0] * length)
        self.v_pipes_Pb = np.array([0.0] * length)
        self.v_pipes_m_max = np.array(tableOfPipes['m_max'])

        length = len(tableOfNodes)
        self.v_nodes_index = np.arange(length)
        self.v_nodes_x = np.array(tableOfNodes['x'])
        self.v_nodes_y = np.array(tableOfNodes['y'])
        self.v_nodes_name = np.array(tableOfNodes['name'])
        self.v_nodes_height = np.array(tableOfNodes['height'])
        self.v_nodes_element = ['node'] * length

        self.v_pipes_esNode = np.column_stack(
                                    (self.v_pipes_eNode, self.v_pipes_sNode))
        esNodes_sprp = self.__get_pipes_sprp(nodeSupply,
                                             tableOfNodes = tableOfNodes)
        self.v_pipes_sprp = self.__set_pipes_sprp(esNodes_sprp)
        self.v_nodes_sprp = self.__set_nodes_sprp(esNodes_sprp)
        
        self.v_nodes_T = 0
        self.v_nodes_P = 0



        self.__str__(nodes=0)
        print("%i pipes \t----> OK" % (len(self.v_pipes_index)))
        self.__str__(pipes=0)
        print("%i nodes \t----> OK\n" % (len(self.v_nodes_index)))
        self._calcVals = []

    def pipes(self, i=slice(None, None)):
        return self._instancesPipe[i]

    def nodes(self, i=slice(None, None)):
        return self._instancesNode[i]

    def subdict_v_Pipes(self):
        attr = self.__dict__
        subdict = {item: attr[item] for item in attr if "v_pipes" in item}
        return subdict

    def subdict_v_Nodes(self):
        subdict = {item: attr[item] for item in attr if "v_nodes" in item}
        return subdict

    def delPipes(self, arr):
        '''
        Deletes all pipes that indices are given.
        input: arr of indices
        '''
        v_pipes = self.subdict_v_Pipes()
        for item in v_pipes:
            item.values = np.delete(item.values(), arr)

    def __get_pipes_sprp(self, nodeSupply = None, tableOfNodes = None):
        '''
        gets an arr of all supply pipes,
        find by class Finder method findAllItems
        return: []
        '''
        if 'sprp' not in tableOfNodes:
            arr = Finder().findAllItems(nodeSupply,
                                        self.v_pipes_esNode)
        else:
            arr = []
            for item0, name in zip(tableOfNodes['sprp'], self.v_nodes_name):
                if item0 is 'J':
                    for index, item1 in enumerate(self.v_pipes_esNode):
                        if (item1[0] or item1[1]) in name:
                            arr.append(item1)
        return arr

    def __set_pipes_sprp(self, arr):
        '''
        names all pipes at sp_rp with 1 for supply pipe and 0 for return pipe
        '''
        arr_pipes = self.v_pipes_esNode

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

    def __importPipes(self, df):
        arr = []
        for index, row in df.iterrows():
            arr.append(Pipe(index, row))
        return arr

    def __importNodes(self, df):
        arr = []
        for index, row in df.iterrows():
            arr.append(Node(index, row))
        return arr



    def getCalculations(self, i=slice(None,None)):
        return self._calcVals[i]

    def setCalculations(self):
        attr = self.__dict__
        attr = {item: attr[item] for item in attr if item not in
                ("_instancesPipe",
                 "_instancesNode",
                 "__str__",
                 "calcVals")}
        self._calcVals.append(attr)



    def pipes_operatingLoad(self):
        arr = self.v_pipes_m_max / 100
        arr = self.v_pipes_m / arr
        return arr

    def __str__(self, pipes=1, nodes=1):
        if pipes is 1:
            index = 0
            for element, sprp, sNode, eNode, length,\
                diameter_inner, diameter_outer, sprp in zip(
                        self.v_pipes_element, self.v_pipes_sprp,
                        self.v_pipes_sNode, self.v_pipes_eNode,
                        self.v_pipes_length,
                        self.v_pipes_diameter_inner,
                        self.v_pipes_diamter_outer,
                        self.v_pipes_sprp):
                if index < 1:
                    print("%s: sprp %i length %4.1f [m] "
                      "d_i %4.2f [m] d_o %4.2f [m] sNode %s "
                      "eNode %s" % (element, sprp, length,
                                    diameter_inner, diameter_outer,
                                    sNode, eNode))
                    index = index + 1
                else:
                    break
        if nodes is 1:
            index = 0
            for element, name, sprp in zip(
                                            self.v_nodes_element,
                                            self.v_nodes_name,
                                            self.v_nodes_sprp):
                if index < 1:
                    print("%s: sprp %i name %s \t\t\t\t\t\t\t\t\t" % (
                            element, sprp, name))
                    index = index + 1
                else:
                    break


if __name__ == "__main__":
    from DataIO import DataIO
    import Dictionary

    print('HeatGrid \t\t run directly')

    DataIO = DataIO(
                os.path.dirname(os.getcwd()) + os.sep +
                'input' + os.sep + 'TestNetz',
                os.path.dirname(os.getcwd()) + os.sep +
                'output' + os.sep + 'TestNetz')

    heatgrid_nodes = DataIO.importDBF(
            'KTestNetz.DBF', dtype=Dictionary.STANET_nodes_allocation)

    heatgrid_pipes = DataIO.importDBF(
            'STestNetz.DBF', dtype=Dictionary.STANET_pipes_allocation)

    testGrid = HeatGrid(heatgrid_pipes, heatgrid_nodes, [["K1017", None]])
    testGrid.subdict_v_Pipes()

else:
    print('HeatGrid \t\t was imported into another module')
    sys.path.append(os.getcwd())
#    print(os.getcwd())
