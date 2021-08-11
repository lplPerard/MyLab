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

    def applySinus(self, args=[]):
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
                return("ERROR")

            try:
                cmd='APPL:SIN ' + str(args[0]) + ' ' + str(args[7]) + ', ' + str(args[1]) + ' ' + str(args[8]) + ', ' + str(args[2])
                self.instrument.ressource.write(cmd)
                self.instrument.ressource.write('PHAS ' + str(args[3]))
                self.instrument.ressource.write('OUTP OFF')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return("ERROR")

        else:
            self.view.view.sendError('004')

    def applySquare(self, args=[]):
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
                return("ERROR")

            try:
                cmd='APPL:SQU ' + str(args[0]) + ' ' + str(args[7]) + ', ' + str(args[1]) + ' ' + str(args[8]) + ', ' + str(args[2])
                self.instrument.ressource.write(cmd)
                self.instrument.ressource.write('PHAS ' + str(args[3]))
                self.instrument.ressource.write('FUNC:SQU:DCYC ' + str(args[4]))
                self.instrument.ressource.write('OUTP OFF')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return("ERROR")

        else:
            self.view.view.sendError('004')

    def applyRamp(self, args=[]):
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
                return("ERROR")

            try:
                cmd='APPL:RAMP ' + str(args[0]) + ' ' + str(args[7]) + ', ' + str(args[1]) + ' ' + str(args[8]) + ', ' + str(args[2])
                self.instrument.ressource.write(cmd)
                self.instrument.ressource.write('PHAS ' + str(args[3]))
                self.instrument.ressource.write('FUNC:RAMP:SYMM ' + str(args[4]))
                self.instrument.ressource.write('OUTP OFF')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return("ERROR")

        else:
            self.view.view.sendError('004')

    def applyPulse(self, args=[]):
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
                return("ERROR")

            try:
                cmd='APPL:PULS ' + str(args[0]) + ' ' + str(args[7]) + ', ' + str(args[1]) + ' ' + str(args[8]) + ', ' + str(args[2])
                self.instrument.ressource.write(cmd)
                self.instrument.ressource.write('PHAS ' + str(args[3]))
                self.instrument.ressource.write('FUNC:PULS:WIDT ' + str(args[4]) + ' ' + str(args[9]))
                print('FUNC:PULS:TRAN:LEAD ' + str(args[5]) + ' ' + str(args[10]))
                print('FUNC:PULS:TRAN:TRA ' + str(args[6]) + ' ' + str(args[11]))
                self.instrument.ressource.write('FUNC:PULS:TRAN:LEAD ' + str(args[5]) + ' ' + str(args[10]))
                self.instrument.ressource.write('FUNC:PULS:TRAN:TRA ' + str(args[6]) + ' ' + str(args[11]))
                self.instrument.ressource.write('OUTP OFF')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return("ERROR")

        else:
            self.view.view.sendError('004')

    def applyNoise(self, args=[]):
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
                return("ERROR")

            try:
                self.instrument.ressource.write('APPL:NOIS 1 KHZ, ' + str(args[0]) + ' ' + str(args[7]) + ', ' + str(args[1]))
                self.instrument.ressource.write('FUNC:NOIS:BWID ' + str(args[2]) + ' ' + str(args[8]))
                self.instrument.ressource.write('OUTP OFF')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return("ERROR")

        else:
            self.view.view.sendError('004')

    def setOutputState(self, args=[]):
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
                if (args[7] == '50') or (args[7] == '50Ω'):
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

    def setMasterState(self, args=[]):
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
        
