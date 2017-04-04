# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 14:11:03 2017

@author: jpelda
"""
import math

cp = 4182


# pipe
def pipe_massflow(m, Ta, Tb, Q, cp=cp):
    res = m * cp * (Tb - Ta) - Q
    return res


def pipe_press(Pa, Pb, m, Ha=0, Hb=0):
    Zeta = 0.02
    rho = 1000
    g = 9.81
    res = (Pa - Pb) * 100000 - Zeta * math.pow(m, 2) + rho * g * (Ha - Hb)
    return res


def pipe_heatflow(Q, Ta, Tb, A=1, k=1, Tamb=273.15 + 10):
    res = (-k*A)*((Tb + Ta)/2 - Tamb) - Q
    return res


# consumer
def consumer_massflow(m, Ta, Tb, Q, cp=cp):
    res = m * cp * (Tb - Ta) - Q
    return res


def consumer_press(Pa, Pb, m):
    zeta = 0
    res = 0  # (Pb - Pa) - zeta * math.pow(m, 2)
    return res


def consumer_temp(Tb_set, Tb):
    res = Tb_set - Tb
    return res


def consumer_heatflow(Q_set, Q):
    res = Q_set - Q
    return res


# producer
def producer_massflow(m, Ta, Tb, Q, cp=cp):
    res = m * cp * (Tb - Ta) - Q
    return res


def producer_press(P_set, P):
    res = P_set - P  # abs(Pb_set - Pb) + abs(Pa_set - Pa)
    return res


def producer_temp(Tb_set, Tb):
    res = Tb_set - Tb
    return res
