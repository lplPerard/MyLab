"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the POwerSupply instrument's View.

"""

from PowerSupplyController import PowerSupplyController
from DeviceFrame import DeviceFrame

from tkinter import Frame, Label
from tkinter import LabelFrame
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import Entry
from tkinter import Radiobutton
from tkinter.ttk import Combobox

from threading import Thread

class PowerSupplyView (DeviceFrame):
    """Class containing the PowerSupply's View

    """

    def __init__(self, root, terminal, model, controller, name):
    #Constructor for the PowerSupply's View

        DeviceFrame.__init__(self, root, terminal, model)
        self.controller = controller

        self.controller.instrument.name = name
        self.initFrame(text=self.controller.instrument.type)
        
        self.initLabelFrame()
        self.initFrameLine()
        self.initLabel()
        self.initCombo()
        self.initVar()
        self.initEntries()
        self.initRadio()

    def updateView(self):
    #This method refresh the content of the view
        self.stringvar_instrumentAdress.set(self.controller.instrument.adress)
        thread=Thread(target=self.controller.connectToDevice)
        thread.start()
        
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=5, fill="y")

        self.labelFrame_source = LabelFrame(self.frame, text="Source")
        self.labelFrame_source.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_source.pack(padx=5, pady=5, fill="y")

        self.labelFrame_measure = LabelFrame(self.frame, text="Measure")
        self.labelFrame_measure.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_measure.pack(padx=5, pady=5, fill="y")

    def initFrameLine(self):
        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument_connectMode = Frame(self.labelFrame_instrument)
        self.frame_instrument_connectMode.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_instrument_connectMode.pack(fill="both", pady=3)

        self.frame_instrument_adress = Frame(self.labelFrame_instrument)
        self.frame_instrument_adress.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_instrument_adress.pack(fill="both", pady=3)

        self.frame_source_voltage = Frame(self.labelFrame_source)
        self.frame_source_voltage.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_voltage.pack(fill="both", pady=5)

        self.frame_source_current = Frame(self.labelFrame_source)
        self.frame_source_current.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_current.pack(fill="both", pady=5)

        self.frame_measure_voltage = Frame(self.labelFrame_measure)
        self.frame_measure_voltage.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_measure_voltage.pack(fill="both", pady=5)

        self.frame_measure_current = Frame(self.labelFrame_measure)
        self.frame_measure_current.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_measure_current.pack(fill="both",pady=5)
    
    def initVar(self):
    #This methods instanciates all the Var
        self.stringvar_instrumentName = StringVar()
        self.stringvar_instrumentName.set(self.controller.instrument.name)
        
        self.stringvar_instrumentAdress = StringVar()
        self.stringvar_instrumentAdress.set(self.controller.instrument.adress)

        self.doubleVar_voltageSource = DoubleVar()
        self.doubleVar_voltageSource.set(0)

        self.doubleVar_currentSource = DoubleVar()
        self.doubleVar_currentSource.set(0)

        self.doubleVar_voltageMeasure = DoubleVar()
        self.doubleVar_voltageMeasure.set(0)

        self.doubleVar_currentMeasure = DoubleVar()
        self.doubleVar_currentMeasure.set(0)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentName.pack(side="left")

        self.label_instrumentConnectMode = Label(self.frame_instrument_connectMode, text="Connect mode :")
        self.label_instrumentConnectMode.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentConnectMode.pack(side="left")

        self.label_instrumentAdress = Label(self.frame_instrument_adress, text="Adress :")
        self.label_instrumentAdress.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentAdress.pack(side="left")

        self.label_voltageSource = Label(self.frame_source_voltage, text="Voltage :")
        self.label_voltageSource.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_voltageSource.pack(side="left")

        self.label_currentSource = Label(self.frame_source_current, text="Current :")
        self.label_currentSource.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_currentSource.pack(side="left")

        self.label_voltageMeasure = Label(self.frame_measure_voltage, text="Voltage :")
        self.label_voltageMeasure.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_voltageMeasure.pack(side="left")

        self.label_currentMeasure = Label(self.frame_measure_current, text="Current :")
        self.label_currentMeasure.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_currentMeasure.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox
        self.combo_instrumentConnectMode = Combobox(self.frame_instrument_connectMode, state="readonly", width=5, values=["USB", "Ethernet"])
        #self.combo_instrumentConnectMode.bind("<<ComboboxSelected>>", self.combo_instrumentConnectMode_callback)
        self.combo_instrumentConnectMode.configure(background='white')
        self.combo_instrumentConnectMode.current(0)
        self.combo_instrumentConnectMode.pack(side="right")

        self.combo_voltageSource = Combobox(self.frame_source_voltage, state="readonly", width=5, values=["V", "mV"])
        #self.combo_voltageSource.bind("<<ComboboxSelected>>", self.combo_voltageSource_callback)
        self.combo_voltageSource.configure(background='white')
        self.combo_voltageSource.current(0)
        self.combo_voltageSource.pack(side="right")
    
        self.combo_currentSource = Combobox(self.frame_source_current, state="readonly", width=5, values=["A", "mA"])
        #self.combo_currentSource.bind("<<ComboboxSelected>>", self.combo_currentSource_callback)
        self.combo_currentSource.configure(background='white')
        self.combo_currentSource.current(0)
        self.combo_currentSource.pack(side="right")
    
        self.combo_voltageMeasure = Combobox(self.frame_measure_voltage, state="readonly", width=5, values=["V", "mV"])
        #self.combo_voltageMeasure.bind("<<ComboboxSelected>>", self.combo_voltageMeasure_callback)
        self.combo_voltageMeasure.configure(background='white')
        self.combo_voltageMeasure.current(0)
        self.combo_voltageMeasure.pack(side="right")
    
        self.combo_currentMeasure = Combobox(self.frame_measure_current, state="readonly", width=5, values=["A", "mA"])
        #self.combo_currentMeasure.bind("<<ComboboxSelected>>", self.combo_currentMeasure_callback)
        self.combo_currentMeasure.configure(background='white')
        self.combo_currentMeasure.current(0)
        self.combo_currentMeasure.pack(side="right")

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_instrumentAdress = Entry(self.frame_instrument_adress, textvariable=self.stringvar_instrumentAdress)
        self.entry_instrumentAdress.pack(side='right', padx=5)

        self.entry_voltageSource = Entry(self.frame_source_voltage, textvariable=self.doubleVar_voltageSource)
        self.entry_voltageSource.bind("<Return>", self.entry_voltageSource_callback)
        self.entry_voltageSource.pack(side='right', padx=5)

        self.entry_currentSource = Entry(self.frame_source_current, textvariable=self.doubleVar_currentSource)
        self.entry_currentSource.bind("<Return>", self.entry_currentSource_callback)
        self.entry_currentSource.pack(side='right', padx=5)

        self.entry_voltageMeasure = Entry(self.frame_measure_voltage, textvariable=self.doubleVar_voltageMeasure)
        self.entry_voltageMeasure.pack(side='right', padx=5)

        self.entry_currentMeasure = Entry(self.frame_measure_current, textvariable=self.doubleVar_currentMeasure)
        self.entry_currentMeasure.pack(side='right', padx=5)

    def initRadio(self):
    #This method instanciates the Radio buttons

        self.channel_activate = Radiobutton(self.labelFrame_source, text='On/Off', indicatoron=0)
        self.channel_activate.pack()

    def entry_voltageSource_callback(self, arg):
    #This methods calls the controller to change the voltage
        voltage = self.doubleVar_voltageSource.get()
        thread=Thread(target=self.controller.setVoltageSource(voltage))
        thread.start()

    def entry_currentSource_callback(self):
    #This methods calls the controller to change the voltage
        current = self.doubleVar_currentSource.get()
        thread=Thread(target=self.controller.setCurrentSource(current))
        thread.start()
        