"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Multimeter Instrument.

"""

from Instrument import Instrument


class Multimeter(Instrument):
    """Class containing Multimeter.

    """

    def __init__(self):
    #Constructor for the Instrument Class
        Instrument.__init__(self)

        self.type = "Multimeter"

        self.measure_DCV = 0
        self.measure_ACV = 0
        self.measure_DCI = 0
        self.measure_ACI = 0
        self.measure_2WR = 0
        self.measure_4WR = 0
        self.measure_diode = 0
        self.measure_frequency = 0
        self.measure_period = 0

        self.measure = {"DC_voltage" : [],
                        "DC_current" : [],
                        "AC_voltage" : [],
                        "AC_current" : [],
                        "2W_resistance" : [],
                        "4W_resistance" : [],
                        "diode" : [],
                        "frequency" : [],
                        "period" : []}

        self.masterState = 0

        self.commandList=["setDCV",
                          "setACV",
                          "setDCI",
                          "setACI",
                          "set2WR",
                          "set4WR",
                          "setDiode",
                          "setFrequency",
                          "setPeriod",
                          "measureDCV",
                          "measureACV",
                          "measureDCI",
                          "measureACI",
                          "measure2WR",
                          "measure4WR",
                          "measureDiode",
                          "measureFrequency",
                          "measurePeriod"]