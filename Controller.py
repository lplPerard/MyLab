"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Controller.

"""


from Instrument import Instrument
from View import View
from Model import Model

import pyvisa

class Controller():
    """Class containing the Controller for MyLab.

    """

    def __init__(self):
    #Constructor for the Controller class     

        self.instrument = Instrument()
        self.instrList=["null"]
        
        self.model = Model(self)
        self.view = View(controller=self, model=self.model)
        self.view.mainloop()

    def VISA_connect(self):
    #This method is used to connect to VISA
        try:
            self.resourceManager = pyvisa.ResourceManager()
            self.findInstruments()

        except:
            self.view.sendError("000")

    def findInstruments(self):
    #This method detects instruments connected via VISA
        try:
            self.instrList = self.resourceManager.list_resources()
        except:
            self.instrList = []
            self.view.sendError("001")
