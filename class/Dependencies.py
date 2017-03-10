# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 14:11:03 2017

@author: jpelda
"""
import math
import numpy as np
cp = 4.182

class Dependencies():
    def __init__(self):
        pass
    
    def func(self):

        a = 0.5
        R = 1.6
    
        return lambda tau : R - ((1.0 - np.exp(-tau))/(1.0 - np.exp(-a*tau))) 
    
    def dependencies_producer_mass(VMass, VTa, VTb, Qproducer):
        res = VMass * cp * (VTa - VTb) + Qsupply
        return res
    
    
    def dependencies_producer_press(VPress, Pproducer):
        VPress = Psupply
    
        return VPress
    
    
    def dependencies_pipe_mass(VMass, VTa, VTb, kA):
        res = VMass * cp * (VTa - VTb) - kA * ((VTa * VTb) / 2)
        return res
    
    def dependencies_pipe_press(VPa, VPb, VMass, VHa, VHb):
    
        Zeta = 1
        rho = 1
        g = 9.81
        res = (VPa - VPb) - Zeta * math.pow(VMass, 2) + rho * g * (VHa - VHb)
        return res
    
    def dependencies_consumer_mass(VMass, VTa, VTb, Qproducer):
        
        res = VMass * cp * (VTa - VTb) - Qconsumer
        return res
    
    def dependencies_consumer_temp(VTb_set, VTb):
        VTb = VTb_set
        return VTb
    
    def dependencies_consumer_press(VPa, VPb, VMass):
    
        Zeta = 1
        res = (VPa - VPb) - zeta * math.pow(VMass, 2)
        return res