# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 21:37:03 2017

@author: jpelda
"""
import numpy as np


def massBalance(inzidenzmatrix, v_massflow):
    '''
    input:
    --------
    inzidenzmatrix = arr
    v_massflow = arr

    return:
    --------
    mass balance (I * m) with length of v_massflow -1
    '''
    arr = np.dot(inzidenzmatrix, v_massflow)
    return arr


def energyBalance_1(inzidenzmatrix_plus, v_massflow, v_Tb,
                    inzidenzmatrix_minus, v_Ta):
    '''
    energy balance (I_plus * diag(m)*T^b + I_minus * diag(m)*T^a)
    '''
    arr = np.dot(inzidenzmatrix_plus, np.dot(np.diag(v_massflow), v_Tb)) +\
        np.dot(inzidenzmatrix_minus, np.dot(np.diag(v_massflow), v_Ta))
    return arr


def energyBalance_2(inzidenzmatrix_minus_T, v_T, v_Ta):
    '''
    energy balance (-1 * I_minus.T * T - T^a)
    '''
    arr = np.dot(np.multiply(-1, inzidenzmatrix_minus_T), v_T) - v_Ta
    return arr

def impulseBalance_1(inzidenzmatrix_minus_T, v_P, v_Pa):
    '''
    impulse balance (-1*I_minus.T*P - P^a)
    '''
    arr = np.dot(np.multiply(-1, inzidenzmatrix_minus_T), v_P) - v_Pa
    return arr


def impulseBalance_2(inzidenzmatrix_plus_T, v_P, v_Pb):
    '''
    impulse balance I_plus.T*P - P^b
    '''
    arr = np.dot(inzidenzmatrix_plus_T, v_P) - v_Pb
    return arr
