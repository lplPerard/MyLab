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

    def __init__(self, frame, view):
    #Constructor for the Paramaters class

        self.frame = Frame(frame)
        self.view = view
        self.model = self.view.model
        self.controller = self.view.controller

        self.initAttributes()
        self.initWidgets()
        self.controller.VISA_connect()

    def initAttributes(self):
    #This method instanciate all attributes
        self.frame.pack(fill="both", expand="yes")

        self.combo_instrumentName = Combobox(self.frame, state="readonly", width=20)

        self.combo_type = Combobox(self.frame, state="readonly", width=20, values=["All",
                                                                                   "USB",
                                                                                   "Ethernet"])

        self.list_devices = Listbox(self.frame, selectmode='single', width=30)

        self.button_actualize = Button(self.frame, text="Actualize", command=self.button_actualize_onclick)
        self.button_select = Button(self.frame, text="Select", command=self.button_select_onclick)

    def initWidgets(self):
    #This method initiates all widgets
        self.frame.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.combo_instrumentName.pack(pady=10)
        self.combo_instrumentName.bind('<<ComboboxSelected>>', self.button_actualize_onclick)
        self.combo_type.current(0)
        self.combo_type.pack(pady=10)

        self.list_devices.pack(pady=5, expand='yes')
        for item in self.view.controller.instrList:
            self.list_devices.insert('end', item)

        self.button_actualize.pack(side="left", pady=5, padx=5)

        self.button_select.pack(side="right", pady=5, padx=5)

    def button_actualize_onclick(self, args=None):
    #This method is called when user clicks on actualize    
        index=self.combo_instrumentName.current() 
        
        if self.view.listViews[index].controller.instrument.type == "Climatic Chamber":
            self.controller.findSERIALInstruments()
            self.list_devices.delete(0, 'end')
            for item in self.view.controller.instrList:
                self.list_devices.insert('end', item)
        else:
            self.controller.VISA_connect()
            self.list_devices.delete(0, 'end')
            for item in self.view.controller.instrList:
                self.list_devices.insert('end', item)
            self.list_devices.insert('end', 'TCPIP0::192.168.0.5::3490::SOCKET')
            self.list_devices.insert('end', 'TCPIP0::169.254.1.1::3490::SOCKET')

    def button_select_onclick(self):
    #This method is called when user clicks on select

        index = self.combo_instrumentName.current()
        self.view.listViews[index].controller.instrument.address = self.list_devices.get(ANCHOR)
        
        if self.view.listViews[self.combo_instrumentName.current()].controller.instrument.address != "":
            self.view.topLevel_connect.withdraw()
            self.view.term_text.insert(END, "address changed for : " + self.view.listViews[index].controller.instrument.name + "\n")   
            self.view.term_text.insert(END, "   New address is : " + self.view.listViews[index].controller.instrument.address + "\n")   
            self.view.listViews[self.combo_instrumentName.current()].controller.instrument.state="free"  
            self.view.listViews[self.combo_instrumentName.current()].state="changed"  
            self.view.refresh()

    def actualizeInstruments(self):
        list=[]
        for item in self.view.listViews:
            list.append(item.controller.instrument.name)

        self.combo_instrumentName.configure(values=list)
        self.combo_instrumentName.current(0)
        self.button_actualize_onclick()