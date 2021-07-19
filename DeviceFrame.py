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

    def __init__(self,  view=None, controller=None, terminal=None, model=None):
    #Constructor for the Sequence_view superclass
        
        self.view = view
        self.term_text = terminal
        self.model = model
        self.controller = controller
        self.frame = LabelFrame(view)

    def initFrame(self, text="", padx=10, pady=10):
    #This method generates the Frame's parameters for the sequence
        self.frame.configure(text=text, padx=padx, pady=pady, bg=self.model.parameters_dict['backgroundColor'])
        self.frame.pack(fill="y", expand="yes", side="left")

        self.labelFrame_instrument = LabelFrame(self.frame, text="Instrument", bg=self.model.parameters_dict['backgroundColor'])

    def clearFrame(self):
    #This method delete the Sequence's frame from the grid
        self.labelFrame_instrument.destroy()
        self.frame.destroy()

    def updateView(self):
    #This method update the content of a device Frame
        self.view.sendError("404")
            
    def clearInstrument(self):
    #This method is used to clear every trace of this instrument before being deleted
        None