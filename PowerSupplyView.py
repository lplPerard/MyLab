"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the POwerSupply instrument's View.

"""

from tkinter.constants import END
from PowerSupplyController import PowerSupplyController
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
        self.labelFrame_measure = LabelFrame(self.frame, text="Measure")

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)
        self.frame_instrument_channel =  Frame(self.labelFrame_instrument)
        self.frame_master = Frame(self.frame)

        self.frame_source_voltage = Frame(self.labelFrame_source)
        self.frame_source_current = Frame(self.labelFrame_source)
        self.frame_source_button = Frame(self.labelFrame_source)
        self.frame_source_radio = Frame(self.labelFrame_source)
        self.frame_measure_voltage = Frame(self.labelFrame_measure)
        self.frame_measure_current = Frame(self.labelFrame_measure)
        self.frame_measure_power = Frame(self.labelFrame_measure)
        self.frame_master_button = Frame(self.frame_master)
        self.frame_master_radio = Frame(self.frame_master)

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentaddress = StringVar()
        self.doubleVar_voltageSource = DoubleVar()
        self.doubleVar_currentSource = DoubleVar()
        self.doubleVar_voltageMeasure = DoubleVar()
        self.doubleVar_currentMeasure = DoubleVar()
        self.doubleVar_powerMeasure = DoubleVar()
        self.intVar_radioValueChannel = IntVar()
        self.intVar_radioValueMaster = IntVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_instrumentaddress = Label(self.frame_instrument_address, text="Address :")
        self.label_instrumentChannel = Label(self.frame_instrument_channel, text="Channel :")

        self.label_voltageSource = Label(self.frame_source_voltage, text="Voltage :")
        self.label_currentSource = Label(self.frame_source_current, text="Current :")
        self.label_voltageMeasure = Label(self.frame_measure_voltage, text="Voltage :")
        self.label_currentMeasure = Label(self.frame_measure_current, text="Current :")
        self.label_powerMeasure = Label(self.frame_measure_power, text="Power :")
        self.label_powerMeasure.after(1000, self.updateMonitoring)

        self.combo_instrumentChannel = Combobox(self.frame_instrument_channel, state="readonly", width=5, values=["1", "2"])

        self.combo_voltageSource = Combobox(self.frame_source_voltage, state="readonly", width=5, values=["V", "mV"])
        self.combo_currentSource = Combobox(self.frame_source_current, state="readonly", width=5, values=["A", "mA"])
        self.combo_voltageMeasure = Combobox(self.frame_measure_voltage, state="readonly", width=5, values=["V", "mV"])
        self.combo_currentMeasure = Combobox(self.frame_measure_current, state="readonly", width=5, values=["A", "mA"])
        self.combo_powerMeasure = Combobox(self.frame_measure_power, state="readonly", width=5, values=["W", "mW"])

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentaddress, state="readonly")

        self.entry_voltageSource = Entry(self.frame_source_voltage, textvariable=self.doubleVar_voltageSource, width=6)
        self.entry_currentSource = Entry(self.frame_source_current, textvariable=self.doubleVar_currentSource, width=6)
        self.entry_voltageMeasure = Entry(self.frame_measure_voltage, textvariable=self.doubleVar_voltageMeasure, state="readonly")
        self.entry_currentMeasure = Entry(self.frame_measure_current, textvariable=self.doubleVar_currentMeasure, state="readonly")
        self.entry_powerMeasure = Entry(self.frame_measure_power, textvariable=self.doubleVar_powerMeasure, state="readonly")

        self.channel_activate = Button(self.frame_source_button, text='Channel ON/OFF', command=self.channel_activate_callback)
        self.master_activate = Button(self.frame_master_button, text='Master ON/OFF', command=self.master_activate_callback)

        self.radio_channelStateOFF = Radiobutton(self.frame_source_radio, text='OFF', variable=self.intVar_radioValueChannel, value=1)
        self.radio_channelStateON = Radiobutton(self.frame_source_radio, text='ON', variable=self.intVar_radioValueChannel, value=2)
        self.radio_masterStateOFF = Radiobutton(self.frame_master_radio, text='OFF', variable=self.intVar_radioValueMaster, value=1)
        self.radio_masterStateON = Radiobutton(self.frame_master_radio, text='ON', variable=self.intVar_radioValueMaster, value=2)
        
        self.img = None
        self.panel = Label(self.frame, bg=self.model.parameters_dict['backgroundColorInstrument'])
        
    def clearInstrument(self):
    #This method is used to clear every trace of this instrument before being deleted
        for i in range(len(self.controller.instrument.channelUsed)):
            if self.controller.instrument.channelUsed[i] == self.controller.instrument:
                self.controller.instrument.channelUsed[i]=""

    def renameInstrument(self):
        i = 0
        for item in self.view.listViews:
            if self.controller.instrument.name == item.controller.instrument.name:    
                newName = self.controller.instrument.name[:-2] + str(i) + ")"
                self.entry_instrumentName_callback(newName=newName)
                i = i+1

    def updateView(self, configuration=False):
    #This method refresh the content of the view
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        self.panel.destroy()
        found=0

        for item in self.model.devices_dict:
            if (item in self.controller.instrument.address):
                if self.model.devices_dict[item][1] == "Power Supply":
                    self.controller.instrument.id = item
                    self.controller.instrument.channelNumber = self.model.devices_dict[item][2]
                    self.combo_instrumentChannel.configure(values=self.controller.instrument.channelNumber)
                    self.controller.instrument.channelState = self.model.devices_dict[item][3]
                    self.controller.instrument.channelUsed = self.model.devices_dict[item][4]

                    newName = self.model.devices_dict[item][0] + " (0)"
                    self.entry_instrumentName_callback(newName=newName)

                    if self.model.devices_dict[item][0] == "HMC8042":   
                        self.img = Image.open(self.model.devices_dict[item][5])
                        self.img = self.img.resize((200, 100), Image.ANTIALIAS)
                        self.img = ImageTk.PhotoImage(self.img)
                        self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
                        self.panel.pack(fill = "both", expand = "yes")

                    if self.model.devices_dict[item][0] == "2220-30-1":   
                        self.img = Image.open(self.model.devices_dict[item][5])
                        self.img = self.img.resize((200, 200), Image.ANTIALIAS)
                        self.img = ImageTk.PhotoImage(self.img)
                        self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
                        self.panel.pack(fill = "both", expand = "yes")

                    break

                found=1

        if (found==1) and (self.model.devices_dict[item][1] != "Power Supply"):
            self.view.menu5_callback(self)
            self.view.sendError('005')

        self.renameInstrument()

        if (found == 0) and (self.controller.instrument.address != ""):                
            self.term_text.insert(END, "\nUnknown device connected")
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
            self.doubleVar_currentSource.set(self.controller.instrument.source_current)
            self.combo_currentSource.set(self.controller.instrument.source_current_caliber)
            
        if self.controller.instrument.address != "":
            self.controller.connectToDevice()
            self.combo_instrumentChannel_callback()
        
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=5, fill="y")

        self.labelFrame_source.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_source.pack(padx=5, pady=5, fill="y")

        self.labelFrame_measure.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_measure.pack(padx=5, pady=5, fill="y")

    def initFrameLine(self):
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_instrument_address.pack(fill="both", pady=3)

        self.frame_instrument_channel.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_instrument_channel.pack(fill="both", pady=3)

        self.frame_source_voltage.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_voltage.pack(fill="both", pady=5)

        self.frame_source_current.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_current.pack(fill="both", pady=5)

        self.frame_source_button.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_button.pack(side="left", fill="both", pady=5)

        self.frame_source_radio.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_radio.pack(side="right", fill="both", pady=5)

        self.frame_measure_voltage.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_measure_voltage.pack(fill="both", pady=5)

        self.frame_measure_current.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_measure_current.pack(fill="both",pady=5)

        self.frame_measure_power.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_measure_power.pack(fill="both",pady=5)

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
        self.doubleVar_currentSource.set(0)
        self.doubleVar_voltageMeasure.set(0)
        self.doubleVar_currentMeasure.set(0)
        self.doubleVar_powerMeasure.set(0)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_instrumentName.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_instrumentaddress.pack(side="left")

        self.label_instrumentChannel.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_instrumentChannel.pack(side="left")

        self.label_voltageSource.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_voltageSource.pack(side="left")

        self.label_currentSource.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_currentSource.pack(side="left")

        self.label_voltageMeasure.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_voltageMeasure.pack(side="left")

        self.label_currentMeasure.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_currentMeasure.pack(side="left")

        self.label_powerMeasure.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_powerMeasure.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox
        self.combo_instrumentChannel.bind("<<ComboboxSelected>>", self.combo_instrumentChannel_callback)
        self.combo_instrumentChannel.configure(background='white')
        self.combo_instrumentChannel.current(0)
        self.combo_instrumentChannel.pack(side="right")
        self.combo_instrumentChannel_callback()

        self.combo_voltageSource.bind("<<ComboboxSelected>>", self.combo_voltageSource_callback)
        self.combo_voltageSource.configure(background='white')
        self.combo_voltageSource.current(0)
        self.combo_voltageSource.pack(side="right")
    
        self.combo_currentSource.bind("<<ComboboxSelected>>", self.combo_currentSource_callback)
        self.combo_currentSource.configure(background='white')
        self.combo_currentSource.current(0)
        self.combo_currentSource.pack(side="right")
    
        #self.combo_voltageMeasure.bind("<<ComboboxSelected>>", self.combo_voltageMeasure_callback)
        self.combo_voltageMeasure.configure(background='white')
        self.combo_voltageMeasure.current(0)
        self.combo_voltageMeasure.pack(side="right")
    
        #self.combo_currentMeasure.bind("<<ComboboxSelected>>", self.combo_currentMeasure_callback)
        self.combo_currentMeasure.configure(background='white')
        self.combo_currentMeasure.current(0)
        self.combo_currentMeasure.pack(side="right")
    
        #self.combo_currentMeasure.bind("<<ComboboxSelected>>", self.combo_currentMeasure_callback)
        self.combo_powerMeasure.configure(background='white')
        self.combo_powerMeasure.current(0)
        self.combo_powerMeasure.pack(side="right")

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_instrumentaddress.bind('<Double-Button-1>', self.view.menu2_Connections_callBack)
        self.entry_instrumentaddress.pack(side='right', padx=5)

        self.entry_voltageSource.bind("<Return>", self.entry_voltageSource_callback)
        self.entry_voltageSource.pack(side='right', padx=5)

        self.entry_currentSource.bind("<Return>", self.entry_currentSource_callback)
        self.entry_currentSource.pack(side='right', padx=5)

        self.entry_voltageMeasure.pack(side='right', padx=5)

        self.entry_currentMeasure.pack(side='right', padx=5)

        self.entry_powerMeasure.pack(side='right', padx=5)

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

    def combo_instrumentChannel_callback(self, arg=None):
    #This method sets the channel to avoid conflict
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
    #This method is called when clicking on combobox
        self.controller.instrument.source_voltage_caliber = self.combo_voltageSource.get()

    def combo_currentSource_callback(self, args=None):
    #This method is called when clicking on combobox
        self.controller.instrument.source_current_caliber = self.combo_currentSource.get()

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
        self.controller.setVoltageSource(self.generateArguments(arg0=voltage, arg7=channel))

    def entry_currentSource_callback(self, arg=None):
    #This method calls the controller to change the voltage
        current = self.doubleVar_currentSource.get()    
        channel = self.combo_instrumentChannel.current() + 1     
        self.controller.instrument.source_current = current                 
        self.controller.setCurrentSource(self.generateArguments(arg0=current, arg7=channel))

    def channel_activate_callback(self):
    #This method call the controller to change output state 
        channel = self.combo_instrumentChannel.current() + 1 
        if self.controller.setChannelState(self.generateArguments(arg7=channel)) != "ERROR":
            if (self.intVar_radioValueChannel.get() == 1) and (self.controller.instrument.address != ""):
                self.entry_currentSource_callback()
                self.entry_voltageSource_callback()

                self.intVar_radioValueChannel.set(2) 
                self.radio_channelStateON.select() 
                self.updateMonitoring()
            else:
                self.intVar_radioValueChannel.set(1)
                self.radio_channelStateOFF.select() 

    def master_activate_callback(self):
    #This method call the controller to change output state 
        if self.controller.setMasterState([]) != "ERROR":
            if (self.intVar_radioValueMaster.get() == 1) and (self.controller.instrument.address != ""):
                self.entry_currentSource_callback()
                self.entry_voltageSource_callback()

                self.intVar_radioValueMaster.set(2) 
                self.radio_masterStateON.select()  
                channel = self.combo_instrumentChannel.current() + 1  
                thread = Thread(target=self.controller.continuousMeasure, args=(self.generateArguments(arg7=channel),)) 
                thread.start()
                self.updateMonitoring()
            else:
                self.intVar_radioValueMaster.set(1)
                self.radio_masterStateOFF.select() 

    def updateMonitoring(self):
    #This method  updates the measurement content
        if (self.intVar_radioValueChannel.get() == 2) and (self.intVar_radioValueMaster.get() == 2): 

            self.doubleVar_currentMeasure.set(self.controller.instrument.measure_current)
            self.doubleVar_voltageMeasure.set(self.controller.instrument.measure_voltage)
            self.doubleVar_powerMeasure.set(self.controller.instrument.measure_power)

            self.label_powerMeasure.after(500, self.updateMonitoring)

    def generateArguments(self, arg0="", arg1="", arg7=""):
    #This method generates a list of arguments to pilot the controller
        liste=[""]*14
        liste[0] = arg0
        liste[1] = arg1
        liste[7] = arg7

        return(liste)