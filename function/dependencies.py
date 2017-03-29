# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 14:11:03 2017

@author: jpelda
"""
import math

cp = 4182


def producer_massflow(m, Ta, Tb, Q, cp=cp):
    res = m * cp * (Ta - Tb) + Q
    return res


#def producer_heatflow(m, Ta, Tb, cp=cp):
#    res = m * cp * (Ta - Tb) - Q
#    return res


def producer_press(Pb_set, Pb):
    res = Pb_set - Pb
    return res


def producer_temp(Tb_set, Tb):
    res = Tb_set - Tb
    return res


def pipe_massflow(m, Ta, Tb, Q, cp=cp):
    res = m * cp * (Ta - Tb) - Q
    return res


def pipe_heatflow(Q, Ta, Tb, A=1, k=1, Tamb=273.15 + 10):
    res = (k*A)*((Ta + Tb)/2 - Tamb) - Q
    return res


def pipe_press(Pa, Pb, m, Ha=0, Hb=0):
    Zeta = 0
    rho = 1
    g = 9.81
    res = (Pa - Pb) - Zeta * math.pow(m, 2) + rho * g * (Ha - Hb)
    return res


def consumer_mass(m, Ta, Tb, Q, cp=cp):
    res = m * cp * (Ta - Tb) - Q
    return res


def consumer_temp(Tb_set, Tb):
    res = Tb_set - Tb
    return res


def consumer_press(Pa, Pb, m):
    zeta = 0
    res = (Pa - Pb) - zeta * math.pow(m, 2)
    return res


def consumer_heatflow(Q_set, Q):
    res = Q_set - Q
    return res
