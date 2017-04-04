# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 14:11:03 2017

@author: jpelda
"""
import math
import numpy as np
cp = 4.182
Tamb = 5+273.15


def consumer_massflow(v_massflow, v_Ta, v_Tb, v_Q, cp=4100):
    res = np.multiply(v_massflow, cp) * (v_Ta - v_Tb) - v_Q
    return res


def consumer_press(v_Pa, v_Pb, v_massflow):
    zeta = 0
    res = (v_Pa - v_Pb) - np.multiply(zeta, math.pow(v_massflow, 2))
    return res


def consumer_Q(v_Q_set, v_Q):
    res = v_Q_set - v_Q
    return res


def consumer_temp(v_Tb_set, v_Tb):
    res = v_Tb_set - v_Tb
    return res


def pipe_massflow(v_massflow, v_Ta, v_Tb, v_Q, cp=4100):
    res = np.multiply(v_massflow, cp) * (v_Ta - v_Tb) - v_Q
    return res


def pipe_press(v_Pa, v_Pb, v_massflow, v_Ha=0, v_Hb=0):
    Zeta = 0
    rho = 1
    g = 9.81
    res = (v_Pa - v_Pb) - np.multiply(Zeta, np.power(v_massflow, 2)) +\
        np.multiply(rho, np.multiply(g, v_Ha - v_Hb))
    return res


def pipe_Q(v_Q, v_Ta, v_Tb, A=1, k=0.0685):
    res = np.multiply(k * A, (v_Ta + v_Tb)/2 - Tamb) - v_Q
    return res


def producer_massflow(v_massflow, v_Ta, v_Tb, v_Q, cp=4100):
    res = np.multiply(v_massflow, cp) * (v_Ta - v_Tb) + v_Q
    return res


def producer_press(v_Pb_set, v_Pb):
    res = v_Pb_set - v_Pb
    return res


def producer_Q(v_massflow, v_Ta, v_Tb, cp=4100):
    res = np.dot(v_massflow, np.multiply(cp,(v_Ta - v_Tb)))
    return res


def producer_temp(v_Tb_set, v_Tb):
    res = v_Tb_set - v_Tb
    return res





