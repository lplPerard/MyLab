"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for CommandLine

"""

from tkinter.ttk import Combobox
from Instrument import Instrument
from tkinter import Canvas, Frame, LabelFrame, Scrollbar
from tkinter import Label
from tkinter import Toplevel
from tkinter import Text
from tkinter import BOTH
from tkinter import YES
from tkinter import END
from tkinter.constants import NONE, TOP


class CommandLine():
    """Class containing the GUI for a Command Lines in Scripts.

    """

    def __init__(self,  frame=None,  root=None, controller=None, terminal=None, model=None, number=999):
    #Constructor for the Sequence_view superclass
        
        self.frame = frame
        self.term_text = terminal
        self.model = model
        self.controller = controller
        self.number=number
        self.root=root

        self.line = Frame(self.frame, bg=self.model.parameters_dict['backgroundColorCommandLine'])
        self.line.pack(fill="x", expand="no", side="top", anchor='nw', pady=2)

        self.label_number = Label(self.line, text=str(self.number), bg=self.model.parameters_dict['backgroundColorCommandLine'])
        self.label_number.pack(expand="no", side="left", anchor='nw', padx=2)

        self.combo_choice1 = Combobox(self.line, value=['WAIT', 'FOR', 'END'], postcommand=self.combo_choice1_callback)
        self.combo_choice1.bind("<<ComboboxSelected>>", self.combo_choice1_callback)
        self.combo_choice1.configure(background='white')
        self.combo_choice1.current(0)
        self.combo_choice1.pack(expand="no", side="left", anchor='nw', padx=2)
        

    def combo_choice1_callback(self):
        liste = ['WAIT', 'FOR', 'END']
        for item in self.root.getInstrList():
            liste.insert(0, item.name)

        self.combo_choice1.configure(value=liste)
