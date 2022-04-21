"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Multimeter Controller.

"""


from Sourcemeter import Sourcemeter
from tkinter.constants import END
import pyvisa

class KT2400():
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
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)

        except:
            self.view.sendError('001')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

        try:
            self.instrument.ressource.write('*RST')
            self.instrument.ressource.write('*CLS')
            self.instrument.ressource.write('SYST:REM')
            self.instrument.ressource.read_termination = "\r\n"

        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def closeConnection(self):    
    #This method close the connection to device   
        if self.instrument.ressource != None:
            try: 
                self.instrument.ressource.close()
                self.instrument.ressource = None
            except:
                self.view.sendError('002')

    def setVoltageSource(self, args=[]):
    #This method set to DCV
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            self.instrument.ressource.write('SOUR:FUNC VOLT')
            self.instrument.ressource.write('SOUR:VOLT ' + str(args[0]))
            self.instrument.ressource.write('SENS:FUNC "CURR"')
            self.instrument.ressource.write('SENS:CURR:PROT ' + str(args[1]))

        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def setCurrentSource(self, args=[]):
    #This method set to DCV
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            self.instrument.ressource.write('SOUR:FUNC CURR')
            self.instrument.ressource.write('SOUR:CURR:MODE FIXED')
            self.instrument.ressource.write('SENS:FUNC "VOLT"')
            self.instrument.ressource.write('SENS:VOLT:PROT ' + str(args[1]))
            self.instrument.ressource.write('SOUR:CURR:LEV ' + str(args[0]))
            
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def measureCurrent(self, args=[]):
    #This method measure the current 
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            self.instrument.ressource.write('MEAS:CURR?')
            result = self.instrument.ressource.read()
            result = result.split(",")

            voltage = float(result[0])
            current = float(result[1])

            self.instrument.result = current
            self.instrument.measure["voltage"] = [voltage]
            self.instrument.measure["current"] = [current]
            self.instrument.measure["power"] = [current * voltage]
            self.instrument.measure["resistance"] = [voltage / current]

        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def measureVoltage(self, args=[]):
    #This method measure the current 
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            self.instrument.ressource.write('MEAS:VOLT?')
            result = self.instrument.ressource.read()
            result = result.split(",")

            voltage = float(result[0])
            current = float(result[1])

            self.instrument.result = voltage
            self.instrument.measure["voltage"] = [voltage]
            self.instrument.measure["current"] = [current]
            self.instrument.measure["power"] = [current * voltage]
            self.instrument.measure["resistance"] = [voltage / current]

        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def setMasterState(self, args=[]):
    #This method modify the output state
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")
        try:
            if self.instrument.masterState == 0:
                self.instrument.ressource.write('OUTP ON')
                self.instrument.masterState = 1
            elif self.instrument.masterState == 1: 
                self.instrument.ressource.write('OUTP OFF')    
                self.instrument.masterState = 0                

        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")


