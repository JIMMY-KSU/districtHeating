# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 14:11:03 2017

@author: jpelda
"""
import math
cp = 4.182
Tamb = 5+273.15


class Dependencies():
    def __init__(self):
        pass

    def producer_Q(m, Ta, Tb, cp=4100):
        Q = m * cp * (Ta - Tb)
        return Q

    def pipe_Q(Ta, Tb, A=1, k=1):
        Q = (k * A) * ((Ta + Tb)/2 - Tamb)
        return Q

    def dependencies_producer_massflow(m, Ta, Tb, Q, cp=4100):
        res = m * cp * (Ta - Tb) + Q
        return res

    def dependencies_producer_temp(Tb_set, Tb):
        res = Tb_set - Tb
        return res

    def dependencies_producer_press(Pb_set, Pb):
        res = Pb_set - Pb
        return res

    def dependencies_pipe_massflow(m, Ta, Tb, Q, kA=1, cp=4100):
        res = m * cp * (Ta - Tb) - Q
        return res

    def dependencies_pipe_press(Pa, Pb, m, Ha=0, Hb=0):
        Zeta = 0
        rho = 1
        g = 9.81
        res = (Pa - Pb) - Zeta * math.pow(m, 2) + rho * g * (Ha - Hb)
        return res

    def dependencies_pipe_Q(Q, Ta, Tb, A=1, k=1):
        res = (k * A) * ((Ta + Tb)/2 - Tamb) - Q
        return res

    def dependencies_consumer_massflow(m, Ta, Tb, Q, cp=4100):
        res = m * cp * (Ta - Tb) - Q
        return res

    def dependencies_consumer_temp(Tb_set, Tb):
        res = Tb_set - Tb
        return res

    def dependencies_consumer_press(Pa, Pb, m):
        zeta = 0
        res = (Pa - Pb) - zeta * math.pow(m, 2)
        return res

    def dependencies_consumer_Q(Q_set, Q):
        res = Q_set - Q
        return res
