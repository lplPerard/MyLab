"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for DeviceFrame.

"""

from Instrument import Instrument
from tkinter import LabelFrame
from tkinter import Label
from tkinter import Toplevel
from tkinter import Text
from tkinter import BOTH
from tkinter import YES
from tkinter import END
from tkinter.constants import NONE, TOP


class DeviceFrame():
    """Superclass containing the GUI for a typical testbench.

    """

    def __init__(self,  root, terminal=None, model=None):
    #Constructor for the Sequence_view superclass
        
        self.term_text = terminal
        self.model = model
        self.frame = LabelFrame(root)


    def initFrame(self, text="", padx=15, pady=15, bg=""):
    #This method generates the Frame's parameters for the sequence
        self.frame.configure(text=text, padx=padx, pady=pady, bg=self.model.parameters_dict['backgroundColor'])
        self.frame.pack(fill="both", expand="yes")

    def clearFrame(self):
    #This method delete the Sequence's frame from the grid
        self.frame.destroy()
