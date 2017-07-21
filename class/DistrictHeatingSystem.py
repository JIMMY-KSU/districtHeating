# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 16:22:28 2017

@author: johannes
"""

import sys
import os
import numpy as np
from scipy.optimize import fsolve
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
        solution = fsolve(solver.gridCalculation, guess)
        solver.save_x(solution)

        return None



if __name__ == "__main__":
    from DataIO import DataIO
    import Dictionary
    print('DistrictHeatingSystem \t run directly \n')

    DataIO = DataIO(
                os.path.dirname(os.getcwd()) + os.sep + 'input',
                os.path.dirname(os.getcwd()) + os.sep + 'output')

    heatgrid_nodes = DataIO.importDBF(
            'TestNetz' + os.sep + 'KTestNetz.DBF',
            Dictionary.HeatGrid_node_dtype,
            Dictionary.HeatGrid_STANET_nodes_allocation)

    heatgrid_pipes = DataIO.importDBF(
            'TestNetz' + os.sep + 'STestNetz.DBF',
            Dictionary.HeatGrid_pipe_dtype,
            Dictionary.HeatGrid_STANET_pipes_allocation)

    heatsink = DataIO.importDBF(
            'TestNetz' + os.sep + 'WTestNetz.DBF',
            Dictionary.HeatSink_consumer_dtype,
            Dictionary.HeatSink_STANET_consumer_allocation)

    heatsource = DataIO.importCSV(
            'TestNetz' + os.sep + 'WTestNetz.csv',
            dtype=Dictionary.HeatSource_producer_dtype,
            startrow=1,
            columnofdate=None,
            dateformat='None')

    DHS1 = DistrictHeatingSystem(
            heatgrid_pipes,
            heatgrid_nodes,
            heatsink,
            heatsource)
    i = 0
    while i < 2:
        print(i)
        DHS1.calculateDHS()
        endTime = time.time()
        DHS1.heatgrid.__str__()
#        DHS1.heatsink.__str__()
#        DHS1.heatsource.__str__()

#        solver.print_x(guess, "guess")
#        solver.print_x(solution, "solution")
        DHS1.heatgrid.setCalculations()
        DHS1.heatsink.setCalculations()
        DHS1.heatsource.setCalculations()
        i = i + 1


    DataIO.exportNumpyArr("HeatGrid", DHS1.heatgrid.getCalculations())
    DataIO.exportNumpyArr("HeatSink", DHS1.heatsink.getCalculations())
    DataIO.exportNumpyArr("HeatSouce", DHS1.heatsource.getCalculations())
    DHS1_Plotter = Plotter(DHS1.heatgrid, DHS1.heatsink, DHS1.heatsource)
#    print(DHS1_Plotter.plot_HeatGrid(DHS1.heatgrid.getCalculations(1)))
#    fig = DHS1_Plotter.plot_HeatGrid(DHS1.heatgrid.getCalculations(1))
#    DataIO.exportFig("test", fig)
    DHS1_Plotter.plot_DHS(DHS1.heatgrid.getCalculations(1),
                          DHS1.heatsink.getCalculations(1),
                          DHS1.heatsource.getCalculations(1))
    DHS1_Plotter.heatExchanger()

else:
    import os
    import sys
    sys.path.append(os.getcwd() + os.sep + 'function')
    print(sys.path.append(os.getcwd() + os.sep + 'function'))
    print('DistrictHeatingSystem \t was imported into another module')
