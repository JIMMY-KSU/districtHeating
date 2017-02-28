# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 17:04:27 2017
@author: jpelda"""

"""these values may not been sorted, the pathWays will not be sorted too!"""
import os
from DataIO import DataIO
from HeatSink_Consumptionprofiles import HeatSink_Consumptionprofiles

class Consumer():

    def __init__(self, consumerValues):

        self.index = consumerValues['index']
        self.heat_exchangerModel = consumerValues['heat_exchangerModel']
        self.start_node_name = consumerValues['start_node_name']
        self.end_node_name = consumerValues['end_node_name']
        self.start_x = consumerValues['start_x']
        self.start_y = consumerValues['start_y']
        self.end_x = consumerValues['end_x']
        self.end_y = consumerValues['end_y']
        self.heat_consumptionProfile = \
            consumerValues['heat_consumptionProfile']
        self.heat_consumptionAverage = \
            consumerValues['heat_consumptionAverage']


    def heat_consumptionProfiles(self, i=slice(None,None)):
        return self.__dataArray['heat_consumptionProfile'][i]

    def heat_consumption(self, heatExProfile, i = slice(None,None)):
        heat_consumption=self.__heat_consumption.consumptionProfile(heatExProfile,i)
        return heat_consumption

    def heat_consumptionAverage(self, i = slice(None,None)):
              return self.__dataArray['heat_consumptionAverage'][i]
