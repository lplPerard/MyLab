"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Instrument.

"""

import json


class Instrument():
    """Class containing Instrument specification.

    """

    def __init__(self):
    #Constructor for the Instrument Class
        
        self.type = ""
        self.name = ""
        self.address = ""
        
        self.masterState = 0 # 0 => OFF state 1 => ON state
        self.state = "free"
        #self.id = ""
        self.ressource = None

        self.commandList = ["To be updated"]
        self.result = ["To be updated"]

        