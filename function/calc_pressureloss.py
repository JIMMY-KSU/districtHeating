# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 14:51:37 2017

@author: jpelda

equations were taken from Hydraulik und Pneumatik 978-3-658-07859-1 S.59ff
"""

class Pipe():
    def __init__(self):

        self.kinvis = 0.48724 * 0.000001
        self.dynvis = 0.00046659  # kg / (s * m)
        self.density_air = 1.293  # kg/m³ @ 1013,25 hPa
        self.density_fluid = 971.79  # kg/m³ @ 80 °C
        self.gravity = 9.81  # m / s^2

        self.start_volumeStream = 3600  # m^3 / h
        self.roughness = 1  # mm
        self.start_height = 20  # m
        self.end_height = 21  # m
        """
        Dynamic Viscosity is dependent on water pressure and temperature.
        If pressure = 1 bar and temperature = 333.15 K => 0,00046659
        """


# CALCULATIONS:

    def start_flowspeed(self):
        """
        calculation of flow speed w
        flowspeed = volumeflow / pipe_cross_section_area

        w = VolumeStream [m^3/s] / A [m^2]
        """

        start_flowspeed = ((self.start_volumeStream / 3600) /
                       (math.pi *
                        math.pow(self.diameter_inner / 2, 2)))  # m / s
        return s_flowspeed

    def reynold(self):
        """
        calculation of reynold number

        Re = (w * d) / kinvis
        """
        reynoldnumber = ((self.start_flowspeed() *
                          self.diameter_inner) /
                         self.kinvis)  # dimensionless
        return reynoldnumber


        
        
        
    def pipe_lambda(self):
        """
        Calculation of lambda

        If the flow is laminar...
        else if the flow is turbulent...
        """
        if self.reynold() < 2000:
            """
            calculation of lambda for laminar flow
            """
            p_lambda = 64 / self.reynold()  # dimensionless
            
        elif self.reynold() >= 2000 and self.reynold() <= 3000:
            """
            calculation of lambda for transition area
            """
            p_lambda = ((1.325 / (math.pow(math.log((self.roughness / ((3.7 * self.diameter_inner)) + (5.74 / math.pow(self.reynold(), 0.9)))), 2))) - 64 / self.reynold()) * ((self.reynold() - 2000) / 1000) + (64 / self.reynold())            

        elif self.reynold() > 3000:
            """
            calculation of lambda for turbulent flow
            """
            p_lambda = (1.325 / (math.pow(math.log((self.roughness /
                                           ((3.7 * self.diameter_inner)) +
                                           (5.74 / math.pow(self.reynold(), 0.9))
                                           )), 2)))  # dimensionless

        return p_lambda

    def pressure_loss_friction(self):
        """
        Difference between PressureStart and PressureEnd
        calculated by Darcy-Law
        """
        p_diff = (((self.pipe_lambda() *
                   (self.length / 1000) *
                   math.pow(
                    (self.start_flowspeed() + self.end_flowspeed() / 2), 2) *
                    self.density_fluid) /
                   (2 * self.diameter_inner)) +
                  self.gravity *
                  (self.density_air - self.density_fluid) *
                  (self.start_height - self.end_height))
        return p_diff  # Pa
        
        
    def pressure_loss_installations(self):
        pass
        
        

    def end_pressure(self, start_pressure):
        end_pressure = start_pressure - self.pressure_loss_friction() # - self.pressure_loss_installations()
        return end_pressure  # Pa

    def end_volumeStream(self):
#        #volumeStream_end =  # (m^3)/h
#        return volumeStream_end
        pass

    def end_flowspeed(self):
#        #end_flowspeed =  # m/s
#        return flowspeed_end
        end_flowspeed = self.start_flowspeed()
        return end_flowspeed



    def volume(self):
#        #volume =  # m^3
#        return volume
        pass


if __name__ == "__main__":

    Pipe = Pipe()

#    print("Heatloss: ", Pipe.heatloss())
#    print("Flowspeed: ", Pipe.start_flowspeed())
#    print("Reynold-Number: ", Pipe.reynold())
#    print("Lambda: ", Pipe.pipe_lambda())
#    print("Pressure loss friction: ", Pipe.pressure_loss_friction())
#    print("Pressure End: ", Pipe.end_pressure(400000))
#    print("End temperature: ", Pipe.end_temperature())

else:
    pass
