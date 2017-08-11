#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 12:43:40 2017

@author: johannes
"""


import math
import numpy as np
from Dictionary import STANET_pipes_allocation as dictionary

class Pipe():
    def __init__(self, index, pipeValues):
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

        self.index = index
        self.start_x = pipeValues['start_x']
        self.start_y = pipeValues['start_y']
        self.end_x = pipeValues['end_x']
        self.end_y = pipeValues['end_y']
        self.sNode = pipeValues['sNode']
        self.eNode = pipeValues['eNode']
        self.esNode = [self.eNode, self.sNode]
        self.length = float(pipeValues['length'])  # [mm]
        self.start_height = float(pipeValues['start_height'])
        self.end_height = float(pipeValues['end_height'])
        self.sprp = float(pipeValues['sprp'])
        self.element = "pipe"
        self.roughness = float(self.__set_roughness(pipeValues))
        self.diameter_inner = float(pipeValues['diameter_0'])
        self.diameter_middleinner = float(pipeValues['diameter_1'])
        self.diameter_middleouter = float(pipeValues['diameter_2'])
        self.diameter_outer = float(pipeValues['diameter_3'])

        self.heatflow = float(0)
        self.m_max_set = float(pipeValues['m_max'])
        
        self.conductivity_inner = float(pipeValues['conductivity_0'])
        self.conductivity_middle = float(pipeValues['conductivity_1'])
        self.conductivity_outer = float(pipeValues['conductivity_2'])

        self.transferCoefficient_inner =\
                    float(pipeValues['transferCoefficient_0'])
        self.transferCoefficient_outer =\
                    float(pipeValues['transferCoefficient_1'])

        self.transitionCoefficient =\
                    self.__set_transitionCoefficient(pipeValues)


        self.Q = float(0)  # [Watt]
        self.m = float(0)   # [kg/s]
        self.Ta = float(0)   # [K]
        self.Tb = float(0)   # [K]
        self.Pa = float(0)  # [Pa]
        self.Pb = float(0)  # [Pb]

# TODO bring def heat_transferCoefficient in correct form, take care of possibility that pipeValues['heat_transferCoefficient_inner'] etc. is empty or not defined..
# TODO implement @property

    def __set_roughness(self, pipeValues):
        if pipeValues['roughness'] is not '':
            roughness = pipeValues['roughness']
            #  k in [mm] from "Druckverluste in Rohrleitungen"
        else:
            roughness = 0.0013
        return roughness

    def __set_transitionCoefficient(self, pipeValues):
        self.transitionCoefficient = 0,23  # [W/m]
        # TODO input Parameter missing. Commented should probably work.
#        if 'heatTransitionCoefficient' in pipeValues is not ('' or 0):
#            self.transitionCoefficient = pipeValues[
#                    'heatTransitionCoefficient']  # [W/m]
#        else:
#            if (self.transferCoefficient_inner,
#                self.transferCoefficient_outer,
#                self.conductivity_inner, self.conductivity_middle,
#                self.conductivity_outer,
#                self.diameter_inner, self.diameter_middleinner,
#                self.diameter_middleouter, self.diameter_outer) is not (
#                        '' or 0):
#                
#                conductivity_inner_coeff = self.conductivity_inner / (
#                        (self.diameter_middleinner -
#                         self.diameter_inner) /
#                         2)
#                conductivity_middle_coeff = self.conductivity_middle / (
#                        (self.diameter_middleouter -
#                         self.diameter_middleinner) /
#                         2)
#                conductivity_outer_coeff = self.conductivity_outer / (
#                        (self.diameter_outer -
#                         self.diameter_middleouter) / 
#                         2)
#                conductivity_sum = conductivity_inner_coeff + \
#                                   conductivity_middle_coeff + \
#                                   conductivity_outer_coeff
#
#                heatTransferResistance = 1 / self.transferCoefficient_inner + \
#                                         1 / conductivity_sum + \
#                                         1 / self.transferCoefficient_outer
#                                         
#                val = 1 / heatTransferResistance
#         else:
#                print('There are missing values'
#                      'for heat transfer or conductivity or pipe diameter')
#        return val
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

    def __str__(self):
        attr = self.__dict__
        attr = {item: attr[item] for item in attr if item not in
                ("pipeValues",
                 "__str__")}
        print(attr)

if __name__=="__main__":
    print('Pipe \t\t\t run directly')
    import os
    from DataIO import DataIO

    dataIO = DataIO(os.path.dirname(os.getcwd()) + os.sep +
                    'input' + os.sep + 'testFiles',
                    os.path.dirname(os.getcwd()) + os.sep +
                    'output' + os.sep + 'testFiles')

    df = dataIO.importCSV('pipes.csv', header = 0)

    pipe = Pipe(0, df)
    pipe.__str__()


else:
    print('Pipe \t\t\t was imported into another module')