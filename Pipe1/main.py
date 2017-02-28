# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#from Pipe import Pipe
#
#
#P_1 = Pipe("Pipename")
#P_2 = Pipe("Pipename")
#
#
#
##for i < len(EX.Sportmarketprice()):
##    Costs = P.EnergyConsumption(i) * EX.Sportmarketprice(i) 
##    
##    i = i + 1
#
#
#print("Enddruck: " + str(P_1.druckverlust())




#from test import test

#example = test("hello")

#print(str(example.sum()))




from Pipe import Pipe


Pipe1 = Pipe('Type1', 3, 1000)
print("Flowspeed: ", Pipe1.calc_flowspeed_start())
print("Lambda: ", Pipe1.calc_pipe_lambda())
print("Reynold: ", Pipe1.calc_reynold())
print("Pressure Difference: ", Pipe1.difference())
print("Pressure End: ", Pipe1.pressure_end(4000000))