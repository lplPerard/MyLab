"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Power Supply Controller.

"""


from tkinter.constants import END
from pyvisa import resources
from Instrument import Instrument
import pyvisa
import time 

class PowerSupplyController():
    """Class containing the PowerSupplyController for MyLab.

    """

    def __init__(self, view=None, term=None):
    #Constructor for the Controller class   

        self.view = view  
        self.term = term
        self.instrument = Instrument()
        self.instrument.type="Power Supply"

        self.resourceManager = pyvisa.ResourceManager()

    def updateView(self, view):
        self.view = view

    def connectToDevice(self):
    #This method establish connection with device using instrument adress   
        if self.instrument.adress != "":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.adress)
            except:
                self.view.view.sendError('001')
            try:
                self.instrument.ressource.write('*RST')
                self.instrument.ressource.write('*CLS')
                self.instrument.ressource.close()
            except:
                self.view.view.sendError('002')

        else:
            self.view.view.sendError('004')

    def setVoltageSource(self, voltage, calibre=0):
    #This method modify the voltage source 
        if self.instrument.adress != "":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.adress)
            except:
                self.view.view.sendError('001')

            try:
                self.instrument.ressource.write('INST:NSEL 1')
                self.instrument.ressource.write('SOUR:VOLT ' + str(voltage))
                self.instrument.ressource.close()
            except:
                self.view.view.sendError('002')

        else:
            self.view.view.sendError('004')

    def setCurrentSource(self, current, calibre=0):
    #This method modify the voltage source 
        if self.instrument.adress != "":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.adress)
            except:
                self.view.view.sendError('001')

            try:
                self.instrument.ressource.write('INST:NSEL 1')
                self.instrument.ressource.write('SOUR:CURR ' + str(current))
                self.instrument.ressource.close()
            except:
                self.view.view.sendError('002')

        else:
            self.view.view.sendError('004')
            
    def setOutputState(self):
    #This method modify the output state 
        if self.instrument.adress != "":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.adress)
            except:
                self.view.view.sendError('001')

            try: 
                self.instrument.ressource.write('OUTP:STAT?')            
                state = float(self.instrument.ressource.read())

                if state == 0:
                    self.instrument.ressource.write('INST:NSEL 1')
                    self.instrument.ressource.write('OUTP:STAT ON ')
                    self.instrument.ressource.close()
                else:
                    self.instrument.ressource.write('INST:NSEL 1')
                    self.instrument.ressource.write('OUTP:STAT OFF ')
                    self.instrument.ressource.close()
            except:
                self.view.view.sendError('002')

        else:
            self.view.view.sendError('004')
        
    def updateMonitoring(self):
    #This method update the content of the view with content from device   
        if self.instrument.adress != "":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.adress)
            except:
                self.view.view.sendError('001')

            try:
                self.instrument.ressource.write('MEAS:CURR?')         
                current = float(self.instrument.ressource.read())
                self.view.doubleVar_currentMeasure.set(current)
                self.term.insert(END, "current : " + str(current) + " A\n")
                
                self.instrument.ressource.write('MEAS:VOLT?')         
                voltage = float(self.instrument.ressource.read())
                self.view.doubleVar_voltageMeasure.set(voltage)
                self.term.insert(END, "voltage : " + str(voltage) + " V\n")
                
                self.instrument.ressource.write('MEAS:POW?')         
                power = float(self.instrument.ressource.read())
            except:
                self.view.view.sendError('002')

        else:
            self.view.view.sendError('004')


