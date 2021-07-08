"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for ConnectionsTL.

"""

from tkinter import LabelFrame
from Model import Model

class ConnectionsTL():
    """Class containing a GUI for Parameters attributes

    """

    def __init__(self, root):
    #Constructor for the Paramaters class

        self.frame = LabelFrame(root, text="Connections")
        self.model = Model()
        self.frame.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.show = True