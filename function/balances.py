# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 21:37:03 2017

@author: jpelda
"""
import numpy as np


def massBalance(inzidenzmatrix, v_m):
    '''
    input:
    --------
    inzidenzmatrix = arr
    v_massflow = arr

    return:
    --------
    mass balance (I * m) with length of v_massflow -1
    '''
    arr = np.dot(inzidenzmatrix, v_m)
    return arr


def energyBalance_1(I_plus, v_m, v_Tb,
                    I_minus, v_Ta):
    '''
    energy balance (I_plus * diag(m)*T^b + I_minus * diag(m)*T^a)
    '''
    arr = np.dot(I_plus, np.dot(np.diag(v_m), v_Tb))\
         + np.dot(I_minus, np.dot(np.diag(v_m), v_Ta))
    return arr


# def energyBalance_2(I_ab, v_T, v_Tab):
    # '''
    # energy balance (I_ab.T * v_T + v_Tab)
    # '''
    # arr = np.dot(I_ab.T, v_T) + v_Tab
    # return arr


def energyBalance_2(inzidenzmatrix_minus_T, v_T, v_Ta):
   '''
   energy balance (-1 * I_minus.T * T - T^a)
   '''
   arr = np.dot(np.dot(-1, inzidenzmatrix_minus_T), v_T) - v_Ta
   return arr


def impulseBalance_1(inzidenzmatrix_minus_T, v_P, v_Pa):
    '''
    impulse balance (-1*I_minus.T*P - P^a)
    '''
    arr = np.dot(np.dot(-1, inzidenzmatrix_minus_T), v_P) - v_Pa
    return arr


def impulseBalance_2(inzidenzmatrix_plus_T, v_P, v_Pb):
    '''
    impulse balance I_plus.T*P - P^b
    '''
    arr = np.dot(inzidenzmatrix_plus_T, v_P) - v_Pb
    return arr
