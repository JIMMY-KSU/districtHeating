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
import time
from datetime import datetime
from datetime import timedelta
from copy import copy
from dbfread import DBF
# from Dictionaries import Dictionaries
# from TRY_Dictionary import TRY_Dictionary

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
                  header=1, encoding='utf-8-sig', decimal=',',
                  lineterminator='\n', thousands='.', names=None):
        
        filepath = self.__filepath_import + os.sep + filename
        arr = pd.read_csv(filepath, delimiter=delimiter, header=header,
                          encoding=encoding, decimal=decimal,
                          lineterminator=lineterminator, thousands=thousands,
                          names=names)
        
        print(arr)
        return arr
        
        
        
#    def importCSV(self, filename_import,
#                  dtype=None, header = 0, startrow=0,
#                  delimiter=";", columnofdate=None, dateformat=None):
#        '''
#        imports CSV and replaces first comma start counting from right
#        #######
#        return:
#            array with dtype
#        '''
#
#        filename = self.__filepath_import + os.sep + filename_import
#        filename_pointAsDec = self.__filepath_import + os.sep +\
#            os.path.splitext(filename_import)[0] +\
#            "_pointAsDec" + os.path.splitext(filename_import)[1]
#        pointAsDec = False
#
#        self.__dataArray = ''
#        self.__dataArrayHeader = ''
#
#        if os.path.isfile(filename_pointAsDec):
#            filename = filename_pointAsDec
#            pointAsDec = True
#
#        with open(filename, encoding='utf-8-sig') as csvfile:
#
#            readCSV = csv.reader(csvfile, delimiter=delimiter)
#            index = 0
#            for index, row in enumerate(readCSV):
#                row1 = []
#                for index, item in enumerate(row):
#                    if index == columnofdate:
#                        row1.append(item)
#                    if pointAsDec is False:
#                        # changes decimalsign , to decimalsign .
#                        item = item.replace(",", ".")
#                        item = item.replace(".", "", item.count(".") - 1)
#                        row1.append(item)
#                    else:
#                        row1.append(item)
#                if index is header:
#                    self.__dataArrayHeader = self.__dataArrayHeader +\
#                                    ','.join(x for x in row1) + '\n'
#                if index > startrow and index is not header:
#                    self.__dataArray = self.__dataArray + ','.join(
#                                            x for x in row1) + '\n'
#            csvfile.close
#            print(self.__dataArray)
#            if pointAsDec is False:
#                # saves data with decimalsign . into new file with
#                # filename_pointAsDec.
#                with open(filename_pointAsDec, "w", delimiter=delimiter) as text_file:
#                    text_file.write(self.__dataArray)
#                    text_file.close()
#            else:
#                self.__dataArray = np.genfromtxt(io.StringIO(self.__dataArray),
#                                              dtype=dtype,
#                                              delimiter=',',
#                                              converters=self.str2date(
#                                                  columnofdate=columnofdate,
#                                                  dateformat=dateformat))
#
#        return self.__dataArray

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

    def importDBF(self, filename_import, dtype=None, dtypeAllocation=None):
        '''
        imports dBASE and allocates values to dtype of returnArray. Allocation
        of values of dBASE to dtype of returnArray must be given in
        dtypeAllocation.
        #######
        return:
           array with dtype
        '''
        try:
            dataArray = DBF(self.__filepath_import + os.sep + filename_import,
                            encoding='cp437', load=True)
        except:
            print("If you import STANET DBF, please make sure to clean"
                  "STANET-File with STANTE-Programm. Former deleted nodes will"
                  "cause error")
        returnArray = np.empty(len(dataArray), dtype=dtype)
        for index, record in enumerate(dataArray):
            for item in dtype['names']:
                try:
                    returnArray[index][item] = record[dtypeAllocation[item]]
                except:
                    pass
        return returnArray

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


#    def writeColHeader(self, filepathAndfilename, tableHeadername):
#        self.__filepathAndfilename = filepathAndfilename
#        with open(self.__filepathAndfilename, "r") as text_file:
#            text_old = text_file.read()
#            text_file.close()
#        with open(self.__filepathAndfilename, "w") as text_file:
#            text_file.write(text_old[0:0] + str(Dictionaries("").csvHeader(tableHeadername)) + text_old[:])
#            text_file.close()

