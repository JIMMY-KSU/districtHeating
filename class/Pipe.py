#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 12:43:40 2017

@author: johannes
"""


import math

class Pipe():
    def __init__(self, pipeValues):

        self.ambient_temp = 15  # °C
        self.fluid_temp = 80  # °C
        self.__heat_capacity = 4.183
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
        self.start_node_name = pipeValues['start_node_name']
        self.end_node_name = pipeValues['end_node_name']
        self.length = pipeValues['length'] * 1000  # [mm]
        self.diameter_inner = pipeValues['diameter_inner']
        self.diameter_outer = pipeValues['diameter_outer']
        self.start_height = pipeValues['start_height']
        self.end_height = pipeValues['end_height']
        self.heatTransitionCoefficient = pipeValues['heatTransitionCoefficient']  # [W/m]
        self.roughness = pipeValues['roughness']
        self.SP_RP = pipeValues['SP_RP']

        self.__heat_transferCoefficient_inner = pipeValues['heat_transferCoefficient_inner']
        self.__heat_transferCoefficient_outer = pipeValues['heat_transferCoefficient_outer']
        
#        if self.__heat_transferCoefficient_inner in ('', 0, None):
#            print('yes')

# TODO bring def heat_transferCoefficient in correct form, take care of possibility that pipeValues['heat_transferCoefficient_inner'] etc. is empty or not defined..
# TODO implement @property

        self.__heat_conductivity_1 = pipeValues['heat_conductivity_1']
        self.__heat_conductivity_2 = pipeValues['heat_conductivity_2']
        self.__heat_conductivity_3 = pipeValues['heat_conductivity_3']

        self.__heat_transferCoefficients = [
                                            self.__heat_transferCoefficient_inner,# steel
                                            self.__heat_transferCoefficient_outer # average heat transition in soil ["W/m*K]
                                            ]
        self.__heat_conductivities = [
                                      self.__heat_conductivity_1,
                                      self.__heat_conductivity_2,
                                      self.__heat_conductivity_3
                                      ]

        self.__diameters = [
                            pipeValues['diameter_1'],
                            pipeValues['diameter_2'],
                            pipeValues['diameter_3']
                            ]



        self.__heatflow = 0

    def setHeatflow(self, heatFlow):
        self.__heatflow += heatFlow

    def getHeatflow(self):
        return self.__heatflow


# CALCULATIONS:

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

    def heat_transferCoefficient(self,
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

    def heatloss(self):
        var = 0

        var += 1 / (self.__heat_transferCoefficients[0] * (self.diameter_inner / 2 ))
        print(str(self.__heat_transferCoefficients[0]) + '|' + str(self.diameter_inner) + '| var0= ' +str(var))
        var += 1 / (self.__heat_transferCoefficients[1] * (self.diameter_outer / 2))
        print(str(self.__heat_transferCoefficients[1]) + '|' + str(self.diameter_outer) + '| var1= ' +str(var))
        var += ((1 / self.__heat_conductivities[0]) *
                (math.log((self.__diameters[0] / 2) /
                          (self.diameter_inner / 2))))
        print(str(self.__heat_conductivities[0]) + '|' + str(self.__diameters[0]) + '| var2= ' +str(var))
        var += ((1 / self.__heat_conductivities[1]) *
                (math.log((self.__diameters[1] / 2) /
                 (self.__diameters[1 - 1] / 2))))
        print(str(self.__heat_conductivities[1]) + '|' + str(self.__diameters[1]) + '| var3= ' +str(var))
        var += ((1 / self.__heat_conductivities[2]) *
                (math.log((self.__diameters[2] / 2) /
                 (self.__diameters[2 - 1] / 2))))
        print(str(self.__heat_conductivities[2]) + '|' + str(self.__diameters[2]) + '| var4= ' +str(var))
        heatloss = (
                    (2 * math.pi * self.length *
                     (self.fluid_temp - self.ambient_temp)) /
                    var
                    )
        return heatloss

    def pipe_lambda(self):
        """
        Calculation of lambda
        If the flow is laminar...
        else if the flow is turbulent...
        """

        if self.reynold() < 2300:
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

    def end_volumeStream(self):
#        #volumeStream_end =  # (m^3)/h
#        return volumeStream_end
        pass

    def end_flowspeed(self):
#        #end_flowspeed =  # m/s
#        return flowspeed_end
        pass
    
    
    def volume(self):
#        #volume =  # m^3
#        return volume
        pass
        
        
#    def index(self, i = slice(None,None)):
#        return self.__dataArray['index'][i]
#    def start_x(self, i = slice(None,None)):
#        return self.__dataArray['start_x'][i]
#    def start_y(self, i = slice(None,None)):
#        return self.__dataArray['start_y'][i]
#    def end_x(self, i = slice(None,None)):
#        return self.__dataArray['end_x'][i]
#    def end_y(self, i = slice(None,None)):
#        return self.__dataArray['end_y'][i]
#    def start_point(self, i = slice(None,None)):
#        return self.__dataArray['start_point'][i]
#    def end_point(self, i = slice(None,None)):
#        return self.__dataArray['end_point'][i]
#    def length(self, i = slice(None,None)):
#        return self.__dataArray['length'][i]
#    def inner_diameter(self, i = slice(None,None)):
#        return self.__dataArray['inner_diameter'][i]
#    def outer_diameter(self, i = slice(None,None)):
#        return self.__dataArray['outer_diameter'][i]
#    def start_height(self, i = slice(None,None)):
#        return self.__dataArray['start_height'][i]
#    def end_height(self, i = slice(None,None)):
#        return self.__dataArray['end_height'][i]
#    def heatTransitionCoefficient(self, i = slice(None,None)):
#        return self.__dataArray['heatTransitionCoefficient'][i]
#    def roughness(self, i = slice(None,None)):
#        return self.__dataArray['roughness'][i]
