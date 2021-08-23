"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Multimeter Controller.

"""


from Multimeter import Multimeter
from tkinter.constants import END
import pyvisa
import time

class MultimeterController():
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

    def setDCV(self, args=[]):
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
                self.instrument.ressource.write('CONF:VOLT:DC ')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setACV(self, args=[]):
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
                self.instrument.ressource.write('CONF:VOLT:AC ')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setDCI(self, args=[]):
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
                if args[8] == "mA":
                    self.instrument.ressource.write('CONF:CURR:DC MIN')
                elif args[8] == "10A":
                    self.instrument.ressource.write('CONF:CURR:DC MAX')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setACI(self, caliber=0, args=[]):
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
                if args[8] == "mA":
                    self.instrument.ressource.write('CONF:CURR:AC MIN')
                elif args[8] == "10A":
                    self.instrument.ressource.write('CONF:CURR:AC MAX')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def set2WR(self, args=[]):
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
                self.instrument.ressource.write('CONF:RES ')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def set4WR(self, args=[]):
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
                self.instrument.ressource.write('CONF:FRES ')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setDiode(self, args=[]):
    #This method set to DCV
        print(args[9])
        print(args[10])
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
                if (str(args[9]) == "5V") and (str(args[10]) == "1mA"):
                    self.instrument.ressource.write('CONF:DIOD 0, 0')
                elif (str(args[9]) == "10V") and (str(args[10]) == "1mA"):
                    self.instrument.ressource.write('CONF:DIOD 0, 1')
                elif (str(args[9]) == "5V") and (str(args[10]) == "0.1mA"):
                    self.instrument.ressource.write('CONF:DIOD 1, 0')
                elif (str(args[9]) == "10V") and (str(args[10]) == "0.1mA"):
                    self.instrument.ressource.write('CONF:DIOD 1, 1')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setContinuity(self, args=[]):
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
                self.instrument.ressource.write('CONF:CONT ')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setFrequency(self, args=[]):
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
                self.instrument.ressource.write('CONF:FREQ ')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setPeriod(self, args=[]):
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
                self.instrument.ressource.write('CONF:PER ')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def measureDCV(self, args=[]):
    #This method update the content of the view with content from device 
        if self.instrument.state == "unreachable":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "free"
            except:
                self.view.view.sendError('001')
                self.instrument.state = "unreachable"
                return(-1)

        if self.instrument.state == "free":
            try:
                while self.instrument.masterState != 0:
                    self.instrument.ressource.write('MEAS:VOLT:DC?')         
                    voltage = float(self.instrument.ressource.read())
                    self.instrument.measure_DCV = voltage
                    self.instrument.result = voltage
                    time.sleep(0.5)    
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def measureACV(self, args=[]):
    #This method update the content of the view with content from device 
        if self.instrument.state == "unreachable":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "free"
            except:
                self.view.view.sendError('001')
                self.instrument.state = "unreachable"
                return(-1)

        if self.instrument.state == "free":
            try:
                while self.instrument.masterState != 0:
                    self.instrument.ressource.write('MEAS:VOLT:AC?')         
                    voltage = float(self.instrument.ressource.read())
                    self.instrument.measure_ACV = voltage
                    self.instrument.result = voltage
                    time.sleep(0.5)    
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def measureDCI(self, args=[]):
    #This method update the content of the view with content from device 
        if self.instrument.state == "unreachable":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "free"
            except:
                self.view.view.sendError('001')
                self.instrument.state = "unreachable"
                return(-1)

        if self.instrument.state == "free":
            try:
                while self.instrument.masterState != 0:
                    self.instrument.ressource.write('MEAS:CURR:DC?')         
                    current = float(self.instrument.ressource.read())
                    self.instrument.measure_DCI = current
                    self.instrument.result = current
                    time.sleep(0.5)    
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def measureACI(self, args=[]):
    #This method update the content of the view with content from device 
        if self.instrument.state == "unreachable":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "free"
            except:
                self.view.view.sendError('001')
                self.instrument.state = "unreachable"
                return(-1)

        if self.instrument.state == "free":
            try:
                while self.instrument.masterState != 0:
                    self.instrument.ressource.write('MEAS:CURR:AC?')         
                    current = float(self.instrument.ressource.read())
                    self.instrument.measure_ACI = current
                    self.instrument.result = current
                    time.sleep(0.5)    
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')


