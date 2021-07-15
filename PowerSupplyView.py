"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the POwerSupply instrument's View.

"""

from tkinter.constants import END
from PowerSupplyController import PowerSupplyController
from DeviceFrame import DeviceFrame

from tkinter import Button, Frame, Label
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

    def __init__(self, view, terminal, model, controller, name):
    #Constructor for the PowerSupply's View

        DeviceFrame.__init__(self, view, controller, terminal, model)

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
        self.initButton()

    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage        
        self.labelFrame_source = LabelFrame(self.frame, text="Source")
        self.labelFrame_measure = LabelFrame(self.frame, text="Measure")

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)
        self.frame_instrument_channel =  Frame(self.labelFrame_instrument)

        self.frame_source_voltage = Frame(self.labelFrame_source)
        self.frame_source_current = Frame(self.labelFrame_source)
        self.frame_measure_voltage = Frame(self.labelFrame_measure)
        self.frame_measure_current = Frame(self.labelFrame_measure)
        self.frame_measure_power = Frame(self.labelFrame_measure)

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentaddress = StringVar()
        self.doubleVar_voltageSource = DoubleVar()
        self.doubleVar_currentSource = DoubleVar()
        self.doubleVar_voltageMeasure = DoubleVar()
        self.doubleVar_currentMeasure = DoubleVar()
        self.doubleVar_powerMeasure = DoubleVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_instrumentaddress = Label(self.frame_instrument_address, text="Address :")
        self.label_instrumentChannel = Label(self.frame_instrument_channel, text="Channel :")

        self.label_voltageSource = Label(self.frame_source_voltage, text="Voltage :")
        self.label_currentSource = Label(self.frame_source_current, text="Current :")
        self.label_voltageMeasure = Label(self.frame_measure_voltage, text="Voltage :")
        self.label_currentMeasure = Label(self.frame_measure_current, text="Current :")
        self.label_powerMeasure = Label(self.frame_measure_power, text="Power :")
        self.label_powerMeasure.after(1000, self.updateMonitoring)

        self.combo_instrumentChannel = Combobox(self.frame_instrument_channel, state="readonly", width=5, values=["1"])

        self.combo_voltageSource = Combobox(self.frame_source_voltage, state="readonly", width=5, values=["V", "mV"])
        self.combo_currentSource = Combobox(self.frame_source_current, state="readonly", width=5, values=["A", "mA"])
        self.combo_voltageMeasure = Combobox(self.frame_measure_voltage, state="readonly", width=5, values=["V", "mV"])
        self.combo_currentMeasure = Combobox(self.frame_measure_current, state="readonly", width=5, values=["A", "mA"])
        self.combo_powerMeasure = Combobox(self.frame_measure_power, state="readonly", width=5, values=["W", "mW"])

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentaddress, state="readonly")
        self.entry_instrumentaddress.bind('<ButtonRelease-1>', self.view.menu2_Connections_callBack)

        self.entry_voltageSource = Entry(self.frame_source_voltage, textvariable=self.doubleVar_voltageSource)
        self.entry_currentSource = Entry(self.frame_source_current, textvariable=self.doubleVar_currentSource)
        self.entry_voltageMeasure = Entry(self.frame_measure_voltage, textvariable=self.doubleVar_voltageMeasure, state="readonly")
        self.entry_currentMeasure = Entry(self.frame_measure_current, textvariable=self.doubleVar_currentMeasure, state="readonly")
        self.entry_powerMeasure = Entry(self.frame_measure_power, textvariable=self.doubleVar_powerMeasure, state="readonly")

        self.channel_activate = Button(self.labelFrame_source, text='On/Off', command=self.channel_activate_callback)
        self.channel_activateState="off"

        self.img = Image.open("HMC8042.png")

    def updateView(self):
    #This method refresh the content of the view
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)

        try:
            if self.model.devices_dict[self.controller.instrument.address][1] == "Power Supply":
                self.controller.instrument.channelNumber = self.model.devices_dict[self.controller.instrument.address][2]
                self.combo_instrumentChannel.configure(values=self.controller.instrument.channelNumber)

                oldname = self.controller.instrument.name
                self.controller.instrument.name = self.model.devices_dict[self.controller.instrument.address][0]
                indexMenu = self.view.menu5.index(oldname)
                self.view.menu5.entryconfigure(indexMenu, label=self.controller.instrument.name)
                self.stringvar_instrumentName.set(self.controller.instrument.name)

                if self.model.devices_dict[self.controller.instrument.address][0] == "HMC8042":   
                    self.img = self.img.resize((200, 100), Image.ANTIALIAS)
                    self.img = ImageTk.PhotoImage(self.img)
                    panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColor'])
                    panel.pack(fill = "both", expand = "yes")

            else:
                self.view.sendError("005")
        except:
            self.term_text.insert(END, "\nUnknown device connected\n")
            
        if self.controller.instrument.address != "":
            self.controller.connectToDevice()
        
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=5, fill="y")

        self.labelFrame_source.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_source.pack(padx=5, pady=5, fill="y")

        self.labelFrame_measure.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_measure.pack(padx=5, pady=5, fill="y")

    def initFrameLine(self):
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_instrument_address.pack(fill="both", pady=3)

        self.frame_instrument_channel.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_instrument_channel.pack(fill="both", pady=3)

        self.frame_source_voltage.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_voltage.pack(fill="both", pady=5)

        self.frame_source_current.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_current.pack(fill="both", pady=5)

        self.frame_measure_voltage.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_measure_voltage.pack(fill="both", pady=5)

        self.frame_measure_current.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_measure_current.pack(fill="both",pady=5)

        self.frame_measure_power.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_measure_power.pack(fill="both",pady=5)
    
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
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentName.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentaddress.pack(side="left")

        self.label_instrumentChannel.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentChannel.pack(side="left")

        self.label_voltageSource.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_voltageSource.pack(side="left")

        self.label_currentSource.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_currentSource.pack(side="left")

        self.label_voltageMeasure.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_voltageMeasure.pack(side="left")

        self.label_currentMeasure.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_currentMeasure.pack(side="left")

        self.label_powerMeasure.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_powerMeasure.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox
        #self.combo_instrumentChannel.bind("<<ComboboxSelected>>", self.combo_instrumentChannel_callback)
        self.combo_instrumentChannel.configure(background='white')
        self.combo_instrumentChannel.current(0)
        self.combo_instrumentChannel.pack(side="right")

        #self.combo_voltageSource.bind("<<ComboboxSelected>>", self.combo_voltageSource_callback)
        self.combo_voltageSource.configure(background='white')
        self.combo_voltageSource.current(0)
        self.combo_voltageSource.pack(side="right")
    
        #self.combo_currentSource.bind("<<ComboboxSelected>>", self.combo_currentSource_callback)
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
        self.channel_activate.pack()

    def entry_instrumentName_callback(self, arg):
    #This method calls the view to change instrument name
        oldname = self.controller.instrument.name
        name = self.stringvar_instrumentName.get()
        self.controller.instrument.name = name
        indexMenu = self.view.menu5.index(oldname)
        self.view.menu5.entryconfigure(indexMenu, label=name)

    def entry_voltageSource_callback(self, arg):
    #This method calls the controller to change the voltage
        voltage = self.doubleVar_voltageSource.get()  
        channel = self.combo_instrumentChannel.current() + 1        
        self.controller.setVoltageSource(voltage, channel)

    def entry_currentSource_callback(self, arg=None):
    #This method calls the controller to change the voltage
        current = self.doubleVar_currentSource.get()    
        channel = self.combo_instrumentChannel.current() + 1                  
        self.controller.setCurrentSource(current, channel)

    def channel_activate_callback(self):
    #This method call the controller to change output state 
        channel = self.combo_instrumentChannel.current() + 1 
        self.controller.setOutputState(channel)

        if self.channel_activateState == "off":
            self.channel_activateState="on"
            self.controller.instrument.state="on"      
            self.controller.updateMonitoring(channel)
        else:
            self.channel_activateState="off"
            self.controller.instrument.state="off"

    def updateMonitoring(self):
    #This method  updates the measurement content         
        self.label_powerMeasure.after(1000, self.updateMonitoring)
        channel = self.combo_instrumentChannel.current() + 1  

        if self.channel_activateState == "on":    
            self.controller.updateMonitoring(channel)