# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 12:22:53 2017

@author: jpelda
"""

class Producer():
    def __init__(self, producerValues):
        
        self.name = producerValues['name']
        self.power = producerValues['power']
        self.sNode = producerValues['sNode']
            # name of point in return pipe
        self.eNode = producerValues['eNode']
            # name of point in supply pipe
        self.supply_pressure = 7
        self.return_pressure = 1
        self.supply_temperature = 130 + 273.15
        # TODO pressure anpassen (nicht fix)
