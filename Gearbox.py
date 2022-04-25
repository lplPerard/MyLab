"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Climatic Chamber Instrument.

"""

from Instrument import Instrument


class Gearbox(Instrument):
    """Class containing Power Supply.

    """

    def __init__(self):
    #Constructor for the Instrument Class
        Instrument.__init__(self)

        self.type = "Gearbox"
        self.image = ""
        
        self.commandList = ["Open_connection", 
                            "Close_connection",
                            "Read_device_info",
                            "Read_identity",
                            "Read_serial_number",
                            "Identify_FE_chip",
                            "Identify_DSP_chip",
                            "Identify_RF_chip",
                            "BLE_DTM_StartTX",
                            "BLE_DTM_StartRX",
                            "BLE_DTM_EndTest",
                            "EAS_set_generator_output",
                            "init_XP",
                            "getClock_XP",
                            "getID_XP",
                            "getVunreg_XP",
                            "stopCMD",
                            "Custom",
                            "CustomRead"]
                            
        self.measure = {"Custom" : [],
                        "SerialNumber" : [],
                        "Identify_FE" : [],
                        "Identify_DSP" : [],
                        "Identify_RF" : [],
                        "BLE_DTM_RX" : []}