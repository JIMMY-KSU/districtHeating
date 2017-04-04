# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 13:56:15 2017

@author: narand
"""
import numpy as np


def getGuess(heatgrid, heatsink, heatsource):
    numberOfNodes = len(heatgrid.nodes())
    numberOfPipes = len(heatgrid.pipes())
    numberOfSinks = len(heatsink.consumer())
    numberOfSources = len(heatsource.producer())
    k = numberOfNodes
    v = (numberOfPipes + numberOfSinks + numberOfSources)
    guess = np.zeros(6*v + 2*k)
    n = 0

    # massflow
#    for index, item in enumerate(heatgrid.pipes()):
#        guess[n] = 1
#        n += 1
    guess[n] = 0.51
    n += 1
    guess[n] = 0.17
    n += 1
    guess[n] = 0.765
    n += 1
    guess[n] = 0.51
    n += 1
    guess[n] = 0.17
    n += 1
    guess[n] = 0.765
    n += 1

    for index, item in enumerate(heatsink.consumer()):
        # TODO make cp variable
        guess[n] = (item.heat_demand*(-1)) / (4182 * (heatsource.producer(0).supply_temperature-item.return_temperature))
        n += 1

    for index, item in enumerate(heatsource.producer()):
        guess[n] = 0.765
        n += 1

    # pressure
#    for index, item in enumerate(heatgrid.nodes()):
#        guess[n] = heatsource.producer(0).supply_pressure
#        n += 1
    guess[n] = 7
    n += 1
    guess[n] = 7
    n += 1
    guess[n] = 7
    n += 1
    guess[n] = 7
    n += 1
    guess[n] = 1
    n += 1
    guess[n] = 1
    n += 1
    guess[n] = 1
    n += 1
    guess[n] = 1
    n += 1

    # pressure a
#    for index, item in enumerate(heatgrid.pipes()):
#        guess[n] = heatsource.producer(0).supply_pressure
#        n += 1
    guess[n] = 7
    n += 1
    guess[n] = 7
    n += 1
    guess[n] = 1
    n += 1
    guess[n] = 1
    n += 1
    guess[n] = 1
    n += 1
    guess[n] = 7
    n += 1

    for index, item in enumerate(heatsink.consumer()):
        guess[n] = heatsource.producer(0).supply_pressure
        n += 1

    for index, item in enumerate(heatsource.producer()):
        guess[n] = heatsource.producer(0).return_pressure
        n += 1

    # pressure b
#    for index, item in enumerate(heatgrid.pipes()):
#        guess[n] = heatsource.producer(0).supply_pressure
#        n += 1
    guess[n] = 7
    n += 1
    guess[n] = 7
    n += 1
    guess[n] = 1
    n += 1
    guess[n] = 1
    n += 1
    guess[n] = 1
    n += 1
    guess[n] = 7
    n += 1

    for index, item in enumerate(heatsink.consumer()):
        guess[n] = heatsource.producer(0).return_pressure
        n += 1

    for index, item in enumerate(heatsource.producer()):
        guess[n] = heatsource.producer(0).supply_pressure
        n += 1

    # temperature
#    for index, item in enumerate(heatgrid.nodes()):
#        guess[n] = heatsource.producer(0).supply_temperature
#        n += 1
    guess[n] = 130+273.15
    n += 1
    guess[n] = 130+273.15
    n += 1
    guess[n] = 130+273.15
    n += 1
    guess[n] = 130+273.15
    n += 1
    guess[n] = 60+273.15
    n += 1
    guess[n] = 60+273.15
    n += 1
    guess[n] = 60+273.15
    n += 1
    guess[n] = 60+273.15
    n += 1

    # temperature a
#    for index, item in enumerate(heatgrid.pipes()):
#        guess[n] = heatsource.producer(0).supply_temperature
#        n += 1
    guess[n] = 130+273.15
    n += 1
    guess[n] = 130+273.15
    n += 1
    guess[n] = 60+273.15
    n += 1
    guess[n] = 60+273.15
    n += 1
    guess[n] = 60+273.15
    n += 1
    guess[n] = 130+273.15
    n += 1

    for index, item in enumerate(heatsink.consumer()):
        guess[n] = heatsource.producer(0).supply_temperature
        n += 1

    for index, item in enumerate(heatsource.producer()):
        guess[n] = 60+273.15#heatsink.consumer(0).return_temperature
        n += 1

    # temperature b
#    for index, item in enumerate(heatgrid.pipes()):
#        guess[n] = heatsource.producer(0).supply_temperature
#        n += 1
    guess[n] = 130+273.15
    n += 1
    guess[n] = 130+273.15
    n += 1
    guess[n] = 60+273.15
    n += 1
    guess[n] = 60+273.15
    n += 1
    guess[n] = 60+273.15
    n += 1
    guess[n] = 130+273.15
    n += 1

    for index, item in enumerate(heatsink.consumer()):
        guess[n] = item.return_temperature
        n += 1

    for index, item in enumerate(heatsource.producer()):
        guess[n] = heatsource.producer(0).supply_temperature
        n += 1

    # heatflow
    for index, item in enumerate(heatgrid.pipes()):
        guess[n] = -1
        n += 1

    for index, item in enumerate(heatsink.consumer()):
        guess[n] = item.heat_demand
        n += 1

    for index, item in enumerate(heatsource.producer()):
        guess[n] = 225000
        n += 1

    return guess
