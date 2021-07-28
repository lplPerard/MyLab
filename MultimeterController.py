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

    def setDCV(self):
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

    def setACV(self):
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

    def setDCI(self, caliber=0):
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
                if caliber == 0:
                    self.instrument.ressource.write('CONF:CURR:DC MIN')
                else:
                    self.instrument.ressource.write('CONF:CURR:DC MAX')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setACI(self, caliber=0):
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
                if caliber == 0:
                    self.instrument.ressource.write('CONF:CURR:AC MIN')
                else:
                    self.instrument.ressource.write('CONF:CURR:AC MAX')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def set2WR(self):
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

    def set4WR(self):
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

    def setDiode(self, current=0, voltage=0):
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
                self.instrument.ressource.write('CONF:DIOD ' + str(current) + ', ' + str(voltage))
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setContinuity(self):
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

    def setFrequency(self):
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

    def setPeriod(self):
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

    def measureDCV(self):
    #This method update the content of the view with content from device 
        print("start")
        if self.instrument.state == "unreachable":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "free"
            except:
                self.view.view.sendError('001')
                self.instrument.state = "unreachable"
                return(-1)

        if self.instrument.state == "free":
                while self.instrument.measureState != 0:
                    self.instrument.ressource.write('MEAS:VOLT:DC?')    
                    time.sleep(1)      
                    voltage = float(self.instrument.ressource.read())
                    print(voltage)
                    self.instrument.measure_DCV = voltage
                    time.sleep(0.5) 
                print("closed")   

        else:
            self.view.view.sendError('004')
            print("closed")

    def measureACV(self):
    #This method update the content of the view with content from device 
        print("start")
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
                while self.instrument.measureState != 0:
                    self.instrument.ressource.write('MEAS:VOLT:AC?')         
                    voltage = float(self.instrument.ressource.read())
                    self.instrument.measure_ACV = voltage
                    time.sleep(0.5)    
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                print("closed")
                return(-1)

        else:
            self.view.view.sendError('004')

    def measureDCI(self):
    #This method update the content of the view with content from device 
        print("start")
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
                while self.instrument.measureState != 0:
                    self.instrument.ressource.write('MEAS:CURR:DC?')         
                    current = float(self.instrument.ressource.read())
                    self.instrument.measure_DCI = current
                    time.sleep(0.5)    
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                print("closed")
                return(-1)

        else:
            self.view.view.sendError('004')

    def measureACI(self):
    #This method update the content of the view with content from device 
        print("start")
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
                while self.instrument.measureState != 0:
                    self.instrument.ressource.write('MEAS:CURR:AC?')         
                    current = float(self.instrument.ressource.read())
                    self.instrument.measure_ACI = current
                    time.sleep(0.5)    
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                print("closed")
                return(-1)

        else:
            self.view.view.sendError('004')


