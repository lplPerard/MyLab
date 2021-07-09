"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for ParametersTL.

"""

from tkinter import LabelFrame
from Model import Model

class ParametersTL():
    """Class containing a GUI for Parameters attributes

    """

    def __init__(self, root, model):
    #Constructor for the Paramaters class

        self.frame = LabelFrame(root, text="Parameters")
        self.model = model
        self.frame.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.show = True