"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Power Supply Controller.

"""


from WaveformGenerator import WaveformGenerator
from tkinter.constants import END
from Instrument import Instrument
import pyvisa

class WaveformGeneratorController():
    """Class containing the WaveformGeneratorController for MyLab.

    """

    def __init__(self, view=None, term=None):
    #Constructor for the Controller class   

        self.view = view  
        self.term = term

        self.instrument = WaveformGenerator()
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
                return(-1)
            try:
                self.instrument.ressource.write('*RST')
                self.instrument.ressource.write('*CLS')
                self.instrument.ressource.close()
            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                return(-1)

        else:
            self.view.view.sendError('004')

    def setMasterState(self):
    #This method modify the output state 
        if (self.instrument.state == "free") or (self.instrument.state == "unreachable"):
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "connected"
            except:
                self.view.view.sendError('001')
                self.instrument.state = "unreachable"
                return(-1)
        
            try:            
                if self.instrument.masterState == 0:
                    self.instrument.ressource.write('OUTP:MAST ON')
                    self.instrument.ressource.close()
                    self.instrument.masterState = 1
                else:
                    self.instrument.ressource.write('OUTP:MAST OFF')
                    self.instrument.ressource.close()                    
                    self.instrument.masterState = 0
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                return(-1)

        else:
            self.view.view.sendError('004')
        
