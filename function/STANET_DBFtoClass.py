# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 09:29:04 2017

@author: jpelda
"""
import os
import sys
import numpy as np
sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'class')
import Dictionary
from DataIO import DataIO

def DBF_knotPipesToClassNetwork():
    
    array_pipes = DataIO(os.path.dirname(os.getcwd()) + os.sep + 'input',
                os.path.dirname(os.getcwd()) + os.sep + 'output').\
                importDBF(
                'TestNetz' + os.sep + 'STestNetz.DBF',
                Dictionary.STANET_pipes,
                Dictionary.Network_pipe_dtype_allocationDBFfromSTANET_pipes)
                
    array_knots = DataIO(os.path.dirname(os.getcwd()) + os.sep + 'input',
                os.path.dirname(os.getcwd()) + os.sep + 'output').\
                importDBF(
                'TestNetz' + os.sep + 'KTestNetz.DBF',
                Dictionary.STANET_knots,
                Dictionary.Network_pipe_dtype_allocationDBFfromSTANET_knots)
                
    print(STestNetz)
    print(KTestNetz)
    
    returnArray = np.empty(len(array_pipes), dtype=Dictionary.Network_pipe_dtype)
    
    for index, item in enumerate(array_pipes):
        print(index, item)
        for name in Dictionary.STANET_pipes['names']:
            print(name)
            returnArray[index][name] = item[name]

DBF_knotPipesToClassNetwork()