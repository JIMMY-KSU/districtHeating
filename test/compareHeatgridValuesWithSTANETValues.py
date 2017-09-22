# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 17:16:35 2017

@author: jpelda
"""

import os
import sys
sys.path.append(os.path.dirname(os.getcwd()) + os.sep + 'class')
print(os.path.dirname(os.getcwd()) + os.sep + 'class')
from DataIO import DataIO
from Plotter import Plotter

import numpy as np

class test_DHS():
    def __init__(self):
        plotter_test_DHS = Plotter()

        pass


    def test_heatsink(self, toT, toTA):

        pass
#        def test_m(self):
#            computed = toT['v_consumers_m']
#            expected = toTA[']
#            for index, item in enumerate(toT):
#                print(item['v_consumers_m'])

#        test_pressure(self)

    def test_heatgrid(self, toT, toTA):
        toT_pipes_sNode = np.asarray(toT['v_pipes_sNode'])
        toT_pipes_eNode = np.asarray(toT['v_pipes_eNode'])
        
        toTA_pipes_sNode = np.asarray(toTA['ANFNAM'])
        toTA_pipes_eNode = np.asarray(toTA['ENDNAM'])
        
        if np.array_equal(toT_pipes_sNode, toTA_pipes_sNode) and\
            np.array_equal(toT_pipes_eNode, toTA_pipes_eNode):
            print("toT and toTA are in same order.")
        else:
            print("toT and toTA are not in same order!")

        computed = toT['v_pipes_m']
        expected = toTA['FLUSS'] / 3600
        tol = 1E-3
        diff = abs(expected) - abs(computed)
        print('Diff of massflow \n')
        print(diff)


if __name__ == "__main__":
    print('comareHeatgridValuesWithSTANETValues \t run directly \n')
    
    filePathTo_values_py = os.path.dirname(os.getcwd()) + os.sep +\
                                     'output' + os.sep + 'TestNetze' + os.sep +\
                                     'TestNetz_einEinspeiser'
    filePathTo_values_st = os.path.dirname(os.getcwd()) + os.sep +\
                                     'output' + os.sep + 'TestNetze' + os.sep +\
                                     'TestNetz_einEinspeiser' + os.sep + 'STANET'
    heatsink_filename_py = 'test_einEinspeiser_heatgrid.npy'
    heatsink_filename_st = 'TestNetz_einEinspeiser.CSV'

    dataIO_toT = DataIO(filePathTo_values_py, '')
    dataIO_toTA = DataIO(filePathTo_values_st, '')

    toT = dataIO_toT.importNumpyArr(heatsink_filename_py)
    toTA = dataIO_toTA.importCSV(heatsink_filename_st, decimal='.',
                                 skiprows=567, nrows=18, header=0,
                                 index_col=False, encoding='ISO-8859-1')

    test = test_DHS()
    print(toTA)
    test.test_heatgrid(toT[0], toTA)
    

else:
    pass
