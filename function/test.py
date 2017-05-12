def energyBalance_1(I_ab, v_T, v_Tab):
    '''
    energy balance (I_plus * diag(m)*T^b + I_minus * diag(m)*T^a)
    '''
    arr = np.dot(I_ab.T, v_T) + v_Tab
    return arr

# def energyBalance_1(inzidenzmatrix_plus, v_m, v_Tb,
#                    inzidenzmatrix_minus, v_Ta):
#    '''
#    energy balance (I_plus * diag(m)*T^b + I_minus * diag(m)*T^a)
#    '''
#    arr = np.dot(np.dot(inzidenzmatrix_plus, np.diag(v_m)), v_Tb) +\
#        np.dot(np.dot(inzidenzmatrix_minus, np.diag(v_m)), v_Ta)
#    return arr


def energyBalance_2(inzidenzmatrix_minus_T, v_T, v_Ta):
    '''
    energy balance (-1 * I_minus.T * T - T^a)
    '''
    arr = np.dot(np.dot(-1, inzidenzmatrix_minus_T), v_T) - v_Ta
    return arr
	
	    energyBalance_1 = np.dot(Iplus, np.dot(np.diag(arrM), arrTb))\
         + np.dot(Iminus, np.dot(np.diag(arrM), arrTa))