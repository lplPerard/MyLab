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

        self.signal_waveform = "Sinus"
        self.signal_frequency = 1000
        self.signal_frequency_caliber = "Hz"
        self.signal_amplitude = 1
        self.signal_amplitude_caliber = "V"
        self.signal_offset = 0
        self.signal_offset_caliber = "V"
        self.signal_phase = 0
        self.signal_phase_caliber = "deg"
        self.signal_dutyCycle = 50
        self.signal_dutyCycle_caliber = "%"
        self.signal_pulseWidth = 1
        self.signal_pulseWidth_caliber = "s"
        self.signal_riseTime = 0
        self.signal_riseTime_caliber = "s"
        self.signal_fallTime = 0
        self.signal_fallTime_caliber = "s"
        self.signal_symetry = 50
        self.signal_symetry_caliber = "%"
        self.signal_bandwidth = 1000
        self.signal_bandwidth_caliber = "Hz"
        self.signal_modulation_state = 1
        self.signal_sweep_state = 1

        self.modulation_type = "AM"
        self.modulation_source = "Internal"
        self.modulation_shape = "Sinus"

        self.sweep_type = "Linear"
        self.sweep_time = 1
        self.sweep_time_caliber = "s"
        self.sweep_startFrequency = 1
        self.sweep_startFrequency_caliber = "Hz"
        self.sweep_stopFrequency = 1000
        self.sweep_stopFrequency_caliber = "Hz"
        self.sweep_holdTime = 0
        self.sweep_holdTime_caliber = "s"
        self.sweep_returnTime = 0
        self.sweep_returnTime_caliber = "s"

        self.output_state = 1 