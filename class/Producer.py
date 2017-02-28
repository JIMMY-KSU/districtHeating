# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 12:22:53 2017

@author: jpelda
"""

class Producer():
    def __init__(self, producerValues):
        
        self.name = producerValues['name']
        self.power = producerValues['power']
        self.start_node_name = producerValues['start_node_name']
        self.end_node_name = producerValues['end_node_name']
