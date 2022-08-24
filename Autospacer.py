"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Climatic Chamber Instrument.

"""

from Instrument import Instrument


class Autospacer(Instrument):
    """Class containing Power Supply.

    """

    def __init__(self):
    #Constructor for the Instrument Class
        Instrument.__init__(self)

        self.type = "Autospacer"
        self.commandList = ["calibrate",
                            "selectMagnet",
                            "placeMagnet",
                            "setDistance"]

        self.measure = {"Distance" : []}
 