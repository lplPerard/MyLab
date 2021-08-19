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
      
    def generateArguments(self, args1="", args2="", args3="", args4="", args5="", args6="", args7="", args8="", args9="", args10="", args11="", args12="", args13="", args14=""):
    #This method generates a list of argument
        liste = [""]*14

        liste[0] = args1
        liste[1] = args2
        liste[2] = args3
        liste[3] = args4
        liste[4] = args5
        liste[5] = args6
        liste[6] = args7
        liste[7] = args8
        liste[8] = args9
        liste[9] = args10
        liste[10] = args11
        liste[11] = args12
        liste[12] = args13
        liste[13] = args14

        return(liste)