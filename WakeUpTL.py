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

    def __init__(self, frame, view, model=None):
    #Constructor for the Paramaters class

        self.frame = Frame(frame)
        self.view = view
        self.model = model

        self.frame.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.initWidgets()

    def initWidgets(self):
    #This method init widgets displayed by main Frame

        self.text = Label(self.frame, text="Please choose an instrument or a configuration : ", bg=self.model.parameters_dict['backgroundColor'])
        self.text.pack(pady=15)

        self.combo_instrument = Combobox(self.frame, state="readonly", width=20, values=["Configuration",
                                                                                         "Power Supply",
                                                                                         "Oscilloscope",
                                                                                         "Source Meter",
                                                                                         "Multimeter",
                                                                                         "Waveform Generator",
                                                                                         "Climatic Chamber",
                                                                                         "VNA"])
        self.combo_instrument.configure(background="white")
        self.combo_instrument.pack(pady=5)
        self.combo_instrument.current(0)

        self.button = Button(self.frame, text="Start", command=self.button_onclick, padx=10)
        self.button.pack(pady=5)

    def button_onclick(self):
        if self.combo_instrument.get() == "Configuration":
            self.view.topLevel_wakeUp.withdraw()
            self.view.menu1_Open_callBack()
        else:
            self.view.listViews.clear()
            self.view.addDeviceFrame(self.combo_instrument.get())
            self.view.topLevel_wakeUp.withdraw()
