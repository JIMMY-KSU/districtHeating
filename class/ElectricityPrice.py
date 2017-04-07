# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:17:01 2017

@author: jpelda
"""

from datetime import datetime

class ElectricityPrice():
    def __init__(self, priceValues):
        self.priceValues = priceValues
        
    def getElectricityPrice(self):
        
        return self.priceValues