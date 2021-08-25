"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Multimeter Instrument.

"""

from Instrument import Instrument


class Sourcemeter(Instrument):
    """Class containing Multimeter.

    """

    def __init__(self):
    #Constructor for the Instrument Class
        Instrument.__init__(self)

        self.type = "Sourcemeter"

        self.measure_voltage = 0
        self.measure_current = 0
        self.measure_resistance = 0

        self.masterState = 0

        self.measure = {"voltage" : [],
                        "current" : [],
                        "resistance" : []}

        self.commandList=["setVoltageSource",
                          "setCurrentSource",
                          "generateVoltageWaveform",
                          "generateCurrentWaveform",
                          "setMasterState"]