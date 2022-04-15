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

    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage   
        self.labelFrame_source = LabelFrame(self.frame, text="Source")

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)
        self.frame_instrument_channel =  Frame(self.labelFrame_instrument)
        self.frame_master = Frame(self.frame)

        self.frame_source_voltage = Frame(self.labelFrame_source)
        self.frame_source_current = Frame(self.labelFrame_source)
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
        self.label_instrumentChannel = Label(self.frame_instrument_channel, text="Channel :")

        self.label_voltageSource = Label(self.frame_source_voltage, text="Voltage :")
        self.label_currentLimit = Label(self.frame_source_current, text="Current :")

        self.combo_instrument = Combobox(self.frame_instrument, state="readonly", width=15, values=["path1"])
        self.combo_instrumentChannel = Combobox(self.frame_instrument_channel, state="readonly", width=5, values=["1", "2", "3", "4"])

        self.combo_voltageSource = Combobox(self.frame_source_voltage, state="readonly", width=5, values=["V", "mV"])
        self.combo_currentLimit = Combobox(self.frame_source_current, state="readonly", width=5, values=["A", "mA"])

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentaddress, state="readonly")

        self.entry_voltageSource = Entry(self.frame_source_voltage, textvariable=self.doubleVar_voltageSource, width=15)
        self.entry_currentLimit = Entry(self.frame_source_current, textvariable=self.doubleVar_currentLimit, width=15)

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
        
    def clearInstrument(self):
    #This method is used to clear every trace of this instrument before being deleted
        for i in range(len(self.controller.instrument.channelUsed)):
            if self.controller.instrument.channelUsed[i] == self.controller.instrument:
                self.controller.instrument.channelUsed[i]=""

    def renameInstrument(self):
    #This method is used to change instrumen'ts name and guarantee there are no duplicates
        for item in self.view.listViews:
            if self.controller.instrument.name == item.controller.instrument.name:  
                if (self != item):
                    index = int(item.controller.instrument.name[-2]) + 1
                    newName = self.controller.instrument.name[:-2] + str(index) + ")"
                    self.entry_instrumentName_callback(newName=newName)

    def updateView(self, configuration=False):
    #This method refresh the content of the view, its is used when loading a configuration file
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        self.renameInstrument()

        if self.controller.instrument.address != "":                
            sys.stdout("\n" + self.combo_instrument.get() + " is now connected to " + self.controller.instrument.address)
            used = 0
            for item in self.view.getInstrList():
                if (item.name != self.controller.instrument.name) and (item.address == self.controller.instrument.address):
                    self.controller.instrument.channelState = item.channelState
                    self.controller.instrument.channelUsed = item.channelUsed
                    used = used + 1

            if used == 0:           
                self.controller.instrument.channelState = [0, 0]
                self.controller.instrument.channelUsed = ["", ""]

        if configuration == True:
            self.doubleVar_voltageSource.set(self.controller.instrument.source_voltage)
            self.combo_voltageSource.set(self.controller.instrument.source_voltage_caliber)
            self.doubleVar_currentLimit.set(self.controller.instrument.source_current)
            self.combo_currentLimit.set(self.controller.instrument.source_current_caliber)
            
        if self.controller.instrument.address != "":
            self.controller.connectToDevice()
            self.combo_instrumentChannel_callback()
        
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

        self.frame_instrument_channel.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_channel.pack(fill="both", pady=3)

        self.frame_source_voltage.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_voltage.pack(fill="both", pady=5)

        self.frame_source_current.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_current.pack(fill="both", pady=5)

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

        self.label_instrumentChannel.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentChannel.pack(side="left")

        self.label_voltageSource.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_voltageSource.pack(side="left")

        self.label_currentLimit.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_currentLimit.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox
        list=[]
        for dir in listdir("C:\\Oticon medical\\MyLab\\Instruments\\PowerSupply"):
            if dir != "__pycache__":
                list.append(dir)
            
        self.combo_instrument.configure(values=list)    
        self.combo_instrument.bind("<<ComboboxSelected>>", self.combo_instrument_callback)
        self.combo_instrument.configure(background='white')
        self.combo_instrument.current(0)
        self.combo_instrument.pack(side="right", padx=3)
        #self.combo_instrumentChannel_callback()

        self.combo_instrumentChannel.bind("<<ComboboxSelected>>", self.combo_instrumentChannel_callback)
        self.combo_instrumentChannel.configure(background='white')
        self.combo_instrumentChannel.current(0)
        self.combo_instrumentChannel.pack(side="right", padx=3)
        self.combo_instrumentChannel_callback()

        self.combo_voltageSource.bind("<<ComboboxSelected>>", self.combo_voltageSource_callback)
        self.combo_voltageSource.configure(background='white')
        self.combo_voltageSource.current(0)
        self.combo_voltageSource.pack(side="right", padx=5)
    
        self.combo_currentLimit.bind("<<ComboboxSelected>>", self.combo_currentLimit_callback)
        self.combo_currentLimit.configure(background='white')
        self.combo_currentLimit.current(0)
        self.combo_currentLimit.pack(side="right", padx=5)

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_instrumentaddress.bind('<Double-Button-1>', lambda event, name=self : self.view.menu2_Connections_callBack(event, name))
        self.entry_instrumentaddress.pack(side='right', padx=5)

        self.entry_voltageSource.bind("<Return>", self.entry_voltageSource_callback)
        self.entry_voltageSource.pack(side='right', padx=5)

        self.entry_currentLimit.bind("<Return>", self.entry_currentLimit_callback)
        self.entry_currentLimit.pack(side='right', padx=5)

    def initButton(self):
    #This method instanciates the buttons
        self.channel_activate.pack(expand="yes")
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

    def combo_instrument_callback(self, arg=None):
    #This method is called when selectionning an instrument via combo_instrument
        list=[]
        for dir in listdir("C:\\Oticon medical\\MyLab\\Instruments\\PowerSupply"):
            if dir != "__pycache__":
                list.append(dir)

        file_path = "C:\\Oticon medical\\MyLab\\Instruments\\PowerSupply\\" + list[self.combo_instrument.current()] + "\\" + list[self.combo_instrument.current()] + ".py"

        mod_name,file_ext = os.path.splitext(os.path.split(file_path)[-1])

        if file_ext.lower() == '.py':
            py_mod = imp.load_source(mod_name, file_path)

        elif file_ext.lower() == '.pyc':
            py_mod = imp.load_compiled(mod_name, file_path)

        controller = getattr(py_mod, self.combo_instrument.get())()

        controller.view = self.controller.view
        controller.term = self.controller.term
        controller.instrument = self.controller.instrument
        controller.resourceManager = self.controller.resourceManager

        self.controller = controller
        self.panel.destroy()

        try :                
            self.img = Image.open("C:\\Oticon medical\\MyLab\\Instruments\\PowerSupply\\" + self.combo_instrument.get() + "\\" + self.combo_instrument.get() + ".png")
            self.img = self.img.resize((300, 150), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)
            self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
            self.panel.pack(fill = "both", expand = "yes")

        except:
            sys.stdout("\n  No Image were found associated to " + self.combo_instrument.get() + "\n")

    def combo_instrumentChannel_callback(self, arg=None):
    #This method is called when selectionning a channel via combo_instrumentChannel
        for i in range(len(self.controller.instrument.channelUsed)):
            if self.controller.instrument.channelUsed[i] == self.controller.instrument:
                self.controller.instrument.channelUsed[i]=""
        
        i=0
        found=0
        liste = self.controller.instrument.channelUsed
        for item in liste:
            if ((item == "") or (item == self.controller.instrument)) and (self.combo_instrumentChannel.current() == i):
                self.combo_instrumentChannel.current(i)
                self.controller.instrument.channelUsed[i]=self.controller.instrument
                found=1
                break         

            i=i+1

        if found == 0:
            i=0
            liste = self.controller.instrument.channelUsed
            for item in liste:
                if (item == ""):
                    self.combo_instrumentChannel.current(i)
                    self.controller.instrument.channelUsed[i]=self.controller.instrument
                    found=2
                    break            

                i=i+1

        if found == 2:
            self.view.sendWarning('003')
        if found == 0:
            self.view.menu5_callback(self)
            self.view.sendError('006')    

    def combo_voltageSource_callback(self, args=None):
    #This method is called when changing units for volatge source 
        self.controller.instrument.source_voltage_caliber = self.combo_voltageSource.get()

    def combo_currentLimit_callback(self, args=None):
    #This method is called when changing units for current limit
        self.controller.instrument.source_current_caliber = self.combo_currentLimit.get()

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
        self.controller.setVoltageSource(self.generateArguments(arg1=voltage, arg8=channel))

    def entry_currentLimit_callback(self, arg=None):
    #This method calls the controller to change the voltage
        current = self.doubleVar_currentLimit.get()    
        channel = self.combo_instrumentChannel.current() + 1     
        self.controller.instrument.source_current = current                 
        self.controller.setcurrentLimit(self.generateArguments(arg1=current, arg8=channel))

    def channel_activate_callback(self):
    #This method call the controller to change channel output state 
        channel = self.combo_instrumentChannel.current() + 1 
        if self.controller.setChannelState(self.generateArguments(arg8=channel)) != "ERROR":
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