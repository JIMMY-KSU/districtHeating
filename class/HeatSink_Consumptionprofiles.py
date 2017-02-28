# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 19:37:50 2017
@author: jpelda"""
import os
from DataIO import DataIO

class HeatSink_Consumptionprofiles():
    def __init__(self,
                filename = os.getcwd() + os.sep + 'heat_consumptionProfiles.csv',
                startrow = 1,
                dtype = {'names':(
                                'date',
                                'house',
                                'industry',
                                ),
                        'formats':(
                                'object',
                                'f',
                                'f',
                                )},
                columnofdate = 0,
                dateformat = '%d.%m.%y %H:%M'):

        self.__filename = filename
        self.__startrow = startrow
        self.__columnofdate = columnofdate
        self.__dateformat = dateformat

        self.__dataArray = DataIO(os.getcwd() + os.sep + 'input', os.getcwd() + os.sep + 'output').importCSV('heat_consumptionProfiles.csv', dtype, startrow = startrow, columnofdate = columnofdate, dateformat = dateformat)

    def date(self, i = slice(None,None)):
        return self.__dataArray['date'][i]
    def consumptionProfile(self, profile, i=slice(None,None)):
        return self.__dataArray[profile][i]
