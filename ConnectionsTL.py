"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for ConnectionsTL.

"""

from tkinter import Frame
from tkinter.ttk import Combobox
from tkinter import Listbox
from tkinter import Button
from Model import Model

class ConnectionsTL():
    """Class containing a GUI for Parameters attributes

    """

    def __init__(self, root):
    #Constructor for the Paramaters class

        self.frame = Frame(root)
        self.model = Model()

        self.frame.pack(fill="both", expand="yes")
        self.frame.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.combo_type = Combobox(self.frame, state="readonly", width=20, values=["USB",
                                                                                   "Ethernet"])
        self.combo_type.current(0)
        self.combo_type.pack(pady=10)

        self.list_devices = Listbox(self.frame)
        self.list_devices.insert(1,"")
        self.list_devices.pack(pady=5)

        self.button_actualize = Button(self.frame, text="Actualize")
        self.button_actualize.pack(side="left", pady=5, padx=30)

        self.button_select = Button(self.frame, text="Select")
        self.button_select.pack(side="right", pady=5, padx=30)