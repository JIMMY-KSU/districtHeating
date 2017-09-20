# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 15:46:53 2017

@author: jpelda
"""

import numpy as np

I = np.asarray([
     [-1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
     [ 1,-1, 0, 0, 0, 0,-1, 0, 0, 0],
     [ 0, 1,-1, 0, 0, 0, 0,-1, 0, 0],
     [ 0, 0, 1, 0, 0, 0, 0, 0,-1, 0],
     [ 0, 0, 0, 0, 0,-1, 0, 0, 1, 0],
     [ 0, 0, 0, 0,-1, 1, 0, 1, 0, 0],
     [ 0, 0, 0,-1, 1, 0, 1, 0, 0, 0],
     [ 0, 0, 0, 1, 0, 0, 0, 0, 0,-1]])
m_consumer = np.asarray([40,60,80])
m_powerPlant = np.sum(m_consumer)
m = np.asarray([0,0,0,40,60,80,0,0,0,m_powerPlant])

#I_pipes = np.concatenate((I[4], I[5]), axis=0)
I_pipes = np.vstack((I[0][:6], I[1][:6], I[2][:6],
                     I[3][:6], I[4][:6], I[5][:6],
                     I[6][:6], I[7][:6]))
print(I_pipes)


m_guess = np.sum(I_pipes*m ,axis=1)
#I[:] = 0
I_pseudo = np.linalg.pinv(I)
#print(I_pseudo)
m = np.dot(I_pseudo, m_guess)
#np.linalg.solve()

#sol = np.linalg.solve(I_pseudo, m)
#print(sol)
#print(m)
#v_m = np.zeros(self._elements)
# # massflow
#iMatrix = self.__I
#v_m_guess = np.sum(-iMatrix[:,(self.__I_sink_slice)] *
#      self.heatsink.v_consumers_m, axis=1)
#print(v_m_guess)
#iMatrix[:, self.__I_sink_slice] = 0
#iMatrix_pseudo = np.linalg.pinv(iMatrix)
#
#v_m = np.dot(iMatrix_pseudo, v_m_guess)
