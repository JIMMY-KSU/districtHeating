#pressure loss in a standard pipe


    #INPUT:

    #IMPORT FILES:
        
from Pipe_Library import Pipe_Library
        



    #IMPORT DATA:
    
class Pipe():
    def __init__(self, pipe_name, volumeStream_start, density):
        self.__length = Pipe_Library.configuration(self, pipe_name, 'pipe_length')
        self.__diameter = Pipe_Library.configuration(self, pipe_name, 'pipe_diameter')
        self.__volumeStream_start = volumeStream_start # (m^3)/h
        self.__density = density # kg/(m^3)
        self.__dynvis = 0.00046659 # kg / (s * m)
        """
        Dynamic Viscosity is dependent on water pressure and temperature.
        
        If pressure = 1 bar and temperature = 333.15 K => 0,00046659
        """


        
        
    #OUTPUT:    

    def difference(self):
        """
        Difference between PressureStart and PressureEnd
        
        calculated by Darcy-Law
        """
        #difference =  # Pa
        difference = self.calc_pipe_lambda() * (self.__length / self.__diameter) * (self.__density / 2) * self.calc_flowspeed_start() * self.calc_flowspeed_start()
        return difference
    
        
    def pressure_end(self, pressure_start):
        '''
        pressure_end =  double [Pa]
        '''
        #pressure_end =  # Pa
        pressure_end = pressure_start - self.difference()
        return pressure_end
        
            
    def volumeStream_end(self):
#        #volumeStream_end =  # (m^3)/h
#        return volumeStream_end
        pass
        
        
    def flowspeed_end(self):
#        #flowspeed_end =  # m/s
#        return flowspeed_end
        pass
    
    
    def volume(self):
#        #volume =  # m^3
#        return volume
        pass
    





        
    #CALCULATIONS AND DEFINITIONS:
       
    def calc_flowspeed_start(self):
        """
        calculation of flow speed
        
        ((m^3)/h) / 3600 = ((m^3)/s)

        w = VolumeStream (in (m^3)/s) / A
        """

        flowspeed_start = (self.__volumeStream_start / 3600) / (3.1415926536 * (self.__diameter / 2) * (self.__diameter / 2)) # m / s
        return flowspeed_start



    def calc_kinematicviscosity(self):
        """
        calculation of kinematic viscosity
        
        kinvis = dynvis / density
        """
        
        kinvis = self.__dynvis / self.__density # (m^2) / s
        return kinvis
    


    def calc_reynold(self):
        """
        calculation of reynold number
        
        Re = (w * d) / kinvis
        """
        reynoldnumber = (self.calc_flowspeed_start() * self.__diameter) / self.calc_kinematicviscosity() #dimensionless
        return reynoldnumber

        

    def calc_pipe_lambda(self):
        """
        calculation of lambda for laminar flow
        
        The calculation of lambda for tubulent flow is different!
        """
        pipe_lambda = 64 / self.calc_reynold() #dimensionless
        return pipe_lambda