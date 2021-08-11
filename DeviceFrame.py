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

    def initFrame(self, text="", padx=15, pady=0):
    #This method generates the Frame's parameters for the sequence
        self.frame.configure(text=text, font=("bold", 12), padx=padx, pady=pady, bg=self.model.parameters_dict['backgroundColorInstrument'],
                                                                                 bd=self.model.parameters_dict['instrumentBorderwidth'])
        self.frame.pack(fill="y", expand="no", side="left", anchor='nw', pady=5)

        self.labelFrame_instrument = LabelFrame(self.frame, text="Instrument", bg=self.model.parameters_dict['backgroundColorInstrumentData'])

    def clearFrame(self):
    #This method delete the Sequence's frame from the grid
        self.labelFrame_instrument.destroy()
        self.frame.destroy()

    def  clearInstrument(self):
        None