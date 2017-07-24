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
                                'sNode',
                                'eNode',
                                'length',
                                'start_height',
                                'end_height',
                                'transitionCoefficient',
                                'roughness',
                                'transferCoefficient_inner',
                                'transferCoefficient_outer',
                                'conductivity_inner',
                                'conductivity_middle',
                                'conductivity_outer',
                                'diameter_inner',
                                'diameter_middleinner',
                                'diamter_middleouter',
                                'diameter_outer',
                                'sprp'),
                       'formats': (
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
                                'U2'
                                )
                               }

HeatGrid_node_dtype =    {'names': (
                                'index',
                                'x',
                                'y',
                                'name',
                                'height',
                                'sprp'
                                ),
                       'formats': (
                                'i',
                                'f',
                                'f',
                                'U10',
                                'f',
                                'U2',
                                )
                               }

HeatSink_consumer_dtype ={'names': (
                                'index',
                                'heat_exchangerModel',
                                'sNode',
                                'eNode',
                                'start_x',
                                'start_y',
                                'end_x',
                                'end_y',
                                'heat_demand',
                                'heat_consumptionProfile',
                                'heat_consumptionAverage',
                                'flow'
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
                                'f',
                                'U30',
                                'U30',
                                'f'
                                )
                               }

HeatGrid_pump_dtype =    {'names': (
                                'index',
                                'profil',
                                'sNode',
                                'eNode',
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
                                     'sNode',
                                     'eNode',
                                     'index',
                                     'power',
                                     'start_x',
                                     'start_y',
                                     'end_x',
                                     'end_y'
                                     ),
                            'formats': (
                                        'U10',
                                        'U10',
                                        'U30',
                                        'f',
                                        'f',
                                        'f',
                                        'f',
                                        'f'
                                        )
                            }

STANET_nodes =          {'names': (
                                'x',
                                'y',
                                'name',
                                'height'
                                ),
                       'formats': (
                                'f',
                                'f',
                                'U10'
                                'f'
                                )
                               }

STANET_pipes =          {'names': (
                                'sNode',
                                'eNode',
                                'length',
                                'heatTransitionCoefficient',
                                'roughness',
                                'XRA',
                                'YHA',
                                'XRB',
                                'YHB'
                                ),
                       'formats': (
                                'U10',
                                'U10',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f'
                                )
                               }

STANET_consumer =       {'names': (
                                'index',
                                'sNode',
                                'eNode'
                                ),
                       'formats': (
                                'i',
                                'U10',
                                'U10'
                                )
                               }

STANET_producer = {'names': (
                            'ANFNAM',
                            'ENDNAM',
                            'NAME',
                            'Power',
                            'XRA',
                            'YHA',
                            'XRB',
                            'YHB'
                            ),
                    'formats': (
                                'U10',
                                'U10',
                                'U30',
                                'f',
                                'f',
                                'f',
                                'f',
                                'f'
                                )
                    }

HeatGrid_STANET_nodes_allocation = {
                                'x': 'XRECHTS',
                                'y': 'YHOCH',
                                'name': 'KNAM',
                                'height': 'GEOH',
                                'sprp': 'SUPPLY'
                                }

HeatGrid_STANET_pipes_allocation = {
                                'index': 0,
                                'start_x': 'XRA',
                                'start_y': 'YHA',
                                'end_x': 'XRB',
                                'end_y': 'YHB',
                                'sNode': 'ANFNAM',
                                'eNode': 'ENDNAM',
                                'length': 'RORL',
                                'start_height': 0,
                                'end_height': 0,
                                'transitionCoefficient': 'WDZAHL',
                                'roughness': 'RAU',
                                'transferCoefficient_inner': 0,
                                'transferCoefficient_outer': 0,
                                'conductivity_inner': 0,
                                'conductivity_middleinner': 0,
                                'conductivity_middleouter':0,
                                'conductivity_outer': 0,
                                'diameter_inner': 'DM',
                                'diameter_middleinner': 0,
                                'diamter_middleouter':0,
                                'diameter_outer': 0,
                                'sprp': 'SUPPLY'
                                }

HeatSink_STANET_consumer_allocation = {
                                'index': 0,
                                'sNode': 'ANFNAM',
                                'eNode': 'ENDNAM',
                                'heat_demand': 'WAERMEMENG',
                                'flow': 'FLUSS',
                                'start_x': 'XRECHTS',
                                'start_y': 'YHOCH',
                                'end_x': 'XRECHTS2',
                                'end_y': 'YHOCH2'
                                }

Pump_STANET_consumer_allocation = {
                                'index': 0,
                                'profil': 'PUMPENTYP',
                                'sNode': 'ANFNAM',
                                'eNode': 'ENDNAM',
                                }

HeatSource_STANET_producer_allocation = {
                                         'index': 'NAME',
                                         'power': 'Power',
                                         'sNode': 'ANFNAM',
                                         'eNode': 'ENDNAM',
                                         'start_x': 'XRA',
                                         'start_y': 'YHA',
                                         'end_x': 'XRB',
                                         'end_y': 'YHB',
                                         'height': 0
                                         }
