"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Multimeter Instrument.

"""

from Instrument import Instrument


class IV(Instrument):
    """Class containing Multimeter.

    """

    def __init__(self):
    #Constructor for the Instrument Class
        Instrument.__init__(self)

        self.type = "IV"
        self.waveform = ""
        self.source = "Current"
        self.limit = 0

        self.measure = {"voltage" : [],
                        "current" : []}

        self.commandList=["IV_test"]