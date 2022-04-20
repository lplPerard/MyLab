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

import sys

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
        tmp = self.controller.VISA_connect()
        if tmp == "ERROR":
            self.view.sendError("000")

    def initAttributes(self):
    #This method instanciate all attributes
        self.frame.pack(fill="both", expand="yes")

        self.combo_instrumentName = Combobox(self.frame, state="readonly", width=35, postcommand=self.actualizeInstruments)

        self.combo_type = Combobox(self.frame, state="readonly", width=35, values=["VISA - All",
                                                                                   "VISA - USB",
                                                                                   "VISA - GPIB",
                                                                                   "VISA - Ethernet",
                                                                                   "Serial"])

        self.list_devices = Listbox(self.frame, selectmode='single', width=40)

        self.button_actualize = Button(self.frame, text="Actualize", command=self.button_actualize_onclick)
        self.button_select = Button(self.frame, text="Select", command=self.button_select_onclick)

    def initWidgets(self):
    #This method initiates all widgets
        self.frame.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.combo_instrumentName.pack(pady=10)
        self.combo_instrumentName.bind('<<ComboboxSelected>>', self.button_actualize_onclick)

        self.combo_type.bind('<<ComboboxSelected>>', self.button_actualize_onclick)
        self.combo_type.current(0)
        self.combo_type.pack(pady=10)

        self.list_devices.pack(pady=5, expand='yes')
        for item in self.view.controller.instrList:
            self.list_devices.insert('end', item)

        self.button_actualize.pack(side="left", pady=5, padx=5)

        self.button_select.pack(side="right", pady=5, padx=5)

    def button_actualize_onclick(self, args=None):
    #This method is called when user clicks on actualize
        try :

            if self.combo_type.current() == 0 :
                self.controller.VISA_connect()
                self.list_devices.delete(0, 'end')
                self.filterByName(":")
                #self.list_devices.insert('end', 'TCPIP0::192.168.0.1::3490::SOCKET')

            elif self.combo_type.current() == 1 :
                self.controller.VISA_connect()
                self.list_devices.delete(0, 'end')
                self.filterByName("USB")

            elif self.combo_type.current() == 2 :
                self.controller.VISA_connect()
                self.list_devices.delete(0, 'end')
                self.filterByName("GPIB")

            elif self.combo_type.current() == 3 :
                self.controller.VISA_connect()
                self.list_devices.delete(0, 'end')
                self.filterByName("TCPIP")
                #self.list_devices.insert('end', 'TCPIP0::192.168.0.1::3490::SOCKET')


            elif self.combo_type.current() == 4 :
                self.controller.findSERIALInstruments()
                self.list_devices.delete(0, 'end')
                for item in self.view.controller.instrList:
                    self.list_devices.insert('end', item)

        except:
            None

    def button_select_onclick(self):
    #This method is called when user clicks on select
        index = self.combo_instrumentName.current()
        self.view.listViews[index].controller.instrument.address = self.list_devices.get(ANCHOR)
        
        if self.view.listViews[self.combo_instrumentName.current()].controller.instrument.address != "":
            self.view.topLevel_connect.withdraw()
            sys.stdout("address changed for : " + self.view.listViews[index].controller.instrument.name + "\n")   
            sys.stdout("   New address is : " + self.view.listViews[index].controller.instrument.address + "\n")   
            self.view.listViews[self.combo_instrumentName.current()].updateView()

    def actualizeInstruments(self):
    #This method
        list = []
        instrList=self.view.getInstrList()
        instrList.reverse()    
        index=self.combo_instrumentName.current() 
        

        for item in instrList:
            list.append(item.name)

        self.combo_instrumentName.configure(values=list)

        try:
            self.combo_instrumentName.current(0)
        except:
            None

        if instrList[index].type == "Climatic Chamber":
            self.combo_type.current(4)
        
        elif instrList[index].type == "Autospacer":
            self.combo_type.current(4)

        else :
            self.combo_type.current(0)

        self.button_actualize_onclick()

    def setCurrentInstrument(self, name):
    #This method
        i=0
        instrList=self.view.getInstrList()
        instrList.reverse()  

        for item in self.view.listViews:
            if item == name:
                self.combo_instrumentName.current(i)
                break
            i+=1

        index=self.combo_instrumentName.current() 

        if instrList[index].type == "Climatic Chamber":
            self.combo_type.current(4)
        
        elif instrList[index].type == "Autospacer":
            self.combo_type.current(4)

        else :
            self.combo_type.current(0)

        self.button_actualize_onclick()

    def filterByName(self, name):
    #This method
        for item in self.view.controller.instrList:
            if (item.find(name) != -1) and (item.find("ASRL") == -1):
                self.list_devices.insert('end', item)