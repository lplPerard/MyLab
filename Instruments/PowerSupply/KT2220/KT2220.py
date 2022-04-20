"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Power Supply Controller.

"""


from PowerSupply import PowerSupply
from tkinter.constants import END
import pyvisa
import time

class KT2220():
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
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
            self.instrument.state == "connected"

        except:
            self.view.view.sendError('001')
            self.instrument.ressource = None
            return("ERROR")

        try:
            self.instrument.ressource.write('*RST')
            self.instrument.ressource.write('*CLS')

        except:
            self.view.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def setVoltageSource(self, args=[]):
    #This method modify the voltage source 
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.view.sendError('001')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

        try:
            self.instrument.ressource.write('INST:NSEL ' + str(args[7])[-1])
            self.instrument.ressource.write('SOUR:VOLT ' + str(args[0]))
        except:
            self.view.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

    def setCurrentLimit(self, args=[]):
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")

        try:
            self.instrument.ressource.write('INST:NSEL ' + str(args[7])[-1])
            self.instrument.ressource.write('SOUR:CURR ' + str(args[0]))
        except:
            self.view.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")
            
    def setChannelState(self, args=[]):
    #This method modify the output state 
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
        except:
            self.view.view.sendError('001')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")
        
        try: 
            if self.instrument.channelState[int(args[7])-1] == 0:
                self.instrument.ressource.write('INST:SEL ' + str(args[7])[-1])
                self.instrument.ressource.write('CHAN:OUTP ON ')
                self.instrument.channelState[int(args[7])-1] = 1
            else:
                self.instrument.ressource.write('INST:SEL ' + str(args[7])[-1])
                self.instrument.ressource.write('CHAN:OUTP OFF ')
                self.instrument.channelState[int(args[7])-1] = 0
        except:
            self.view.view.sendError('002')
            self.instrument.ressource.close()
            self.instrument.ressource = None
            return("ERROR")
            
    def setMasterState(self, args=[]):
    #This method modify the output state 
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
            self.instrument.state == "connected"
        except:
            self.view.view.sendError('001')
            return("ERROR")

        try:            
            if self.instrument.masterState == 0:
                self.instrument.ressource.write('OUTP:ENAB 1')
                self.instrument.masterState = 1
            else:
                self.instrument.ressource.write('OUTP:ENAB 0')          
                self.instrument.masterState = 0
        except:
            self.view.view.sendError('002')
            return("ERROR")
        
    def Measure(self, args=[]):
    #This method update the content of the view with content from device   
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
            self.instrument.ressource.write('INST:NSEL ' + str(args[7])[-1])
        except:
            self.view.view.sendError('001')
            self.instrument.ressource.close()
            return("ERROR")

            
        try:
            self.instrument.ressource.write('MEAS:CURR?')         
            current = float(self.instrument.ressource.read())
            self.instrument.measure["currentChannel"+ str(args[7])[-1]] = [current]
            
            self.instrument.ressource.write('MEAS:VOLT?')         
            voltage = float(self.instrument.ressource.read())
            self.instrument.measure["voltageChannel"+ str(args[7])[-1]] = [voltage]
            
            self.instrument.ressource.write('MEAS:POW?')         
            power = float(self.instrument.ressource.read())
            self.instrument.measure["powerChannel"+ str(args[7])[-1]] = [power]

        except:
            self.view.view.sendError('001')
            self.instrument.ressource.close()
            return("ERROR")
        
    def MeasureVoltage(self, args=[]):
    #This method update the content of the view with content from device   
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
            self.instrument.ressource.write('INST:NSEL ' + str(args[7])[-1])
        except:
            self.view.view.sendError('001')
            return("ERROR")
        
        try:                
            self.instrument.ressource.write('MEAS:VOLT?')         
            voltage = float(self.instrument.ressource.read())
            self.instrument.measure["voltageChannel"+ str(args[7])[-1]] = [voltage]
            self.instrument.result = voltage

        except:
            self.view.view.sendError('001')
            self.instrument.ressource.close()
            return("ERROR")

    def MeasureCurrent(self, args=[]):
    #This method update the content of the view with content from device   
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
            self.instrument.ressource.write('INST:NSEL ' + str(args[7])[-1])
        except:
            self.view.view.sendError('001')
            return("ERROR")

        
        try:                
            self.instrument.ressource.write('MEAS:CURR?')         
            current = float(self.instrument.ressource.read())
            self.instrument.measure["currentChannel"+ str(args[7])[-1]] = [current]
            self.instrument.result = current

        except:
            self.view.view.sendError('001')
            self.instrument.ressource.close()
            return("ERROR")
        
    def MeasurePower(self, args=[]):
    #This method update the content of the view with content from device   
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
            self.instrument.ressource.write('INST:NSEL ' + str(args[7])[-1])
        except:
            self.view.view.sendError('001')
            return("ERROR")

        
        try:                
            self.instrument.ressource.write('MEAS:POW?')         
            power = float(self.instrument.ressource.read())
            self.instrument.measure["powerChannel+ str(args[7])[-1]"] = [power]
            self.instrument.result = power

        except:
            self.view.view.sendError('001')
            self.instrument.ressource.close()
            return("ERROR")



