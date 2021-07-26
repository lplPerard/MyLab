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

    def __init__(self, view=None, term=None, instrument=None):
    #Constructor for the Controller class   

        self.view = view  
        self.term = term

        self.instrument = WaveformGenerator()
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
                return(-1)
            try:
                self.instrument.ressource.write('*RST')
                self.instrument.ressource.write('*CLS')
                self.instrument.ressource.close()
                self.instrument.ressource = None
            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                return(-1)

        else:
            self.view.view.sendError('004')

    def applySinus(self, amplitude=None, amplitudeType=None, frequency=None, frequencyUnit=None, offset=None, offsetUnit=1, phase=0):
    #this method set the parameters for a sinus waveform    
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
                self.instrument.ressource.write('APPL:SIN ' + str(frequency) + ' ' + str(frequencyUnit) + ', ' + str(amplitude) + ' ' + str(amplitudeType) + ', ' + str(offset*offsetUnit))
                self.instrument.ressource.write('PHAS ' +str(phase))
                self.instrument.ressource.write('OUTP OFF')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def applySquare(self, amplitude=None, amplitudeType=None, frequency=None, frequencyUnit=None, offset=None, offsetUnit=1, phase=0, dutyCycle=50):
    #this method set the parameters for a sinus waveform    
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
                self.instrument.ressource.write('APPL:SQU ' + str(frequency) + ' ' + str(frequencyUnit) + ', ' + str(amplitude) + ' ' + str(amplitudeType) + ', ' + str(offset*offsetUnit))
                self.instrument.ressource.write('PHAS ' + str(phase))
                self.instrument.ressource.write('FUNC:SQU:DCYC ' + str(dutyCycle))
                self.instrument.ressource.write('OUTP OFF')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def applyRamp(self, amplitude=None, amplitudeType=None, frequency=None, frequencyUnit=None, offset=None, offsetUnit=1, symetry=0, phase=0):
    #this method set the parameters for a sinus waveform    
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
                self.instrument.ressource.write('APPL:RAMP ' + str(frequency) + ' ' + str(frequencyUnit) + ', ' + str(amplitude) + ' ' + str(amplitudeType) + ', ' + str(offset*offsetUnit))
                self.instrument.ressource.write('FUNC:RAMP:SYMM ' +str(symetry))
                self.instrument.ressource.write('PHAS ' +str(phase))
                self.instrument.ressource.write('OUTP OFF')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def applyPulse(self, amplitude=None, amplitudeType=None, frequency=None, frequencyUnit=None, offset=None, offsetUnit=1, phase=0, lead=0, leadUnit="ns", trail=0, trailUnit="ns", pulseWidth=1, pulseWidthUnit='ms'):
    #this method set the parameters for a sinus waveform    
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
                self.instrument.ressource.write('APPL:PULS ' + str(frequency) + ' ' + str(frequencyUnit) + ', ' + str(amplitude) + ' ' + str(amplitudeType) + ', ' + str(offset*offsetUnit))
                self.instrument.ressource.write('PHAS ' + str(phase))
                self.instrument.ressource.write('FUNC:PULS:TRAN:LEAD ' + str(lead) + ' ' + str(leadUnit))
                self.instrument.ressource.write('FUNC:PULS:TRAN:TRA ' + str(trail) + ' ' + str(trailUnit))
                self.instrument.ressource.write('FUNC:PULS:WIDT ' + str(pulseWidth) + ' ' + str(pulseWidthUnit))
                self.instrument.ressource.write('OUTP OFF')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def applyNoise(self, amplitude=None, amplitudeType=None, bandwidth=1e5, bandwidthUnit=1, offset=None, offsetUnit=1):
    #this method set the parameters for a sinus waveform    
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
                self.instrument.ressource.write('APPL:NOIS 1 KHZ, ' + str(amplitude) + ' ' + str(amplitudeType) + ', ' + str(offset*offsetUnit))
                self.instrument.ressource.write('FUNC:NOIS:BWID ' + str(bandwidth*bandwidthUnit))
                self.instrument.ressource.write('OUTP OFF')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')

    def setOutputState(self, state=0):
    #This method set the output state at 50ohm or High Z
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
                if state == 0:
                    self.instrument.ressource.write('OUTP:LOAD 50')
                    self.instrument.masterState = 1
                else:
                    self.instrument.ressource.write('OUTP:LOAD INF')      
                    self.instrument.masterState = 0
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
        
            try:            
                if self.instrument.masterState == 0:
                    self.instrument.ressource.write('OUTP ON')
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    self.instrument.masterState = 1
                else:
                    self.instrument.ressource.write('OUTP OFF')
                    self.instrument.ressource.close()    
                    self.instrument.ressource = None                
                    self.instrument.masterState = 0
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                return(-1)

        else:
            self.view.view.sendError('004')
        
