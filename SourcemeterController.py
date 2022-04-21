"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Multimeter Controller.

"""


from Sourcemeter import Sourcemeter
from tkinter.constants import END
import pyvisa
import time

class SourcemeterController():
    """Class containing the Multimeter Controller for MyLab.

    """

    def __init__(self, view=None, term=None, instrument=None, model=None):
    #Constructor for the Controller class   

        self.view = view  
        self.term = term
        self.model = model

        self.instrument = Sourcemeter()
        if instrument != None:
            self.instrument = instrument

        self.resourceManager = pyvisa.ResourceManager()

    def updateView(self, view):
    #Setter method for view attribute
        self.view = view

    def connectToDevice(self):
    #This method establish connection with device using instrument address
        pass

    def closeConnection(self):    
    #This method close the connection to device   
        pass

    def setVoltageSource(self, args=[]):
    #This method set to DCV
        pass

    def setCurrentSource(self, args=[]):
    #This method set to DCV
        pass

    def measureCurrent(self, args=[]):
    #This method measure the current 
        pass

    def measureVoltage(self, args=[]):
    #This method measure the current 
        pass

    def setMasterState(self, args=[]):
    #This method modify the output state
        pass


