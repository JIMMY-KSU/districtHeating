# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 20:26:34 2016

@author: jpelda

This class plots figures.
It inherits from Plotter_helper

yAxis must be importet as array always.
"""
import numpy as np
#from datetime import datetime
#import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker

import os
import sys

import datetime
from DataIO import DataIO
from matplotlib.ticker import FormatStrFormatter
import math

class Plotter():

    def __init__(self):
        self.title = ''
        
        
    def grid(self):
        pass
        
        
        
    def color(self, i):
     self.__color = [
                ['black',                '#000000'],
                ['hawk_red',             '#C24C43'],
                ['hawk_blue',            '#43B9C2'],
                ['hawk_green',           '#B9C243'],
                ['orange',               '#FFA500'],
                ['blue',                 '#0000FF'],
                ['hawk_magenta',         '#C243B9'],                        
                ['olive',                '#808000'],
                ]
     return self.__color[i][1]
     
    def scatter(self, x, y, s = 2  # 0 to 15 point radii
                , c = 'blue', alha = 0.5):
        plt.scatter(x, y, s, c, alpha =0.5)
        plt.show()
    def plot_xyLine(self,
                    xAxis, yAxis,
                    lineStyle = "-",
                    xLabel = '', yLabel = '',
                    title = '', legend = '',
                    position = "upper right",rotation= None,
                    pltStyle='latex-classic'):
        """
        Parameters
        -----------
        xAxis = [] \n
        yAxis = [[],[],[], ...] \n
        lineStyle = 'string' str: '-', '--', '-.', ':' etc. \n
        xLabel = 'string' \n
        yLabel = 'string' \n
        title = 'string' \n
        legend = ['string x Achse', 'string x Achse 2'] \n
        positon = 'string' str: "upper right", "upper left", "lower right" etc.
        rotation= 0 - 360 \n

        Return
        ------------
        fig
        """
        self.__xAxis = xAxis
        self.__yAxis = yAxis
        self.__title = title
        self.__lineStyle = lineStyle

        fig = plt.figure(figsize=(12.6, 7.09))
        ax = fig.add_subplot(111)
        plt.style.use(pltStyle)
        try:
            if isinstance(self.__xAxis[0], (datetime.datetime, datetime.date)):
                if len(self.__xAxis) <= 15000:
                    years = mdates.YearLocator()
                    months = mdates.MonthLocator()
                    days = mdates.DayLocator()
                    ax.xaxis_date()
                    ax.xaxis.set_major_locator(months)
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
                    ax.xaxis.set_minor_locator(days)
                    for index, item in enumerate(self.__yAxis):
                        if item is not None:
                            plt.plot(self.__xAxis, item, color=self.color(index))
                        else:
                            break
                else:
                    years = mdates.YearLocator()
                    months = mdates.MonthLocator()
                    days = mdates.DayLocator()
                    ax.xaxis_date()
                    ax.xaxis.set_major_locator(years)
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
                    ax.xaxis.set_minor_locator(months)
                    for index, item in enumerate(self.__yAxis):
                        if item is not None:
                            plt.plot(self.__xAxis, item,
                                     colo=self.color(index))
                        else:
                            break

            elif isinstance(float(self.__xAxis[0]), float):
                '''loops through all y values and adds them to the figure'''

                ax.tick_params(direction="out", pad=5)

                plt.plot(self.__xAxis, self.__yAxis[0], color=self.color(0))
                for index, item in enumerate(self.__yAxis[1:]):
                    if item is not None:
                        plt.plot(self.__xAxis, item, color=self.color(index+1))
    #        elif isinstance(str(self.__xAxis[0]), str):
    #            plt.xticks(np.arange(len(xAxis)), xAxis)
    #            for index, item in enumerate(self.__yAxis):
    #                if item is not None:
    #                    ax.plot(np.arange(len(xAxis)), item, self.__lineStyle)
                        
    #            ax.set_xlim(xmin = self.__xMin, xmax = self.__xMax)
    #            ax.set_ylim(self.__yMin, self.__yMax)
        except:
            raise


        plt.show()
        return fig

    def plot_xyLinehvLine(self,
                          xData,
                          yData,
                          yMax=0,
                          xMax=0,
                          lineStyle="-",
                          xLabel='', yLabel='',
                          title='', legend='',
                          rotation=None,
                          pltStyle='latex-classic'):
        """
        Parameters
        -----------
        xData = [Values of xAxis0]
        yData = [[Values of yAxis0], [Values of yAxis1], ...]
        lineStyle = str
        """
        self.__xAxis = xData
        self.__yAxis = yData
        self.__title = title
        self.__lineStyle = ['-', '--', ':']
        fig = plt.figure(figsize = (12.6, 7.09))
        rcParams["figure.figsize"] = 8, 4.5
#        Plotter_Helper.font(self)

        plt.style.use(pltStyle)
        ax_0 = fig.add_subplot(111)
#        ax_0.tick_params(axis="x", pad=105)
        ax_1 = fig.add_subplot(111)
        ax_2 = fig.add_subplot(111)
        try:
            if isinstance(self.__xAxis[0], datetime.date):
                years = mdates.YearLocator()
                months = mdates.MonthLocator()
                days = mdates.DayLocator()
                yearsFmt = mdates.DateFormatter('%b %y')
                ax_0.xaxis_date()
                ax_0.xaxis.set_major_locator(months)
                ax_0.xaxis.set_major_formatter(yearsFmt)
                ax_0.xaxis.set_minor_locator(days)
                for index, item in enumerate(self.__yAxis):
                    if item is not None:
                        ax_0.plot(self.__xAxis[index], item, 
                                  color=self.color(index))
                    else:
                        break
            elif isinstance(float(self.__xAxis[0][0]), float):
                '''loops through all y values
                and adds them to the figure'''      
                ax_0.tick_params(direction="out", top="off",
                                 right="off", pad=5)
                ax_1.tick_params(direction="out", top="off",
                                 right="off", pad=5)
                ax_2.tick_params(direction="out", top="off",
                                 right="off", pad=5)
                for index0, item0 in enumerate(self.__yAxis):
                    legend_index = 0
                    if index0 == 0:
                        for index, item in enumerate(item0):
                            if item is not None:
                                if index == 0 or index % 2 != 0:
                                   '''checks for the legend setting'''
                                   ax_0.plot(self.__xAxis[index], item,
                                             self.__lineStyle[index0],
                                             linewidth = 3,
                                             color=self.color(
                                                     round(index / 2 + 0.40)),
                                             label=legend[index0]
                                             [legend_index])
                                   legend_index = legend_index + 1
                                else:
                                    ax_0.plot(self.__xAxis[index],
                                              item, self.__lineStyle[index0],
                                              linewidth=3,
                                              color = self.color(
                                                      round(index / 2 + 0.40)))
                        ax_0.set_yticks(self.__yAxis[0][0])
                    elif index0 == 1:
                        for index, item in enumerate(item0):
                            if item is not None:
                                if index == 0 or index % 2 != 0:
                                    
                                   print(legend[index0][legend_index])
                                   '''checks for the legend setting'''
                                   ax_1.plot(self.__xAxis[index], item, self.__lineStyle[index0],
                                             linewidth = 1,
                                             color = self.color(round(index / 2 + 0.40)),
                                             label = legend[index0][legend_index])
                                   legend_index +=1
                                else:
                                    ax_1.plot(self.__xAxis[index], item, self.__lineStyle[index0], linewidth = 1, color = self.color(round(index / 2 + 0.40)))

                        ax_0.set_yticks(self.__yAxis[0][0] + self.__yAxis[1][0])                    
                    elif index0 == 2:
                        for index, item in enumerate(item0):
                            if item is not None:
                                if index == 0 or index % 2 != 0:
                                   '''checks for the legend setting'''
                                   ax_2.plot(self.__xAxis[index], item, self.__lineStyle[index0],
                                             linewidth = 1.5,
                                             color = self.color(round(index / 2 + 0.40)),
                                             label = legend[index0][legend_index])
                                   legend_index += 1
                                else:
                                   ax_2.plot(self.__xAxis[index], item, self.__lineStyle[index0],
                                             linewidth = 1.5,
                                             color = self.color(round(index / 2 + 0.40)))
                        ax_0.set_yticks(self.__yAxis[0][0] + self.__yAxis[1][0] + self.__yAxis[2][0])
                          
  #        elif isinstance(str(self.__xAxis[0]), str):
    #            plt.xticks(np.arange(len(xAxis)), xAxis)
    #            for index, item in enumerate(self.__yAxis):
    #                if item is not None:
    #                    ax.plot(np.arange(len(xAxis)), item, self.__lineStyle)
                        
    #            ax.set_xlim(xmin = self.__xMin, xmax = self.__xMax)
        except:
            print("in Plotter.plot_xyLine: No format for xAxis found")

        
        Plotter_Helper.figureLabelingXYLineHVLine(self, xLabel, yLabel, title, ax_0,rotation, bbox = len(self.__yAxis))
#        Plotter_Helper.font(self)
        
        ax_0.set_xticks(self.__xAxis[0])
        ax_0.annotate("Teilnetz Vogelstang", xy = (100,400), xytext=(100,400))
        ax_1.annotate("Teilnetz Nord", xy = (100, 699), xytext=(100,699))
        ax_2.annotate("Teilnetz Ost", xy = (100, 1026), xytext = (100, 1026))
#        ax_0.set_xlim(0, yMax)
#        ax_1.set_yticks(self.__yAxis[1][0])
#        ax_2.set_yticks(self.__yAxis[2][0])
#        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#        plt.subplots_adjust(bottom =0.5)
        plt.grid("off")
        plt.show()
        return fig
    def plot_xyyLine(self, xAxis, yAxis0, yAxis1, legend0, legend1, xLabel = "", yLabel0 = "", yLabel1 = "",
                     title = "", rotation = 0, lineStyle0 = "-", lineStyle1 = ["-","-","-"], 
                     kind = None, alpha0 = 1, pltStyle='latex-classic'):
        """
        xAxis must be of []
        yAxis0 must be of [[]]
        yAxis1 must be of [[]]
        legends must be of []
        kind can be of bar, then first yAxis is a bar-plot
        """
        self.__xAxis = xAxis 
        self.__yAxis0 = yAxis0
        self.__yAxis1 = yAxis1
        self.__lineStyle0 = lineStyle0
        self.__lineStyle1 = lineStyle1
        
#        Plotter_Helper.font(self)
        plt.style.use(pltStyle)
        fig = plt.figure(figsize = (12.6,7.09))
              
        plt.xticks(np.arange(len(self.__xAxis)), self.__xAxis, rotation = rotation) #stays here, otherwise no rotation

        ax_0 = fig.add_subplot(111)
        ax_1 = ax_0.twinx()
        if isinstance(self.__xAxis[0], datetime.date):
            self.__xAxis
            years = mdates.YearLocator()
            months = mdates.MonthLocator()
            days = mdates.DayLocator()
            yearsFmt = mdates.DateFormatter('%b %y')
            ax_0.xaxis_date()
            ax_0.xaxis.set_major_locator(months)
            ax_0.xaxis.set_major_formatter(yearsFmt)
            ax_0.xaxis.set_minor_locator(days)
            ax_1.xaxis_date()
            ax_1.xaxis.set_major_locator(months)
            ax_1.xaxis.set_major_formatter(yearsFmt)
            ax_1.xaxis.set_minor_locator(days)

        else:
            '''loops through all y values and adds them to the figure'''              
      
        ax_0.tick_params(direction="out", pad = 5)
        ax_1.tick_params(direction = "out", pad = 5)
        
        index0 = 0
        for index0, item in enumerate(self.__yAxis0):
            if item is not None:            
                if kind == None:
                    ax_0.plot(np.arange(len(self.__xAxis)), item, self.__lineStyle0, color= self.color(index0), label = legend0[index0])
                elif kind == "bar":
                    ax_0.bar(np.arange(len(self.__xAxis)), item, width = 0.3, align = "center", color = self.color(index0),alpha = alpha0, label = legend0[index0])
        
        index0 = 0
        index1 = 0
        for index1, item1 in enumerate(self.__yAxis1):
                if item is not None:
                   ax_1.plot(np.arange(len(self.__xAxis)), item1, self.__lineStyle1[index1], color = self.color(index0 + index1 +1), label = legend1[index1], markersize = 10)                
                
        
#      # automatically update ylim of ax2 when ylim of ax1 changes.
##        ax_0.callbacks.connect("ylim_changed", convert_ax_1_to_celsius)
#        ax_0.plot(np.linspace(-40, 120, 100))
#        ax_1.set_ylim(0, 6)
        
        Plotter_Helper.figureLabelingXYYLine(self, ax_0, ax_1, xLabel = xLabel, yLabel0 = yLabel0, yLabel1 = yLabel1, title = title)
#        Plotter_Helper.font(self)
#        plt.tight_layout()
        plt.show()
        
        return fig
        
