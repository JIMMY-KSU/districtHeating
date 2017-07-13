# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 12:22:53 2017

@author: jpelda
"""

import numpy as np

class Producer():
    def __init__(self, producerValues):
        
        self.name = producerValues['name']
        self.power = producerValues['power']
        self.sNode = producerValues['sNode']
            # name of point in return pipe
        self.eNode = producerValues['eNode']
            # name of point in supply pipe
        self.Pb = 7  # supply pressure
        self.Pa = 1  # return pressure
        self.Tb = 130 + 273.15  # supply temperature
        self.element = "producer"

