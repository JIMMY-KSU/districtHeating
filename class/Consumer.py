# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 17:04:27 2017
@author: jpelda"""

"""these values may not been sorted, the pathWays will not be sorted too!"""
import os
from DataIO import DataIO
from HeatSink_Consumptionprofiles import HeatSink_Consumptionprofiles
import numpy as np

class Consumer():

    def __init__(self, index, consumerValues):
        self.index = index
        self.sNode = consumerValues['sNode']
        self.eNode = consumerValues['eNode']
        self.start_x = consumerValues['start_x']
        self.start_y = consumerValues['start_y']
        self.end_x = consumerValues['end_x']
        self.end_y = consumerValues['end_y']
        self.profile = consumerValues['profile']
        self.average = consumerValues['average']
        self.Q = float(-np.abs(consumerValues['Q'])) #Watt

        self.Ta = float(130 + 273.15)
        self.Tb = float(60 + 273.15)
        self.Pa = float(0)
        self.Pb = float(0)
        self.cp = float(4183)  # J/(kg*K)
        self.m = float(self.__massflow(self.Q, self.cp, self.Ta, self.Tb))  # t/h

        self.element = "consumer"

    def heat_consumptionProfiles(self, i=slice(None,None)):
        return self.__dataArray['heat_consumptionProfile'][i]

    def heatflow(self, heatExProfile, i = slice(None,None)):
#        arr = consumptionProfile(heatExProfile,i)
        arr = 1000 #  [kW]
        return arr

    def heat_consumptionAverage(self, i = slice(None,None)):
        return self.__dataArray['heat_consumptionAverage'][i]

    def __massflow(self, Q, cp, Ta, Tb):
        val = Q / (cp * (Tb - Ta))
        return val

if __name__ == "__main__":
    print("Consumer \t\t run directly")

    consumerValues = {'sNode': 'K1017', 'eNode': 'K1018',
                      'start_x': 11, 'start_y': 21, 'end_x': 10, 'end_y': 20,
                      'heat_consumptionProfile': 'house',
                      'heat_demand': 1000, 'profile':'test', 'average':'test'
                      }
    consumer = Consumer(0, consumerValues)
    print(consumer.__dict__)

else:
    print("Consumer \t\t was imported into another module")
