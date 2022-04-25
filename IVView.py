"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the Sourcemeter instrument's View.

"""

import imp
from os import listdir
import os
import threading
from tkinter.constants import END
from IVController import IVController
from DeviceFrame import DeviceFrame

from tkinter import Button, Canvas, Frame, IntVar, Label, Scrollbar, filedialog
from tkinter import LabelFrame
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import Entry
from tkinter import Radiobutton
from tkinter.ttk import Combobox, Progressbar
from PIL import Image, ImageTk

from Graph import Graph

from threading import Thread

import sys

class IVView (DeviceFrame):
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
        self.combo_instrument_callback()
  
    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage     
        self.state="freeze"   
        self.testState = "STOP"

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)

        self.labelFrame_testBench = LabelFrame(self.frame, text="TestBench")

        self.frameline_waveform = Frame(self.labelFrame_testBench)
        self.frameline_source = Frame(self.labelFrame_testBench)
        self.frameline_limit = Frame(self.labelFrame_testBench)

        self.frameline_button = Frame(self.frame)

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentaddress = StringVar()
        self.stringvar_waveform = StringVar("")

        self.doubleVar_limit= DoubleVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_instrument = Label(self.frame_instrument, text="Instrument :")
        self.label_instrumentaddress = Label(self.frame_instrument_address, text="Address :")
        
        self.label_waveform = Label(self.frameline_waveform, text="Waveform :    ")
        self.label_source = Label(self.frameline_source, text="Source Type  :")
        self.label_limit = Label(self.frameline_limit, text="Source Limit (V) :")

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName, width=25)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentaddress, width=25, state="readonly")

        self.entry_waveform = Entry(self.frameline_waveform, textvariable=self.stringvar_waveform, width=20, state="readonly")
        self.entry_limit = Entry(self.frameline_limit, textvariable=self.doubleVar_limit, justify="right", width=18)

        self.combo_instrument = Combobox(self.frame_instrument, state="readonly", width=15, values=["path1"])
        self.combo_source = Combobox(self.frameline_source, state="readonly", width=20, values=["Current (A)", "Voltage (V)"])

        self.progressbar = Progressbar(self.frameline_button, orient='horizontal', length = 100, mode = 'determinate')
        self.progressbar.after(50, self.updateProgressBar)

        self.graphImg = Image.open("Images/sine.png")
        self.graphImg = self.graphImg.resize((12, 13), Image.ANTIALIAS)
        self.graphImg = ImageTk.PhotoImage(self.graphImg)

        self.button_waveform = Button(self.frameline_waveform, image=self.graphImg, command=self.view.menu3_Waveform_callBack)
        self.button_launch = Button(self.frameline_button, text="Launch", command=self.button_launch_callback)

        self.graph = None

    def updateView(self, instrument=None):
    #This method refresh the content of the view, its is used when loading a configuration file
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        self.renameInstrument()

        if self.controller.instrument.address != "":                
            sys.stdout("\n" + self.combo_instrument.get() + " is now connected to " + self.controller.instrument.address)
            
        if instrument != None :
            self.combo_instrument.set(instrument.ident)
            self.combo_instrument_callback(instrument=instrument)
            self.stringvar_instrumentaddress.set(self.controller.instrument.address)
            self.stringvar_waveform.set(self.controller.instrument.waveform)
            self.combo_source.set(self.controller.instrument.source)
            self.doubleVar_limit.set(self.controller.instrument.limit)
            self.combo_source_callback()
                       
        if self.controller.instrument.address != "":
            self.controller.connectToDevice()
               
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=5, fill="y")

        self.labelFrame_testBench.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_testBench.pack(padx=5, pady=5, fill="y")

    def initFrameLine(self):
    #This method instanciates all the frames used as lines
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_address.pack(fill="both", pady=3)

        self.frameline_waveform.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_waveform.pack(fill="both", pady=2)

        self.frameline_source.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_source.pack(fill="both", pady=2)

        self.frameline_limit.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_limit.pack(fill="both", pady=2)

        self.frameline_button.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_button.pack(padx=5, pady=3, fill="y", expand="yes")
    
    def initVar(self):
    #This methods instanciates all the Var
        self.stringvar_instrumentName.set(self.controller.instrument.name)    
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        
        self.doubleVar_limit.set(0)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentName.pack(side="left")

        self.label_instrument.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrument.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentaddress.pack(side="left")

        self.label_waveform.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_waveform.pack(side="left", anchor='ne')

        self.label_source.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_source.pack(side="left", anchor='ne')

        self.label_limit.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_limit.pack(side="left", anchor='ne')

    def initCombo(self):
    #This methods instanciates all the combobox
        list=[]
        for dir in listdir("C:\\Oticon medical\\MyLab\\Instruments\\IV"):
            if dir != "__pycache__":
                list.append(dir)
            
        self.combo_instrument.configure(values=list)    
        self.combo_instrument.configure(background='white')
        self.combo_instrument.current(0)
        self.combo_instrument.pack(side="right", padx=3)
        self.combo_instrument.bind("<<ComboboxSelected>>", self.combo_instrument_callback)

        self.combo_source.configure(background='white')
        self.combo_source.current(0)
        self.combo_source.bind("<<ComboboxSelected>>", self.combo_source_callback)
        self.combo_source.pack(side="right", padx=5)

    def combo_instrument_callback(self, arg=None, instrument=None):
    #This method is called when selectionning an instrument via combo_instrument
        list=[]
        for dir in listdir("C:\\Oticon medical\\MyLab\\Instruments\\IV"):
            if dir != "__pycache__":
                list.append(dir)

        if instrument == None :
            file_path = "C:\\Oticon medical\\MyLab\\Instruments\\IV\\" + list[self.combo_instrument.current()] + "\\" + list[self.combo_instrument.current()] + ".py"
            self.controller.instrument.ident = list[self.combo_instrument.current()]

        else :            
            file_path = "C:\\Oticon medical\\MyLab\\Instruments\\IV\\" + instrument.ident + "\\" + instrument.ident + ".py"
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
        
    def combo_source_callback(self, arg=None):
#This method is called when clicking on Combo source
        self.controller.instrument.source = self.combo_source.get()

        if self.combo_source.current() == 1:
            self.label_limit.configure(text="Source Limit (A) :")

        elif self.combo_source.current() == 0:
            self.label_limit.configure(text="Source Limit (V) :")

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.pack(side='right', padx=5)
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)

        self.entry_instrumentaddress.pack(side='right', padx=5)
        self.entry_instrumentaddress.bind('<Double-Button-1>', lambda event, name=self : self.view.menu2_Connections_callBack(event, name))

        self.entry_limit.pack(side='right', padx=5)
        self.entry_limit.bind('<Return>', self.entry_limit_callback)

        self.entry_waveform.pack(side='left', padx=5)
        self.entry_waveform.bind('<Double-Button-1>', self.entry_waveform_callback)

    def initButton(self):
    #This method instanciates the buttons

        self.progressbar.pack(side='right', expand="yes", padx=5, fill='x', pady=4)
        self.button_launch.pack(expand="yes", padx=3)

        self.button_waveform.pack(side='right', expand="yes", padx=3)

        self.graph = Graph(frame=self.frame, model=self.model, size=(6,7))
        self.graph.clearGraph()
        self.graph.addLinGraph(xlabel="Voltage", ylabel="Current")

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

    def entry_limit_callback(self, args=[]):
    #This method set Voltage source and current limit
        self.controller.instrument.limit = self.doubleVar_limit.get()

    def entry_waveform_callback(self, args=[]):
    #This method set Voltage source and current limit           
        self.path = filedialog.askopenfilename(title = "Select file", filetypes = (("all files","*.*"), ("Waveform files","*.waveform")))

        if self.path != '':
            name = self.path.split('/')
            self.stringvar_waveform.set(name[-1][:-9])

        self.controller.instrument.waveform = self.path

    def button_launch_callback(self, args=None):
    #This method plays the desired waveform
        self.graph.clearGraph()

        if (self.testState != "RUN") and (self.stringvar_waveform.get() != ""):
            sys.stdout("\nNew IV testBench started\n")
            self.testState = "RUN"
            run = threading.Thread(target=self.controller.IV_test, args=[self.generateArguments(args1=self.path, args2=self.doubleVar_limit.get(), args8=self.combo_source.get())])
            self.updateProgressBar()
            run.daemon = True
            run.start()

    def updateProgressBar(self, args=None):
    #This methods updates the progressbar
        self.progressbar['value'] = self.controller.progress
        self.progressbar.after(50, self.updateProgressBar)
