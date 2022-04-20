"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the Multimeter instrument's View.

"""

import imp
from os import listdir
import os
from tkinter.constants import END
from MultimeterController import MultimeterController
from DeviceFrame import DeviceFrame

from tkinter import Button, Canvas, Frame, IntVar, Label, Scrollbar
from tkinter import LabelFrame
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import Entry
from tkinter import Radiobutton
from tkinter.ttk import Combobox
from PIL import Image, ImageTk

from threading import Thread

import sys

class MultimeterView (DeviceFrame):
    """Class containing the Multimeter's View

    """

    def __init__(self, view, frame, terminal, model, controller, name):
    #Constructor for the Multimeter's View

        DeviceFrame.__init__(self, frame, controller, terminal, model)

        self.controller.instrument.name = name
        self.view=view

        self.initFrame(text=self.controller.instrument.type)
        self.initAttributes()
                
        self.initLabelFrame()
        self.initFrameLine()
        self.initLabel()
        self.initCombo()
        self.initVar()
        self.initEntries()
        self.combo_instrument_callback()
  
    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage     
        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentaddress = StringVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_instrument = Label(self.frame_instrument, text="Instrument :")
        self.label_instrumentaddress = Label(self.frame_instrument_address, text="Address :")

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName, width=25)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentaddress, width=25, state="readonly")  

        self.combo_instrument = Combobox(self.frame_instrument, state="readonly", width=15, values=["path1"])

        self.img = None
        self.panel = Label(self.frame, bg=self.model.parameters_dict['backgroundColorInstrument'])

    def updateView(self, instrument=None):
    #This method refresh the content of the view, its is used when loading a configuration file
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        self.renameInstrument()

        if self.controller.instrument.address != "":                
            sys.stdout("\n" + self.combo_instrument.get() + " is now connected to " + self.controller.instrument.address)
            
        if instrument != None :
            self.combo_instrument.set(instrument.ident)
            self.combo_instrument_callback(instrument=instrument)
            self.stringvar_instrumentaddress.set(self.controller.instrument.address)
                       
        if self.controller.instrument.address != "":
            self.controller.connectToDevice()
             
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=5, fill="y")

    def initFrameLine(self):
    #This method instanciates all the frames used as lines
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_address.pack(fill="both", pady=3)
    
    def initVar(self):
    #This methods instanciates all the Var
        self.stringvar_instrumentName.set(self.controller.instrument.name)    
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentName.pack(side="left")

        self.label_instrument.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrument.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentaddress.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox
        list=[]
        for dir in listdir("C:\\Oticon medical\\MyLab\\Instruments\\Multimeter"):
            if dir != "__pycache__":
                list.append(dir)
            
        self.combo_instrument.configure(values=list)    
        self.combo_instrument.configure(background='white')
        self.combo_instrument.current(0)
        self.combo_instrument.pack(side="right", padx=3)
        self.combo_instrument.bind("<<ComboboxSelected>>", self.combo_instrument_callback)

    def combo_instrument_callback(self, arg=None, instrument=None):
    #This method is called when selectionning an instrument via combo_instrument
        list=[]
        for dir in listdir("C:\\Oticon medical\\MyLab\\Instruments\\Multimeter"):
            if dir != "__pycache__":
                list.append(dir)

        if instrument == None :
            file_path = "C:\\Oticon medical\\MyLab\\Instruments\\Multimeter\\" + list[self.combo_instrument.current()] + "\\" + list[self.combo_instrument.current()] + ".py"
            self.controller.instrument.ident = list[self.combo_instrument.current()]

        else :            
            file_path = "C:\\Oticon medical\\MyLab\\Instruments\\Multimeter\\" + instrument.ident + "\\" + instrument.ident + ".py"
            self.controller.instrument = instrument

        mod_name,file_ext = os.path.splitext(os.path.split(file_path)[-1])

        if file_ext.lower() == '.py':
            py_mod = imp.load_source(mod_name, file_path)

        elif file_ext.lower() == '.pyc':
            py_mod = imp.load_compiled(mod_name, file_path)

        if instrument == None :
            controller = getattr(py_mod, list[self.combo_instrument.current()])()
        
        else :
            controller = getattr(py_mod, instrument.ident)()

        controller.view = self.controller.view
        controller.term = self.controller.term
        controller.instrument = self.controller.instrument
            
        self.controller = controller

        self.panel.destroy()

        try :                
            self.img = Image.open("C:\\Oticon medical\\MyLab\\Instruments\\Multimeter\\" + self.combo_instrument.get() + "\\" + self.combo_instrument.get() + ".png")
            self.img = self.img.resize((220, 110), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)
            self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
            self.panel.pack(fill = "both", expand = "yes")

        except:
            sys.stdout("\n  No Image were found associated to " + self.combo_instrument.get() + "\n")

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_instrumentaddress.bind('<Double-Button-1>', lambda event, name=self : self.view.menu2_Connections_callBack(event, name))
        self.entry_instrumentaddress.pack(side='right', padx=5)

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
        self.view.menu5.entryconfig(indexMenu, label=name)

    def entry_instrumentaddress_callback(self, arg=None):
    #This method is called when double click on the address
        self.controller.closeConnection()
        self.stringvar_instrumentaddress.set("")
        self.view.menu2_Connections_callBack()

