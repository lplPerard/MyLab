"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the Climatic Chamber instrument's View.

"""

import imp
from os import listdir
import os
from tkinter.constants import END
from ClimaticChamberController import ClimaticChamberController
from DeviceFrame import DeviceFrame

from tkinter import Button, Frame, IntVar, Label
from tkinter import LabelFrame
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import Entry
from tkinter import Radiobutton
from tkinter.ttk import Combobox
from PIL import Image, ImageTk

from threading import Thread

import sys

class ClimaticChamberView (DeviceFrame):
    """Class containing the Climatic Chamber's View

    """

    def __init__(self, view, frame, terminal, model, controller, name):
    #Constructor for the Climatic Chamber's View

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

    def updateView(self, instrument=None):
    #This method refresh the content of the view, its is used when loading a configuration file
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        self.renameInstrument()

        if self.controller.instrument.address != "":                
            sys.stdout("\n" + self.combo_instrument.get() + " is now connected to " + self.controller.instrument.address)
            
        if instrument != None :
            #Load here
            self.combo_instrument.set(instrument.ident)
            self.combo_instrument_callback(instrument=instrument)
            self.stringvar_instrumentaddress.set(self.controller.instrument.address)
            self.doubleVar_temperatureSource.set(self.controller.instrument.temperatureSource)
                       
        if self.controller.instrument.address != "":  
            adress = self.controller.instrument.address.split(" ")[0]
            self.controller.connectToDevice(adress)
    
    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage     
        self.state="freeze"   
        self.labelFrame_setup = LabelFrame(self.frame, text="Setup")

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)

        self.frame_source_temperature = Frame(self.labelFrame_setup)
        self.frame_source_radio = Frame(self.labelFrame_setup)
        self.frame_measure_temperature = Frame(self.labelFrame_setup)

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentaddress = StringVar()
        self.doubleVar_temperatureSource = DoubleVar()
        self.doubleVar_temperatureMeasure = DoubleVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_instrument = Label(self.frame_instrument, text="Instrument :")
        self.label_instrumentaddress = Label(self.frame_instrument_address, text="Address :")

        self.label_temperatureSource = Label(self.frame_source_temperature, text="Temperature setpoint (°C) :")
        self.label_temperatureMeasure = Label(self.frame_measure_temperature, text="Current Temperature (°C) :")

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentaddress, state="readonly")

        self.entry_temperatureSource = Entry(self.frame_source_temperature, textvariable=self.doubleVar_temperatureSource, justify="right", width=6)
        self.entry_temperatureMeasure = Entry(self.frame_measure_temperature, textvariable=self.doubleVar_temperatureMeasure, justify="right", width=6, state="readonly")

        self.combo_instrument = Combobox(self.frame_instrument, state="readonly", width=15, values=["path1"])

        self.button_set = Button(self.labelFrame_setup, text='  Set  ', command=self.button_set_callback)
        self.button_measure = Button(self.labelFrame_setup, text=' Measure ', command=self.button_measure_callback)
        
        self.img = Image.open("Images/VT4002_EMC.png")
        self.img = self.img.resize((220, 330), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
             
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=5, fill="y")

        self.labelFrame_setup.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_setup.pack(padx=5, pady=5, fill="y")
        
        self.panel.pack(fill = "both", expand = "yes")

    def initFrameLine(self):
    #This method instanciates all the Frame Lines
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_address.pack(fill="both", pady=3)

        self.frame_source_temperature.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_temperature.pack(fill="both", pady=5)
        
        self.button_set.pack(padx=5, pady=5, fill="y")

        self.frame_measure_temperature.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_measure_temperature.pack(fill="both", pady=5)

        self.button_measure.pack(padx=5, pady=5, fill="y")
    
    def initVar(self):
    #This methods instanciates all the Var
        self.stringvar_instrumentName.set(self.controller.instrument.name)    
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        self.doubleVar_temperatureSource.set(0)
        self.doubleVar_temperatureMeasure.set(0)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentName.pack(side="left")

        self.label_instrument.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrument.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentaddress.pack(side="left")

        self.label_temperatureSource.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_temperatureSource.pack(side="left")

        self.label_temperatureMeasure.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_temperatureMeasure.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox
        list=[]
        for dir in listdir("C:\\Oticon medical\\MyLab\\Instruments\\ClimaticChamber"):
            if dir != "__pycache__":
                list.append(dir)
            
        self.combo_instrument.configure(values=list)    
        self.combo_instrument.configure(background='white')
        self.combo_instrument.current(0)
        self.combo_instrument.pack(side="right", padx=3)
        self.combo_instrument.bind("<<ComboboxSelected>>", self.combo_instrument_callback)

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_instrumentaddress.bind('<Double-Button-1>', lambda event, name=self : self.view.menu2_Connections_callBack(event, name))
        self.entry_instrumentaddress.pack(side='right', padx=5)

        self.entry_temperatureSource.pack(side='right', padx=5)

        self.entry_temperatureMeasure.pack(side='right', padx=5)

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

    def combo_instrument_callback(self, arg=None, instrument=None):
    #This method is called when selectionning an instrument via combo_instrument
        list=[]
        for dir in listdir("C:\\Oticon medical\\MyLab\\Instruments\\ClimaticChamber"):
            if dir != "__pycache__":
                list.append(dir)

        if instrument == None :
            file_path = "C:\\Oticon medical\\MyLab\\Instruments\\ClimaticChamber\\" + list[self.combo_instrument.current()] + "\\" + list[self.combo_instrument.current()] + ".py"
            self.controller.instrument.ident = list[self.combo_instrument.current()]

        else :            
            file_path = "C:\\Oticon medical\\MyLab\\Instruments\\ClimaticChamber\\" + self.controller.instrument.ident + "\\" + self.controller.instrument.ident + ".py"
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
            self.img = Image.open("C:\\Oticon medical\\MyLab\\Instruments\\ClimaticChamber\\" + self.combo_instrument.get() + "\\" + self.combo_instrument.get() + ".png")
            self.img = self.img.resize((170, 260), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)
            self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
            self.panel.pack(fill = "both", expand = "yes")

        except:
            sys.stdout("\n  No Image were found associated to " + self.combo_instrument.get() + "\n")
 
    def button_set_callback(self):
    #This method call the controller to change output state     
        temperature = self.doubleVar_temperatureSource.get()
        self.controller.setTemperature(self.generateArguments(args1=temperature))
        self.controller.instrument.temperatureSource = temperature
 
    def button_measure_callback(self):
    #This method call the controller to change output state     
        temperature = self.controller.getTemperature()
        self.doubleVar_temperatureMeasure.set(temperature)