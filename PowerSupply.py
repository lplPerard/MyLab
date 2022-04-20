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
        self.ident = ""

        self.source_voltage = 0
        self.source_current = 0

        self.commandList=["setVoltageSource",
                          "setCurrentLimit",
                          "setChannelState",
                          "setMasterState",
                          "MeasureVoltage",
                          "MeasureCurrent",
                          "MeasurePower"]

        self.measure = {"voltage_C1" : [],
                        "current_C1" : [],
                        "power_C1" : [],
                        "voltage_C2" : [],
                        "current_C2" : [],
                        "power_C2" : [],
                        "voltage_C3" : [],
                        "current_C3" : [],
                        "power_C3" : [],
                        "voltage_C4" : [],
                        "current_C4" : [],
                        "power_C4" : []}

