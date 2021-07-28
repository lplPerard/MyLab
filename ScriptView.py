"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for ScriptView.

"""

from Instrument import Instrument
from tkinter import Canvas, Frame, LabelFrame, Scrollbar
from tkinter import Label
from tkinter import Toplevel
from tkinter import Text
from tkinter import BOTH
from tkinter import YES
from tkinter import END
from tkinter.constants import NONE, TOP


class ScriptView():
    """Class containing the GUI for a typical scripts.

    """

    def __init__(self,  view=None, controller=None, terminal=None, model=None):
    #Constructor for the Sequence_view superclass
        
        self.view = view
        self.term_text = terminal
        self.model = model
        self.controller = controller
        self.dataFrame = LabelFrame(self.view)
        self.mainCanva= Canvas(self.view, scrollregion=(0,0,0,2000), bd=0, highlightthickness=0, bg=self.model.parameters_dict['backgroundColor'])
        self.defilY_setup = Scrollbar(self.mainCanva, orient='vertical', command=self.mainCanva.yview, bg=self.model.parameters_dict['backgroundColor'])
        self.mainFrame= LabelFrame(self.mainCanva, bg=self.model.parameters_dict['backgroundColor'])

        self.label_test = Label(self.dataFrame, text="test")
        

    def initFrame(self, padx=10, pady=10):
    #This method generates the Frame's parameters for the sequence
        self.dataFrame.configure(text="Script", padx=padx, pady=pady, bg=self.model.parameters_dict['backgroundColor'])
        self.dataFrame.pack(fill="y", expand="no", side="left", anchor='nw')

        self.mainCanva.create_window(0, 0, anchor='nw', window=self.mainFrame)
        self.mainFrame.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.mainCanva.config(yscrollcommand= self.defilY_setup.set)
        self.mainCanva.pack(fill="both", expand="yes", side="left", anchor='nw')
        self.defilY_setup.pack(fill="y", side='right', padx='5') 

        self.mainFrame.pack(padx=5, pady=5, fill="both", expand="yes")

        self.label_test.pack()

    def clearFrame(self):
    #This method delete the Sequence's frame from the grid
        self.labelFrame_instrument.destroy()
        self.frame.destroy()

    def  clearInstrument(self):
        None