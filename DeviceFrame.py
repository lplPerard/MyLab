"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for DeviceFrame.

"""

from tkinter import LabelFrame
from tkinter import Button
from tkinter import Toplevel
from tkinter import Text
from tkinter import BOTH
from tkinter import YES
from tkinter import END

class DeviceFrame():
    """Superclass containing the GUI for a typical testbench.

    """

    def __init__(self,  root, terminal):
    #Constructor for the Sequence_view superclass
        
        self.term_text = terminal

        self.frame = LabelFrame(root)


    def initFrame(self, text="",column=0, columnspan=1, row=0, rowspan=1, padx=15, pady=15, bg=""):
    #This method generates the Frame's parameters for the sequence
        self.frame.configure(text=text, padx=padx, pady=pady, bg=bg)
        self.frame.grid(column=column, columnspan=columnspan, row=row, rowspan=rowspan)
        
    def clearFrame(self):
    #This method delete the Sequence's frame from the grid
        self.frame.grid_forget()

