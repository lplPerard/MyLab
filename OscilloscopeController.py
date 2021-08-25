"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Power Supply Controller.

"""


from threading import Thread
import numpy as np
from Oscilloscope import Oscilloscope
from tkinter.constants import END
from matplotlib import pyplot as plt
import pyvisa

from struct import unpack

class OscilloscopeController():
    """Class containing the OscilloscopeController for MyLab.

    """

    def __init__(self, view=None, term=None, instrument=None, model=None):
    #Constructor for the Controller class   

        self.view = view  
        self.term = term
        self.model = model

        self.instrument = Oscilloscope()
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
            
    def setChannelState(self, args=[]):
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

            if self.instrument.id == "0x0699::0x0377":
                try: 
                    if self.instrument.channelState[int(args[7])-1] == 0:
                        self.instrument.ressource.write('SEL:CH' + str(args[7]) + ' ON')
                        self.instrument.channelState[int(args[7])-1] = 1
                    else:
                        self.instrument.ressource.write('SEL:CH' + str(args[7]) + ' OFF')
                        self.instrument.channelState[int(args[7])-1] = 0
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

            else:
                try: 
                    if self.instrument.channelState[args[7]] == 0:
                        print(self.instrument.channelState[args[7]])
                        self.instrument.ressource.write('SEL:CH' + str(args[7] + 1) + ' ON')
                        print('SEL:CH' + str(args[7] + 1) + 'ON')
                        self.instrument.channelState[args[7]] = 1
                        print(self.instrument.channelState[args[7]])
                    else:
                        self.instrument.ressource.write('SEL:CH' + str(args[7] + 1) + ' OFF')
                        print('SEL:CH' + str(args[7] + 1) + 'OFF')
                        self.instrument.channelState[args[7]] = 0
                        print(self.instrument.channelState[args[7]])
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

        else:
            self.view.view.sendError('004')
            
    def setBandwidth(self, args=[]):
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

            if self.instrument.id == "0x0699::0x0377":
                try: 
                    if args[7] == "FULL":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':BAN FUL')
                    elif args[7] == "20MHZ":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':BAN TWE')
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

            else:
                try: 
                    if args[7] == "FULL":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':BAN FUL')
                    elif args[7] == "20MHZ":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':BAN TWE')
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

        else:
            self.view.view.sendError('004')
           
    def setCoupling(self, args=[]):
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

            if self.instrument.id == "0x0699::0x0377":
                try: 
                    if args[7] == "DC":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':COUP DC')
                    elif args[7] == "AC":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':COUP AC')
                    elif args[7] == "GND":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':COUP GND')
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

            else:
                try: 
                    if args[7] == "DC":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':COUP DC')
                    elif args[7] == "AC":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':COUP AC')
                    elif args[7] == "GND":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':COUP GND')
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

        else:
            self.view.view.sendError('004')
            
    def setOffset(self, args=[]):
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

            if self.instrument.id == "0x0699::0x0377":
                try: 
                    self.instrument.ressource.write('CH' + str(args[7]) + ':POS ' + str(args[0]))
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

            else:
                try: 
                    if args[8] == "DC":
                        self.instrument.ressource.write('CH' + str(args[7]) + ':BAN DC')
                    elif args[8] == "AC":
                        self.instrument.ressource.write('CH' + str(args[7]) + ':BAN AC')
                    elif args[8] == "GND":
                        self.instrument.ressource.write('CH' + str(args[7]) + ':BAN GND')
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

        else:
            self.view.view.sendError('004')
           
    def setProbe(self, args=[]):
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

            if self.instrument.id == "0x0699::0x0377":
                try: 
                    if args[7] == "x1":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':PRO:GAIN 1.0')
                    elif args[7] == "x10":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':PRO:GAIN 0.1')
                    elif args[7] == "x100":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':PRO:GAIN 0.01')
                    elif args[7] == "x1000":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':PRO:GAIN 0.001')
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

            else:
                try: 
                    if args[7] == "x1":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':PRO:GAIN 1.0')
                    elif args[7] == "x10":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':PRO:GAIN 0.1')
                    elif args[7] == "x100":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':PRO:GAIN 0.01')
                    elif args[7] == "x1000":
                        self.instrument.ressource.write('CH' + str(args[8]) + ':PRO:GAIN 0.001')
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

        else:
            self.view.view.sendError('004')
            
    def setChannelScale(self, args=[]):
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

            if self.instrument.id == "0x0699::0x0377":
                try: 
                    self.instrument.ressource.write('CH' + str(args[7]) + ':SCA ' + str(args[0]))
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

            else:
                try: 
                    self.instrument.ressource.write('CH' + str(args[7]) + ':SCA ' + str(args[0]))
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

        else:
            self.view.view.sendError('004')
            
    def setTimeScale(self, args=[]):
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

            if self.instrument.id == "0x0699::0x0377":
                try: 
                    self.instrument.ressource.write('HOR:SCA ' + str(args[0]))
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

            else:
                try: 
                    self.instrument.ressource.write('HOR:SCA ' + str(args[0]))
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

        else:
            self.view.view.sendError('004')
            
    def setPosition(self, args=[]):
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

            if self.instrument.id == "0x0699::0x0377":
                try: 
                    self.instrument.ressource.write('HOR:DEL:MOD OFF')
                    self.instrument.ressource.write('HOR:POS ' + str(args[0]))
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

            else:
                try: 
                    self.instrument.ressource.write('HOR:POS ' + str(args[0]))
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

        else:
            self.view.view.sendError('004')
                        
    def getCurve(self, args=[]):
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

            if self.instrument.id == "0x0699::0x0377":
                try: 
                    if int(args[7]) == 1:
                        self.instrument.ressource.write('DATA:SOU ch1')
                    elif int(args[7]) == 2:
                        self.instrument.ressource.write('DATA:SOU ch2')
                    elif int(args[7]) == 3:
                        self.instrument.ressource.write('DATA:SOU ch3')
                    elif int(args[7]) == 4:
                        self.instrument.ressource.write('DATA:SOU ch4')
                        
                    self.instrument.ressource.write('DATA:WIDTH 1')
                    self.instrument.ressource.write('DATA:ENC RPB')

                    ymult = float(self.instrument.ressource.query('WFMPRE:YMULT?'))
                    yzero = float(self.instrument.ressource.query('WFMPRE:YZERO?'))
                    yoff = float(self.instrument.ressource.query('WFMPRE:YOFF?'))
                    xincr = float(self.instrument.ressource.query('WFMPRE:XINCR?'))
                    
                    self.instrument.ressource.write('CURVE?')
                    data = self.instrument.ressource.read_raw()
                    header_len = 2 + int(data[1])
                    header = data[:header_len]
                    ADC_wave = data[header_len:-1]

                    ADC_wave = np.array(unpack('%sB' % len(ADC_wave), ADC_wave))

                    volt = (ADC_wave - yoff) * ymult + yzero
                    time = np.arange(0, xincr * len(volt), xincr)

                    if int(args[7]) == 1:
                        self.instrument.measure["channel_1_timebase"] = time
                        self.instrument.measure["channel_1_waveform"] = volt 
                    elif int(args[7]) == 2:
                        self.instrument.measure["channel_2_timebase"] = time
                        self.instrument.measure["channel_2_waveform"] = volt 
                    elif int(args[7]) == 3:
                        self.instrument.measure["channel_3_timebase"] = time
                        self.instrument.measure["channel_3_waveform"] = volt 
                    elif int(args[7]) == 4:
                        self.instrument.measure["channel_4_timebase"] = time
                        self.instrument.measure["channel_4_waveform"] = volt 


                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

            else:
                try: 
                    self.instrument.ressource.write('HOR:POS ' + str(args[0]))
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

        else:
            self.view.view.sendError('004')
            
    def setRunStop(self, args=[]):
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

            if self.instrument.id == "0x0699::0x0377":
                try: 
                    self.instrument.ressource.write('ACQ:STATE?')
                    state = float(self.instrument.ressource.read())

                    if state == 0:                        
                        self.instrument.ressource.write('ACQ:STATE ON')
                    else :
                        self.instrument.ressource.write('ACQ:STATE OFF')

                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

            else:
                try: 
                    self.instrument.ressource.write('HOR:POS ' + str(args[0]))
                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return(-1)

        else:
            self.view.view.sendError('004')

    def plotCurve(self, args=[]):
    #This method plots the last captured curve
        if int(args[7]) == 1:
            time = self.instrument.measure["channel_1_timebase"]
            volt = self.instrument.measure["channel_1_waveform"]
        elif int(args[7]) == 2:
            time = self.instrument.measure["channel_2_timebase"]
            volt = self.instrument.measure["channel_2_waveform"]
        elif int(args[7]) == 3:
            time = self.instrument.measure["channel_3_timebase"]
            volt = self.instrument.measure["channel_3_waveform"]
        elif int(args[7]) == 4:
            time = self.instrument.measure["channel_4_timebase"]
            volt = self.instrument.measure["channel_4_waveform"]

        fig = plt.figure(facecolor=self.model.parameters_dict['backgroundColorInstrument'])
        ax1 = fig.add_subplot(111)
        ax1.set_xlabel(('Time (s)'))
        ax1.set_ylabel(('Voltage (V)'))
        ax1.plot(time, volt)
        plt.grid()
        plt.show()