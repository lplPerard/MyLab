"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Instrument.

"""

class Instrument():
    """Class containing Instrument specification.

    """

    def __init__(self):
    #Constructor for the Instrument Class

        self.name = ""
        self.type = ""
        self.connectMode = ""
        self.address = ""
        self.state = "off"

        self.channelNumber = ["1"]

        self.ressource = None