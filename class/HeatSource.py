# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:55:48 2017

@author: jpelda
"""
from Producer import Producer

class HeatSource():

    def __init__(self, tableOfProducer):

        self._instancesProducer = []
        self.__importProducer(tableOfProducer)
        
        self.nodes = self.__nodes()
        self.sNodes = self.__sNodes()
        self.eNodes = self.__eNodes()
        
        self.__str__()
        
    def __importProducer(self, tableOfProducer):
        self._instancesProducer.append(Producer(tableOfProducer))

    def producer(self, i=slice(None,None)):
        return self._instancesProducer[i]
        
    def __nodes(self):
        arr = [[0,0]]*len(self.producer())
        for index, item in enumerate(self.producer()):
            arr[index] = [item.sNode, item.eNode]
        return arr
    def __sNodes(self):
        arr = [[None,None]]*len(self.producer())
        for index, item in enumerate(self.producer()):
            arr[index] = [item.sNode, None]
        return arr
    
    def __eNodes(self):
        arr = [[None,None]]*len(self.producer())
        for index, item in enumerate(self.producer()):
            arr[index] = [item.eNode, None]
        return arr
    
    def __str__(self):
        for item in self.producer():
            print("Producer: name %s power %5.0f sNode %s eNode %s sP %2.1f rP %2.1f "
                  "sT %3.2f" % (item.name, item.power, item.sNode,
                  item.eNode, item.supply_pressure,
                  item.return_pressure, item.supply_temperature))
        print("%i Producer \t----> OK \n" % (len(self.producer())))

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