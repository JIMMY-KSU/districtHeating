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
from Plotter import Plotter
from matplotlib import pyplot as plt


DataIO = DataIO(os.getcwd() + os.sep + 'input',
                    os.getcwd() + os.sep + 'output')

heatgrid_nodes = DataIO.importCSV('Hannover_workshopNet1'  + os.sep + 'heatnet_nodes.csv',
                                 dtypeSource = Dictionary.HeatGrid_node_dtype,
                                 startrow=1,
                                 columnofdate=None,
                                 dateformat='None')
#print(heatgrid_nodes['name'])

heatgrid_pipes = DataIO.importCSV('Hannover_workshopNet1' + os.sep + 'heatnet_pipes.csv',
                                  dtypeSource = Dictionary.HeatGrid_pipe_dtype,
                                  startrow=1,
                                  columnofdate=None,
                                  dateformat='None')
#print(heatgrid_pipes['index'])

heatsink_consumer = DataIO.importCSV('Hannover_workshopNet1' + os.sep + 'consumer.csv',
                               dtypeSource=Dictionary.HeatSink_consumer_dtype,
                               startrow=1,
                               columnofdate=None,
                               dateformat='None')

#print('Consumer:  ' +
#      'start node: ' + str(heatsink_consumer['start_node_name']) +
#      'end node: ' + str(heatsink_consumer['end_node_name']))


heatsource = DataIO.importCSV('Hannover_workshopNet1' + os.sep + 'producer.csv',
                              dtypeSource=Dictionary.HeatSource_producer_dtype,
                              startrow=1,
                              columnofdate=None,
                              dateformat='None')

DHS1 = DistrictHeatingSystem(heatgrid_pipes, heatgrid_nodes, heatsink_consumer, heatsource)
















'''heatgrid2'''

#heatgrid_nodes = DataIO.importCSV('Hannover_workshopNet2'  + os.sep + 'heatnet_nodes.csv',
#                                 dtypeSource = Dictionary.HeatGrid_node_dtype,
#                                 startrow=1,
#                                 columnofdate=None,
#                                 dateformat='None')
##print(heatgrid_nodes['name'])
#
#heatgrid_pipes = DataIO.importCSV('Hannover_workshopNet2' + os.sep + 'heatnet_pipes.csv',
#                                  dtypeSource = Dictionary.HeatGrid_pipe_dtype,
#                                  startrow=1,
#                                  columnofdate=None,
#                                  dateformat='None')
##print(heatgrid_pipes['index'])
#
#heatsink_consumer = DataIO.importCSV('Hannover_workshopNet2' + os.sep + 'consumer.csv',
#                               dtypeSource=Dictionary.HeatSink_consumer_dtype,
#                               startrow=1,
#                               columnofdate=None,
#                               dateformat='None')
#
##print('Consumer:  ' +
##      'start node: ' + str(heatsink_consumer['start_node_name']) +
##      'end node: ' + str(heatsink_consumer['end_node_name']))
#
#
#heatsource = DataIO.importCSV('Hannover_workshopNet2' + os.sep + 'producer.csv',
#                              dtypeSource=Dictionary.HeatSource_producer_dtype,
#                              startrow=1,
#                              columnofdate=None,
#                              dateformat='None')
#
#DHS1 = DistrictHeatingSystem(heatgrid_pipes, heatgrid_nodes, heatsink_consumer, heatsource)


'''old versions'''

#heatsource = DataIO.importCSV('Hannover_workshopNet' + os.sep + 'WTestNetz.csv',
#                              dtype = Dictionary.HeatSource_producer_dtype,
#                              dtypeSource= Dictionary.STANET_producer,
#                              dtypeAllocation =
#                              Dictionary.HeatSource_STANET_producer_allocation,
#                              startrow=1,
#                              columnofdate=None,
#                              dateformat='None')
#DHS1= DistrictHeatingSystem(heatgrid_pipes, heatgrid_nodes, heatsink, heatsource)
#

#print (DHS1.calculateDHS())

#plotter = Plotter()
#
#nodes_x = []
#nodes_y = []
#for item in DHS1.heatgrid.nodes():
#
#    nodes_x.append(item.x)
#    nodes_y.append(item.y)
#
#
#pipes_x = []
#pipes_y= []
#
#for pipe in DHS1.heatgrid.pipes():
#    for node in DHS1.heatgrid.nodes():
#        if pipe.start_node_name == node.name:
#            pipes_x.append(node.x)
#            pipes_y.append(node.y)
#        if pipe.end_node_name == node.name:
#            pipes_x.append(node.x)
#            pipes_y.append(node.x)
#
#
#
#plt.plot(pipes_y, pipes_y)
#
#plotter.scatter(nodes_x, nodes_y, s = 30)
#print(pipes_x)
#
#plt.plot([1,2,3],[[2,4,2],[3,2,3]])


#DataIO = DataIO(os.getcwd() + os.sep + 'input',
#                    os.getcwd() + os.sep + 'output')

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

#heatgrid_nodes = DataIO.importDBF('TestNetz' + os.sep + 'KTestNetz.DBF',
#                                  Dictionary.HeatGrid_node_dtype,
#                                  Dictionary.HeatGrid_STANET_nodes_allocation)
#heatgrid_pipes = DataIO.importDBF('TestNetz' + os.sep + 'STestNetz.DBF',
#                                  Dictionary.HeatGrid_pipe_dtype,
#                                  Dictionary.HeatGrid_STANET_pipes_allocation)
#
#heatsink = DataIO.importDBF('TestNetz' + os.sep + 'WTestNetz.DBF',
#                               Dictionary.HeatSink_consumer_dtype,
#                               Dictionary.HeatSink_STANET_consumer_allocation)
#
#heatsource = DataIO.importCSV('TestNetz' + os.sep + 'WTestNetz.csv',
#                              dtype = Dictionary.HeatSource_producer_dtype,
#                              dtypeSource= Dictionary.STANET_producer,
#                              dtypeAllocation =
#                              Dictionary.HeatSource_STANET_producer_allocation,
#                              startrow=1,
#                              columnofdate=None,
#                              dateformat='None')