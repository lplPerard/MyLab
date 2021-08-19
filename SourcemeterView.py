"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the Sourcemeter instrument's View.

"""

from tkinter.constants import END
from SourcemeterController import SourcemeterController
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
  
    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage     
        self.state="freeze"   

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)

        self.labelFrame_source = LabelFrame(self.frame, text="Source")
        self.labelFrame_measure = LabelFrame(self.frame, text="Measure")

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

        self.frame_measure_voltage = Frame(self.labelFrame_measure)
        self.frame_measure_current = Frame(self.labelFrame_measure)
        self.frame_measure_resistance = Frame(self.labelFrame_measure)

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentaddress = StringVar()

        self.doubleVar_source_voltage = DoubleVar()
        self.doubleVar_source_currentCompliance = DoubleVar()
        self.doubleVar_source_current = DoubleVar()
        self.doubleVar_source_voltageCompliance = DoubleVar()
        self.doubleVar_measure_voltage = DoubleVar()
        self.doubleVar_measure_current = DoubleVar()
        self.doubleVar_measure_resistance = DoubleVar()
        self.intVar_radio_source = IntVar()
        self.intVar_radio_masterState = IntVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_instrumentaddress = Label(self.frame_instrument_address, text="Address :")
        
        self.label_source_voltage = Label(self.frame_source_voltage, text="Voltage :")
        self.label_source_currentCompliance = Label(self.frame_source_currentCompliance, text="C.C.  :")
        self.label_source_current = Label(self.frame_source_current, text="Current :")
        self.label_source_voltageCompliance = Label(self.frame_source_voltageCompliance, text="V.C.  :")
        self.label_measure_voltage = Label(self.frame_measure_voltage, text="Voltage :    ")
        self.label_measure_current = Label(self.frame_measure_current, text="Current :    ")
        self.label_measure_resistance = Label(self.frame_measure_resistance, text="Resistance :")

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName, width=25)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentaddress, width=25, state="readonly")

        self.entry_source_voltage = Entry(self.frame_source_voltage, textvariable=self.doubleVar_source_voltage, width=10)
        self.entry_source_currentCompliance = Entry(self.frame_source_currentCompliance, textvariable=self.doubleVar_source_currentCompliance, width=10)
        self.entry_source_current = Entry(self.frame_source_current, textvariable=self.doubleVar_source_current, width=10)
        self.entry_source_voltageCompliance = Entry(self.frame_source_voltageCompliance, textvariable=self.doubleVar_source_voltageCompliance, width=10)
        self.entry_measure_voltage = Entry(self.frame_measure_voltage, textvariable=self.doubleVar_measure_voltage, width=10)
        self.entry_measure_current = Entry(self.frame_measure_current, textvariable=self.doubleVar_measure_current, width=10)
        self.entry_measure_resistance = Entry(self.frame_measure_resistance, textvariable=self.doubleVar_measure_resistance, width=10)

        self.combo_source_voltage = Combobox(self.frame_source_voltage, state="readonly", width=8, values=["V", "mV"])
        self.combo_source_currentCompliance = Combobox(self.frame_source_currentCompliance, state="readonly", width=8, values=["A", "mA"])
        self.combo_source_current = Combobox(self.frame_source_current, state="readonly", width=8, values=["A", "mA"])
        self.combo_source_voltageCompliance = Combobox(self.frame_source_voltageCompliance, state="readonly", width=8, values=["V", "mV"])
        self.combo_measure_voltage = Combobox(self.frame_measure_voltage, state="readonly", width=8, values=["V", "mV"])
        self.combo_measure_current = Combobox(self.frame_measure_current, state="readonly", width=8, values=["A", "mA"])        
        self.combo_measure_resistance = Combobox(self.frame_measure_resistance, state="readonly", width=8, values=["kΩ", "Ω", "MΩ"])

        self.img = None
        self.panel = Label(self.frame, bg=self.model.parameters_dict['backgroundColorInstrument'])
        
        self.radio_source1 = Radiobutton(self.frame_source1_radio, variable=self.intVar_radio_source, value=0)
        self.radio_source2 = Radiobutton(self.frame_source2_radio, variable=self.intVar_radio_source, value=1)

        self.radio_masterStateOFF = Radiobutton(self.frameline_button, text='OFF', variable=self.intVar_radio_masterState, value=0)
        self.radio_masterStateON = Radiobutton(self.frameline_button, text='ON', variable=self.intVar_radio_masterState, value=1)

        self.master_activate = Button(self.frameline_button, text='Master ON/OFF', command=self.master_activate_callback)

    def updateView(self, configuration=False):
    #This method refresh the content of the view
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        self.state="freeze"
        self.panel.destroy() 
        found=0

        for item in self.model.devices_dict:
            if item in self.controller.instrument.address:
                newName = self.model.devices_dict[item][0] + " (0)"
                self.entry_instrumentName_callback(newName=newName)

                if self.model.devices_dict[item][0] == "2400":   
                    self.img = Image.open(self.model.devices_dict[item][2])
                    self.img = self.img.resize((230, 105), Image.ANTIALIAS)
                    self.img = ImageTk.PhotoImage(self.img)
                    self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
                    self.panel.pack(fill = "both", expand = "yes")

                found=1
                break

        if (found==1) and (self.model.devices_dict[item][1] != "Sourcemeter"):
            self.view.menu5_callback(self)
            self.view.sendError('005')

        self.renameInstrument()

        if (found == 0) and (self.controller.instrument.address != ""):                
            self.term_text.insert(END, "\nUnknown device connected")
                       
        if self.controller.instrument.address != "":
            self.controller.connectToDevice()
  
    def renameInstrument(self):
        i = 0
        liste = self.view.listViews
        for item in liste:
            if self.controller.instrument.name == item.controller.instrument.name:    
                newName = self.controller.instrument.name[:-2] + str(i) + ")"
                self.entry_instrumentName_callback(newName=newName)
                i = i+1
             
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=5, fill="y")

        self.labelFrame_source.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_source.pack(padx=5, pady=5, fill="y")

        self.labelFrame_measure.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_measure.pack(padx=5, pady=5, fill="y")

    def initFrameLine(self):
    #This method instanciates all the frames used as lines
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_address.pack(fill="both", pady=3)

        self.frame_source1.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source1.pack(fill="both", pady=5)

        self.frame_source1_radio.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source1_radio.pack(side='left', fill="both", pady=5)

        self.frame_source1_setup.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source1_setup.pack(side='left', fill="both", pady=5)

        self.frame_source2.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source2.pack(fill="both", pady=5)

        self.frame_source2_radio.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source2_radio.pack(side='left', fill="both", pady=5)

        self.frame_source2_setup.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source2_setup.pack(side='left', fill="both", pady=5)

        self.frame_source_voltage.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_voltage.pack(fill="both", pady=5)

        self.frame_source_currentCompliance.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_currentCompliance.pack(fill="both", pady=5)

        self.frame_source_current.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_current.pack(fill="both", pady=5)

        self.frame_source_voltageCompliance.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_voltageCompliance.pack(fill="both", pady=5)        

        self.frame_measure_voltage.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_measure_voltage.pack(padx=5, pady=5, fill="y")

        self.frame_measure_current.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_measure_current.pack(padx=5, pady=5, fill="y")

        self.frame_measure_resistance.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_measure_resistance.pack(padx=5, pady=5, fill="y")

        self.frameline_button.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_button.pack(padx=5, pady=5, fill="y")
    
    def initVar(self):
    #This methods instanciates all the Var
        self.stringvar_instrumentName.set(self.controller.instrument.name)    
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        
        self.doubleVar_source_voltage.set(0)
        self.doubleVar_source_currentCompliance.set(0)
        self.doubleVar_source_current.set(0)
        self.doubleVar_source_voltageCompliance.set(0)
        self.doubleVar_measure_voltage.set(0)
        self.doubleVar_measure_current.set(0)
        self.doubleVar_measure_resistance.set(0)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentName.pack(side="left")

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

        self.label_measure_voltage.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_measure_voltage.pack(side="left")

        self.label_measure_current.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_measure_current.pack(side="left")

        self.label_measure_resistance.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_measure_resistance.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox
        #self.combo_source_voltage.bind("<<ComboboxSelected>>", self.combo_temperatureSource_callback)
        self.combo_source_voltage.configure(background='white')
        self.combo_source_voltage.current(0)
        self.combo_source_voltage.pack(side="right", padx=5)
        
        self.combo_source_currentCompliance.configure(background='white')
        self.combo_source_currentCompliance.current(0)
        self.combo_source_currentCompliance.pack(side="right", padx=5)
        
        self.combo_source_current.configure(background='white')
        self.combo_source_current.current(0)
        self.combo_source_current.pack(side="right", padx=5)
        
        self.combo_source_voltageCompliance.configure(background='white')
        self.combo_source_voltageCompliance.current(0)
        self.combo_source_voltageCompliance.pack(side="right", padx=5)
        
        self.combo_measure_voltage.configure(background='white')
        self.combo_measure_voltage.current(0)
        self.combo_measure_voltage.pack(side="right", padx=5)
        
        self.combo_measure_current.configure(background='white')
        self.combo_measure_current.current(0)
        self.combo_measure_current.pack(side="right", padx=5)
        
        self.combo_measure_resistance.configure(background='white')
        self.combo_measure_resistance.current(0)
        self.combo_measure_resistance.pack(side="right", padx=5)

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_instrumentaddress.bind('<Double-Button-1>', self.entry_instrumentaddress_callback)
        self.entry_instrumentaddress.pack(side='right', padx=5)

        self.entry_source_voltage.pack(side='right', padx=5)
        self.entry_source_voltage.bind('<Return>', self.entry_source_voltage_callback)

        self.entry_source_currentCompliance.pack(side='right', padx=5)
        self.entry_source_currentCompliance.bind('<Return>', self.entry_source_voltage_callback)
        
        self.entry_source_current.pack(side='right', padx=5)
        self.entry_source_current.bind('<Return>', self.entry_source_current_callback)
        
        self.entry_source_voltageCompliance.pack(side='right', padx=5)
        self.entry_source_voltageCompliance.bind('<Return>', self.entry_source_current_callback)
        
        self.entry_measure_voltage.pack(side='right', padx=5)
        
        self.entry_measure_current.pack(side='right', padx=5)
        
        self.entry_measure_resistance.pack(side='right', padx=5)

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
        if self.controller.setMasterState() != -1:
            if (self.intVar_radio_masterState.get() == 0) and (self.controller.instrument.address != ""):
                None
                #self.entry_currentSource_callback()
                #self.entry_voltageSource_callback()

                self.intVar_radio_masterState.set(1) 
                self.radio_masterStateON.select()  
                thread = Thread(target=self.controller.Measure) 
                thread.start()
                self.updateMonitoring()
            else:
                self.intVar_radio_masterState.set(0)
                self.radio_masterStateOFF.select() 

    def entry_source_voltage_callback(self, args=[]):
    #This method set Voltage source and current limit
        voltage = self.doubleVar_source_voltage.get()
        current = self.doubleVar_source_currentCompliance.get()

        self.controller.setVoltageSource(self.generateArguments(args1=voltage, args2=current))

    def entry_source_current_callback(self, args=[]):
    #This method set Voltage source and current limit
        current = self.doubleVar_source_current.get()
        voltage = self.doubleVar_source_voltageCompliance.get()

        self.controller.setCurrentSource(self.generateArguments(args1=current, args2=voltage))

    def updateMonitoring(self):
    #This method  updates the measurement content
        if self.intVar_radio_masterState.get() == 1: 
            self.doubleVar_measure_voltage.set(self.controller.instrument.measure_voltage)
            self.doubleVar_measure_current.set(self.controller.instrument.measure_current)
            self.doubleVar_measure_resistance.set(self.controller.instrument.measure_resistance)

            self.label_instrumentName.after(500, self.updateMonitoring)
