# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 16:22:28 2017

@author: johannes
"""

import sys
import os
import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import root
import time

#sys.path.append(os.getcwd())
#print(os.getcwd())
    
sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'function')
print(os.path.dirname(os.getcwd()) + os.sep + 'function')
import dependencies as dp 

from HeatGrid import HeatGrid
from HeatSink import HeatSink
from HeatSource import HeatSource
from Plotter import Plotter
from scipy.optimize import root
from Solver import Solver
from collections import Counter


import logging
logger = logging.getLogger('stackoverflow_rocks')

class DistrictHeatingSystem():
    def __init__(self, heatgrid_pipes, heatgrid_nodes, heatsink, heatsource):

        self.heatsink = HeatSink(heatsink)
        self.heatsource = HeatSource(heatsource)
        self.heatgrid = HeatGrid(heatgrid_pipes,
                                 heatgrid_nodes,
                                 nodeSupply=np.column_stack((
                                     self.heatsource.v_producers_eNode,
                                     np.array([None]*len(
                                         self.heatsource.v_producers_eNode)))))

#        logger.debug("This is a debug log")
#        logger.critical("This is critical")
#        logger.error("An error occurred")
#        logger.info("This is an info log")

    def calculateDHS(self):
        print("---->\tstart to calculate heatgrid\n")
        solver = Solver(self.heatgrid, self.heatsink, self.heatsource)
        guess = solver.getGuess()
        solver.print_x(guess, 'guess')
        solution = root(solver.gridCalculation, guess)
        solver.print_x(solution, 'solution')
        solver.save_x(solution)
        return None



        
#        print(len(self.heatgrid.v_pipes_eNode),
#              len(self.heatgrid.v_pipes_sNode),
#              len(self.heatgrid.v_nodes_name))
#        print(type(self.heatgrid.v_pipes_eNode))
#        v_pipes_eNode = self.heatgrid.v_pipes_eNode
#        v_pipes_sNode = self.heatgrid.v_pipes_sNode
#        setOfElements_eNode = set(v_pipes_eNode)
#        setOfElements_sNode = set(v_pipes_sNode)
#        setOfHeatsink_sNode = set(self.heatsink.v_consumers_sNode)
#        setOfHeatsink_eNode = set(self.heatsink.v_consumers_eNode)
#        setOfHeatsource_sNode = set(self.heatsource.v_producers_sNode)
#        setOfHeatsource_eNode = set(self.heatsource.v_producers_eNode)
#        
#        setOfHeatsinkHeatsource_nodes = set(setOfHeatsink_sNode |
#                setOfHeatsink_eNode | setOfHeatsource_sNode |
#                setOfHeatsource_eNode)
#
#        setOfElements_nodes = (setOfElements_eNode | setOfElements_sNode) -\
#                               setOfHeatsinkHeatsource_nodes
#        index = 0
#        for eNode, sNode in zip(v_pipes_eNode, v_pipes_sNode):
#            if eNode not in setOfElements_nodes:
#                v_pipes_eNode[index] = None
#            if sNode not in setOfElements_nodes:
#                v_pipes_sNode[index] = None
#            index = index + 1
#        
#        countsEqualOne_eNode = Counter(v_pipes_eNode)
#        countsEqualOne_sNode = Counter(v_pipes_sNode)
#        countsEqualOne_eNode = [item for item in countsEqualOne_eNode.items()
#                                if item[1] == 1]
#        countsEqualOne_sNode = [item for item in countsEqualOne_sNode.items()
#                                if item[1] == 1]
#
#        countsEqualOne_nodes = np.append(countsEqualOne_eNode,
#                                        countsEqualOne_sNode)
#        countsEqualOne_nodes = Counter(countsEqualOne_nodes)
#        countsEqualOne_nodes = [item for item in countsEqualOne_nodes.items()]
#        print(countsEqualOne_nodes)
#        print(len(countsEqualOne_nodes))
#        

#        leaves = setElements_eNode - setElements_sNode
#        print(leaves)
#        deadEnds = set(self.heatgrid.v_nodes_name) - (
#                                set(self.heatsink.v_consumers_eNode) &
#                                set(self.heatsink.v_consumers_sNode) &
#                                set(self.heatsource.v_producers_eNode) &
#                                set(self.heatsource.v_producers_sNode))
#
#        print(deadEnds)


if __name__ == "__main__":
    from DataIO import DataIO
    import Dictionary
    print('DistrictHeatingSystem \t run directly \n')


#    DataIO = DataIO(
#                os.path.dirname(os.getcwd()) + os.sep +
#                'input' + os.sep + 'TestNetz',
#                os.path.dirname(os.getcwd()) + os.sep +
#                'output' + os.sep + 'TestNetz')
#
#    heatgrid_nodes = DataIO.importDBF(
#            'KTestNetz.DBF', dtype=Dictionary.STANET_nodes_allocation)
#
#    heatgrid_pipes = DataIO.importDBF(
#            'STestNetz.DBF', dtype=Dictionary.STANET_pipes_allocation)
#
#    heatsink = DataIO.importDBF(
#            'WTestNetz.DBF', dtype=Dictionary.STANET_consumer_allocation)
#
#    heatsource = DataIO.importCSV(
#            'WTestNetz.csv', dtype=Dictionary.STANET_producer_allocation,
#            delimiter='\t', header=0)
#    DataIO = DataIO(
#                os.path.dirname(os.getcwd()) + os.sep +
#                'input' + os.sep + 'TestNetz' + os.sep + "vog",
#                os.path.dirname(os.getcwd()) + os.sep +
#                'output' + os.sep + 'TestNetz' + os.sep + "vog")
#
    dataIO = DataIO(
            os.path.dirname(os.path.dirname(os.getcwd())) + os.sep + 'vog' ,
            os.path.dirname(os.path.dirname(os.getcwd())) + os.sep + 'vog')
#    dataIO= DataIO(
#            'D:\jpelda\Python Scripts\\vog\\vog_gross',
#            'D:\jpelda\Python Scripts\\vog\\vog_gross\\output')
#
    heatgrid_nodes = dataIO.importDBF(
            'K20150909_F-MVV_TL-West.DBF',
            dtype=Dictionary.STANET_nodes_allocation)

    heatgrid_pipes = dataIO.importDBF(
            'S20150909_F-MVV_TL-West.DBF',
            dtype=Dictionary.STANET_pipes_allocation)

    heatsink = dataIO.importDBF(
            'W20150909_F-MVV_TL-West.DBF',
            dtype=Dictionary.STANET_consumer_allocation)

    heatsource = dataIO.importCSV(
            'W20150909_F-MVV_TL-West.csv',
            dtype=Dictionary.STANET_vog_producer_allocation,
            delimiter=';', header=0)


    DHS1 = DistrictHeatingSystem(
            heatgrid_pipes,
            heatgrid_nodes,
            heatsink,
            heatsource)

    DHS1_Plotter = Plotter()
#    DHS1_Plotter.plot_graph(DHS1.heatgrid.v_nodes_name,
#                            DHS1.heatgrid.v_pipes_esNode)

    
    i = 0
    while i < 1:
        print('#####\trun number %i\t#####' %i)
        DHS1.calculateDHS()
        endTime = time.time()
#        DHS1.heatgrid.__str__()
#        DHS1.heatsink.__str__()
#        DHS1.heatsource.__str__()

#        solver.print_x(guess, "guess")
#        solver.print_x(solution, "solution")
        DHS1.heatgrid.setCalculations()
        DHS1.heatsink.setCalculations()
        DHS1.heatsource.setCalculations()
        i = i + 1
#
#    dataIO.exportNumpyArr("HeatGrid", DHS1.heatgrid.getCalculations())
#    dataIO.exportNumpyArr("HeatSink", DHS1.heatsink.getCalculations())
#    dataIO.exportNumpyArr("HeatSouce", DHS1.heatsource.getCalculations())
#    DHS1_Plotter = Plotter(figsize=1)
#
#    fig = DHS1_Plotter.plot_DHS(DHS1.heatgrid.getCalculations(0),
#                          DHS1.heatsink.getCalculations(0),
#                          DHS1.heatsource.getCalculations(0))
#    dataIO.exportFig('test', fig)

else:
    import os
    import sys
    sys.path.append(os.getcwd() + os.sep + 'function')
    print(sys.path.append(os.getcwd() + os.sep + 'function'))
    print('DistrictHeatingSystem \t was imported into another module')
