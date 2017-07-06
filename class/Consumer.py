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
        self.heat_profile = consumerValues['heat_consumptionProfile']
        self.heat_average = consumerValues['heat_consumptionAverage']

        self.Q = consumerValues['heat_demand']

        self.flow = consumerValues['flow']
        self.Ta = 130 + 273.15
        self.Tb = 60 + 273.15
        self.cp = 4.1
        self.m = self.__massflow(self.Q, self.cp, self.Ta, self.Tb) # t/h

        # TODO implement function for massflow


    def heat_consumptionProfiles(self, i=slice(None,None)):
        return self.__dataArray['heat_consumptionProfile'][i]

    def heatflow(self, heatExProfile, i = slice(None,None)):
#        arr = consumptionProfile(heatExProfile,i)
        arr = 1000 #  [kW]
        return arr

    def heat_consumptionAverage(self, i = slice(None,None)):
        return self.__dataArray['heat_consumptionAverage'][i]

    def __massflow(self, Q, cp, Ta, Tb):
        val = Q / (cp * (Ta - Tb))
        return val
