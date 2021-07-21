"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Power Supply Instrument.

"""

import json
from Instrument import Instrument


class PowerSupply(Instrument):
    """Class containing Power Supply.

    """

    def __init__(self):
    #Constructor for the Instrument Class
        Instrument.__init__(self)

        self.type = "Power Supply"
 
        self.channelNumber = ["1", "2"]
        self.channelState = [0, 0]         # 0 => OFF state 1 => ON state
        self.channelUsed = ["", ""]        # "" => free state 

        self.source_voltage = 0
        self.source_current = 0
