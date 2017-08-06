# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 11:03:13 2017

@author: jpelda
"""


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
        'DP': 'm_max',  # for testing, is not the correct key
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

STANET_vog_producer_allocation = {
                             'NAME': 'name',
                             'ANFNAM': 'sNode',
                             'ENDNAM': 'eNode',
                             'XRA': 'start_x',
                             'YHA': 'start_y',
                             'XRB': 'end_x',
                             'YHB': 'end_y',
                             None:[1,2,3, 'power']
                             }

