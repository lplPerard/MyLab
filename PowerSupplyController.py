"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Power Supply Controller.

"""


from Instrument import Instrument
import pyvisa

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
        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.adress)
            self.instrument.ressource.write('*RST')
            self.instrument.ressource.write('*CLS')
            self.instrument.ressource.close()
        except:
            self.term.insert("end", "error")

    def setVoltageSource(self, voltage, calibre=0):
    #This method modify the voltage source

        try:
            self.instrument.ressource = self.resourceManager.open_resource(self.instrument.adress)
            self.instrument.ressource.write('SOUR:VOLT:LEV:IMM:AMP' + str(voltage))
        except:
            self.term.insert("end", "error")




        