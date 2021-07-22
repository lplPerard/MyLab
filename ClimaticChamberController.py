"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Climatic Chamber Controller.

"""


from ClimaticChamber import ClimaticChamber
import pyvisa

class ClimaticChamberController():
    """Class containing the PowerSupplyController for MyLab.

    """

    def __init__(self, view=None, term=None, instrument=None):
    #Constructor for the Controller class   

        self.view = view  
        self.term = term

        self.instrument = ClimaticChamber()
        if instrument != None:
            self.instrument = instrument
        #self.resourceManager = pyvisa.ResourceManager()
    
    def updateView(self, view):
    #Setter method for view attribute
        self.view = view