# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 11:03:13 2017

@author: jpelda
"""


#HeatGrid_pipe_dtype =    {'names':(
#                                'index',
#                                'start_x',
#                                'start_y',
#                                'end_x',
#                                'end_y',
#                                'sNode',
#                                'eNode',
#                                'length',
#                                'start_height',
#                                'end_height',
#                                'transitionCoefficient',
#                                'roughness',
#                                'transferCoefficient_inner',
#                                'transferCoefficient_outer',
#                                'conductivity_inner',
#                                'conductivity_middle',
#                                'conductivity_outer',
#                                'diameter_inner',
#                                'diameter_middleinner',
#                                'diameter_middleouter',
#                                'diameter_outer',
#                                'sprp'),
#                       'formats': (
#                                'i',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'U10',
#                                'U10',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'U2'
#                                )
#                               }
#
#HeatGrid_node_dtype =    {'names': (
#                                'index',
#                                'x',
#                                'y',
#                                'name',
#                                'height',
#                                'sprp'
#                                ),
#                       'formats': (
#                                'i',
#                                'f',
#                                'f',
#                                'U10',
#                                'f',
#                                'U2',
#                                )
#                               }
#
#HeatSink_consumer_dtype ={'names': (
#                                'index',
#                                'heat_exchangerModel',
#                                'sNode',
#                                'eNode',
#                                'start_x',
#                                'start_y',
#                                'end_x',
#                                'end_y',
#                                'heat_demand',
#                                'heat_consumptionProfile',
#                                'heat_consumptionAverage',
#                                'flow'
#                                ),
#                       'formats': (
#                                'i',
#                                'U30',
#                                'U10',
#                                'U10',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'U30',
#                                'U30',
#                                'f'
#                                )
#                               }
#
#HeatGrid_pump_dtype =    {'names': (
#                                'index',
#                                'profil',
#                                'sNode',
#                                'eNode',
#                                'start_x',
#                                'start_y',
#                                'end_x',
#                                'end_y',
#                                ),
#                       'formats': (
#                                'i',
#                                'U30',
#                                'U10',
#                                'U10',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                )
#                               }
#
#HeatSource_producer_dtype = {'names': (
#                                     'sNode',
#                                     'eNode',
#                                     'index',
#                                     'power',
#                                     'start_x',
#                                     'start_y',
#                                     'end_x',
#                                     'end_y'
#                                     ),
#                            'formats': (
#                                        'U10',
#                                        'U10',
#                                        'U30',
#                                        'f',
#                                        'f',
#                                        'f',
#                                        'f',
#                                        'f'
#                                        )
#                            }

#STANET_nodes =          {'names': (
#                                'x',
#                                'y',
#                                'name',
#                                'height'
#                                ),
#                       'formats': (
#                                'f',
#                                'f',
#                                'U10'
#                                'f'
#                                )
#                               }
#
#STANET_pipes =          {'names': (
#                                'sNode',
#                                'eNode',
#                                'length',
#                                'heatTransitionCoefficient',
#                                'roughness',
#                                'XRA',
#                                'YHA',
#                                'XRB',
#                                'YHB'
#                                ),
#                       'formats': (
#                                'U10',
#                                'U10',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f'
#                                )
#                               }
#
#STANET_consumer =       {'names': (
#                                'index',
#                                'sNode',
#                                'eNode'
#                                ),
#                       'formats': (
#                                'i',
#                                'U10',
#                                'U10'
#                                )
#                               }
#
#STANET_producer = {'names': (
#                            'index',
#                            'ANFNAM',
#                            'ENDNAM',
#                            'NAME',
#                            'Power',
#                            'XRA',
#                            'YHA',
#                            'XRB',
#                            'YHB'
#                            ),
#                    'formats': (
#                                'i',
#                                'U10',
#                                'U10',
#                                'U30',
#                                'f',
#                                'f',
#                                'f',
#                                'f',
#                                'f'
#                                )
#                    }

STANET_nodes_allocation = {
        'GEOH': 'height',
        'KNAM': 'name',
        'SUPPLY': 'sprp',
        'XRECHTS': 'x',
        'YHOCH': 'y'}

STANET_pipes_allocation = {
        'XRA': 'start_x',
        'YHA': 'start_y',
        'XRB': 'end_x',
        'YHB': 'end_y',
        'ANFNAM': 'sNode',
        'ENDNAM': 'eNode',
        'RORL': 'length',
        'WDZAHL': 'transitionCoefficient',
        'RAU': 'roughness',
        'DM': 'diameter_inner',
        'DP':'m_max', #  for testing, is not the correct key
        None: ['start_height', 'end_height',
               'transferCoefficient_inner',
               'transferCoefficient_outer',
               'conductivity_inner',
               'conductivity_middle',
               'conductivity_outer',
               'diameter_middleinner',
               'diameter_middleouter',
               'diameter_outer',
               'sprp',
			   'index'
               ]}


STANET_consumer_allocation = {
        'ANFNAM': 'sNode',
        'ENDNAM': 'eNode',
        'WAERMEMENG': 'Q',
        'FLUSS': 'flow',
        'XRECHTS': 'start_x',
        'YHOCH': 'start_y',
        'XRECHTS2': 'end_x',
        'YHOCH2': 'end_y',
        None:['index', 'profile', 'average']
        }


STANET_pump_allocation = {
                            'PUMPENTYP': 'profil',
                            'ANFNAM': 'sNode',
                            'ENDNAM': 'eNode'
                            }

STANET_producer_allocation = {
                             'NAME': 'name',
                             'POWER': 'power',
                             'ANFNAM': 'sNode',
                             'ENDNAM': 'eNode',
                             'XRA': 'start_x',
                             'YHA': 'start_y',
                             'XRB': 'end_x',
                             'YHB': 'end_y',
                             None:[1,2,3]
                             }

STANET_vogelstang_producer_allocation = {
                             'NAME': 'name',
                             'ANFNAM': 'sNode',
                             'ENDNAM': 'eNode',
                             'XRA': 'start_x',
                             'YHA': 'start_y',
                             'XRB': 'end_x',
                             'YHB': 'end_y',
                             None:[1,2,3, 'power']
                             }

