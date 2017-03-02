# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 16:22:28 2017

@author: johannes
"""

import sys
import os
import inspect

sys.path.append(os.getcwd() + os.sep + 'class')


from DataIO import DataIO
from DistrictHeatingSystem import DistrictHeatingSystem
import Dictionary


DataIO = DataIO(os.getcwd() + os.sep + 'input',
                    os.getcwd() + os.sep + 'output')

#heatgrid_pipes = DataIO.importCSV('heatnet_pipes.csv',
#                                 dtype = Dictionary.HeatGrid_pipe_dtype,
#                                 startrow=1,
#                                 columnofdate=None,
#                                 dateformat='None')
#heatgrid_nodes = DataIO.importCSV('heatnet_nodes.csv',
#                                  dtype = Dictionary.HeatGrid_node_dtype,
#                                  startrow=1,
#                                  columnofdate=None,
#                                  dateformat='None')

heatgrid_nodes = DataIO.importDBF('TestNetz' + os.sep + 'KTestNetz.DBF',
                                  Dictionary.HeatGrid_node_dtype,
                                  Dictionary.HeatGrid_STANET_nodes_allocation)
heatgrid_pipes = DataIO.importDBF('TestNetz' + os.sep + 'STestNetz.DBF',
                                  Dictionary.HeatGrid_pipe_dtype,
                                  Dictionary.HeatGrid_STANET_pipes_allocation)

heatsink = DataIO.importDBF('TestNetz' + os.sep + 'WTestNetz.DBF',
                               Dictionary.HeatSink_consumer_dtype,
                               Dictionary.HeatSink_STANET_consumer_allocation)

heatsource = DataIO.importCSV('TestNetz' + os.sep + 'WTestNetz.csv',
                              dtype = Dictionary.HeatSource_producer_dtype,
                              dtypeSource= Dictionary.STANET_producer,
                              dtypeAllocation =
                              Dictionary.HeatSource_STANET_producer_allocation,
                              startrow=1,
                              columnofdate=None,
                              dateformat='None')


DHS1= DistrictHeatingSystem(heatgrid_pipes, heatgrid_nodes, heatsink, heatsource)


for i in DHS1.heatgrid.pipes():
    print(i.start_node_name)

print (DHS1.calculateDHS())




