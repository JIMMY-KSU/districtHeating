# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 10:42:51 2017

@author: narand
"""

import os
import numpy as np
import Pipe as Pipe
import Node as Node
import HeatExchanger as HeatExchanger
from dbfread import DBF

url = os.path.join(os.path.abspath(".") , os.path.join('input', 'TestNetz'))

def getPipe(namePipe):
    tablePipe = DBF(os.path.join(url, namePipe), load=True)
    returnArray = np.empty(len(tablePipe), dtype='O')
    for i in range(len(tablePipe)):
        index                     = i
        start_x                   = 0
        start_y                   = 0
        end_x                     = 0
        end_y                     = 0
        start_node                = tablePipe.records[i]['ANFNAM']
        end_node                  = tablePipe.records[i]['ENDNAM']
        length                    = tablePipe.records[i]['RORL']
        diameter_inner            = tablePipe.records[i]['DM']
        diameter_outer            = 0
        start_height              = 0
        end_height                = 0
        heatTransitionCoefficient = tablePipe.records[i]['WDZAHL']
        roughness                 = tablePipe.records[i]['RAU']
        returnArray[i]            = Pipe.Pipe(index, start_x, start_y, end_x, end_y, start_node, end_node, length, diameter_inner, diameter_outer, start_height, end_height, heatTransitionCoefficient, roughness)
    return returnArray

def getNode(nameNode):
    tableNode = DBF(os.path.join(url, nameNode), load=True)
    returnArray = np.empty(len(tableNode), dtype='O')
    for i in range(len(tableNode)):
        index          = i
        node           = tableNode.records[i]['KNAM']
        height         = tableNode.records[i]['GEOH']
        x              = tableNode.records[i]['XRECHTS']
        y              = tableNode.records[i]['YHOCH']
        VL_RL          = tableNode.records[i]['SUPPLY']
        returnArray[i] = Node.Node(index, node, height, x, y, VL_RL)
    return returnArray
    
def getHeatExchanger(nameHeatExchanger):
    tableHeatExchanger = DBF(os.path.join(url, nameHeatExchanger), load=True)
    returnArray = np.empty(len(tableHeatExchanger), dtype='O')
    for i in range(len(tableHeatExchanger)):
        index              = i
        heat_performance   = tableHeatExchanger.records[i]['WAERMEMENG']
        kw                 = tableHeatExchanger.records[i]['ISKW']
        start_node         = tableHeatExchanger.records[i]['ANFNAM']
        end_node           = tableHeatExchanger.records[i]['ENDNAM']
        returnArray[i]     = HeatExchanger.HeatExchanger(index, heat_performance, kw, start_node, end_node)
    return returnArray