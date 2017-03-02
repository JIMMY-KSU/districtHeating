# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 09:37:38 2017

@author: narand
"""

import sys
import os

sys.path.append(os.path.join(os.path.abspath(".."),'class'))

import Pipe

pipeValue = {
             'index': 12,
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
             'heatTransitionCoefficient': 12,
             'roughness': 'RAU',
             'heat_transferCoefficient_inner': 10,
             'heat_transferCoefficient_outer': 20,
             'heat_conductivity_1': 30,
             'heat_conductivity_2': 40,
             'heat_conductivity_3': 50,
             'diameter_1': 0,
             'diameter_2': 0,
             'diameter_3': 0,
             'SP_RP': 'SUPPLY'
             }

Pipe1 = Pipe.Pipe(pipeValue)