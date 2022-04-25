"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the Sourcemeter instrument's View.

"""

import imp
from os import listdir
import os
from tkinter.constants import END
from SourcemeterController import SourcemeterController
from DeviceFrame import DeviceFrame

from tkinter import Button, Canvas, Frame, IntVar, Label, Scrollbar, filedialog
from tkinter import LabelFrame
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import Entry
from tkinter import Radiobutton
from tkinter.ttk import Combobox
from PIL import Image, ImageTk

from threading import Thread

import sys

class SourcemeterView (DeviceFrame):
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
        self.initButton()
        self.initLabel()
        self.initCombo()
        self.initVar()
        self.initEntries()
        self.combo_instrument_callback()
  
    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage     
        self.state="freeze"   

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)

        self.labelFrame_source = LabelFrame(self.frame, text="Source")

        self.frame_source1 = Frame(self.labelFrame_source)
        self.frame_source1_radio = Frame(self.frame_source1)
        self.frame_source1_setup = Frame(self.frame_source1)
        self.frame_source_voltage = Frame(self.frame_source1_setup)
        self.frame_source_currentCompliance = Frame(self.frame_source1_setup)
        self.frame_source2 = Frame(self.labelFrame_source)
        self.frame_source2_radio = Frame(self.frame_source2)
        self.frame_source2_setup = Frame(self.frame_source2)
        self.frame_source_current = Frame(self.frame_source2_setup)
        self.frame_source_voltageCompliance = Frame(self.frame_source2_setup)
        self.frameline_button = Frame(self.frame)

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentaddress = StringVar()

        self.doubleVar_source_voltage = DoubleVar()
        self.doubleVar_source_currentCompliance = DoubleVar()
        self.doubleVar_source_current = DoubleVar()
        self.doubleVar_source_voltageCompliance = DoubleVar()
        self.intVar_radio_source = IntVar()
        self.intVar_source3_type = IntVar()
        self.intVar_radio_masterState = IntVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_instrument = Label(self.frame_instrument, text="Instrument :")
        self.label_instrumentaddress = Label(self.frame_instrument_address, text="Address :")
        
        self.label_source_voltage = Label(self.frame_source_voltage, text="Voltage (V) :")
        self.label_source_currentCompliance = Label(self.frame_source_currentCompliance, text="C.C. (A) :")
        self.label_source_current = Label(self.frame_source_current, text="Current (A) :")
        self.label_source_voltageCompliance = Label(self.frame_source_voltageCompliance, text="V.C. (V) :")

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName, width=25)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentaddress, width=25, state="readonly")

        self.entry_source_voltage = Entry(self.frame_source_voltage, textvariable=self.doubleVar_source_voltage, justify="right", width=13)
        self.entry_source_currentCompliance = Entry(self.frame_source_currentCompliance, textvariable=self.doubleVar_source_currentCompliance, justify="right", width=13)
        self.entry_source_current = Entry(self.frame_source_current, textvariable=self.doubleVar_source_current, justify="right", width=13)
        self.entry_source_voltageCompliance = Entry(self.frame_source_voltageCompliance, textvariable=self.doubleVar_source_voltageCompliance, justify="right", width=13)

        self.combo_instrument = Combobox(self.frame_instrument, state="readonly", width=15, values=["path1"])

        self.img = None
        self.panel = Label(self.frame, bg=self.model.parameters_dict['backgroundColorInstrument'])
        
        self.radio_source1 = Radiobutton(self.frame_source1_radio, variable=self.intVar_radio_source, value=0, command=self.radio_source_callback)
        self.radio_source2 = Radiobutton(self.frame_source2_radio, variable=self.intVar_radio_source, value=1, command=self.radio_source_callback)

        self.radio_masterStateOFF = Radiobutton(self.frameline_button, text='OFF', variable=self.intVar_radio_masterState, value=0)
        self.radio_masterStateON = Radiobutton(self.frameline_button, text='ON', variable=self.intVar_radio_masterState, value=1)

        self.master_activate = Button(self.frameline_button, text='Master ON/OFF', command=self.master_activate_callback)

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

        self.labelFrame_source.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_source.pack(padx=5, pady=5, fill="y")

    def initFrameLine(self):
    #This method instanciates all the frames used as lines
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_address.pack(fill="both", pady=3)

        self.frame_source1.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source1.pack(fill="both", pady=2)

        self.frame_source1_radio.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source1_radio.pack(side='left', fill="both", pady=2)

        self.frame_source1_setup.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source1_setup.pack(side='left', fill="both", pady=2)

        self.frame_source2.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source2.pack(fill="both", pady=2)

        self.frame_source2_radio.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source2_radio.pack(side='left', fill="both", pady=2)

        self.frame_source2_setup.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source2_setup.pack(side='left', fill="both", pady=2)

        self.frame_source_voltage.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_voltage.pack(fill="both", pady=3)

        self.frame_source_currentCompliance.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_currentCompliance.pack(fill="both", pady=3)

        self.frame_source_current.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_current.pack(fill="both", pady=3)

        self.frame_source_voltageCompliance.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_voltageCompliance.pack(fill="both", pady=3)        

        self.frameline_button.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_button.pack(padx=5, pady=3, fill="y")
    
    def initVar(self):
    #This methods instanciates all the Var
        self.stringvar_instrumentName.set(self.controller.instrument.name)    
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        
        self.doubleVar_source_voltage.set(0)
        self.doubleVar_source_currentCompliance.set(0)
        self.doubleVar_source_current.set(0)
        self.doubleVar_source_voltageCompliance.set(0)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentName.pack(side="left")

        self.label_instrument.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrument.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentaddress.pack(side="left")

        self.label_source_voltage.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_source_voltage.pack(side="left", anchor='ne')

        self.label_source_currentCompliance.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_source_currentCompliance.pack(side="left", anchor='ne')

        self.label_source_current.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_source_current.pack(side="left")

        self.label_source_voltageCompliance.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_source_voltageCompliance.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox
        list=[]
        for dir in listdir("C:\\Oticon medical\\MyLab\\Instruments\\Sourcemeter"):
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
        for dir in listdir("C:\\Oticon medical\\MyLab\\Instruments\\Sourcemeter"):
            if dir != "__pycache__":
                list.append(dir)

        if instrument == None :
            file_path = "C:\\Oticon medical\\MyLab\\Instruments\\Sourcemeter\\" + list[self.combo_instrument.current()] + "\\" + list[self.combo_instrument.current()] + ".py"
            self.controller.instrument.ident = list[self.combo_instrument.current()]

        else :            
            file_path = "C:\\Oticon medical\\MyLab\\Instruments\\Sourcemeter\\" + instrument.ident + "\\" + instrument.ident + ".py"
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
            self.img = Image.open("C:\\Oticon medical\\MyLab\\Instruments\\Sourcemeter\\" + self.combo_instrument.get() + "\\" + self.combo_instrument.get() + ".png")
            self.img = self.img.resize((240, 120), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)
            self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
            self.panel.pack(fill = "both", expand = "yes")

        except:
            sys.stdout("\n  No Image were found associated to " + self.combo_instrument.get() + "\n")

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.pack(side='right', padx=5)
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)

        self.entry_instrumentaddress.pack(side='right', padx=5)
        self.entry_instrumentaddress.bind('<Double-Button-1>', lambda event, name=self : self.view.menu2_Connections_callBack(event, name))

        self.entry_source_voltage.pack(side='right', padx=5)
        self.entry_source_voltage.bind('<Return>', self.entry_source_voltage_callback)

        self.entry_source_currentCompliance.pack(side='right', padx=5)
        self.entry_source_currentCompliance.bind('<Return>', self.entry_source_voltage_callback)
        
        self.entry_source_current.pack(side='right', padx=5)
        self.entry_source_current.bind('<Return>', self.entry_source_current_callback)
        
        self.entry_source_voltageCompliance.pack(side='right', padx=5)
        self.entry_source_voltageCompliance.bind('<Return>', self.entry_source_current_callback)

    def initButton(self):
    #This method instanciates the buttons
        self.radio_source1.pack(expand="yes")
        self.radio_source1.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_source2.pack(expand="yes")
        self.radio_source2.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        
        self.master_activate.pack(side='left', expand="yes")

        self.radio_masterStateON.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateON.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")
        self.radio_masterStateOFF.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateOFF.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")

        self.radio_source_callback()

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

    def entry_instrumentaddress_callback(self, arg=None):
    #This method is called when double click on the address
        self.controller.closeConnection()
        self.stringvar_instrumentaddress.set("")
        self.view.menu2_Connections_callBack()

    def master_activate_callback(self):
    #This method call the controller to change output state 
        if (self.controller.instrument.masterState == 0) and (self.controller.instrument.address != ""):
            self.intVar_radio_masterState.set(1) 
            self.radio_masterStateON.select()  
            self.controller.setMasterState()

        elif self.controller.instrument.address != "":
            self.intVar_radio_masterState.set(0)
            self.radio_masterStateOFF.select() 
            self.controller.setMasterState()

    def entry_source_voltage_callback(self, args=[]):
    #This method set Voltage source and current limit
        voltage = self.doubleVar_source_voltage.get()
        current = self.doubleVar_source_currentCompliance.get()

        self.controller.setVoltageSource(self.generateArguments(args1=voltage, args2=current))

    def radio_source_callback(self, args=[]):
    #This methods updates the view according to the radio_source state
        for child in self.frame_source1_radio.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_source_voltage.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_source_currentCompliance.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_source2_radio.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_source_current.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_source_voltageCompliance.winfo_children():
            child.configure(state="disabled")
                
        self.radio_source1.configure(fg="grey24")
        self.radio_source2.configure(fg="grey24")

        if self.intVar_radio_source.get() == 0:
            for child in self.frame_source1_radio.winfo_children():
                child.configure(state="normal")
            for child in self.frame_source_voltage.winfo_children():
                child.configure(state="normal")
            for child in self.frame_source_currentCompliance.winfo_children():
                child.configure(state="normal")
            self.radio_source1.configure(fg="black")

        if self.intVar_radio_source.get() == 1:
            for child in self.frame_source2_radio.winfo_children():
                child.configure(state="normal")
            for child in self.frame_source_current.winfo_children():
                child.configure(state="normal")
            for child in self.frame_source_voltageCompliance.winfo_children():
                child.configure(state="normal")
            self.radio_source2.configure(fg="black")

        if self.intVar_radio_source.get() == 2:
            for child in self.frame_source1_radio.winfo_children():
                child.configure(state="normal")

        self.radio_source1.configure(state='normal')
        self.radio_source2.configure(state='normal')

    def entry_source_current_callback(self, args=[]):
    #This method set Voltage source and current limit
        current = self.doubleVar_source_current.get()
        voltage = self.doubleVar_source_voltageCompliance.get()

        self.controller.setCurrentSource(self.generateArguments(args1=current, args2=voltage))
