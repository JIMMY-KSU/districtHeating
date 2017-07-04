# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 11:23:57 2017

@author: jpelda
"""
import numpy as np

def inzidenzmatrix_nodePipe_VL(row, column):
    '''
    column = [int]
    row = [int]
    '''

    for index, nodeNumber in enumerate(row):
            i = 0
            while i < len(column):
                if nodeNumber == column(i).start_node:
                    conMatrix_VL[index][i] = 1
                if nodeNumber == column(i).end_node:
                    conMatrix_VL[index][i] = -1
                i = i + 1
    print(conMatrix_VL)
    conMatrix_VL = np.asarray(conMatrix_VL)
    return print('matrix working')

