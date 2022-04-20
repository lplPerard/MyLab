"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Multimeter Controller.

"""


from Multimeter import Multimeter
from tkinter.constants import END
import pyvisa
import time

class FL8845A():
    """Class containing the Multimeter Controller for MyLab.

    """

    def __init__(self, view=None, term=None, instrument=None):
    #Constructor for the Controller class   

        self.view = view  
        self.term = term

        self.instrument = Multimeter()
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
            self.instrument.ressource.read_termination = '\r\n'
            if "GPIB" in self.instrument.address :
                None
            else :
                self.instrument.ressource.write('SYST:REM')


        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def closeConnection(self):    
    #This method close the connection to device   
        try: 
            self.instrument.ressource.close()
            self.instrument.ressource = None
        except:
                self.view.sendError('002')

    def setDCV(self, args=[]):
    #This method set to DCV
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            self.instrument.ressource.write('CONF:VOLT:DC ')
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def setACV(self, args=[]):
    #This method set to ACV
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            self.instrument.ressource.write('CONF:VOLT:AC ')
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def setDCI(self, args=[]):
    #This method set to DCI
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            if args[8] == "mA":
                self.instrument.ressource.write('CONF:CURR:DC MIN')
            elif args[8] == "10A":
                self.instrument.ressource.write('CONF:CURR:DC MAX')
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def setACI(self, args=[]):
    #This method set to ACI
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            if args[8] == "mA":
                self.instrument.ressource.write('CONF:CURR:AC MIN')
            elif args[8] == "10A":
                self.instrument.ressource.write('CONF:CURR:AC MAX')
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def set2WR(self, args=[]):
    #This method set to Resistance
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            self.instrument.ressource.write('CONF:RES ')
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def set4WR(self, args=[]):
    #This method set to 4WR
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            self.instrument.ressource.write('CONF:FRES ')
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def setDiode(self, args=[]):
    #This method set to Diode
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            if (str(args[9]) == "5V") and (str(args[10]) == "1mA"):
                self.instrument.ressource.write('CONF:DIOD 0, 0')
            elif (str(args[9]) == "10V") and (str(args[10]) == "1mA"):
                self.instrument.ressource.write('CONF:DIOD 0, 1')
            elif (str(args[9]) == "5V") and (str(args[10]) == "0.1mA"):
                self.instrument.ressource.write('CONF:DIOD 1, 0')
            elif (str(args[9]) == "10V") and (str(args[10]) == "0.1mA"):
                self.instrument.ressource.write('CONF:DIOD 1, 1')
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def setContinuity(self, args=[]):
    #This method set to continuity
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            self.instrument.ressource.write('CONF:CONT ')
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def setFrequency(self, args=[]):
    #This method set to Frequency
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
            self.instrument.state == "free"
        except:
            self.view.sendError('001')
            return("ERROR")
        try:
            self.instrument.ressource.write('CONF:FREQ ')
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def setPeriod(self, args=[]):
    #This method set to Period
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            self.instrument.ressource.write('CONF:PER ')
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def measureDCV(self, args=[]):
    #Measure DCV 
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            self.instrument.ressource.write('MEAS:VOLT:DC?') 
            time.sleep(1)        
            voltage = float(self.instrument.ressource.read())
            self.instrument.measure["DC_voltage"] = [voltage]
            self.instrument.result = voltage 
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def measureACV(self, args=[]):
    #Measure ACV 
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")
        try:
            self.instrument.ressource.write('MEAS:VOLT:AC?')         
            voltage = float(self.instrument.ressource.read())
            self.instrument.measure["AC_voltage"] = [voltage]
            self.instrument.result = voltage
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def measureDCI(self, args=[]):
    #Measure DCI
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            self.instrument.ressource.write('MEAS:CURR:DC?')
            current = float(self.instrument.ressource.read())
            self.instrument.measure["DC_current"] = [current]
            self.instrument.result = current
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def measureACI(self, args=[]):
    #Measure ACI
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.sendError('001')
            return("ERROR")

        try:
            self.instrument.ressource.write('MEAS:CURR:AC?')         
            current = float(self.instrument.ressource.read())
            self.instrument.measure["AC_current"] = [current]
            self.instrument.result = current 
        except:
            self.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")