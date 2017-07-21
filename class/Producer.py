# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 12:22:53 2017

@author: jpelda
"""


class Producer():
    def __init__(self, producerValues):

        self.cp = 4183  # J/(kg*K)

        self.index = producerValues['index']
        self.sNode = producerValues['sNode']  # name of point in return pipe
        self.eNode = producerValues['eNode']  # name of point in supply pipe
        self.start_x = producerValues['start_x']
        self.start_y = producerValues['start_y']
        self.end_x = producerValues['end_x']
        self.end_y = producerValues['end_y']


        self.Q = producerValues['power']
        self.Pa = 100000  # return pressure [Pa] 1bar = 100000Pa
        self.Pb = 700000  # supply pressure [Pa] 1bar = 100000Pa
        self.Tb = 130 + 273.15  # supply temperature
        self.Ta = 0
        self.m = self.__massflow(self.Q, self.cp, self.Ta, self.Tb)  # t/h
        self.element = "producer"

    def __massflow(self, Q, cp, Ta, Tb):
        val = Q / (cp * (Tb - Ta))
        return val
