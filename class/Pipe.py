#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 12:43:40 2017

@author: johannes
"""


import math


class Pipe():
    def __init__(self, pipeValues):
        self.ambient_temp = 273.15 + 15  # in Kelvin
        self.fluid_temp = 273.15 + 80  # in Kelvin
        self.__heat_capacity = 4183  # J/(kg*K)
        self.__kinvis = 0.48724 * 0.000001
        self.__dynvis = 0.00046659  # kg / (s * m)
        """
        Dynamic Viscosity is dependent on water pressure and temperature.
        If pressure = 1 bar and temperature = 333.15 K => 0,00046659
        """
        self.__density_air = 1.293  # kg/m³ @ 1013,25 hPa
        self.__density_fluid = 971.79  # kg/m³ @ 80 °C

        self.index = pipeValues['index']
        self.start_x = pipeValues['start_x']
        self.start_y = pipeValues['start_y']
        self.end_x = pipeValues['end_x']
        self.end_y = pipeValues['end_y']
        self.sNode = pipeValues['sNode']
        self.eNode = pipeValues['eNode']
        self.seNode = [self.sNode, self.eNode]
        self.length = pipeValues['length']  # [mm]
        self.start_height = pipeValues['start_height']
        self.end_height = pipeValues['end_height']
        self.sprp = pipeValues['sprp']
        self.element = "pipe"
        self.roughness = self.__set_roughness(pipeValues)
        self.__diameter_inner = pipeValues['diameter_inner']
        self.__diameter_middleinner = pipeValues['diameter_middleinner']
        self.__diameter_middleouter = pipeValues['diameter_middleouter']
        self.__diameter_outer = pipeValues['diameter_outer']

        self.__heatflow = 0
        self.__conductivity_inner = pipeValues['conductivity_inner']
        self.__conductivity_middle = pipeValues[
                'conductivity_middle']
        self.__conductivity_outer = pipeValues['conductivity_outer']

        self.__transferCoefficient_inner = pipeValues[
                        'transferCoefficient_inner']
        self.__transferCoefficient_outer = pipeValues[
                        'transferCoefficient_outer']

        self.transitionCoefficient = self.__set_transitionCoefficient(
                pipeValues)


        self.Q = 0  # [Watt]
        self.m = 0  # [kg/s]
        self.Ta = 0  # [K]
        self.Tb = 0  # [K]
        self.Pa = 0  # [Pa]
        self.Pb = 0  # [Pb]


# TODO bring def heat_transferCoefficient in correct form, take care of possibility that pipeValues['heat_transferCoefficient_inner'] etc. is empty or not defined..
# TODO implement @property

    def __set_roughness(self, pipeValues):
        if pipeValues['roughness'] is not '':
            self.roughness = pipeValues['roughness']
            #  k in [mm] from "Druckverluste in Rohrleitungen"
        else:
            self.roughness = 0.0013
        return self.roughness

    def __set_transitionCoefficient(self, pipeValues):
        if 'heatTransitionCoefficient' in pipeValues is not ('' or None):
            self.transitionCoefficient = pipeValues[
                    'heatTransitionCoefficient']  # [W/m]
        else:
            if (self.__transferCoefficient_inner,
                self.__transferCoefficient_outer,
                self.__conductivity_inner, self.__conductivity_middle,
                self.__conductivity_outer,
                self.__diameter_inner, self.__diameter_middleinner,
                self.__diameter_middleouter, self.__diameter_outer) is not (
                        '' or None):
                
                conductivity_inner_coeff = self.__conductivity_inner / (
                        (self.__diameter_middleinner -
                         self.__diameter_inner) /
                         2)
                conductivity_middle_coeff = self.__conductivity_middle / (
                        (self.__diameter_middleouter -
                         self.__diameter_middleinner) /
                         2)
                conductivity_outer_coeff = self.__conductivity_outer / (
                        (self.__diameter_outer -
                         self.__diameter_middleouter) / 
                         2)
                conductivity_sum = conductivity_inner_coeff + \
                                   conductivity_middle_coeff + \
                                   conductivity_outer_coeff

                heatTransferResistance = 1 / self.__transferCoefficient_inner + \
                                         1 / conductivity_sum + \
                                         1 / self.__transferCoefficient_outer
                                         
                val = 1 / heatTransferResistance
            else:
                print('There are missing values'
                      'for heat transfer or conductivity or pipe diameter')
        return val
# CALCULATIONS:


    def transferCoefficient(self,
                                 transferCoefficients,
                                 layer_heat_conductivities,
                                 layer_thicknesses):
        '''
        array of transferCoefficients = alpha [W / m²*K]
        array of heat_conductivities = lamda [W / m*K]
        '''
        h_tC = 0

        for layer_thickness, layer_heat_conductivity in \
                zip(layer_thicknesses, layer_heat_conductivities):
            h_tC += layer_thickness / layer_heat_conductivity
        return h_tC

#    def heatloss(self):
## TODO Berechungen überprüfen
#        var = 0
#
#        var += 1 / (self.__heat_transferCoefficients[0] * (self.diameter_inner / 2 ))
##        print(str(self.__heat_transferCoefficients[0]) + '|' + str(self.diameter_inner) + '| var0= ' +str(var))
#        var += 1 / (self.__heat_transferCoefficients[1] * (self.diameter_outer / 2))
##        print(str(self.__heat_transferCoefficients[1]) + '|' + str(self.diameter_outer) + '| var1= ' +str(var))
#        var += ((1 / self.__heat_conductivities[0]) *
#                (math.log((self.__diameters[0] / 2) /
#                          (self.diameter_inner / 2))))
##        print(str(self.__heat_conductivities[0]) + '|' + str(self.__diameters[0]) + '| var2= ' +str(var))
#        var += ((1 / self.__heat_conductivities[1]) *
#                (math.log((self.__diameters[1] / 2) /
#                 (self.__diameters[1 - 1] / 2))))
##        print(str(self.__heat_conductivities[1]) + '|' + str(self.__diameters[1]) + '| var3= ' +str(var))
#        var += ((1 / self.__heat_conductivities[2]) *
#                (math.log((self.__diameters[2] / 2) /
#                 (self.__diameters[2 - 1] / 2))))
##        print(str(self.__heat_conductivities[2]) + '|' + str(self.__diameters[2]) + '| var4= ' +str(var))
#        heatloss = (
#                    (2 * math.pi * self.length *
#                     (self.fluid_temp - self.ambient_temp)) /
#                    var
#                    )
#        return heatloss

    def start_flowspeed(self):
        """
        calculation of flow speed

        ((m^3)/h) / 3600 = ((m^3)/s)

        w = VolumeStream (in (m^3)/s) / A (in m^2)
        """

        s_flowspeed = ((self.start_volumeStream / 3600) /
                       (3.1415926536 *
                        math.pow(self.diameter_inner / 2, 2)))  # m / s
        return s_flowspeed

    def reynold(self):
        """
        calculation of reynold number

        Re = (w * d) / kinvis
        """
        reynoldnumber = ((self.start_flowspeed() *
                          self.diameter_inner) /
                         self.__kinvis)  # dimensionless
        return reynoldnumber

    def pipe_lambda(self):
        """
        Calculation of lambda
        If the flow is laminar...
        else if the flow is turbulent...
        """

        if self.reynold() < 2320:
            """
            #calculation of lambda for laminar flow
            """
            p_lambda = 64 / self.reynold()  # dimensionless

        elif self.reynold() >= 2300:
            """
            calculation of lambda for turbulent flow
            """
            p_lambda = (
                        1.325 / (
                         math.pow(
                          math.log(
                           (
                            self.roughness / (3.7 * self.diameter_inner) +
                            (5.74 / math.pow(self.reynold(), 0.9))
                           )
                                 ), 2)
                                 )
                        )  # dimensionless

        return p_lambda

    def pressure_difference(self):
        """
        Difference between PressureStart and PressureEnd
        calculated by Darcy-Law
        """
        p_diff = (((self.pipe_lambda() *
                   self.length *
                   math.pow(
                    (self.start_flowspeed() + self.end_flowspeed() / 2), 2) *
                    self.__density_fluid) /
                   (2 * self.diameter_inner)) +
                  self.__gravity *
                  (self.__density_air - self.__density_fluid) *
                  (self.start_height - self.end_height))
        return p_diff  # Pa

    def end_pressure(self, start_pressure):
        end_pressure = start_pressure - self.pressure_difference()
        return end_pressure  # Pa

if __name__=="__main__":
    print('Pipe \t\t\t run directly')
    import os
    from DataIO import DataIO

    dataIO = DataIO(os.path.dirname(os.getcwd()) + os.sep +
                    'input' + os.sep + 'testFiles',
                    os.path.dirname(os.getcwd()) + os.sep +
                    'output' + os.sep + 'testFiles')
    pipe = Pipe(dataIO.importCSV('pipes.csv', header = 0))
    
    
    
else:
    print('Pipe \t\t\t was imported into another module')