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

        self.measure_state = 0