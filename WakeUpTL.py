"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for WakeUpTL.

"""

from tkinter import Frame
from tkinter import Label
from tkinter.constants import BOTTOM, TOP
from tkinter.ttk import Combobox
from tkinter import Button

class WakeUpTL():
    """Class containing a GUI for Parameters attributes

    """

    def __init__(self, root, View, model=None):
    #Constructor for the Paramaters class

        self.frame = Frame(root)
        self.view = View
        self.model = model
        self.frame.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.initWidgets()

    def initWidgets(self):
    #This method init widgets displayed by main Frame

        self.text = Label(self.frame, text="Please choose an instrument type to start : ", bg=self.model.parameters_dict['backgroundColor'])
        self.text.pack(pady=15)

        self.combo_instrument = Combobox(self.frame, state="readonly", width=20, values=["Power Supply",
                                                                                   "Oscilloscope",
                                                                                   "Source Meter",
                                                                                   "Multimeter",
                                                                                   "RLC Meter",
                                                                                   "Climatic Chamber",
                                                                                   "VNA"])
        self.combo_instrument.configure(background="white")
        self.combo_instrument.pack(pady=5)
        self.combo_instrument.current(0)

        self.button = Button(self.frame, text="Start", command=self.button_onclick, padx=10)
        self.button.pack(pady=5)

    def button_onclick(self):
        self.view.frame.clearFrame()
        self.view.changeDeviceFrame(self.combo_instrument.get())
        self.view.topLevel_wakeUp.withdraw()
