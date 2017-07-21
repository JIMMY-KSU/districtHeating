# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:55:48 2017

@author: jpelda
"""

import numpy as np
from Producer import Producer

class HeatSource():

    def __init__(self, tableOfProducer):

        self._instancesProducer = self.__importProducers(tableOfProducer)
        
        self.nodes = self.__nodes()
        self.sNodes = self.__sNodes()
        self.eNodes = self.__eNodes()
        
        self.supply_pressure = 7
        self.return_pressure = 1
        self.supply_temperature = 130 + 273.15

        arr = self.__producers()
        self.v_producers_index = arr[0]
        self.v_producers_Q = np.asarray(arr[1])
        self.v_producers_m = np.asarray(arr[2])
        self.v_producers_Ta = np.asarray(arr[3])
        self.v_producers_Tb = np.asarray(arr[4])  # supply temperature
        self.v_producers_Pb = np.asarray(arr[5])  # supply pressure
        self.v_producers_Pa = np.asarray(arr[6])  # return pressure
        self.v_producers_sNode = arr[7]
        self.v_producers_eNode = arr[8]
        self.v_producers_element = arr[9]
        self.v_producers_start_x = arr[10]
        self.v_producers_start_y = arr[11]
        self.v_producers_end_x = arr[12]
        self.v_producers_end_y = arr[13]

        self.__str__()
        print("%i producer \t----> OK \n" % (len(self.producers())))

        self.calcVals = []


    def producers(self, i=slice(None, None)):
        return self._instancesProducer[i]

    def __nodes(self):
        arr = [[0, 0]]*len(self.producers())
        for index, item in enumerate(self.producers()):
            arr[index] = [item.sNode, item.eNode]
        return arr

    def __sNodes(self):
        arr = [[None, None]]*len(self.producers())
        for index, item in enumerate(self.producers()):
            arr[index] = [item.sNode, None]
        return arr

    def __eNodes(self):
        arr = [[None, None]]*len(self.producers())
        for index, item in enumerate(self.producers()):
            arr[index] = [item.eNode, None]
        return arr

    def __producers(self):
        length = len(self.producers())
        retarr_index = [0]*length
        retarr_Q = [0]*length
        retarr_m = [0]*length
        retarr_Ta = [0]*length
        retarr_Tb = [0]*length  # Tb is supply temperature
        retarr_Pa = [0]*length  # Pa is return pressure
        retarr_Pb = [0]*length  # Pb is supply pressure
        retarr_sNode = [0]*length
        retarr_eNode = [0]*length
        retarr_element = [0]*length
        retarr_start_x = [0]*length
        retarr_start_y = [0]*length
        retarr_end_x = [0]*length
        retarr_end_y = [0]*length
        for index, item in enumerate(self.producers()):
            retarr_index[index] = item.index
            retarr_Q[index] = item.Q
            retarr_m[index] = item.m
            retarr_Ta[index] = item.Ta
            retarr_Tb[index] = item.Tb
            retarr_Pa[index] = item.Pa
            retarr_Pb[index] = item.Pb
            retarr_sNode[index] = item.sNode
            retarr_eNode[index] = item.eNode
            retarr_element[index] = item.element
            retarr_start_x[index] = item.start_x
            retarr_start_y[index] = item.start_y
            retarr_end_x[index] = item.end_x
            retarr_end_y[index] = item.end_y
        return retarr_index, retarr_Q, retarr_m, retarr_Ta, retarr_Tb,\
            retarr_Pa, retarr_Pb,\
            retarr_sNode, retarr_eNode, retarr_element,\
            retarr_start_x, retarr_start_y, retarr_end_x, retarr_end_y

    def __importProducers(self, tableOfProducer):
        arr = []
        for item in [tableOfProducer]:
            arr.append(Producer(tableOfProducer))
        return arr

    def setCalculations(self):
        attr = self.__dict__
        attr = {item: attr[item] for item in attr if item not in
                ("_instancesProducers",
                 "__str__",
                 "calcVals")}
        self.calcVals.append(attr)

    def getCalculations(self, i=slice(None,None)):
        return self.calcVals[i]

    def __str__(self):
        for element, index, Q, m, Ta, Tb, Pa, Pb, sNode, eNode in zip(
                self.v_producers_element,
                self.v_producers_index,
                self.v_producers_Q,
                self.v_producers_m,
                self.v_producers_Ta,
                self.v_producers_Tb,
                self.v_producers_Pa,
                self.v_producers_Pb,
                self.v_producers_sNode,
                self.v_producers_eNode):
            print("%s: i %s Q %10.f [W] m %7.3f [m/s] Ta %3.2f [K] "
                  "Tb %3.2f [K] Pa %6.f [Pa] Pb %6.f [Pa] sNode %s eNode %s"
                  % (element, index, Q, m, Ta, Tb, Pa, Pb, sNode, eNode))

if __name__ == "__main__":
    import os
    from DataIO import DataIO
    import Dictionary
    print('HeatSource \t\t run directly \n')
    
    DataIO = DataIO(
            os.path.dirname(os.getcwd()) + os.sep + 'input',
            os.path.dirname(os.getcwd()) + os.sep + 'output')
    
    heatsource = DataIO.importCSV(
        'TestNetz' + os.sep + 'WTestNetz.csv',
        dtype=Dictionary.HeatSource_producer_dtype,
        startrow=1,
        columnofdate=None,
        dateformat='None')
    
    testSource = HeatSource(heatsource)
    testSource.setCalculations()
    print(testSource.getCalculations())
    
else:
    print('HeatSource \t\t was imported into another module')