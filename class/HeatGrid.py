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
import math


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
#        print(tableOfPipes)

        self.lengthPipes = len(tableOfPipes)
        self.v_pipes_index = np.arange(self.lengthPipes)
        self.v_pipes_start_x = np.array(tableOfPipes['start_x'])
        self.v_pipes_start_y = np.array(tableOfPipes['start_y'])
        self.v_pipes_end_x = np.array(tableOfPipes['end_x'])
        self.v_pipes_end_y = np.array(tableOfPipes['end_y'])
        self.v_pipes_sNode = np.array(tableOfPipes['sNode'])
        self.v_pipes_eNode = np.array(tableOfPipes['eNode'])

        self.transferCoefficient_inner = np.array(
                [46.5] * self.lengthPipes)  # [W/mK] fluid pipe
        self.transferCoefficient_outer = np.array(
                [1] * self.lengthPipes)  # [W/mK] pipe ground



        self.v_pipes_length = np.array(tableOfPipes['length'])  # m

        self.v_pipes_diameter_0,\
        self.v_pipes_diameter_1,\
        self.v_pipes_diameter_2,\
        self.v_pipes_diameter_3 = self.__set_pipes_diameter(tableOfPipes)

        self.v_pipes_conductivity_0,\
        self.v_pipes_conductivity_1,\
        self.v_pipes_conductivity_2 = self.__set_pipes_conductivity(
                tableOfPipes)

        self.__v_pipes_thermalTransmissionCoefficient = tableOfPipes[
                'thermalTransmissionCoefficient']  # [W/m²K]
        self.__v_pipes_resistivity = tableOfPipes['resistivity']  # [W/K]
        self.v_pipes_resistivity = self.__calc_resistivity()

        self.v_pipes_sHeight = np.array(tableOfPipes['start_height'])
        self.v_pipes_eHeight = np.array(tableOfPipes['end_height'])
        self.v_pipes_roughness = np.array(tableOfPipes['roughness'])

#        self.v_pipes_conductivity_inner = tableOfPipes['conductivity_inner']
#        self.v_pipes_conductivity_middle = tableOfPipes['conductivity_middle']
#        self.v_pipes_conductivity_outer = tableOfPipes['conductivity_outer']

        self.v_pipes_element = ['pipe'] * self.lengthPipes
        self.v_pipes_Q = np.array([0.0] * self.lengthPipes)
        self.v_pipes_m = np.array([0.0] * self.lengthPipes)
        self.v_pipes_Ta = np.array([0.0] * self.lengthPipes)
        self.v_pipes_Tb = np.array([0.0] * self.lengthPipes)
        self.v_pipes_Pa = np.array([0.0] * self.lengthPipes)
        self.v_pipes_Pb = np.array([0.0] * self.lengthPipes)

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

    def __calc_resistivity(self):
        '''
        returns thermal resistivity
        '''
        if not np.isnan(self.__v_pipes_resistivity).all():
            thRes = self.__v_pipes_resistivity * self.v_pipes_length  # [W/K]
        elif not np.isnan(self.__v_pipes_thermalTransmissionCoefficient).all():
            thRes = self.__v_pipes_thermalTransmissionCoefficient *\
                    self.v_pipes_length * self.v_pipes_diameter_3 *\
                    math.pi  # [W/K]
        else:
#            if self.v_pipes_diameter_0.all() is None and\
#               self.v_pipes_diameter_1.all() is None and\
#               self.v_pipes_diameter_2.all() is None and\
#               self.v_pipes_diameter_3.all() is None and\
#               self.v_pipes_conductivity_0.all() is None and\
#               self.v_pipes_conductivity_1.all() is None and\
#               self.v_pipes_conductivity_2.all() is None and\
#               self.v_pipes_length.all() is None:
#                thRes = tableOfPipes['resistivity']
            if self.v_pipes_diameter_0.all() is not None and\
               self.v_pipes_diameter_1.all() is None and\
               self.v_pipes_diameter_2.all() is None and\
               self.v_pipes_diameter_3.all() is not None and\
               self.v_pipes_conductivity_0.all() is not None or\
               self.v_pipes_conductivity_1.all() is not None or\
               self.v_pipes_conductivity_2.all() is not None and\
               self.v_pipes_length.all() is not None:
                conductivity = self.v_pipes_conductivity_0 +\
                                self.v_pipes_conductivity_1 +\
                                self.v_pipes_conductivity_2
                thRes = (2 * math.pi * self.v_pipes_length) / (
                    (1 / conductivity) *
                    np.log(self.v_pipes_diameter_3 / self.v_pipes_diameter_0)
                    )  # [W/K]
            else:
                thRes = (2 * math.pi * self.v_pipes_length) * (
                    (1 / self.v_pipes_conductivity_0) *
                    np.log(self.v_pipes_diameter_1 / self.v_pipes_diameter_0) +
                    (1 / self.v_pipes_conductivity_1) *
                    np.log(self.v_pipes_diameter_2 / self.v_pipes_diameter_1) +
                    (1 / self.v_pipes_conductivity_2) *
                    np.log(self.v_pipes_diameter_3 / self.v_pipes_diameter_2)
                    )  # [W/K]
        return thRes

    def __get_pipes_sprp(self, nodeSupply=None, tableOfNodes=None):
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

    def __set_pipes_conductivity(self, tableOfPipes):
        '''
        Sets the conductivity [W/mK] of Pipes.
        conductivity_0 [W/mK] pipe material
        conductivity_1 [W/mK] isolation material
        conductivity_2 [W/mK] pipe coat
        returns tuple of 3 np.arrays
        '''
        tupVal = 0
        tupVal = np.array(tableOfPipes['conductivity_0']),\
            np.array(tableOfPipes['conductivity_1']),\
            np.array(tableOfPipes['conductivity_2'])

        return tupVal

    def __set_pipes_diameter(self, tableOfPipes):
        '''
        Sets the diameters of pipes in [m]
        diameter_0 is the inner diameter, diameter_3 is the outer diamter
        returns tuple of 4 np.arrays
        '''
        tupVal = 0
        tupVal = np.array(tableOfPipes['diameter_0']),\
            np.array(tableOfPipes['diameter_1']),\
            np.array(tableOfPipes['diameter_2']),\
            np.array(tableOfPipes['diameter_3'])

        return tupVal

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


    def __str__(self, pipes=1, nodes=1):
        if pipes is 1:
            index = 0
            for element, sprp, sNode, eNode, length,\
                diameter_inner, diameter_outer, sprp, resistivity in zip(
                        self.v_pipes_element, self.v_pipes_sprp,
                        self.v_pipes_sNode, self.v_pipes_eNode,
                        self.v_pipes_length,
                        self.v_pipes_diameter_0,
                        self.v_pipes_diameter_3,
                        self.v_pipes_sprp,
                        self.v_pipes_resistivity):
                if index < 1:
                    print("%s: sprp %i length %4.1f [m] "
                      "d_0 %4.2f [m] d_3 %4.2f [m] resistivity %2.2f [W/K] "
                      "sNode %s eNode %s" % (element, sprp, length,
                                             diameter_inner, diameter_outer,
                                             resistivity, sNode, eNode))
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
                'input' + os.sep + 'TestNetze' + os.sep +
                'TestNetz_einEinspeiser',
                os.path.dirname(os.getcwd()) + os.sep +
                'output' + os.sep + 'TestNetze' + os.sep +
                'TestNetz_einEinspeiser')

    heatgrid_nodes = DataIO.importDBF(
            'KTestNetz_einEinspeiser.DBF', dtype=Dictionary.STANET_nodes_allocation)

    heatgrid_pipes = DataIO.importDBF(
            'STestNetz_einEinspeiser.DBF', dtype=Dictionary.STANET_pipes_allocation)

    testGrid = HeatGrid(heatgrid_pipes, heatgrid_nodes, [["K1017", None]])
    testGrid.subdict_v_Pipes()

else:
    print('HeatGrid \t\t was imported into another module')
    sys.path.append(os.getcwd())
#    print(os.getcwd())
