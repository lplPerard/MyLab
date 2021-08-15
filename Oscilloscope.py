"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Power Supply Instrument.

"""

import json
from Instrument import Instrument


class Oscilloscope(Instrument):
    """Class containing Power Supply.

    """

    def __init__(self):
    #Constructor for the Instrument Class
        Instrument.__init__(self)

        self.type = "Oscilloscope"

        self.commandList=["activateChannel"]
 
        self.channelNumber = ["Channel 1", "Channel 2", "Channel 3", "Channel 4"]
        self.channelState = [0, 0, 0, 0]         # 0 => OFF state 1 => ON state
        self.channelUsed = ["", "", "", ""]        # "" => free state 
