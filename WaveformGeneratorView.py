"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the WaveformGenerator instrument's View.

"""

from tkinter.constants import END
from WaveformGeneratorController import WaveformGeneratorController
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

class WaveformGeneratorView (DeviceFrame):
    """Class containing the Waveform Generator's View

    """

    def __init__(self, view, terminal, model, controller, name):
    #Constructor for the Waveform Generator's View

        DeviceFrame.__init__(self, view, controller, terminal, model)

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
        self.state="freeze"   
        self.labelFrame_signal = LabelFrame(self.frame, text="Source")

        self.canva_signal = Canvas(self.labelFrame_signal, scrollregion=(-200,-200,500,500), bg=self.model.parameters_dict['backgroundColor'])

        self.defilY = Scrollbar(self.labelFrame_signal, orient='vertical', command=self.canva_signal.yview, bg=self.model.parameters_dict['backgroundColor'])
        

        self.frame_instrument_name = Frame(self.canva_signal)
        self.frame_instrument_address = Frame(self.canva_signal)
        self.frame_master = Frame(self.frame)

        self.frame_source_voltage = Frame(self.canva_signal)
        self.frame_source_current = Frame(self.canva_signal)
        self.frame_source_button = Frame(self.canva_signal)
        self.frame_source_radio = Frame(self.canva_signal)
        self.frame_measure_voltage = Frame(self.canva_signal)
        self.frame_measure_current = Frame(self.canva_signal)
        self.frame_measure_power = Frame(self.canva_signal)
        self.frame_master_button = Frame(self.canva_signal)
        self.frame_master_radio = Frame(self.canva_signal)

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentaddress = StringVar()
        self.doubleVar_voltageSource = DoubleVar()
        self.doubleVar_currentSource = DoubleVar()
        self.doubleVar_voltageMeasure = DoubleVar()
        self.doubleVar_currentMeasure = DoubleVar()
        self.doubleVar_powerMeasure = DoubleVar()
        self.intVar_radioValueMaster = IntVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_instrumentaddress = Label(self.frame_instrument_address, text="Address :")

        self.label_voltageSource = Label(self.frame_source_voltage, text="Voltage :")
        self.label_currentSource = Label(self.frame_source_current, text="Current :")
        self.label_voltageMeasure = Label(self.frame_measure_voltage, text="Voltage :")
        self.label_currentMeasure = Label(self.frame_measure_current, text="Current :")
        self.label_powerMeasure = Label(self.frame_measure_power, text="Power :")
        self.label_powerMeasure.after(1000, self.updateMonitoring)

        self.combo_voltageSource = Combobox(self.frame_source_voltage, state="readonly", width=5, values=["V", "mV"])
        self.combo_currentSource = Combobox(self.frame_source_current, state="readonly", width=5, values=["A", "mA"])
        self.combo_voltageMeasure = Combobox(self.frame_measure_voltage, state="readonly", width=5, values=["V", "mV"])
        self.combo_currentMeasure = Combobox(self.frame_measure_current, state="readonly", width=5, values=["A", "mA"])
        self.combo_powerMeasure = Combobox(self.frame_measure_power, state="readonly", width=5, values=["W", "mW"])

        self.entry_instrumentName = Entry(self.frame_instrument_name, width=30, textvariable=self.stringvar_instrumentName)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, width=30, textvariable=self.stringvar_instrumentaddress, state="readonly")

        self.entry_voltageSource = Entry(self.frame_source_voltage, textvariable=self.doubleVar_voltageSource, width=6)
        self.entry_currentSource = Entry(self.frame_source_current, textvariable=self.doubleVar_currentSource, width=6)
        self.entry_voltageMeasure = Entry(self.frame_measure_voltage, textvariable=self.doubleVar_voltageMeasure, state="readonly")
        self.entry_currentMeasure = Entry(self.frame_measure_current, textvariable=self.doubleVar_currentMeasure, state="readonly")
        self.entry_powerMeasure = Entry(self.frame_measure_power, textvariable=self.doubleVar_powerMeasure, state="readonly")

        self.master_activate = Button(self.frame_master_button, text='Master ON/OFF', command=self.master_activate_callback)

        self.radio_masterStateOFF = Radiobutton(self.frame_master_radio, text='OFF', variable=self.intVar_radioValueMaster, value=1)
        self.radio_masterStateON = Radiobutton(self.frame_master_radio, text='ON', variable=self.intVar_radioValueMaster, value=2)
        
        self.img = None
        
    def clearInstrument(self):
    #This method is used to clear every trace of this instrument before being deleted
        None

    def renameInstrument(self):
        i = 0
        for item in self.view.listInstruments:
            if self.controller.instrument.name == item.controller.instrument.name:    
                newName = self.controller.instrument.name[:-2] + str(i) + ")"
                self.entry_instrumentName_callback(newName=newName)
                i = i+1

    def updateView(self):
    #This method refresh the content of the view
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        self.state="freeze" 
        found=0

        for item in self.model.devices_dict:
            if (item in self.controller.instrument.address) and (self.model.devices_dict[item][1] == "Waveform Generator"):
                self.controller.instrument.id = item

                newName = self.model.devices_dict[item][0] + " (0)"
                self.entry_instrumentName_callback(newName=newName)

                if self.model.devices_dict[item][0] == "33500B":   
                    self.img = Image.open(self.model.devices_dict[item][2])
                    self.img = self.img.resize((200, 120), Image.ANTIALIAS)
                    self.img = ImageTk.PhotoImage(self.img)
                    panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColor'])
                    panel.pack(fill = "both", expand = "yes")

                found=1
                break

        if (found==1) and (self.model.devices_dict[item][1] != "Waveform Generator"):
            self.view.menu5_callback(self)
            self.view.sendError('005')

        self.renameInstrument()

        if (found == 0) and (self.controller.instrument.address != ""):                
            self.term_text.insert(END, "\nUnknown device connected")
            
        if self.controller.instrument.address != "":
            self.controller.connectToDevice()
        
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=5, fill="y")
        
        self.canva_signal['yscrollcommand'] = self.defilY.set
        self.canva_signal.pack(side="left", fill="both")
        self.defilY.pack(fill="y", side='right', padx='5')

        self.labelFrame_signal.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_signal.pack(padx=5, pady=5, fill="y")

        self.labelFrame_signal.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_signal.pack(padx=5, pady=5, fill="y")

    def initFrameLine(self):
    #This method instanciates all the frame lines
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_instrument_address.pack(fill="both", pady=3)

        self.frame_source_voltage.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_voltage.pack(fill="both", pady=5)

        self.frame_source_current.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_current.pack(fill="both", pady=5)

        self.frame_source_button.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_button.pack(side="left", fill="both", pady=5)

        self.frame_source_radio.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_radio.pack(side="right", fill="both", pady=5)

        self.frame_measure_voltage.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_measure_voltage.pack(fill="both", pady=5)

        self.frame_measure_current.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_measure_current.pack(fill="both",pady=5)

        self.frame_measure_power.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_measure_power.pack(fill="both",pady=5)

        self.frame_master.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_master.pack(padx=5, pady=5, fill="y")

        self.frame_master_button.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_master_button.pack(side="left", padx=5, pady=5, fill="y")

        self.frame_master_radio.configure(bg=self.model.parameters_dict['backgroundColor'])
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
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentName.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentaddress.pack(side="left")

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

        self.entry_instrumentaddress.bind('<ButtonRelease-1>', self.view.menu2_Connections_callBack)
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
        self.master_activate.pack(expand="yes")

        self.radio_masterStateON.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateON.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled", disabledforeground="black")
        self.radio_masterStateOFF.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateOFF.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled", disabledforeground="black")

        self.intVar_radioValueMaster.set(1)

    def entry_instrumentName_callback(self, newName=None, arg=None):
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

    def entry_currentSource_callback(self, arg=None):
    #This method calls the controller to change the voltage
        current = self.doubleVar_currentSource.get()         

    def master_activate_callback(self):
    #This method call the controller to change output state 
        if self.controller.setMasterState() != -1:
            if (self.intVar_radioValueMaster.get() == 1) and (self.controller.instrument.address != ""):
                self.entry_currentSource_callback()
                self.entry_voltageSource_callback()

                self.intVar_radioValueMaster.set(2) 
                self.radio_masterStateON.select() 
                self.updateMonitoring()
            else:
                self.intVar_radioValueMaster.set(1)
                self.radio_masterStateOFF.select() 

    def updateMonitoring(self):
    #This method  updates the measurement content         
            None
            #self.label_powerMeasure.after(1000, self.updateMonitoring)