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
        print("Getting solution\n")
        solution = root(solver.gridCalculation, guess)
        solver.print_x(solution, 'solution')
        solver.save_x(solution)
        return None


if __name__ == "__main__":
    from DataIO import DataIO
    import Dictionary
    print('DistrictHeatingSystem \t run directly \n')


#    DHS1_dataIO = DataIO(
#                os.path.dirname(os.getcwd()) + os.sep +
#                'input' + os.sep + 'TestNetz',
#                os.path.dirname(os.getcwd()) + os.sep +
#                'output' + os.sep + 'TestNetz')
#
#    heatgrid_nodes = DHS1_dataIO.importDBF(
#            'KTestNetz.DBF', dtype=Dictionary.STANET_nodes_allocation)
#
#    heatgrid_pipes = DHS1_dataIO.importDBF(
#            'STestNetz.DBF', dtype=Dictionary.STANET_pipes_allocation)
#
#    heatsink = DHS1_dataIO.importDBF(
#            'WTestNetz.DBF', dtype=Dictionary.STANET_consumer_allocation)
#
#    heatsource = DHS1_dataIO.importCSV(
#            'WTestNetz.csv', dtype=Dictionary.STANET_producer_allocation,
#            delimiter='\t', header=0)

#
    DHS1_dataIO = DataIO(
            os.path.dirname(os.path.dirname(os.getcwd())) + os.sep + 'vNetz' +
            os.sep + 'v_klein',
            os.path.dirname(os.path.dirname(os.getcwd())) + os.sep + 'vNetz' +
            os.sep + 'v_klein' + os.sep + 'output')
#    DHS1_dataIO= DataIO(
#            'D:\jpelda\Python Scripts\\vNetz\\v_klein',
#            'D:\jpelda\Python Scripts\\vNetz\\v_klein\\output')
##
    heatgrid_nodes = DHS1_dataIO.importDBF(
            'K20170808_vKlein.DBF',
            dtype=Dictionary.STANET_nodes_allocation)

    heatgrid_pipes = DHS1_dataIO.importDBF(
            'S20170808_vKlein.DBF',
            dtype=Dictionary.STANET_pipes_allocation)

    heatsink = DHS1_dataIO.importDBF(
            'W20170808_vKlein.DBF',
            dtype=Dictionary.STANET_consumer_allocation)

    heatsource = DHS1_dataIO.importCSV(
            'W20170808_vKlein.csv',
            dtype=Dictionary.STANET_vog_producer_allocation,
            delimiter=';', header=0)

    DHS1 = DistrictHeatingSystem(
        heatgrid_pipes,
        heatgrid_nodes,
        heatsink,
        heatsource)

#    i = 0
#    while i < 1:
#        print('#####\trun number %i\t#####' %i)
#        DHS1.calculateDHS()
#        endTime = time.time()
##        DHS1.heatgrid.__str__()
##        DHS1.heatsink.__str__()
##        DHS1.heatsource.__str__()
#
##        solver.print_x(guess, "guess")
##        solver.print_x(solution, "solution")
#        DHS1.heatgrid.setCalculations()
#        DHS1.heatsink.setCalculations()
#        DHS1.heatsource.setCalculations()
#        i = i + 1
#
#    dataIO.exportNumpyArr("HeatGrid", DHS1.heatgrid.getCalculations())
#    dataIO.exportNumpyArr("HeatSink", DHS1.heatsink.getCalculations())
#    dataIO.exportNumpyArr("HeatSouce", DHS1.heatsource.getCalculations())

    DHS1_Plotter = Plotter()
    #  look that v_producers_sNode is not empty
    for index_c, item_c in enumerate(DHS1.heatgrid.v_nodes_name):
        for index_p, item_ps in enumerate(DHS1.heatsource.v_producers_sNode):
            if item_c is item_ps:
                DHS1.heatsource.v_producers_start_x[index_p] =\
                DHS1.heatgrid.v_nodes_x[index_c]
                DHS1.heatsource.v_producers_start_y[index_p] =\
                DHS1.heatgrid.v_nodes_y[index_c]
        for index_p, item_pe in enumerate(DHS1.heatsource.v_producers_eNode):
            if item_c is item_pe:
                DHS1.heatsource.v_producers_end_x[index_p] =\
                DHS1.heatgrid.v_nodes_x[index_c]
                DHS1.heatsource.v_producers_end_y[index_p] =\
                DHS1.heatgrid.v_nodes_y[index_c]
    print(DHS1.heatsource.v_producers_start_x,
           DHS1.heatsource.v_producers_start_y,
           DHS1.heatsource.v_producers_end_x,
           DHS1.heatsource.v_producers_end_y,
           DHS1.heatsource.v_producers_Q)
    fig = DHS1_Plotter.plot_DHS(
            v_pipes_start_x=DHS1.heatgrid.v_pipes_start_x,
            v_pipes_start_y=DHS1.heatgrid.v_pipes_start_y,
            v_pipes_end_x=DHS1.heatgrid.v_pipes_end_x,
            v_pipes_end_y=DHS1.heatgrid.v_pipes_end_y,
            v_pipes_Q=DHS1.heatgrid.v_pipes_Q,
            v_nodes_x=DHS1.heatgrid.v_nodes_x,
            v_nodes_y=DHS1.heatgrid.v_nodes_y,
            v_consumers_start_x=DHS1.heatsink.v_consumers_start_x,
            v_consumers_start_y=DHS1.heatsink.v_consumers_start_y,
            v_consumers_end_x=DHS1.heatsink.v_consumers_end_x,
            v_consumers_end_y=DHS1.heatsink.v_consumers_end_y,
            v_consumers_Q=DHS1.heatsink.v_consumers_Q,
            v_producers_start_x=DHS1.heatsource.v_producers_start_x,
            v_producers_start_y=DHS1.heatsource.v_producers_start_y,
            v_producers_end_x=DHS1.heatsource.v_producers_end_x,
            v_producers_end_y=DHS1.heatsource.v_producers_end_y,
            v_producers_Q=DHS1.heatsource.v_producers_Q
            )

    DHS1_dataIO.exportFig("v_klein", fig)


else:
    import os
    import sys
    sys.path.append(os.getcwd() + os.sep + 'function')
    print(sys.path.append(os.getcwd() + os.sep + 'function'))
    print('DistrictHeatingSystem \t was imported into another module')
