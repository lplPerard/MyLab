"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Power Supply Controller.

"""


from PowerSupply import PowerSupply
from tkinter.constants import END
import pyvisa
import time

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
        if (self.instrument.state == "free") or (self.instrument.state == "unreachable"):
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "connected"

            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('001')
                    self.instrument.state = "unreachable"
                self.instrument.ressource = None
                return("ERROR")

            try:
                self.instrument.ressource.write('*RST')
                self.instrument.ressource.write('*CLS')

            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return("ERROR")

        else:
            self.view.view.sendError('004')

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



