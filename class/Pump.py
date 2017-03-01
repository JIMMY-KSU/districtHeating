# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:17:01 2017

@author: jpelda
"""


class Pump():
    def __init__(self, pumpValues):
        self.index = pumpValues['index']
        self.profil = pumpValues['profil']
        self.start_node_name = pumpValues['start_node_name']
        self.end_node_name = pumpValues['end_node_name']
narandbrunch