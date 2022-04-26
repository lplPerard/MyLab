"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for IV testBench Controller.

"""


import sys
import win32com.client  # Python ActiveX Client
from RFSensitivity import RFSensitivity
from tkinter.constants import END
import pyvisa
import time

class RFSensitivityController():
    """Class containing the Multimeter Controller for MyLab.

    """

    def __init__(self, view=None, term=None, instrument=None, model=None):
    #Constructor for the Controller class   

        self.view = view  
        self.term = term
        self.model = model

        self.progress = 0

        self.instrument = RFSensitivity()
        if instrument != None:
            self.instrument = instrument

    def updateView(self, view):
    #Setter method for view attribute
        self.view = view

    def RFSensitivity_testbench(self, args=[]):
    #this methods generates a IV characterization waveform 
        try:
            frequencyList = self.view.getFrequencies()
            attenuation = args[1]
            power = args[0]
            per = args[2]
            bitRate = args[7]
            self.instrument.measure["frequency"] = []
            self.instrument.measure["sensitivity"] = []

        except:
            self.view.testState = "STOP"
            sys.stdout("\nERROR while loading test parameters\n")
            return("ERROR")

        progressLength = len(frequencyList)
        currentProgress = 0  

        try:
            self.progress = 1
            for frequency in frequencyList:
                sys.stdout("\nProgress = " + str(self.progress) + "%")

                LabVIEW = win32com.client.Dispatch("Labview.Application")
                VI = LabVIEW.getvireference("C:\\Users\\Public\\Documents\\National Instruments\\TestStand 2017 (32-bit)\\Components\\StepTypes\\Oticon\\RF Measurements\\Receiver Sensitivity_Config_LUEA.vi")  # Path to LabVIEW VI
                VI._FlagAsMethod("Call")  # Flag "Call" as Method

                try:
                    VI.setcontrolvalue('Attenuation', attenuation)  # Set Input 1
                    VI.setcontrolvalue('Frequency', frequency)  # Set Input 2
                    VI.setcontrolvalue('PER only In', False)  # Set Input 3
                    VI.setcontrolvalue('PER Target in', per)  # Set Input 4
                    VI.setcontrolvalue('Power Level', power)  # Set Input 5
                    VI.setcontrolvalue('BitRate', bitRate)  # Set Input 5

                    VI.Call()  # Run the VI

                    self.instrument.measure["frequency"].append(frequency)
                    sensitivity = VI.getcontrolvalue('Level@PER Target')
                    self.instrument.measure["sensitivity"].append(sensitivity)

                    sys.stdout("\nFrequency : " + str(frequency))
                    sys.stdout("\n  Sensitivity : " + str(sensitivity) + " dBm\n")

                except:
                    sys.stdout("\nError during VI'execution\n")
                    self.view.testState = "STOP"
                    return("ERROR")

                currentProgress = currentProgress + 1
                self.progress = (currentProgress/progressLength)*100
            
            self.progress = 0
            sys.stdout("\nProgress = 100%")
            sys.stdout("\nRF Sensitivity test is finished\n")
            self.view.testState = "STOP"

        except:
            sys.stdout("\n    Impossible to start the VI\n")
            self.view.testState = "STOP"
            return("ERROR")