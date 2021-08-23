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
        if (self.instrument.state == "free") or (self.instrument.state == "unreachable"):
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "free"

            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('001')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

            try:
                self.instrument.ressource.write('*RST')
                self.instrument.ressource.write('*CLS')
                self.instrument.ressource.write('SYST:REM')
                self.instrument.ressource.read_termination = "\r\n"

            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

        else:
            self.view.view.sendError('004')

    def closeConnection(self):    
    #This method close the connection to device   
        if self.instrument.ressource != None:
            try: 
                self.instrument.ressource.close()
                self.instrument.ressource = None
            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"

    def setVoltageSource(self, args=[]):
    #This method set to DCV
        if self.instrument.state == "unreachable":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "free"
            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('001')
                    self.instrument.state = "unreachable"
                return(-1)

        if self.instrument.state == "free":
            try:
                self.instrument.ressource.write('SOUR:FUNC VOLT')
                self.instrument.ressource.write('SOUR:VOLT ' + str(args[0]))
                self.instrument.ressource.write('SENS:FUNC "CURR"')
                self.instrument.ressource.write('SENS:CURR:PROT ' + str(args[1]))

            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setCurrentSource(self, args=[]):
    #This method set to DCV
        print(args)
        if self.instrument.state == "unreachable":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "free"
            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('001')
                    self.instrument.state = "unreachable"
                return(-1)

        if self.instrument.state == "free":
            try:
                self.instrument.ressource.write('SOUR:FUNC CURR')
                self.instrument.ressource.write('SOUR:CURR:MODE FIXED')
                self.instrument.ressource.write('SENS:FUNC "VOLT"')
                self.instrument.ressource.write('SENS:VOLT:PROT ' + str(args[1]))
                self.instrument.ressource.write('SOUR:CURR:LEV ' + str(args[0]))
                
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def generateCurrentWaveform(self, args=[]):
    #this methods generate the desired voltage waveform    
        liste = self.model.openConfiguration(args[0])

        if self.instrument.state == "unreachable":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "free"
            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('001')
                    self.instrument.state = "unreachable"
                return(-1)

        if self.instrument.state == "free":
            try:
                self.instrument.ressource.write('SOUR:FUNC CURR')
                self.instrument.ressource.write('SOUR:CURR:MODE FIXED')

                for item in liste[1]:
                    self.instrument.ressource.write('SOUR:CURR:LEV ' + str(item))

            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def generateVoltageWaveform(self, args=[]):
    #this methods generate the desired voltage waveform     
        liste = self.model.openConfiguration(args[0])

        if self.instrument.state == "unreachable":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "free"
            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('001')
                    self.instrument.state = "unreachable"
                return(-1)

        if self.instrument.state == "free":
            try:
                self.instrument.ressource.write('SOUR:FUNC VOLT')

                for item in liste[1]:
                    self.instrument.ressource.write('SOUR:VOLT ' + str(item))
                
                self.instrument.ressource.write('SOUR:VOLT 0')

            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setMasterState(self, args=[]):
    #This method modify the output state
        if self.instrument.state == "unreachable":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "free"
            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('001')
                    self.instrument.state = "unreachable"
                return(-1)

        if self.instrument.state == "free":
            try:
                #self.instrument.ressource.write('OUTP?')
                #self.instrument.masterState = float(self.instrument.read())

                if self.instrument.masterState == 0:
                    self.instrument.ressource.write('OUTP ON')
                    self.instrument.masterState = 1
                elif self.instrument.masterState == 1: 
                    self.instrument.ressource.write('OUTP OFF')    
                    self.instrument.masterState = 0                

            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')


