"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the Climatic Chamber instrument's View.

"""

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

                if self.model.devices_dict[item][0] == "VT4002 EMC":   
                    self.img = Image.open(self.model.devices_dict[item][2])
                    self.img = self.img.resize((200, 300), Image.ANTIALIAS)
                    self.img = ImageTk.PhotoImage(self.img)
                    self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
                    self.panel.pack(fill = "both", expand = "yes")

                found=1
                break

        if (found==1) and (self.model.devices_dict[item][1] != "Climatic Chamber"):
            self.view.menu5_callback(self)
            self.view.sendError('005')

        self.renameInstrument()

        if (found == 0) and (self.controller.instrument.address != ""):                
            self.term_text.insert(END, "\nUnknown device connected")
                       
        if self.controller.instrument.address != "":  
            #adress = self.stringvar_instrumentaddress.get()   
            adress = self.controller.instrument.address.split(" ")[0]
            self.controller.connectToDevice(adress)
    
    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage     
        self.state="freeze"   
        self.labelFrame_source = LabelFrame(self.frame, text="Source")
        self.labelFrame_measure = LabelFrame(self.frame, text="Measure")

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)
        self.frame_master = Frame(self.frame)

        self.frame_source_temperature = Frame(self.labelFrame_source)
        self.frame_source_button = Frame(self.labelFrame_source)
        self.frame_source_radio = Frame(self.labelFrame_source)
        self.frame_measure_temperature = Frame(self.labelFrame_measure)
        self.frame_master_button = Frame(self.frame_master)
        self.frame_master_radio = Frame(self.frame_master)

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentaddress = StringVar()
        self.doubleVar_temperatureSource = DoubleVar()
        self.doubleVar_temperatureMeasure = DoubleVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_instrumentaddress = Label(self.frame_instrument_address, text="Address :")

        self.label_temperatureSource = Label(self.frame_source_temperature, text="Temperature :")
        self.label_temperatureMeasure = Label(self.frame_measure_temperature, text="Temperature :")

        self.combo_temperatureSource = Combobox(self.frame_source_temperature, state="readonly", width=5, values=["°C", "°F"])
        self.combo_temperatureMeasure = Combobox(self.frame_measure_temperature, state="readonly", width=5, values=["°C", "°F"])

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentaddress, state="readonly")

        self.entry_temperatureSource = Entry(self.frame_source_temperature, textvariable=self.doubleVar_temperatureSource, width=6)
        self.entry_temperatureMeasure = Entry(self.frame_measure_temperature, textvariable=self.doubleVar_temperatureMeasure, width=6, state="readonly")

        self.button_set = Button(self.frame, text='Set Temperature', command=self.button_set_callback)
        self.button_measure = Button(self.frame, text='Measure Temperature', command=self.button_measure_callback)
        
        self.img = None
        self.panel = Label(self.frame, bg=self.model.parameters_dict['backgroundColorInstrument'])

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
        
        self.button_set.pack(padx=5, pady=5, fill="y")

        self.labelFrame_measure.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_measure.pack(padx=5, pady=5, fill="y")

        self.button_measure.pack(padx=5, pady=5, fill="y")

    def initFrameLine(self):
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_address.pack(fill="both", pady=3)

        self.frame_source_temperature.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_temperature.pack(fill="both", pady=5)

        self.frame_source_button.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_button.pack(side="left", fill="both", pady=5)

        self.frame_source_radio.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_radio.pack(side="right", fill="both", pady=5)

        self.frame_measure_temperature.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_measure_temperature.pack(fill="both", pady=5)

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
        self.doubleVar_temperatureSource.set(0)
        self.doubleVar_temperatureMeasure.set(0)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentName.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentaddress.pack(side="left")

        self.label_temperatureSource.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_temperatureSource.pack(side="left")

        self.label_temperatureMeasure.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_temperatureMeasure.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox
        #self.combo_temperatureSource.bind("<<ComboboxSelected>>", self.combo_temperatureSource_callback)
        self.combo_temperatureSource.configure(background='white')
        self.combo_temperatureSource.current(0)
        self.combo_temperatureSource.pack(side="right", padx=5)
    
        #self.combo_temperatureMeasure.bind("<<ComboboxSelected>>", self.combo_temperatureMeasure_callback)
        self.combo_temperatureMeasure.configure(background='white')
        self.combo_temperatureMeasure.current(0)
        self.combo_temperatureMeasure.pack(side="right", padx=5)

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_instrumentaddress.bind('<Double-Button-1>', lambda event, name=self : self.view.menu2_Connections_callBack(event, name))
        self.entry_instrumentaddress.pack(side='right', padx=5)

        #self.entry_temperatureSource.bind("<Return>", self.entry_temperatureSource_callback)
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
 
    def button_set_callback(self):
    #This method call the controller to change output state     
        temperature = self.doubleVar_temperatureSource.get()
        self.controller.setTemperature(self.generateArguments(args0=temperature))
 
    def button_measure_callback(self):
    #This method call the controller to change output state     
        temperature = self.controller.getTemperature()
        self.doubleVar_temperatureMeasure.set(temperature)

    def generateArguments(self, args0=""):
        liste=[""]*14

        liste[0] = args0

        return(liste)
        