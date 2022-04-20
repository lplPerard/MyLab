"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Power Supply Controller.

"""


from PowerSupply import PowerSupply
from tkinter.constants import END
import pyvisa

class PowerSupplyController():
    """Class containing the PowerSupplyController for MyLab.

    """

    def __init__(self, view=None, term=None, instrument=None):
    #Constructor for the Controller class   

        self.view = view  
        self.term = term

        self.instrument = PowerSupply()
        if instrument != None:
            self.instrument = instrument

        self.resourceManager = pyvisa.ResourceManager()

    def updateView(self, view):
    #Setter method for view attribute
        self.view = view

    def connectToDevice(self):
    #This method establish connection with device using instrument address   
        pass

    def setVoltageSource(self, args=[]):
    #This method modify the voltage source 
        pass

    def setCurrentLimit(self, args=[]):
        pass
            
    def setChannelState(self, args=[]):
    #This method modify the output state 
        pass
            
    def setMasterState(self, args=[]):
    #This method modify the output state 
        pass
             
    def Measure(self, args=[]):
    #This method update the content of the view with content from device   
        pass
        
    def MeasureVoltage(self, args=[]):
    #This method update the content of the view with content from device   
        pass
        
    def MeasureCurrent(self, args=[]):
    #This method update the content of the view with content from device   
        pass
        
    def MeasurePower(self, args=[]):
    #This method update the content of the view with content from device   
        pass