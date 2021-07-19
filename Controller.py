"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Controller.

"""


from Instrument import Instrument
from View import View
from Model import Model

import pyvisa
from serial import Serial
import serial.tools.list_ports as port_list

class Controller():
    """Class containing the Controller for MyLab.

    """

    def __init__(self):
    #Constructor for the Controller class     

        self.instrument = Instrument()
        self.instrList=[]
        
        self.model = Model(self)
        self.view = View(controller=self, model=self.model)
        self.view.mainloop()

    def VISA_connect(self):
    #This method is used to connect to VISA
        try:
            self.resourceManager = pyvisa.ResourceManager()
            self.findVISAInstruments()

        except:
            self.view.sendError("000")

    def findVISAInstruments(self):
    #This method detects instruments connected via VISA
        try:
            self.instrList = self.resourceManager.list_resources()
        except:
            self.instrList = []
            self.view.sendError("001")

    def SERIAL_connect(self):
    #This method is used to connect to a serial instrument
        None
            
    def findSERIALInstruments(self):
    #This method detects instruments connected via VISA
        ports = list(port_list.comports())
        self.instrList = []
        for p in ports:
            self.instrList.append(p)
