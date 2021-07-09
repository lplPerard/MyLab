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

class PowerSupplyView (DeviceFrame):
    """Class containing the PowerSupply's View

    """

    def __init__(self, root, terminal, model, controller):
    #Constructor for the PowerSupply's View

        DeviceFrame.__init__(self, root, terminal, model)
        self.controller = controller

        self.initFrame(text=self.localController.instrument.type)
        
        self.initLabelFrame()
        self.initFrameLine()
        self.initLabel()
        self.initCombo()
        self.initVar()
        self.initEntries()
        self.initRadio()

    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_source = LabelFrame(self.frame, text="Source")
        self.labelFrame_source.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_source.pack(padx=5, pady=5)

        self.labelFrame_measure = LabelFrame(self.frame, text="Measure")
        self.labelFrame_measure.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_measure.pack(padx=5, pady=5)

    def initFrameLine(self):

        self.frame_source_voltage = Frame(self.labelFrame_source)
        self.frame_source_voltage.pack(fill="both")

        self.frame_source_current = Frame(self.labelFrame_source)
        self.frame_source_current.pack(fill="both")

        self.frame_measure_voltage = Frame(self.labelFrame_measure)
        self.frame_measure_voltage.pack(fill="both")

        self.frame_measure_current = Frame(self.labelFrame_measure)
        self.frame_measure_current.pack(fill="both")
    
    def initVar(self):
    #This methods instanciates all the Var
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
        self.label_voltageSource = Label(self.frame_source_voltage, text="Voltage")
        self.label_voltageSource.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_voltageSource.pack(side="left")

        self.label_currentSource = Label(self.frame_source_current, text="Current")
        self.label_currentSource.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_currentSource.pack(side="left")

        self.label_voltageMeasure = Label(self.frame_measure_voltage, text="Voltage")
        self.label_voltageMeasure.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_voltageMeasure.pack(side="left")

        self.label_currentMeasure = Label(self.frame_measure_current, text="Current")
        self.label_currentMeasure.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_currentMeasure.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox

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
        self.entry_voltageSource = Entry(self.frame_source_voltage, textvariable=self.doubleVar_voltageSource)
        self.entry_voltageSource.pack(side='right')

        self.entry_currentSource = Entry(self.frame_source_current, textvariable=self.doubleVar_currentSource)
        self.entry_currentSource.pack(side='right')

        self.entry_voltageMeasure = Entry(self.frame_measure_voltage, textvariable=self.doubleVar_voltageMeasure)
        self.entry_voltageMeasure.pack(side='right')

        self.entry_currentMeasure = Entry(self.frame_measure_current, textvariable=self.doubleVar_currentMeasure)
        self.entry_currentMeasure.pack(side='right')

    def initRadio(self):
    #This method instanciates the Radio buttons

        self.channel_activate = Radiobutton(self.labelFrame_source, text='On/Off', indicatoron=0)
        self.channel_activate.pack()