"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the PowerSupply instrument's View.

"""

import imp
import sys
import os
from os import listdir

from PowerSupplyController import PowerSupplyController
from DeviceFrame import DeviceFrame

from tkinter import Button, Frame, IntVar, Label
from tkinter import LabelFrame
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import Entry
from tkinter import Radiobutton
from tkinter.ttk import Combobox
from tkinter.constants import END

from PIL import Image, ImageTk



class PowerSupplyView (DeviceFrame):
    """Class containing the PowerSupply's View

    """

    def __init__(self, view, frame, terminal, model, controller, name):
    #Constructor for the PowerSupply's View

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
        self.labelFrame_source = LabelFrame(self.frame, text="Source")

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)
        self.frame_master = Frame(self.frame)

        self.frame_source_voltage = Frame(self.labelFrame_source)
        self.frame_source_current = Frame(self.labelFrame_source)
        self.frame_source_channel =  Frame(self.labelFrame_source)
        self.frame_source_button = Frame(self.labelFrame_source)
        self.frame_source_radio = Frame(self.labelFrame_source)
        self.frame_master_button = Frame(self.frame_master)
        self.frame_master_radio = Frame(self.frame_master)

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentaddress = StringVar()
        self.doubleVar_voltageSource = DoubleVar()
        self.doubleVar_currentLimit = DoubleVar()
        self.intVar_radioValueChannel = IntVar()
        self.intVar_radioValueMaster = IntVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_instrument = Label(self.frame_instrument, text="Instrument :")
        self.label_instrumentaddress = Label(self.frame_instrument_address, text="Address :")
        self.label_instrumentChannel = Label(self.frame_source_channel, text="Channel :")

        self.label_voltageSource = Label(self.frame_source_voltage, text="Voltage (V) :")
        self.label_currentLimit = Label(self.frame_source_current, text="Current (A) :")

        self.combo_instrument = Combobox(self.frame_instrument, state="readonly", width=15, values=["path1"])
        self.combo_instrumentChannel = Combobox(self.frame_source_channel, state="readonly", width=5, values=["1", "2", "3", "4"])

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentaddress, state="readonly")

        self.entry_voltageSource = Entry(self.frame_source_voltage, textvariable=self.doubleVar_voltageSource, justify="right", width=15)
        self.entry_currentLimit = Entry(self.frame_source_current, textvariable=self.doubleVar_currentLimit, justify="right", width=15)

        self.channel_activate = Button(self.frame_source_button, text='Channel ON/OFF', command=self.channel_activate_callback)
        self.master_activate = Button(self.frame_master_button, text='Master ON/OFF', command=self.master_activate_callback)

        self.radio_channelStateOFF = Radiobutton(self.frame_source_radio, text='OFF', variable=self.intVar_radioValueChannel, value=1)
        self.radio_channelStateON = Radiobutton(self.frame_source_radio, text='ON', variable=self.intVar_radioValueChannel, value=2)
        self.radio_masterStateOFF = Radiobutton(self.frame_master_radio, text='OFF', variable=self.intVar_radioValueMaster, value=1)
        self.radio_masterStateON = Radiobutton(self.frame_master_radio, text='ON', variable=self.intVar_radioValueMaster, value=2)
        
        self.img = Image.open("Images/HMC8042.png")
        self.img = self.img.resize((300, 150), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])

    def updateView(self, instrument=None):
    #This method refresh the content of the view, its is used when loading a configuration file
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        self.renameInstrument()

        if self.controller.instrument.address != "":                
            sys.stdout("\n" + self.combo_instrument.get() + " is now connected to " + self.controller.instrument.address)
            
        if instrument != None :
            self.combo_instrument.set(instrument.ident)
            self.combo_instrument_callback(instrument=instrument)
            self.doubleVar_voltageSource.set(self.controller.instrument.source_voltage)
            self.doubleVar_currentLimit.set(self.controller.instrument.source_current)
            self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=5, fill="y")

        self.labelFrame_source.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_source.pack(padx=5, pady=5, fill="y")

        self.panel.pack(fill = "both", expand = "yes")

    def initFrameLine(self):
    #This method instanciates all the Framelines
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_address.pack(fill="both", pady=3)

        self.frame_source_voltage.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_voltage.pack(fill="both", pady=5)

        self.frame_source_current.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_current.pack(fill="both", pady=5)

        self.frame_source_channel.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_channel.pack(fill="both", pady=5)

        self.frame_source_button.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_button.pack(side="left", fill="both", pady=5)

        self.frame_source_radio.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_radio.pack(side="right", fill="both", pady=5)

        self.frame_master.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_master.pack(padx=5, pady=5, fill="y")

        self.frame_master_button.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_master_button.pack(side="left", padx=5, pady=5, fill="y")

        self.frame_master_radio.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_master_radio.pack(side="right", padx=5, pady=5, fill="y")
    
    def initVar(self):
    #This methods instanciates all the Var
        self.stringvar_instrumentName.set(self.controller.instrument.name)    
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        self.doubleVar_voltageSource.set(0)
        self.doubleVar_currentLimit.set(0)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentName.pack(side="left")

        self.label_instrument.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrument.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentaddress.pack(side="left")

        self.label_voltageSource.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_voltageSource.pack(side="left")

        self.label_currentLimit.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_currentLimit.pack(side="left")

        self.label_instrumentChannel.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_instrumentChannel.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox
        list=[]
        for dir in listdir("C:\\Oticon medical\\MyLab\\Instruments\\PowerSupply"):
            if dir != "__pycache__":
                list.append(dir)
            
        self.combo_instrument.configure(values=list)    
        self.combo_instrument.configure(background='white')
        self.combo_instrument.current(0)
        self.combo_instrument.pack(side="right", padx=3)
        self.combo_instrument.bind("<<ComboboxSelected>>", self.combo_instrument_callback)

        self.combo_instrumentChannel.configure(background='white')
        self.combo_instrumentChannel.current(0)
        self.combo_instrumentChannel.pack(side="right", padx=3)

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_instrumentaddress.bind('<Double-Button-1>', lambda event, name=self : self.view.menu2_Connections_callBack(event, name))
        self.entry_instrumentaddress.pack(side='right', padx=5)

        self.entry_voltageSource.bind("<Return>", self.entry_voltageSource_callback)
        self.entry_voltageSource.bind("<KeyRelease>", self.entry_voltageSource_callback2)
        self.entry_voltageSource.pack(side='right', padx=5)

        self.entry_currentLimit.bind("<Return>", self.entry_currentLimit_callback)
        self.entry_currentLimit.bind("<KeyRelease>", self.entry_currentLimit_callback2)
        self.entry_currentLimit.pack(side='right', padx=5)

    def initButton(self):
    #This method instanciates the buttons
        self.channel_activate.pack(expand="yes", padx=5)
        self.master_activate.pack(expand="yes")

        self.radio_channelStateON.pack(side="top", expand="yes", fill="both")
        self.radio_channelStateON.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")
        self.radio_channelStateOFF.pack(side="top", expand="yes", fill="both")
        self.radio_channelStateOFF.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")
        self.radio_masterStateON.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateON.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")
        self.radio_masterStateOFF.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateOFF.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")

        self.intVar_radioValueChannel.set(1)
        self.intVar_radioValueMaster.set(1)

    def combo_instrument_callback(self, arg=None, instrument=None):
    #This method is called when selectionning an instrument via combo_instrument
        list=[]
        for dir in listdir("C:\\Oticon medical\\MyLab\\Instruments\\PowerSupply"):
            if dir != "__pycache__":
                list.append(dir)

        if instrument == None :
            file_path = "C:\\Oticon medical\\MyLab\\Instruments\\PowerSupply\\" + list[self.combo_instrument.current()] + "\\" + list[self.combo_instrument.current()] + ".py"
            self.controller.instrument.ident = list[self.combo_instrument.current()]

        else :            
            file_path = "C:\\Oticon medical\\MyLab\\Instruments\\PowerSupply\\" + instrument.ident + "\\" + instrument.ident + ".py"
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
            self.img = Image.open("C:\\Oticon medical\\MyLab\\Instruments\\PowerSupply\\" + self.combo_instrument.get() + "\\" + self.combo_instrument.get() + ".png")
            self.img = self.img.resize((220, 110), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)
            self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
            self.panel.pack(fill = "both", expand = "yes")

        except:
            sys.stdout("\n  No Image were found associated to " + self.combo_instrument.get() + "\n")

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

    def entry_voltageSource_callback(self, arg=None):
    #This method calls the controller to change the voltage
        voltage = self.doubleVar_voltageSource.get()  
        channel = self.combo_instrumentChannel.current() + 1    
        self.controller.instrument.source_voltage = voltage   
        self.controller.setVoltageSource(self.generateArguments(args1=voltage, args8=channel))

    def entry_voltageSource_callback2(self, arg=None):
    #This method calls the controller to change the voltage
        voltage = self.doubleVar_voltageSource.get()   
        self.controller.instrument.source_voltage = voltage   

    def entry_currentLimit_callback(self, arg=None):
    #This method calls the controller to change the voltage
        current = self.doubleVar_currentLimit.get()    
        channel = self.combo_instrumentChannel.current() + 1     
        self.controller.instrument.source_current = current                 
        self.controller.setCurrentLimit(self.generateArguments(args1=current, args8=channel))

    def entry_currentLimit_callback2(self, arg=None):
    #This method calls the controller to change the voltage
        current = self.doubleVar_currentLimit.get()     
        self.controller.instrument.source_current = current                 

    def channel_activate_callback(self):
    #This method call the controller to change channel output state 
        channel = self.combo_instrumentChannel.current() + 1 
        if self.controller.setChannelState(self.generateArguments(args8=channel)) != "ERROR":
            if (self.intVar_radioValueChannel.get() == 1) and (self.controller.instrument.address != ""):
                self.entry_currentLimit_callback()
                self.entry_voltageSource_callback()

                self.intVar_radioValueChannel.set(2) 
                self.radio_channelStateON.select() 
            else:
                self.intVar_radioValueChannel.set(1)
                self.radio_channelStateOFF.select() 

    def master_activate_callback(self):
    #This method call the controller to change Master output state 
        if self.controller.setMasterState([]) != "ERROR":
            if (self.intVar_radioValueMaster.get() == 1) and (self.controller.instrument.address != ""):
                self.entry_currentLimit_callback()
                self.entry_voltageSource_callback()

                self.intVar_radioValueMaster.set(2) 
                self.radio_masterStateON.select()  
                
            else:
                self.intVar_radioValueMaster.set(1)
                self.radio_masterStateOFF.select() 