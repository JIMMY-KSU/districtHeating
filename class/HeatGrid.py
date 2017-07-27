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
        self.v_pipes_Q = np.asarray(arr[14])
        self.v_pipes_m = np.asarray(arr[15])
        self.v_pipes_Ta = np.asarray(arr[16])
        self.v_pipes_Tb = np.asarray(arr[17])
        self.v_pipes_Pa = np.asarray(arr[18])
        self.v_pipes_Pb = np.asarray(arr[19])

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

    def __pipes(self):
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
        retarr_Q = [0]*length
        retarr_m = [0]*length
        retarr_Ta = [0]*length
        retarr_Tb = [0]*length
        retarr_Pa = [0]*length
        retarr_Pb = [0]*length
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
            retarr_Q[index] = item.Q
            retarr_m[index] = item.m
            retarr_Ta[index] = item.Ta
            retarr_Tb[index] = item.Tb
            retarr_Pa[index] = item.Pa
            retarr_Pb[index] = item.Pb
        return retarr_index, retarr_start_x, retarr_start_y, retarr_end_x,\
            retarr_end_y, retarr_sNode, retarr_eNode,\
            retarr_length, retarr_diameter_inner, retarr_diameter_outer,\
            retarr_start_height, retarr_end_height, retarr_roughness,\
            retarr_element, retarr_Q, retarr_m, retarr_Ta, retarr_Tb,\
            retarr_Pa, retarr_Pb

#    def set_calculatedValuesIntoPipes(self, Q, m, Ta, Tb, Pa, Pb):
#        '''
#        sets customized or calculated values into pipes of HeatGrid:
#            Q, m, Ta, Tb, Pa, Pb
#        '''
#        self.v_pipes_Q = Q
#        self.v_pipes_m = m
#        self.v_pipes_Ta = Ta
#        self.v_pipes_Tb = Tb
#        self.v_pipes_Pa = Pa
#        self.v_pipes_Pb = Pb

#    def set_calculatedValuesIntoNodes(self, T, P):
#        '''
#        sets customized or calculated values into nodes of HeatGrid:
#            T, P
#        '''
#        self.v_nodes_T = T
#        self.v_nodes_P = P
#        
#        
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

    def setCalculations(self):
        attr = self.__dict__
        attr = {item: attr[item] for item in attr if item not in
                ("_instancesPipe",
                 "_instancesNode",
                 "__str__",
                 "calcVals")}
        self._calcVals.append(attr)


    def getCalculations(self, i=slice(None,None)):
        return self._calcVals[i]

    def __str__(self, pipes=1, nodes=1):
        if pipes is 1:

            for element, sprp, Q, m, Ta, Tb, Pa, Pb, sNode, eNode, length,\
                diameter_inner, diameter_outer, sprp in zip(
                        self.v_pipes_element, self.v_pipes_sprp,
                        self.v_pipes_Q, self.v_pipes_m,
                        self.v_pipes_Ta, self.v_pipes_Tb,
                        self.v_pipes_Pa, self.v_pipes_Pb,
                        self.v_pipes_sNode, self.v_pipes_eNode,
                        self.v_pipes_length,
                        self.v_pipes_diameter_inner,
                        self.v_pipes_diamter_outer,
                        self.v_pipes_sprp):
                print("%s: sprp %i Q %6.f [W] m %7.3f [m/s] Ta %3.2f [K] "
                      "Tb %3.2f [K] Pa %6.f [Pa] Pb %6.f [Pa] \n"
                      "\t\t\t\t\t\t\t\t l %4.1f [m] "
                      "d_i %4.2f [m] d_o %4.2f [m] sNode %s "
                      "eNode %s" % (element, sprp, Q, m, Ta, Tb, Pa, Pb,
                                    length, diameter_inner, diameter_outer,
                                    sNode, eNode))
        if nodes is 1:
            for element, name, sprp in zip(
                                            self.v_nodes_element,
                                            self.v_nodes_name,
                                            self.v_nodes_sprp):
                        print("%s: sprp %s \t\t\t\t\t\t\t\t\t Node %s" % (
                                element, sprp, name))

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
