"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the Sourcemeter instrument's View.

"""

import threading
from tkinter.constants import END
from RFSensitivityController import RFSensitivityController
from DeviceFrame import DeviceFrame

from tkinter import Button, Frame, Label, Listbox
from tkinter import LabelFrame
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import Entry
from tkinter.ttk import Combobox, Progressbar
from PIL import Image, ImageTk

from threading import Thread

import sys

class RFSensitivityView (DeviceFrame):
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
        self.initListBox()
  
    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage
        self.testState = "STOP"

        self.labelFrame_testBench = LabelFrame(self.frame, text="TestBench")

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frameline_frequency = Frame(self.labelFrame_testBench)
        self.frameline_power = Frame(self.labelFrame_testBench)
        self.frameline_attenuation = Frame(self.labelFrame_testBench)
        self.frameline_bitRate= Frame(self.labelFrame_testBench)
        self.frameline_PER = Frame(self.labelFrame_testBench)
        self.frameline_button = Frame(self.frame)

        self.stringvar_instrumentName = StringVar()    
        self.doubleVar_power = DoubleVar()
        self.doubleVar_attenuation = DoubleVar()
        self.doubleVar_PER = DoubleVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_frequency = Label(self.frameline_frequency, text="Frequency : ")
        self.label_power = Label(self.frameline_power, text="Initial Power (dBm) : ")
        self.label_attenuation = Label(self.frameline_attenuation, text="Attenuation (dB) :     ")
        self.label_bitRate = Label(self.frameline_bitRate, text="Bit Rate : ")
        self.label_PER = Label(self.frameline_PER, text="PER Target (%) :         ")

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName)
        self.entry_power = Entry(self.frameline_power, textvariable=self.doubleVar_power, justify="right", width=10)
        self.entry_attenuation = Entry(self.frameline_attenuation, textvariable=self.doubleVar_attenuation, justify="right", width=10)
        self.entry_PER = Entry(self.frameline_PER, textvariable=self.doubleVar_PER, justify="right", width=10)
        
        self.listbox_frequency = Listbox(self.frameline_frequency, selectmode='extended', width=17, height=6)

        self.combo_bitRate = Combobox(self.frameline_bitRate, state="readonly", width=15, values=["BLE (1 Mpbs)",
                                                                                                  "ABLE (1 Mpbs)",
                                                                                                  "OBLE (4 Mpbs)",
                                                                                                  "OBLE (2 Mpbs)"])

        self.progressbar = Progressbar(self.frameline_button, orient='horizontal', length = 130, mode = 'determinate')

        self.button_launch = Button(self.frameline_button, text="Launch", command=self.button_launch_callback)
        
        self.img = Image.open("Images/SMU200A.png")
        self.img = self.img.resize((250, 110), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])

    def updateView(self, instrument=None):
    #This method refresh the content of the view, its is used when loading a configuration file
        self.renameInstrument()

        if instrument != None :
            pass
          
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=5, fill="y")

        self.labelFrame_testBench.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_testBench.pack(padx=5, pady=5, fill="y")

    def initFrameLine(self):
    #This method instanciates all the frames used as lines
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frameline_frequency.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_frequency.pack(fill="both", pady=2)

        self.frameline_power.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_power.pack(fill="both", pady=2)

        self.frameline_attenuation.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_attenuation.pack(fill="both", pady=2)

        self.frameline_bitRate.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_bitRate.pack(fill="both", pady=2)

        self.frameline_PER.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_PER.pack(fill="both", pady=2)

        self.frameline_button.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_button.pack(padx=5, pady=3, fill="y", expand="yes")
    
    def initVar(self):
    #This methods instanciates all the Var
        self.stringvar_instrumentName.set(self.controller.instrument.name)    

        self.doubleVar_power.set(-90)
        self.doubleVar_attenuation.set(6)
        self.doubleVar_PER.set(30.8)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentName.pack(side="left")

        self.label_frequency.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_frequency.pack(side="left", anchor='ne')

        self.label_power.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_power.pack(side="left", anchor='ne')

        self.label_attenuation.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_attenuation.pack(side="left", anchor='ne')

        self.label_bitRate.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_bitRate.pack(side="left", anchor='ne')

        self.label_PER.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_PER.pack(side="left", anchor='ne')

    def initCombo(self):
    #This methods instanciates all the combobox
        #self.combo_source_voltage.bind("<<ComboboxSelected>>", self.combo_temperatureSource_callback)
        self.combo_bitRate.configure(background='white')
        self.combo_bitRate.current(0)
        self.combo_bitRate.pack(side="right", padx=5)

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_power.pack(side='left', padx=5)
        self.entry_attenuation.pack(side='left', padx=5)
        self.entry_PER.pack(side='left', padx=5)

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

    def initButton(self):
    #This method instanciates the buttons
        self.progressbar.pack(side='right', expand="yes", padx=5, fill='x', pady=4)
        self.button_launch.pack(expand="yes", padx=3)

        self.panel.pack(fill = "both", expand = "yes")

    def button_launch_callback(self, args=None):
    #This method plays the desired waveform
        if (self.testState != "RUN"):
            run = threading.Thread(target=self.controller.RFSensitivity_test, args=[self.generateArguments(args1=self.doubleVar_power.get(),
                                                                                                           args2=self.doubleVar_attenuation.get(),
                                                                                                           args3=self.doubleVar_PER.get(),
                                                                                                           args8=self.combo_bitRate.get())])
            self.updateProgressBar()
            run.daemon = True
            run.start()
            sys.stdout("\nNew RF Sensitivity testBench started\n")
            self.testState = "RUN"

    def initListBox(self, args=None):
    #This method initialize Listboxes
        frequencies = ["2.402GHz (ch. 37)",
                       "2.404GHz (ch. 00)",
                       "2.406GHz (ch. 01)",
                       "2.408GHz (ch. 02)",
                       "2.410GHz (ch. 03)",
                       "2.412GHz (ch. 04)",
                       "2.414GHz (ch. 05)",
                       "2.416GHz (ch. 06)",
                       "2.418GHz (ch. 07)",
                       "2.420GHz (ch. 08)",
                       "2.422GHz (ch. 09)",
                       "2.424GHz (ch. 10)",
                       "2.426GHz (ch. 38)",
                       "2.428GHz (ch. 11)",
                       "2.430GHz (ch. 12)",
                       "2.432GHz (ch. 13)",
                       "2.434GHz (ch. 14)",
                       "2.436GHz (ch. 15)",
                       "2.438GHz (ch. 16)",
                       "2.440GHz (ch. 17)",
                       "2.442GHz (ch. 18)",
                       "2.444GHz (ch. 19)",
                       "2.446GHz (ch. 20)",
                       "2.448GHz (ch. 21)",
                       "2.450GHz (ch. 22)",
                       "2.452GHz (ch. 23)",
                       "2.454GHz (ch. 24)",
                       "2.456GHz (ch. 25)",
                       "2.458GHz (ch. 26)",
                       "2.460GHz (ch. 27)",
                       "2.462GHz (ch. 28)",
                       "2.464GHz (ch. 29)",
                       "2.466GHz (ch. 30)",
                       "2.468GHz (ch. 31)",
                       "2.470GHz (ch. 32)",
                       "2.472GHz (ch. 33)",
                       "2.474GHz (ch. 34)",
                       "2.476GHz (ch. 35)",
                       "2.478GHz (ch. 36)",
                       "2.480GHz (ch. 39)"]

        for item in frequencies:
            self.listbox_frequency.insert('end', item)

        self.listbox_frequency.pack(pady=5, expand='yes')
        self.listbox_frequency.configure(selectbackground="grey")
        self.listbox_frequency.selection_set(0, len(frequencies))

    def getFrequencies(self, args=None):
    #This method return the selected frequencies from the Frequency ListBox
        liste = self.listbox_frequency.curselection()
        tmp = []

        for index in liste :
            tmp.append(self.listbox_frequency.get(index))

        return(tmp)

    def updateProgressBar(self, args=None):
    #This methods updates the progressbar
            self.progressbar['value'] = self.controller.progress
            self.progressbar.after(50, self.updateProgressBar)

