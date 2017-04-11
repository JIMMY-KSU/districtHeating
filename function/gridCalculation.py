# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 14:45:18 2017

@author: narand
"""

import dependencies as dp
import numpy as np

def gridCalculation(x, args):
    heatgrid = args[0]
    heatsink = args[1]
    heatsource = args[2]
    I = args[3]

    numberOfNodes = len(heatgrid.nodes())
    numberOfPipes = len(heatgrid.pipes())
    numberOfSinks = len(heatsink.consumer())
    numberOfSources = len(heatsource.producer())

    silceOfPipes = slice(0,
                         numberOfPipes)
    silceOfSinks = slice(numberOfPipes,
                         numberOfPipes + numberOfSinks)
    sliceOfSources = slice(numberOfPipes + numberOfSinks,
                           numberOfPipes + numberOfSinks + numberOfSources)
    k = numberOfNodes
    v = (numberOfPipes + numberOfSinks + numberOfSources)
    Iplus = np.zeros_like(I)
    Iminus = np.zeros_like(I)
    for i, row in enumerate(I):
        for j, item in enumerate(row):
            if(item == 1):
                Iplus[i, j] = item
            if(item == -1):
                Iminus[i, j] = item
    returnArray = np.zeros(6*v + 2*k)
    arrSupplyPressureSources = np.zeros(numberOfSources)
    arrSupplyTemperatureSources = np.zeros(numberOfSources)
    arrReturnTemperatureSinks = np.zeros(numberOfSinks)
    arrHeatDemandSinks = np.zeros(numberOfSinks)

    for index, item in enumerate(heatsource.producer()):
        arrSupplyPressureSources[index] = item.supply_pressure
        arrSupplyTemperatureSources[index] = item.supply_temperature

    for index, item in enumerate(heatsink.consumer()):
        arrReturnTemperatureSinks[index] = item.return_temperature
        arrHeatDemandSinks[index] = item.heat_demand

    n = 0
    arrM = x[n: n + v]
    n += len(arrM)
    arrP = x[n: n + k]
    n += len(arrP)
    arrPa = x[n: n + v]
    n += len(arrPa)
    arrPb = x[n: n + v]
    n += len(arrPb)
    arrT = x[n: n + k]
    n += len(arrT)
    arrTa = x[n: n + v]
    n += len(arrTa)
    arrTb = x[n: n + v]
    n += len(arrTb)
    arrQ = x[n: n + v]
    arrTab = np.zeros_like(arrM)
    arrMa = [1 if i >= 0 else 0 for i in arrM]
    arrMb = [-1 if i < 0 else 0 for i in arrM]
    Iab = np.dot(Iminus, np.diag(arrMa)) + \
          np.dot(Iplus, np.diag(arrMb))
    for index, item in enumerate(arrM):
        if item >= 0:
            arrTab[index] = arrTa[index]
        else:
            arrTab[index] = arrTb[index]
    '''
    equations of solver
    '''
    massBalance = np.dot(I, arrM)
    massBalance = massBalance[0:len(massBalance)-1]

    energyBalance_1 = \
        np.dot(np.transpose(Iab), arrT) + arrTab

    energyBalance_2 = \
        np.dot(np.multiply(-1, np.transpose(Iminus)), arrP) - arrPa

    impulseBalance_1 = \
        np.dot(np.transpose(Iplus), arrP) - arrPb

    impulseBalance_2 = \
         np.dot(Iplus, np.dot(np.diag(arrM), arrTb))\
         + np.dot(Iminus, np.dot(np.diag(arrM), arrTa))
    '''
    constitutive relations
    '''
    # vector of massflow
    pipeMassflow = dp.pipe_massflow(
                              arrM[silceOfPipes],
                              arrTa[silceOfPipes],
                              arrTb[silceOfPipes],
                              arrQ[silceOfPipes])

    consumerMassflow = dp.consumer_massflow(
                              arrM[silceOfSinks],
                              arrTa[silceOfSinks],
                              arrTb[silceOfSinks],
                              arrQ[silceOfSinks])

    producerMassflow = dp.producer_massflow(
                              arrM[sliceOfSources],
                              arrTa[sliceOfSources],
                              arrTb[sliceOfSources],
                              arrQ[sliceOfSources])

    pipePress = dp.pipe_press(
                              arrPa[silceOfPipes],
                              arrPb[silceOfPipes],
                              arrM[silceOfPipes])

    producerPressSupply = dp.producer_press(
                              arrSupplyPressureSources,
                              arrPb[sliceOfSources])

    producerPressReturn = dp.producer_press(
                              heatsource.producer(0).return_pressure,
                              arrPa[sliceOfSources])

    # temperatur
    consumerTemp = dp.consumer_temp(
                              arrReturnTemperatureSinks,
                              arrTb[silceOfSinks])

    producerTemp = dp.producer_temp(
                              arrSupplyTemperatureSources,
                              arrTb[sliceOfSources])

    # heatflow
    pipeQ = dp.pipe_heatflow(
                              arrQ[silceOfPipes],
                              arrTa[silceOfPipes],
                              arrTb[silceOfPipes])

    consumerQ = dp.consumer_heatflow(
                              arrHeatDemandSinks,
                              arrQ[silceOfSinks])

    returnArray = np.concatenate((
                     massBalance,
                     energyBalance_1, energyBalance_2,
                     impulseBalance_1, impulseBalance_2,
                     pipeMassflow, consumerMassflow, producerMassflow,
                     pipePress, producerPressSupply, producerPressReturn,
                     consumerTemp, producerTemp,
                     pipeQ, consumerQ))

    return returnArray
