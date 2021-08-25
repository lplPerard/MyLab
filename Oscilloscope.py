"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Power Supply Instrument.

"""

import json
from Instrument import Instrument


class Oscilloscope(Instrument):
    """Class containing Power Supply.

    """

    def __init__(self):
    #Constructor for the Instrument Class
        Instrument.__init__(self)

        self.type = "Oscilloscope"

        self.commandList=["activateChannel"]
 
        self.channelNumber = ["Channel 1", "Channel 2", "Channel 3", "Channel 4"]
        self.channelState = [1, 0, 0, 0]         # 0 => OFF state 1 => ON state
        self.channelUsed = ["", "", "", ""]        # "" => free state 
        self.bandwidth = ["Full", "200MHz", "20MHz", "2MHz"]
        self.coupling = ["DC", "AC", "GND"]

        self.measure = {"channel_1_timebase" : [],
                        "channel_1_waveform" : [],
                        "channel_2_timebase" : [],
                        "channel_2_waveform" : [],
                        "channel_3_timebase" : [],
                        "channel_3_waveform" : [],
                        "channel_4_timebase" : [],
                        "channel_4_waveform" : [],}

        self.commandList=["setChannelState",
                          "setBandwidth",
                          "setCoupling",
                          "setOffset",
                          "setProbe",
                          "setChannelScale",
                          "setTimeScale",
                          "setPosition",
                          "getCurve",
                          "setRunStop"]
