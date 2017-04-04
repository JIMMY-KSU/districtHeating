# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 09:14:00 2017

@author: jpelda
"""

import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import root
import math
import dependencies as dp

Tamb = 5+273.15

class Solver():
    def __init__(self):
        pass
    
    def gridCalculation_thermical(x, args):
    
        i = 0
        arrM = [0] * args['massflow']  # length of entities of pipes
        arrP = [0] * args['pressure']  # length of entities of nodes
        arrPa = [0] * args['Pa']  # length of entities of pipes
        arrPb = [0] * args['Pb']  # length of entities of pipes
        arrT = [0] * args['T']  # length of entities of nodes
        arrTa = [0] * args['Ta']  # length of entities of pipes
        arrTb = [0] * args['Tb']  # length of entities of pipes
        arrQ = [0] * args['heatflow']  # length of entities of nodes

        i = 0
        arrM = x[i: i + len(arrM)]
        i = i + len(arrM)
        arrP = x[i: i + len(arrP)]
        i = i + len(arrP)
        arrPa = x[i: i + len(arrPa)]
        i = i + len(arrPa)
        arrPb = x[i: i + len(arrPb)]
        i = i + len(arrPb)
        arrT = x[i: i + len(arrT)]
        i = i + len(arrT)
        arrTa = x[i: i + len(arrTa)]
        i = i + len(arrTa)
        arrTb = x[i: i + len(arrTb)]
        i = i + len(arrTb)
        arrQ = x[i: i + len(arrQ)]

        F = np.zeros(32)

        # mass balance M/M
        F[0] = arrM[0] - arrM[1]
        F[1] = arrM[1] - arrM[2]
        F[2] = arrM[2] - arrM[3]
    #    F[3] = -arrM[0] + arrM[3]
        # energy balance T/Ta
        F[4] = arrT[3] - arrTa[0]
        F[5] = arrT[0] - arrTa[1]
        F[6] = arrT[1] - arrTa[2]
        F[7] = arrT[2] - arrTa[3]
        # impulse balance P/Pb
        F[8] = arrP[0] - arrPb[0]
        F[9] = arrP[1] - arrPb[1]
        F[10] = arrP[2] - arrPb[2]
        F[11] = arrP[3] - arrPb[3]
        # impulse balance P/Pa
        F[12] = arrP[3] - arrPa[0]
        F[13] = arrP[0] - arrPa[1]
        F[14] = arrP[1] - arrPa[2]
        F[15] = arrP[2] - arrPa[3]
        # temperature balance TbM/TaM
        F[16] = arrTb[0]*arrM[0] - arrTa[1]*arrM[1]
        F[17] = arrTb[1]*arrM[1] - arrTa[2]*arrM[2]
        F[18] = arrTb[2]*arrM[2] - arrTa[3]*arrM[3]
        F[19] = arrTb[3]*arrM[3] - arrTa[0]*arrM[0]
    
        F[20] = dp.producer_massflow(arrM[0], arrTa[0], arrTb[0], arrQ[0])
        F[21] = dp.pipe_press(arrPa[1], arrPb[1], arrM[1])
        F[22] = dp.pipe_press(arrPa[3], arrPb[3], arrM[3])
        F[23] = dp.consumer_temp(30+273.15, arrTb[2])
    
        F[24] = dp.consumer_mass(arrM[2], arrTa[2], arrTb[2], arrQ[2])
        F[25] = dp.consumer_press(arrPa[2], arrPb[2], arrM[2])
        F[26] = dp.pipe_heatflow(arrQ[1], arrTa[1], arrTb[1], Tamb=273.15 + 10)
        F[27] = dp.pipe_heatflow(arrQ[3], arrTa[3], arrTb[3], Tamb=273.15 + 10)
        F[28] = dp.pipe_massflow(arrM[1], arrTa[1], arrTb[1], arrQ[1])
        F[29] = dp.pipe_massflow(arrM[3], arrTa[3], arrTb[3], arrQ[3])
        F[30] = dp.producer_press(7, arrPb[0])
        F[31] = dp.producer_temp(80+273.15, arrTb[0])
        F[3] = dp.consumer_heatflow(args['initialValues_heatflow'][1], arrQ[2])
    
    #    F[32] = arrQ[0] - arrQ[1]
    #    F[33] = arrQ[1] - arrQ[2]
    #    F[34] = arrQ[2] - arrQ[3]
    #    F[35] = -arrQ[0] + arrQ[3]
    
        return F
    
if __name__=="__main__":
    print('DistrictHeatingSystem run directly')
    args = {}
    args['massflow'] = 4  # length of elements
    args['pressure'] = 4  # length of nodes
    args['Pa'] = 4  # length of elements
    args['Pb'] = 4  # lengtha of elements
    args['T'] = 4  # length of nodes
    args['Ta'] = 4  # length of elements
    args['Tb'] = 4  # length of elements
    args['heatflow'] = 4  # length of elements
    args['initialValues_heatflow'] = [12000, 23000]
    
    xGuess = np.array((57, 57, 57, 57,  # massflow
                       7, 7, 7, 7,  # pressure
                       7, 7, 7, 7,  # Pa
                       7, 7, 7, 7,  # Pb
                       80+273.15, 80+273.15, 15+273.15, 15+273.15,  # T
                       15+273.15, 80+273.15, 80+273.15, 15+273.15,  # Ta
                       80+273.15, 80+273.15, 15+273.15, 15+273.15,  # Tb
                       12000, 0, -12000, 0  # heatflow
                       ))
    
    initialValues_heatflow = 12000
    solution = fsolve(gridCalculation_thermical, xGuess, args)
    
    massflow = 'Massflow: \t'
    pressure = 'Pressure P: \t'
    pressureA = 'Pressure Pa: \t'
    pressureB = 'Pressure Pb: \t'
    temperature = 'Temperature T: \t'
    temperatureA = 'Temperature Ta: '
    temperatureB = 'Temperature Tb: '
    heatflow = 'Heatflow Q: \t'
    arrayNames = [massflow, pressure, pressureA,
                  pressureB, temperature, temperatureA,
                  temperatureB, heatflow]
    
    i = -1
    j = 1
    for index, item in enumerate(solution):
        j = j + 1
        if index % 4 == 0:
            i = i + 1
            j = 1
        print(str(arrayNames[i]) + str(j) + '  |  ' + str(item))
    
    print('numbers of unknown variables: ' + str(len(solution)))
    print('numbers of equations: ' + str(len(gridCalculation_thermical(xGuess, args))))

else:
    print('DistrictHeatingSystem was imported into another module')
    args = {}
    args['massflow'] = 4  # length of elements
    args['pressure'] = 4  # length of nodes
    args['Pa'] = 4  # length of elements
    args['Pb'] = 4  # lengtha of elements
    args['T'] = 4  # length of nodes
    args['Ta'] = 4  # length of elements
    args['Tb'] = 4  # length of elements
    args['heatflow'] = 4  # length of elements
    args['initialValues_heatflow'] = [12000, 23000]
    
    xGuess = np.array((57, 57, 57, 57,  # massflow
                       7, 7, 7, 7,  # pressure
                       7, 7, 7, 7,  # Pa
                       7, 7, 7, 7,  # Pb
                       80+273.15, 80+273.15, 15+273.15, 15+273.15,  # T
                       15+273.15, 80+273.15, 80+273.15, 15+273.15,  # Ta
                       80+273.15, 80+273.15, 15+273.15, 15+273.15,  # Tb
                       12000, 0, -12000, 0  # heatflow
                       ))
    
    initialValues_heatflow = 12000
    solution = fsolve(Solver.gridCalculation_thermical, xGuess, args)
    massflow = 'Massflow: \t'
    pressure = 'Pressure P: \t'
    pressureA = 'Pressure Pa: \t'
    pressureB = 'Pressure Pb: \t'
    temperature = 'Temperature T: \t'
    temperatureA = 'Temperature Ta: '
    temperatureB = 'Temperature Tb: '
    heatflow = 'Heatflow Q: \t'
    arrayNames = [massflow, pressure, pressureA,
                  pressureB, temperature, temperatureA,
                  temperatureB, heatflow]
    
    i = -1
    j = 1
    for index, item in enumerate(solution):
        j = j + 1
        if index % 4 == 0:
            i = i + 1
            j = 1
        print(str(arrayNames[i]) + str(j) + '  |  ' + str(item))
    
    print('numbers of unknown variables: ' + str(len(solution)))
    print('numbers of equations: ' + str(len(Solver.gridCalculation_thermical(xGuess, args))))

