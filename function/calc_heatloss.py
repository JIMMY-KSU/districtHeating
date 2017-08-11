# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 14:06:27 2017

@author: jpelda


equations were taken from technische Thermodynamik 9783446415614 Seite 363
"""

import math

class Pipe():
    def __init__(self):
        self.transferCoefficient_inner = 46.5  # [W/mK] fluid pipe
        self.transferCoefficient_outer = 1  # [W/mK] pipe ground
        self.conductivity_0 = 59  # [W/mK] pipe material
        self.conductivity_1 = 0.037  # [W/mK] isolation material
        self.conductivity_2 = 238  # [W/mK] pipe coat

        self.length = 40  # m
        self.diameter_0 = 0.05  # [m] inner diameter
        self.diameter_1 = 0.052  # [m]
        self.diameter_2 = 0.082  # [m]
        self.diameter_3 = 0.083  # [m] outer diameter

        self.ambient_temp = 35  # °C
        self.start_fluid_temp = 220  # °C

        self.resistivity = self.calc_resistivity()
        self.Q = self.calc_Q()
        """
        Dynamic Viscosity is dependent on water pressure and temperature.
        If pressure = 1 bar and temperature = 333.15 K => 0,00046659
        """


# CALCULATIONS:

    def calc_resistivity(self):
        '''
        returns thermal resistivity
        '''
        thRes = (1 / (2 * math.pi * self.length)) * (
                (1 / self.conductivity_0) * math.log(self.diameter_1 /
                                                     self.diameter_0) +
                (1 / self.conductivity_1) * math.log(self.diameter_2 /
                                                     self.diameter_1) +
                (1 / self.conductivity_2) * math.log(self.diameter_3 /
                                                     self.diameter_2))
        return thRes

    def calc_Q(self):

        thLoss = (1 / self.resistivity) * (self.start_fluid_temp -
                                           self.ambient_temp)
        return thLoss

    def end_temperature(self):
        """

        """
        end_temperature = self.start_fluid_temp - (self.heatloss() / (self.start_volumeStream * self.heat_capacity * self.density_fluid))
        return end_temperature


if __name__ == "__main__":

    Pipe = Pipe()
    print(Pipe.resistivity)
    print(Pipe.Q)

    # TODO check for consistency value should be 2300 W



else:
    pass
