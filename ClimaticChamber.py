"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Climatic Chamber Instrument.

"""

from Instrument import Instrument


class ClimaticChamber(Instrument):
    """Class containing Power Supply.

    """

    def __init__(self):
    #Constructor for the Instrument Class
        Instrument.__init__(self)

        self.type = "Climatic Chamber"
        self.ident = ""
        self.temperatureSource = 25
        
        self.commandList = ["setTemperature",
                            "getTemperature"]

        self.measure = {"temperature" : []}
 