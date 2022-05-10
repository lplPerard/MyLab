"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Oscilloscope Controller.

"""


from threading import Thread
import numpy as np
from Oscilloscope import Oscilloscope
from tkinter.constants import END
from matplotlib import pyplot as plt
import pyvisa

from struct import unpack

class HMO3004():
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

                if self.instrument.id == "0x0699::0x0377":
                        if self.instrument.channelState[int(str(args[7])[-1])-1] == 0:
                            self.instrument.ressource.write('SEL:CH' + str(args[7])[-1] + ' ON')
                            self.instrument.channelState[int(str(args[7])[-1])-1] = 1
                        else:
                            self.instrument.ressource.write('SEL:CH' + str(args[7])[-1] + ' OFF')
                            self.instrument.channelState[int(str(args[7])[-1])-1] = 0

                elif (self.instrument.id == "0x0AAD::0x01D6") or (self.instrument.id == "GPIB0::25::INSTR") or (self.instrument.id == "0x0AAD::0x0117"):
                        if self.instrument.channelState[int(str(args[7])[-1])-1] == 0:
                            self.instrument.ressource.write('CHAN' + str(args[7])[-1] + ':STAT ON')
                            self.instrument.channelState[int(str(args[7])[-1])-1] = 1
                        else:
                            self.instrument.ressource.write('CHAN' + str(args[7])[-1] + ':STAT OFF')
                            self.instrument.channelState[int(str(args[7])[-1])-1] = 0

                elif (self.instrument.id == "0x0B21::0x0032") or (self.instrument.id == "0x0B21::0x0023"):
                        if self.instrument.channelState[int(str(args[7])[-1])-1] == 0:
                            self.instrument.ressource.write(':CHAN' + str(args[7])[-1] + ':DISP ON')
                            self.instrument.channelState[int(str(args[7])[-1])-1] = 1
                        else:
                            self.instrument.ressource.write(':CHAN' + str(args[7])[-1] + ':DISP OFF')
                            self.instrument.channelState[int(str(args[7])[-1])-1] = 0
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

                if self.instrument.id == "0x0699::0x0377":
                    if args[8] == "FULL":
                        self.instrument.ressource.write('CH' + str(args[7])[-1] + ':BAN FUL')
                    elif args[8] == "20MHZ":
                        self.instrument.ressource.write('CH' + str(args[7])[-1]+ ':BAN TWE')

                elif (self.instrument.id == "0x0AAD::0x01D6") or (self.instrument.id == "GPIB0::25::INSTR") or (self.instrument.id == "0x0AAD::0x0117"):
                    if args[8] == "200MHZ":
                        self.instrument.ressource.write('CHAN' + str(args[7])[-1] + ':BAND B200')
                    if args[8] == "100MHZ":
                        self.instrument.ressource.write('CHAN' + str(args[7])[-1] + ':BAND B100')
                    elif args[8] == "20MHZ":
                        self.instrument.ressource.write('CHAN' + str(args[7])[-1] + ':BAND B20')

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

                if self.instrument.id == "0x0699::0x0377":
                        if args[8] == "DC":
                            self.instrument.ressource.write('CH' + str(args[7])[-1] + ':COUP DC')
                        elif args[8] == "AC":
                            self.instrument.ressource.write('CH' + str(args[7])[-1] + ':COUP AC')
                        elif args[8] == "GND":
                            self.instrument.ressource.write('CH' + str(args[7])[-1] + ':COUP GND')

                elif (self.instrument.id == "0x0AAD::0x01D6") or (self.instrument.id == "GPIB0::25::INSTR") or (self.instrument.id == "0x0AAD::0x0117"):
                        if args[8] == "DC":
                            self.instrument.ressource.write('CHAN' + str(args[7])[-1] + ':COUP DCL')
                        if args[8] == "DC-50":
                            self.instrument.ressource.write('CHAN' + str(args[7])[-1] + ':COUP DC')
                        elif args[8] == "AC":
                            self.instrument.ressource.write('CHAN' + str(args[7])[-1] + ':COUP ACL')
                        elif args[8] == "AC-50":
                            self.instrument.ressource.write('CHAN' + str(args[7])[-1] + ':COUP AC')
                        elif args[8] == "GND":
                            self.instrument.ressource.write('CHAN' + str(args[7])[-1] + ':COUP GND')

                elif (self.instrument.id == "0x0B21::0x0032") or (self.instrument.id == "0x0B21::0x0023"):
                        if args[8] == "DC":
                            self.instrument.ressource.write(':CHAN' + str(args[7])[-1] + ':COUP DC')
                        if args[8] == "DC-50":
                            self.instrument.ressource.write(':CHAN' + str(args[7])[-1] + ':COUP DC50')
                        elif args[8] == "AC":
                            self.instrument.ressource.write(':CHAN' + str(args[7])[-1] + ':COUP AC')
                        elif args[8] == "GND":
                            self.instrument.ressource.write(':CHAN' + str(args[7])[-1] + ':COUP GND')
                            
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

                if self.instrument.id == "0x0699::0x0377":
                        self.instrument.ressource.write('CH' + str(args[7])[-1] + ':POS ' + str(args[0]))

                elif (self.instrument.id == "0x0AAD::0x01D6") or (self.instrument.id == "GPIB0::25::INSTR") or (self.instrument.id == "0x0AAD::0x0117"):
                    self.instrument.ressource.write('CHAN' + str(args[7])[-1] + ':OFFS ' + str(int(args[0])))

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

                if self.instrument.id == "0x0699::0x0377":
                        if args[8] == "x1":
                            self.instrument.ressource.write('CH' + str(args[7])[-1] + ':PRO:GAIN 1.0')
                        elif args[8] == "x10":
                            self.instrument.ressource.write('CH' + str(args[7])[-1] + ':PRO:GAIN 0.1')
                        elif args[8] == "x100":
                            self.instrument.ressource.write('CH' + str(args[7])[-1] + ':PRO:GAIN 0.01')
                        elif args[8] == "x1000":
                            self.instrument.ressource.write('CH' + str(args[7])[-1] + ':PRO:GAIN 0.001')

                elif (self.instrument.id == "0x0AAD::0x01D6") or (self.instrument.id == "GPIB0::25::INSTR") or (self.instrument.id == "0x0AAD::0x0117"):
                        if args[8] == "x1":
                            self.instrument.ressource.write('PROB' + str(args[7])[-1] + ':SET:ATT:MAN 1')
                        elif args[8] == "x10":
                            self.instrument.ressource.write('PROB' + str(args[7])[-1] + ':SET:ATT:MAN 10')
                        elif args[8] == "x100":
                            self.instrument.ressource.write('PROB' + str(args[7])[-1] + ':SET:ATT:MAN 100')
                        elif args[8] == "x1000":
                            self.instrument.ressource.write('PROB' + str(args[7])[-1] + ':SET:ATT:MAN 1000')
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

                if self.instrument.id == "0x0699::0x0377":
                    self.instrument.ressource.write('CH' + str(args[7])[-1] + ':SCA ' + str(args[0]))

                elif (self.instrument.id == "0x0AAD::0x01D6") or (self.instrument.id == "GPIB0::25::INSTR") or (self.instrument.id == "0x0AAD::0x0117"):
                    self.instrument.ressource.write('CHAN' + str(args[7])[-1] + ':SCAL ' + str(args[0]))

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

                if self.instrument.id == "0x0699::0x0377":
                        self.instrument.ressource.write('HOR:SCA ' + str(args[0]))

                elif (self.instrument.id == "0x0AAD::0x01D6") or (self.instrument.id == "GPIB0::25::INSTR") or (self.instrument.id == "0x0AAD::0x0117"):
                    self.instrument.ressource.write('TIM:SCAL ' + str(args[0]))

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

                if self.instrument.id == "0x0699::0x0377":
                    self.instrument.ressource.write('HOR:DEL:MOD OFF')
                    self.instrument.ressource.write('HOR:POS ' + str(args[0]))

                elif (self.instrument.id == "0x0AAD::0x01D6") or (self.instrument.id == "GPIB0::25::INSTR") or (self.instrument.id == "0x0AAD::0x0117"):
                    self.instrument.ressource.write('TIM:POS ' + str(args[0]))
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

                if self.instrument.id == "0x0699::0x0377":
                    self.instrument.ressource.write('DATA:SOU ch' + str(args[7])[-1])
                        
                    self.instrument.ressource.write('DATA:WIDTH 1')
                    self.instrument.ressource.write('DATA:ENC RPB')

                    ymult = float(self.instrument.ressource.query('WFMPRE:YMULT?'))
                    yzero = float(self.instrument.ressource.query('WFMPRE:YZERO?'))
                    yoff = float(self.instrument.ressource.query('WFMPRE:YOFF?'))
                    xincr = float(self.instrument.ressource.query('WFMPRE:XINCR?'))
                    
                    self.instrument.ressource.write('CURVE?')
                    data = self.instrument.ressource.read_raw()
                    header_len = 2 + int(data[1])
                    ADC_wave = data[header_len:-1]

                    ADC_wave = np.array(unpack('%sB' % len(ADC_wave), ADC_wave))

                    volt = (ADC_wave - yoff) * ymult + yzero
                    time = np.arange(0, xincr * len(volt), xincr)
                    
                    self.instrument.measure["channel_" + str(args[7])[-1] + "_timebase"] = time
                    self.instrument.measure["channel_" + str(args[7])[-1] + "_waveform"] = volt 

                elif (self.instrument.id == "0x0AAD::0x01D6") or (self.instrument.id == "GPIB0::25::INSTR") or (self.instrument.id == "0x0AAD::0x0117"):
                    self.instrument.ressource.write('CHAN:DATA:POIN DMAX')
                    self.instrument.ressource.write('*OPC')
                    header = self.instrument.ressource.query('CHAN' + str(args[7])[-1] +':DATA:HEAD?')
                    header = header.split(',')
                    yor = self.instrument.ressource.query('CHAN' + str(args[7])[-1] +':DATA:YOR?')
                    xor = self.instrument.ressource.query('CHAN:DATA:XOR?')
                    xinc = self.instrument.ressource.query('CHAN:DATA:XINC?')
                    self.instrument.ressource.write('FORM UINT,8')
                    yinc = self.instrument.ressource.query('CHAN:DATA:YINC?')
                    self.instrument.ressource.write('CHAN' + str(args[7])[-1] + ':DATA?')
                    data = self.instrument.ressource.read_raw()

                    time = np.arange(0, float(xinc) * float(header[2]), float(xinc)) + float(xor)
                    data = np.array(unpack('%sB' % len(data), data))
                    data = data[(len(data)-len(time)):-10]
                    time = time[:-10]
                    volt = float(yor) + (float(yinc) * data)

                    self.instrument.measure["channel_" + str(args[7])[-1] + "_timebase"] = time
                    self.instrument.measure["channel_" + str(args[7])[-1] + "_waveform"] = volt 

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

                if self.instrument.id == "0x0699::0x0377":
                
                    self.instrument.ressource.write('ACQ:STATE?')
                    state = float(self.instrument.ressource.read())

                    if state == 0:                        
                        self.instrument.ressource.write('ACQ:STATE ON')
                    else :
                        self.instrument.ressource.write('ACQ:STATE OFF')

                elif (self.instrument.id == "0x0AAD::0x01D6") or (self.instrument.id == "GPIB0::25::INSTR") or (self.instrument.id == "0x0AAD::0x0117"):
                
                    self.instrument.ressource.write('ACQ:STATE?')
                    state = float(self.instrument.ressource.read())

                    if state == 0:                        
                        self.instrument.ressource.write('RUN')
                    else :
                        self.instrument.ressource.write('STOP')

            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')
            
    def addMeasurement(self, args=[]):
    #This method modify the output state 
        if (self.instrument.state == "free") or (self.instrument.state == "unreachable"):
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "connected"

                if self.instrument.id == "0x0699::0x0377":
                    self.instrument.ressource.write('MEASU:MEAS' + str(args[8])[-1] + ':SOURCE CH' + str(args[7])[-1])
                    self.instrument.ressource.write('MEASU:MEAS' + str(args[8])[-1] + ':TYP ' + str(args[9]))
                    self.instrument.ressource.write('MEASU:MEAS' + str(args[8])[-1] + ':STATE ON')

                elif (self.instrument.id == "0x0AAD::0x01D6") or (self.instrument.id == "GPIB0::25::INSTR") or (self.instrument.id == "0x0AAD::0x0117"):
                    if str(args[9]) == "PK2Pk":
                        type = "PEAK"
                    elif str(args[9]) == "AMPlitude" :
                        type = "AMPL"
                    else :
                        type = str(args[9])

                    self.instrument.ressource.write('MEAS' + str(args[8])[-1] + ':MAIN ' + type)
                    self.instrument.ressource.write('MEAS' + str(args[8])[-1] + ':SOUR CH' + str(args[7])[-1])
                    self.instrument.ressource.write('MEAS' + str(args[8])[-1] + ' ON')
            except:
                self.view.view.sendError('002')
                self.instrument.state = "unreachable"
                self.instrument.ressource.close()
                self.instrument.ressource = None
                return(-1)

        else:
            self.view.view.sendError('004')
            
    def getMeasurement(self, args=[]):
    #This method modify the output state 
        if (self.instrument.state == "free") or (self.instrument.state == "unreachable"):
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "connected"

                if self.instrument.id == "0x0699::0x0377":
                    measurement = self.instrument.ressource.query('MEASU:MEAS' + str(args[8])[-1] + ':VAL?')
                    self.instrument.measure["measure_" + str(args[8])[-1]] = [measurement]

                elif (self.instrument.id == "0x0AAD::0x01D6") or (self.instrument.id == "GPIB0::25::INSTR") or (self.instrument.id == "0x0AAD::0x0117"):
                    measurement = self.instrument.ressource.query('MEAS' + str(args[8])[-1] + ':RES?')
                    self.instrument.measure["measure_" + str(args[8])[-1]] = [measurement]

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
        time = self.instrument.measure["channel_" + str(args[7])[-1] + "_timebase"]
        volt = self.instrument.measure["channel_" + str(args[7])[-1] + "_waveform"] 

        fig = plt.figure(facecolor=self.model.parameters_dict['backgroundColorInstrument'])
        ax1 = fig.add_subplot(111)
        ax1.set_xlabel(('Time (s)'))
        ax1.set_ylabel(('Voltage (V)'))
        ax1.plot(time, volt)
        plt.grid()
        plt.show()