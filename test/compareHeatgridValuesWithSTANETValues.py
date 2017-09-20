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

class test_DHS():
    def __init__(self, filePathToValuesToTest,
             filePathToValuesToTestAgainst):

        self.__dataIO_toT = DataIO(filePathTo_values_py, '')
        self.__dataIO_toTA = DataIO(filePathTo_values_st, '')

    def test_heatsink(self, filename_toT, filename_toTA,
                      toTA_decimal=';', toTA_skiprows=None,
                      toTA_nrows=None,toTA_header=None,
                      toTA_index_col=None, toTA_encoding='ISO-8859-1'):

        toT = self.__dataIO_toT.importNumpyArr(filename_toT)
        toTA = self.__dataIO_toTA.importCSV(filename_toTA,
                                            decimal=toTA_decimal,
                                            skiprows=toTA_skiprows,
                                            nrows=toTA_nrows,
                                            header=toTA_header,
                                            index_col=toTA_index_col,
                                            encoding=toTA_encoding)
#        def test_m(self):
#            computed = toT['v_consumers_m']
#            expected = toTA[']
#            for index, item in enumerate(toT):
#                print(item['v_consumers_m'])

#        test_pressure(self)

    def test_heatgrid(self, filename_toT, filename_toTA,
                      toTA_decimal=';', toTA_skiprows=None,
                      toTA_nrows=None,toTA_header=None,
                      toTA_index_col=None, toTA_encoding='ISO-8859-1'):
        toT = self.__dataIO_toT.importNumpyArr(filename_toT)
        toTA = self.__dataIO_toTA.importCSV(decimal=toTA_decimal,
                                            skiprows=toTA_skiprows,
                                            nrows=toTA_nrows,
                                            header=toTA_header,
                                            index_col=toTA_index_col,
                                            encoding=toTA_encoding)
        def test_m(self):
            computed = toT['v_pipes_m']
            expected = toTA['FLUSS']
            tol = 1E-3
            diff = abs(expected - computed)
            assert diff < tol, 'diff=%g' % diff

if __name__ == "__main__":
    print('comareHeatgridValuesWithSTANETValues \t run directly \n')
    
    filePathTo_values_py = os.path.dirname(os.getcwd()) + os.sep +\
                                     'output' + os.sep + 'TestNetze' + os.sep +\
                                     'TestNetz_einEinspeiser'
    filePathTo_values_st = os.path.dirname(os.getcwd()) + os.sep +\
                                     'output' + os.sep + 'TestNetze' + os.sep +\
                                     'TestNetz_einEinspeiser' + os.sep + 'STANET'
    heatsink_filename_py = 'Heatsink.npy'
    heatsink_filename_st = 'TestNetz_einEinspeiser.CSV'

    test = test_DHS(filePathTo_values_py, filePathTo_values_st)
    test_heatsink=test.test_heatsink(heatsink_filename_py, heatsink_filename_st,
                       toTA_decimal='.', toTA_skiprows=590, toTA_nrows=4,
                                          toTA_header=0, toTA_index_col=False,
                                          toTA_encoding='ISO-8859-1')

    heatgrid_filename_py = 'Heatgrid.npy'
    heatgrid_filename_st = 'TestNetz_einEinspeiser.CSV'

    test = test_DHS(filePathTo_values_py, filePathTo_values_st)
    test_heatgrid=test.test_heatgrid(heatgrid_filename_py, heatgrid_filename_st,
                       toTA_decimal='.', toTA_skiprows=567, toTA_nrows=18,
                                          toTA_header=0, toTA_index_col=False,
                                          toTA_encoding='ISO-8859-1')
    

else:
    pass
