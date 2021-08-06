"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Command.

"""


class Command():
    """Class containing Command.

    """

    def __init__(self):
    #Constructor for the Instrument Class
        
        self.combo_choice1 = ""
        self.combo_instrCommand = ""
        
        self.entry_attribute1 = ""
        self.entry_attribute2 = ""
        self.entry_attribute3 = ""
        self.entry_attribute4 = ""
        self.entry_attribute5 = ""
        self.entry_attribute6 = ""
        self.entry_attribute7 = ""

        self.combo_attribute1 = ""
        self.combo_attribute2 = ""
        self.combo_attribute3 = ""
        self.combo_attribute4 = ""
        self.combo_attribute5 = ""
        self.combo_attribute6 = ""
        self.combo_attribute7 = ""

        self.state = "FREE"
        self.forstate = 0