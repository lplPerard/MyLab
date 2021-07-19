"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Waveform Generator Instrument.

"""

from Instrument import Instrument


class WaveformGenerator(Instrument):
    """Class containing Waveform Generator.

    """

    def __init__(self):
    #Constructor for the Instrument Class
        Instrument.__init__(self)

        self.type = "Waveform Generator"
 