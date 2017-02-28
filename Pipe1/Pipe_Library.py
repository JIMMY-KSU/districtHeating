# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 11:05:31 2016

@author: Pascal

###############
This library contains all possible pipe configurations

"""

class Pipe_Library():
    def __init__(self):
        pass
        
    def configuration(self, pipe_name, value):
        self.__dataConfiguration=    {'Type1':{
                                      'pipe_length':20,
                                      'pipe_diameter':1
                                     },
                                      
                                      'Type2':{
                                      'pipe_length':50,
                                      'pipe_diameter':2
                                     },
                                                 
                                     
                                     
                                     }
        
        return self.__dataConfiguration[pipe_name][value]
