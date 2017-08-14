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
        'WDZAHL': 'thermalTransmissionCoefficient',  # W/m²K
        'RAU': 'roughness',
        'DM': 'diameter_0',
        'DP': 'm_max',  # for testing, is not the correct key
        None: ['start_height', 'end_height',
               'transferCoefficient_0',
               'transferCoefficient_1',
               'conductivity_0',
               'conductivity_1',
               'conductivity_2',
               'diameter_1',
               'diameter_2',
               'diameter_3',
               'sprp',
               'index',
               'resistivity'  # W/mK
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

