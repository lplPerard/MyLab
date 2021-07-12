"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for ConnectionsTL.

"""

from tkinter import Frame
from tkinter.constants import ACTIVE, ANCHOR, END
from tkinter.ttk import Combobox
from tkinter import Listbox
from tkinter import Button
from Model import Model

class ConnectionsTL():
    """Class containing a GUI for Parameters attributes

    """

    def __init__(self, root, view):
    #Constructor for the Paramaters class

        self.frame = Frame(root)
        self.view = view
        self.model = self.view.model

        self.frame.pack(fill="both", expand="yes")
        self.frame.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.combo_instrumentName = Combobox(self.frame, state="readonly", width=20)
        self.combo_instrumentName.pack(pady=10)

        self.combo_type = Combobox(self.frame, state="readonly", width=20, values=["All",
                                                                                   "USB",
                                                                                   "Ethernet"])
        self.combo_type.current(0)
        self.combo_type.pack(pady=10)

        self.list_devices = Listbox(self.frame, selectmode='single')
        self.list_devices.pack(pady=5, expand='yes')

        self.button_actualize = Button(self.frame, text="Actualize", command=self.button_actualize_onclick)
        self.button_actualize.pack(side="left", pady=5, padx=30)
        self.button_actualize_onclick()

        self.button_select = Button(self.frame, text="Select", command=self.button_select_onclick)
        self.button_select.pack(side="right", pady=5, padx=30)

    def button_actualize_onclick(self):
    #This method is called when user clicks on actualize 
        self.view.controller.VISA_connect()

        self.list_devices.delete(0, 'end')
        for item in self.view.controller.instrList:
            self.list_devices.insert('end', item)

    def button_select_onclick(self):
    #This method is called when user clicks on select

        index = self.combo_instrumentName.current()
        self.view.listInstruments[index].controller.instrument.adress = self.list_devices.get(ANCHOR)
        
        if self.view.listInstruments[self.combo_instrumentName.current()].controller.instrument.adress != "":
            self.view.topLevel_connect.withdraw()
            self.view.term_text.insert(END, "Adress changed for : " + self.view.listInstruments[index].controller.instrument.name + "\n")   
            self.view.term_text.insert(END, "   New adress is : " + self.view.listInstruments[index].controller.instrument.adress + "\n")    
            self.view.refresh()

    def actualizeInstruments(self):
        list=[]
        for item in self.view.listInstruments:
            list.append(item.controller.instrument.name)

        self.combo_instrumentName.configure(values=list)
        self.combo_instrumentName.current(0)