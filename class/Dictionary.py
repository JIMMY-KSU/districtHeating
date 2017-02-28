# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 11:03:13 2017

@author: jpelda
"""

HeatGrid_pipe_dtype =    {'names':(
                                'index',
                                'start_x',
                                'start_y',
                                'end_x',
                                'end_y',
                                'start_node_name',
                                'end_node_name',
                                'length',
                                'diameter_inner',
                                'diameter_outer',
                                'start_height',
                                'end_height',
                                'heatTransitionCoefficient',
                                'roughness',
                                'heat_transferCoefficient_inner',
                                'heat_transferCoefficient_outer',
                                'heat_conductivity_1',
                                'heat_conductivity_2',
                                'heat_conductivity_3',
                                'diameter_1',
                                'diameter_2',
                                'diameter_3',
                                'SP_RP'),
                       'formats':(
                                'i',
                                'f',
                                'f',
                                'f',
                                'f',
                                'U10',
                                'U10',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f',
                                'U2'
                                )
                               }

HeatGrid_node_dtype =    {'names':(
                                'index',
                                'x',
                                'y',
                                'name',
                                'height',
                                'SP_RP'
                                ),
                       'formats':(
                                'i',
                                'f',
                                'f',
                                'U10',
                                'f',
                                'U2',
                                )
                               }
                               
HeatSink_consumer_dtype ={'names':(
                                'index',
                                'heat_exchangerModel',
                                'start_node_name',
                                'end_node_name',
                                'start_x',
                                'start_y',
                                'end_x',
                                'end_y',
                                'heat_consumptionProfile',
                                'heat_consumptionAverage'
                                ),
                       'formats':(
                                'i',
                                'U30',
                                'U10',
                                'U10',
                                'f',
                                'f',
                                'f',
                                'f',
                                'U30',
                                'U30',
                                )
                               }
                           
HeatGrid_pump_dtype =    {'names': (
                                'index',
                                'profil',
                                'start_node_name',
                                'end_node_name',
                                'start_x',
                                'start_y',
                                'end_x',
                                'end_y',
                                ),
                       'formats': (
                                'i',
                                'U30',
                                'U10',
                                'U10',
                                'f',
                                'f',
                                'f',
                                'f',
                                )
                               }

HeatSource_producer_dtype = {'names': (
                                     'name',
                                     'power',
                                     'start_node_name',
                                     'end_node_name',
                                     ),
                            'formats': (
                                        'U10',
                                        'f',
                                        'U10',
                                        'U10'
                                        )
                            }

STANET_nodes =          {'names':(
                                'x',
                                'y',
                                'name'
                                ),
                       'formats':(
                                'f',
                                'f',
                                'U10'
                                )
                               }
                               
STANET_pipes =          {'names':(
                                'start_node_name',
                                'end_node_name',
                                'length',
                                'heatTransitionCoefficient',
                                'roughness'
                                ),
                       'formats':(
                                'U10',
                                'U10',
                                'f',
                                'f',
                                'f'
                                )
                               }
                               
STANET_consumer =       {'names':(
                                'index',
                                'start_node_name',
                                'end_node_name',
                                ),
                       'formats':(
                                'i',
                                'U10',
                                'U10'
                                )
                               }

HeatGrid_STANET_nodes_allocation = {
                                'x': 'XRECHTS',
                                'y': 'YHOCH',
                                'name': 'KNAM'
                                }

HeatGrid_STANET_pipes_allocation = {
                                'index': 0,
                                'start_x': 0,
                                'start_y': 0,
                                'end_x': 0,
                                'end_y': 0,
                                'start_node_name': 'ANFNAM',
                                'end_node_name': 'ENDNAM',
                                'length': 'RORL',
                                'diameter_inner': 'DM',
                                'diameter_outer': 0,
                                'start_height': 0,
                                'end_height': 0,
                                'heatTransitionCoefficient': 'WDZAHL',
                                'roughness': 'RAU',
                                'heat_transferCoefficient_inner': 0,
                                'heat_transferCoefficient_outer': 0,
                                'heat_conductivity_1': 0,
                                'heat_conductivity_2': 0,
                                'heat_conductivity_3': 0,
                                'diameter_1': 0,
                                'diameter_2': 0,
                                'diameter_3': 0,
                                'SP_RP': 'SUPPLY'
                                }

HeatSink_STANET_consumer_allocation = {
                                'index': 0,
                                'start_node_name': 'ANFNAM',
                                'end_node_name': 'ENDNAM',
                                'performance': 'WAERMEMENG'
                                }

Pump_STANET_consumer_allocation = {
                                'index': 0,
                                'profil': 'PUMPENTYP',
                                'start_node_name': 'ANFNAM',
                                'end_node_name': 'ENDNAM',
                                }

HeatSource_STANET_producer_allocation = {
                                         'index': 0,
                                         'name': 'NAME',
                                         'power': 'Power',
                                         'start_node_name': 'ANFNAM',
                                         'end_node_name': 'ENDNAM',
                                         'start_x': 0,
                                         'start_y': 0,
                                         'end_x': 0,
                                         'end_y': 0,
                                         'height': 0
                                         }
