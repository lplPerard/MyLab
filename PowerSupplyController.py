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
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

            try:
                self.instrument.ressource.write('*RST')
                self.instrument.ressource.write('*CLS')

            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setVoltageSource(self, voltage, channel, calibre=0):
    #This method modify the voltage source 
        if (self.instrument.state == "free") or (self.instrument.state == "unreachable"):
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "connected"
            except:
                self.view.view.sendError('001')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

            try:
                self.instrument.ressource.write('INST:NSEL ' + str(channel))
                self.instrument.ressource.write('SOUR:VOLT ' + str(voltage))
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setCurrentSource(self, current, channel, calibre=0):
    #This method modify the voltage source 
        if (self.instrument.state == "free") or (self.instrument.state == "unreachable"):
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "connected"
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

            try:
                self.instrument.ressource.write('INST:NSEL ' + str(channel))
                self.instrument.ressource.write('SOUR:CURR ' + str(current))
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')
            
    def setChannelState(self, channel):
    #This method modify the output state 
        if (self.instrument.state == "free") or (self.instrument.state == "unreachable"):
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "connected"
            except:
                self.view.view.sendError('001')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)
        
            if self.instrument.id == "0x05E6::0x2220":
                try: 
                    if self.instrument.channelState[channel-1] == 0:
                        self.instrument.ressource.write('INST:SEL ' + str(channel))
                        self.instrument.ressource.write('CHAN:OUTP ON ')
                        self.instrument.channelState[channel-1] = 1
                    else:
                        self.instrument.ressource.write('INST:SEL ' + str(channel))
                        self.instrument.ressource.write('CHAN:OUTP OFF ')
                        self.instrument.channelState[channel-1] = 0
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

            else:
                try: 
                    if self.instrument.channelState[channel-1] == 0:
                        self.instrument.ressource.write('INST:NSEL ' + str(channel))
                        self.instrument.ressource.write('OUTP:CHAN ON ')
                        self.instrument.channelState[channel-1] = 1
                    else:
                        self.instrument.ressource.write('INST:NSEL ' + str(channel))
                        self.instrument.ressource.write('OUTP:CHAN OFF ')
                        self.instrument.channelState[channel-1] = 0
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
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
        
            if self.instrument.id == "0x05E6::0x2220":

                try:            
                    if self.instrument.masterState == 0:
                        self.instrument.ressource.write('OUTP:ENAB 1')
                        self.instrument.masterState = 1
                    else:
                        self.instrument.ressource.write('OUTP:ENAB 0')          
                        self.instrument.masterState = 0
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    return(-1)
            
            else:
                try:            
                    if self.instrument.masterState == 0:
                        self.instrument.ressource.write('OUTP:MAST ON')
                        self.instrument.masterState = 1
                    else:
                        self.instrument.ressource.write('OUTP:MAST OFF')         
                        self.instrument.masterState = 0
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    return(-1)

        else:
            self.view.view.sendError('004')
        
    def Measure(self, channel=1):
    #This method update the content of the view with content from device   
        if (self.instrument.state == "free") or (self.instrument.state == "unreachable") or (self.instrument.masterState == 0):
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "connected"
                self.instrument.ressource.write('INST:NSEL ' + str(channel))
            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('001')
                    self.instrument.state = "unreachable"
                return(-1)

            
            try:
                while self.instrument.masterState != 0:
                    self.instrument.ressource.write('MEAS:CURR?')         
                    current = float(self.instrument.ressource.read())
                    self.instrument.measure_current = current
                    
                    self.instrument.ressource.write('MEAS:VOLT?')         
                    voltage = float(self.instrument.ressource.read())
                    self.instrument.measure_voltage = voltage
                    
                    self.instrument.ressource.write('MEAS:POW?')         
                    power = float(self.instrument.ressource.read())
                    self.instrument.measure_power = power
                    time.sleep(0.5)                

            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('001')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                return(-1)

        else:
            self.view.view.sendError('004')

