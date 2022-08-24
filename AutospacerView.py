"""
Developped by : Luc PERARD

File description : Class container for the Autospacer instrument's View.

"""
from os import listdir

from tkinter.constants import END
from DeviceFrame import DeviceFrame

from tkinter import Button, Frame, Label, StringVar, filedialog
from tkinter import Entry
from tkinter.ttk import Combobox
from PIL import Image, ImageTk

from threading import Thread

class AutospacerView (DeviceFrame):
    """Class containing the Autospacer's View

    """

    def __init__(self, view, frame, terminal, model, controller, name):
    #Constructor for the Autospacer's View

        DeviceFrame.__init__(self, frame, controller, terminal, model)

        self.controller.instrument.name = name
        self.view=view

        self.initFrame(text=self.controller.instrument.type)
        self.initAttributes()
                
        self.initLabelFrame()
        self.initFrameLine()
        self.initVar()
        self.initLabel()
        self.initEntries()

    def updateView(self, configuration=False):
    #This method refresh the content of the view
        self.stringvar_instrumentPort.set(self.controller.instrument.address)

        for item in self.model.devices_dict:
            if item in self.controller.instrument.address:
                newName = self.model.devices_dict[item][0] + " (0)"
                self.entry_instrumentName_callback(newName=newName)

        self.renameInstrument()
    
    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage     
        self.state="CLOSE"

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)
        self.frame_instrument_button = Frame(self.labelFrame_instrument)

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name   : ")
        self.label_instrumentPort = Label(self.frame_instrument_address, text="Port    : ")

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentPort = StringVar()   

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName, width=30)
        self.entry_instrumentPort = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentPort, width=30)

        self.button_set = Button(self.frame_instrument_button, text='Open Connection', command=self.button_set_callback)
        self.button_close = Button(self.frame_instrument_button, text='Close Connection', command=self.button_close_callback)

        self.img = Image.open("Images/autospacer.png")
        self.img = self.img.resize((300, 240), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.breakpointImg = Image.open("Images/breakpoint.png")
        self.breakpointImg = self.breakpointImg.resize((15, 15), Image.ANTIALIAS)
        self.breakpointImg = ImageTk.PhotoImage(self.breakpointImg)

        self.connectImg = Image.open("Images/connect.png")
        self.connectImg = self.connectImg.resize((15, 15), Image.ANTIALIAS)
        self.connectImg = ImageTk.PhotoImage(self.connectImg)

        self.connect_point = Label(self.frame_instrument_button, image=self.breakpointImg, bg=self.model.parameters_dict['backgroundColorInstrumentData'])
             
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=5, fill="y")
        
        self.panel.pack(fill = "both", expand = "yes")

    def initFrameLine(self):
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_address.pack(fill="both", pady=3)

        self.frame_instrument_button.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_button.pack(fill="both", pady=5)

    def initVar(self):
    #This methods instanciates all the Var
        self.stringvar_instrumentName.set(self.controller.instrument.name) 
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentName.pack(side="left")

        self.label_instrumentPort.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentPort.pack(side="left")

        self.button_set.pack(side="left", pady=5, padx=5, expand="true")
        self.button_close.pack(side="left", pady=5, padx=5, expand="true")

        self.connect_point.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.connect_point.pack(side="left", pady=5, padx=5, fill="y")

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_instrumentPort.bind('<Double-Button-1>', lambda event, name=self : self.view.menu2_Connections_callBack(event, name))
        self.entry_instrumentPort.pack(side='right', padx=5)

    def entry_instrumentName_callback(self, arg=None, newName=None):
    #This method calls the view to change instrument name
        oldname = self.controller.instrument.name
        if newName == None:
            name = self.stringvar_instrumentName.get()
        else:
            name = newName
            self.stringvar_instrumentName.set(name)
        self.controller.instrument.name = name
        indexMenu = self.view.menu5.index(oldname)
        self.view.menu5.entryconfigure(indexMenu, label=name)
 
    def button_set_callback(self):
    #This method call the controller to change output state 
        if self.state == "CLOSE":
            if self.controller.connectToDevice(self.controller.instrument.address) != "ERROR":
                self.state = "CONNECTED"
                self.connect_point.configure(image=self.connectImg)

    def button_close_callback(self):
    #This method call the controller to change output state 
        if self.state == "CONNECTED":
            self.state = "CLOSE"
            self.connect_point.configure(image=self.breakpointImg)  

    def close(self):
        if self.state == "CONNECTED":
            None