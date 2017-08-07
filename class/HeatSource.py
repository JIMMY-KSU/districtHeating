# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:55:48 2017

@author: jpelda
"""

import numpy as np
from Producer import Producer

class HeatSource():

    def __init__(self, tableOfProducer):

        Tb = 130 + 273.15
        Ta = 0.0
        Pa = 100000.0  # return pressure [Pa] 1bar = 100000Pa
        Pb = 700000.0  # supply pressure [Pa] 7bar = 700000Pa
        
        self._instancesProducer = self.__importProducers(tableOfProducer)

        self.nodes = self.__nodes()
        self.sNodes = self.__sNodes()
        self.eNodes = self.__eNodes()

        length = len(tableOfProducer)
        self.v_producers_name = np.array(tableOfProducer['name'])
        self.v_producers_Q = np.array([0.0] * length)
        self.v_producers_m = np.array([0.0] * length)
        self.v_producers_Ta = np.array([Ta] * length)
        self.v_producers_Tb = np.array([Tb] * length)  # supply temperature
        self.v_producers_Pa = np.array([Pa] * length)  # return pressure
        self.v_producers_Pb = np.array([Pb] * length)  # supply pressure
        self.v_producers_sNode = np.array(tableOfProducer['sNode'])
        self.v_producers_eNode = np.array(tableOfProducer['eNode'])
        self.v_producers_esNode = np.column_stack((self.v_producers_eNode,
                                                   self.v_producers_sNode))
        self.v_producers_element = ['producer'] * length
        self.v_producers_start_x = np.array(tableOfProducer['start_x'])
        self.v_producers_start_y = np.array(tableOfProducer['start_y'])
        self.v_producers_end_x = np.array(tableOfProducer['end_x'])
        self.v_producers_end_y = np.array(tableOfProducer['end_y'])
        self.v_producers_index = np.arange(length)

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

    def __importProducers(self, df):
        arr = []
        for index, row in df.iterrows():
            arr.append(Producer(index, row))
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
        index = 0
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
            if index < 1:
                print("%s: i %s Q %10.f [W] m %7.3f [m/s] Ta %3.2f [K] "
                      "Tb %3.2f [K] Pa %6.f [Pa] Pb %6.f [Pa] sNode %s"
                      " eNode %s" % (element, index, Q, m, Ta, Tb, Pa, Pb,
                                     sNode, eNode))
                index = index + 1
            else:
                break
if __name__ == "__main__":
    import os
    from DataIO import DataIO
    import Dictionary
    print('HeatSource \t\t run directly \n')
    
    DataIO = DataIO(
                os.path.dirname(os.getcwd()) + os.sep +
                'input' + os.sep + 'TestNetz',
                os.path.dirname(os.getcwd()) + os.sep +
                'output' + os.sep + 'TestNetz')
    
    heatsource = DataIO.importCSV(
            'WTestNetz.csv', dtype=Dictionary.STANET_producer_allocation,
            delimiter='\t', header=0)
    
    testSource = HeatSource(heatsource)
    testSource.setCalculations()
#    print(testSource.getCalculations())
    
else:
    print('HeatSource \t\t was imported into another module')