"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for IV testBench Controller.

"""


import sys
from IV import IV
from tkinter.constants import END
import pyvisa
import time

class KT2400():
    """Class containing the Multimeter Controller for MyLab.

    """

    def __init__(self, view=None, term=None, instrument=None, model=None):
    #Constructor for the Controller class   

        self.view = view  
        self.term = term
        self.model = model

        self.progress = 0

        self.instrument = IV()
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
                    return("ERROR")

            try:
                self.instrument.ressource.write('*RST')
                self.instrument.ressource.write('*CLS')
                self.instrument.ressource.write('SYST:REM')
                self.instrument.ressource.read_termination = "\r\n"

            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    return("ERROR")

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

    def IV_test(self, args=[]):
    #this methods generates a IV characterization waveform   

        try:
            liste = self.model.openConfiguration(args[0])

        except:
            sys.stdout("    Can't open waveform file\n")
            self.view.testState = "STOP"
            return("ERROR")

        progressLength = len(liste[1])
        currentProgress = 0

        if self.instrument.state == "unreachable":
            try:
                self.instrument.ressource = self.resourceManager.open_resource(self.instrument.address)
                self.instrument.state == "free"
            except:
                if(self.instrument.state != "unreachable"):
                    self.view.view.sendError('001')
                    self.instrument.state = "unreachable"
                self.view.testState = "STOP"
                return("ERROR")

        if self.instrument.state == "free":
            if args[7] == "Voltage":

                sys.stdout("Voltage waveform\n")

                try:
                    self.instrument.ressource.write('SOUR:FUNC VOLT')
                    self.instrument.ressource.write('SENS:FUNC "CURR"')
                    self.instrument.ressource.write('SENS:CURR:PROT ' + str(args[1]))
                    self.instrument.ressource.write('OUTP ON')

                    for item in liste[1]:
                        sys.stdout("\nProgress = " + str(self.progress) + "%")
                        self.instrument.ressource.write('SOUR:VOLT ' + str(item))
                        self.instrument.ressource.write('MEAS:CURR?')
                        result = self.instrument.ressource.read()
                        result = result.split(",")

                        voltage = float(result[0])
                        sys.stdout("\n  Voltage = " + str(voltage))
                        current = float(result[1])
                        sys.stdout("\n  Current = " + str(current) + "\n")


                        self.instrument.result = current
                        self.instrument.measure["voltage"].append(voltage)
                        self.instrument.measure["current"].append(current)

                        currentProgress = currentProgress + 1
                        self.progress = (currentProgress/progressLength)*100
                    
                    self.instrument.ressource.write('SOUR:VOLT 0')
                    self.instrument.ressource.write('OUTP OFF')  

                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    self.view.testState = "STOP"
                    return("ERROR")
            
            elif args[7] =="Current":

                sys.stdout("Current waveform\n")

                try:
                    self.instrument.ressource.write('SOUR:FUNC CURR')
                    self.instrument.ressource.write('SOUR:CURR:MODE FIXED')
                    self.instrument.ressource.write('SENS:FUNC "VOLT"')
                    self.instrument.ressource.write('SENS:VOLT:PROT ' + str(args[1]))
                    self.instrument.ressource.write('OUTP ON')  

                    for item in liste[1]:
                        sys.stdout("\nProgress = " + str(self.progress) + "%")
                        self.instrument.ressource.write('SOUR:CURR:LEV ' + str(item))
                        self.instrument.ressource.write('MEAS:VOLT?')
                        result = self.instrument.ressource.read()
                        result = result.split(",")

                        voltage = float(result[0])
                        sys.stdout("\n  Voltage = " + str(voltage))
                        current = float(result[1])
                        sys.stdout("\n  Current = " + str(current) + "\n")

                        self.instrument.result = voltage
                        self.instrument.measure["voltage"].append(voltage)
                        self.instrument.measure["current"].append(current)
                        self.progress = (currentProgress/progressLength)*100

                        currentProgress = currentProgress + 1
                    
                    self.instrument.ressource.write('SOUR:CURR:LEV 0')
                    self.instrument.ressource.write('OUTP OFF')  

                except:
                    self.view.view.sendError('002')
                    self.instrument.state = "unreachable"
                    self.instrument.ressource.close()
                    self.instrument.ressource = None
                    self.view.testState = "STOP"
                    return("ERROR")

            else:
                self.view.testState = "STOP"
                return()

            self.view.graph.addLinGraph(x=self.instrument.measure["voltage"], xlabel="voltage", y=self.instrument.measure["current"], ylabel="current")
            self.view.testState = "STOP"
            self.progress = 0

        else:
            self.view.view.sendError('004')
            self.view.testState = "STOP"