# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 20:30:03 2016

@author: johannes
"""

import csv
import os
import io
import numpy as np
import pandas as pd
import pysal as ps
import time
from datetime import datetime
from datetime import timedelta
from copy import copy
from dbfread import DBF
import Dictionary
from collections import OrderedDict

from matplotlib import dates as dates
# from DataIO_Helper import DataIO_Helper

# from dbf import dbf


class DataIO():

    def __init__(self, filepath_import, filepath_export):
        '''
        DataIO for Import and Export of data
        '''
        self.__filepath_import = filepath_import
        self.__filepath_export = filepath_export

#    def import CSV(self):

    def importCSV(self, filename, delimiter=';', dtype=None,
                  header=0, encoding='utf-8-sig', decimal=',', usecols=None,
                  lineterminator='\n', thousands='.', names=None,
                  infer_datetime_format=False):
        '''
        str, for more inputparameter see pandas read_csv
        output
        pandas DataFrame
        '''
        filepath = self.__filepath_import + os.sep + filename

            
        if dtype is not None:
            usecols = []
            for value, key in zip(dtype.keys(), dtype.values()):
                if value is not None:
                    usecols.append(value)

        df = pd.read_csv(filepath, delimiter=delimiter, header=header,
                          encoding=encoding, decimal=decimal, usecols=usecols,
                          lineterminator=lineterminator, thousands=thousands,
                          names=names, infer_datetime_format=False)

        if dtype is not None:
            if None in dtype.keys():
                df_length = len(df)
                for item in dtype[None]:
                    arr = np.empty(df_length)
                    arr[:] = False
                    df[item] = pd.Series(arr, index=df.index)
                # adds columns that are probably not given in dtype
                # but are used add instances of class
            df = df.rename(columns=dtype)

        print('loading %s \t----> OK ' %filename)

        return df


    def importTRY(self, location, year, season, quarterHour, startrow, dtype):
        self.__table = []
        self.__location = location
        self.__year = year
        self.__season = season
        self.__columnofdate = 2
        self.__dateformat = '%m-%d-%H'
        self.__filename = self.__filepath_import + os.sep +\
            str("TRY" + str(self.__year) + "_" +
                TRY_Dictionary.TRYDictLocations(self, self.__location) + "_" +
                TRY_Dictionary.TRYDictLocations(self, self.__season) + ".dat")
        self.__quarterHour = quarterHour
        self.__startrow = startrow
        self.__dtype = dtype

        with open(self.__filename, encoding='cp437') as csvfile:
            linereader = csv.reader(csvfile)
            for indexRow, row in enumerate(linereader):
                if indexRow >= self.__startrow:
                    for item in row:
                        item = item.split()
                        if self.__quarterHour is False:
                            item[2:5] = [datetime(int(self.__year),
                                                  int(item[2]), int(item[3]),
                                                  int(item[4])-1)]
                            self.__table.append(item)
                        else:
                            item[2:5] = [datetime(int(self.__year),
                                                  int(item[2]), int(item[3]),
                                                  int(item[4])-1, 0)]
                            self.__table.append(copy(item))
                            i = 0
                            while i < 3:
                                item[2] += timedelta(minutes=15)
                                self.__table.append(copy(item))
                                i += 1

#
            self.__table = [tuple(i) for i in self.__table]
            print('Import ' + self.__filename + ' successfully')

            return np.asarray(self.__table, dtype=self.__dtype)

    def importDBF(self, filename, dtype=None):
        '''
        imports dBASE and allocates values to dtype of returnArray. Allocation
        of values of dBASE to dtype of returnArray must be given in
        dtypeAllocation.
        #######
        return:
           Pandas DataFrame
        '''
        dbf = ps.open(self.__filepath_import + os.sep + filename)
        d = {col: dbf.by_col(col) for col in dbf.header}
        df = pd.DataFrame(d)
        
        
        if dtype is not None:
            if None in dtype.keys():
                df_length = len(df)
                for item in dtype[None]:
                    arr = np.empty(df_length)
                    arr[:] = False
                    df[item] = pd.Series(arr, index=df.index)
                # adds columns that are probably not given in dtype
                # but are used add instances of class
        df = df.rename(columns=dtype)

        print('loading %s \t----> OK ' %filename)

        return df

    def exportCSV(self, filename, results, delimiter=";"):
        '''
        exports results as CSV with "," as decimal seperator
        filename = string without '.csv'
        results = []
        '''
        self.__results = results
        '''opens file and writes into it'''
        with open(self.__filepath_export + os.sep + filename +
                  ".csv", 'w') as pyfile:
            for item0 in self.__results:
                for item1 in item0:
                    if type(item1) == float:
                        item1 = str(item1)
                        item1 = item1.replace(".", ",")
                    pyfile.write(
                                 item1 + delimiter
                                 )

                pyfile.write("\n")
            pyfile.close()

    def exportNumpyArr(self, filename, arr):
        np.save(self.__filepath_export + os.sep + filename, arr)

    def importNumpyArr(self, filename, arr):
        np.load(self.__filepath_import + os.sep + filename, arr)
        return arr

    def exportFig(self, filename, fig):
        '''
        exports matplotlib grafik as pdf and png\n
        #######\n
        return:\n
            pp.close()
        '''

        fig.savefig(self.__filepath_export + os.sep + filename +
                    ".png", bbox_inches='tight', dpi=300)
        print("Saved PNG to: " + str(self.__filepath_export +
                                     os.sep + filename + ".png"))
        fig.savefig(self.__filepath_export + os.sep + filename +
                    ".pdf", filetype="pdf", bbox_inches='tight', dpi=300)
        print("Saved PDF to: " + str(self.__filepath_export +
                                     os.sep + filename + ".pdf"))

    def str2date(self, columnofdate=None, dateformat=None):
        if columnofdate is None or dateformat is None:
            return None
        else:
            func_str2date = {columnofdate: lambda x: datetime.strptime(
                    x.decode("utf-8"), dateformat)}
            return func_str2date

    def str2num(self, column):
        func_str2num = {column: lambda x: dates.date2num(
                    x.decode("utf-8"), '%d.%m.%Y %H:%M')}
        return func_str2num

    def strpdate2num(self, column):
        func_strpdate2num = {column: dates.strpdate2num('%d.%m.%Y %H:%M')}
        return func_strpdate2num
    
    
if __name__ == "__main__":
    import Dictionary
    print('DataIO \t run directly \n')
    DataIO = DataIO(
            os.path.dirname(os.getcwd()) + os.sep +
            'input' + os.sep + 'TestNetz',
            os.path.dirname(os.getcwd()) + os.sep +
            'output' + os.sep + 'TestNetz')
    heatgrid_pipes = DataIO.importDBF(
            'STestNetz.DBF', dtype=Dictionary.STANET_pipes_allocation)

    heatsource = DataIO.importCSV(
            'WTestNetz.csv', dtype=Dictionary.STANET_producer_allocation,
            delimiter='\t', header=0)
    print(heatsource)

else:
    import os
    import sys
    sys.path.append(os.getcwd() + os.sep + 'function')
    print(sys.path.append(os.getcwd() + os.sep + 'function'))
    print('DistrictHeatingSystem \t was imported into another module')
