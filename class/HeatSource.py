# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:55:48 2017

@author: jpelda
"""
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
        self.v_producers_name = arr[0]
        self.v_producers_Q = arr[1]
        self.v_producers_sNode = arr[2]
        self.v_producers_eNode = arr[3]
        self.v_producers_Pb = arr[4]  # supply pressure
        self.v_producers_Pa = arr[5]  # return pressure
        self.v_producers_Tb = arr[6]  #supply temperature
        self.v_producers_element = arr[7]


        self.__str__()

    def producers(self, i=slice(None,None)):
        return self._instancesProducer[i]
        
    def __nodes(self):
        arr = [[0,0]]*len(self.producers())
        for index, item in enumerate(self.producers()):
            arr[index] = [item.sNode, item.eNode]
        return arr
    def __sNodes(self):
        arr = [[None,None]]*len(self.producers())
        for index, item in enumerate(self.producers()):
            arr[index] = [item.sNode, None]
        return arr
    
    def __eNodes(self):
        arr = [[None,None]]*len(self.producers())
        for index, item in enumerate(self.producers()):
            arr[index] = [item.eNode, None]
        return arr

    def __producers(self):
        length = len(self.producers())
        retarr_name = [0]*length
        retarr_Q = [0]*length
        retarr_sNode = [0]*length
        retarr_eNode = [0]*length
        retarr_Pb = [0]*length  # Pb is supply pressure
        retarr_Pa = [0]*length  # Pa is return pressure
        retarr_Tb = [0]*length  # Tb is supply temperature
        retarr_element = [0]*length
        for index, item in enumerate(self.producers()):
            retarr_name[index] = item.name
            retarr_Q[index] = item.Q
            retarr_sNode[index] = item.sNode
            retarr_eNode[index] = item.eNode
            retarr_Pb[index] = item.Pb
            retarr_Pa[index] = item.Pa
            retarr_Tb[index] = item.Tb
            retarr_element[index] = item.element
        return retarr_name, retarr_Q, retarr_sNode, retarr_eNode,\
            retarr_Pb, retarr_Pa, retarr_Tb, retarr_element

    def __importProducers(self, tableOfProducer):
        arr = []
        for item in [tableOfProducer]:
            arr.append(Producer(tableOfProducer))
        return arr

    def __str__(self):
        for element, name, Q, sNode, eNode, Pb, Pa, Tb in zip(
                self.v_producers_element, self.v_producers_name,
                self.v_producers_Q, self.v_producers_sNode,
                self.v_producers_eNode, self.v_producers_Pb,
                self.v_producers_Pa, self.v_producers_Tb):
            print("%s: name %s Q  %5.0f  [W] Tb %3.2f [K] "
                  "Pa %9.1f [Pa] Pb %9.1f [Pa]  sNode %s eNode %s "
                  % (element, name, Q, Tb, Pa, Pb, sNode, eNode))
        print("%i producer \t----> OK \n" % (len(self.producers())))

if __name__ == "__main__":
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
    
else:
    print('HeatSource \t\t was imported into another module')