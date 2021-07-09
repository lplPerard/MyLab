"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the POwerSupply instrument's View.

"""

from DeviceFrame import DeviceFrame

from tkinter import Label
from tkinter import LabelFrame
from tkinter import Button
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import IntVar
from tkinter import Entry
from tkinter import messagebox
from tkinter.ttk import Combobox

class PowerSupplyView (DeviceFrame):
    """Class containing the PowerSupply's View

    """

    def __init__(self, root, terminal, model):
    #Constructor for the PowerSupply's View

        DeviceFrame.__init__(self, root, terminal, model)
        self.instrument.type = "Power Supply"

        self.initFrame(text=self.instrument.type)
        
        self.text = Label(self.frame, text="Power supply to come !")
        self.text.pack()

