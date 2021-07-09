"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Power Supply Controller.

"""


from Instrument import Instrument

import pyvisa

class PowerSupplyController():
    """Class containing the PowerSupplyController for MyLab.

    """

    def __init__(self):
    #Constructor for the Controller class     

        self.instrument = Instrument()