# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 14:11:03 2017
@author: jpelda
"""

cp = 4182  # J/(kg*K)


# pipe
def pipe_massflow(m, Ta, Tb, Q, cp=cp):
    res = m * cp * (Tb - Ta) - Q
    return res


def pipe_heatflow(Q, Ta, Tb, A=1, k=1, Tamb=273.15 + 10):
#    print('pipe_heatflow %s %s %s' %(type(Q), type(Ta), type(Tb)))
    res = (k * A) * (Tamb -(Ta + Tb) / 2) - Q
    return res


def pipe_press(Pa, Pb, m, Ha=0, Hb=0):
    Zeta = 0.2
    rho = 1000
    g = 9.81
#    print('pipe_press %s %s %s' %(type(Pa), type(Pb), type(m)))
    res = (Pa - Pb) * 100000 - Zeta * m * abs(m) + rho * g * (Ha - Hb)
    return res


# consumer
def consumer_massflow(m, Ta, Tb, Q, cp=cp):
#    print('consumer_massflow %s %s %s %s' %(type(m), type(Ta), type(Tb), type(Q)))
    res = m * cp * (Tb - Ta) - Q
    return res


def consumer_heatflow(Q_set, Q):
#    print('consumer_heatflow %s %s' %(type(Q_set), type(Q)))
    res = Q_set - Q
    return res


def consumer_temp(Tb_set, Tb):
#    print('consumer_temp %s %s' %(type(Tb_set), type(Tb)))
    res = Tb_set - Tb
    return res


def consumer_press(Pa, Pb, m):
    zeta = 0
    res = 0  # (Pa - Pb) - zeta * m * abs(m)
    return res


# producer
def producer_massflow(m, Ta, Tb, Q, cp=cp):
#    print("producer_massflow %s %s %s %s" %(type(m), type(Ta), type(Tb), type(Q)))
    res = m * cp * (Tb - Ta) - Q
    return res


def producer_temp(Tb_set, Tb):
#    print("producer_temp %s %s" %(type(Tb_set), type(Tb)))
    res = Tb_set - Tb
    return res


def producer_press(P_set, Pb):
#    print("producer_press %s %s" %(type(P_set), type(Pb)))
    res = P_set - Pb
    return res
