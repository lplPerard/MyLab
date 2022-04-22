"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the Gearbox instrument's View.

"""
from os import listdir
import sys

from tkinter.constants import END
from DeviceFrame import DeviceFrame

from tkinter import Button, Frame, Label, StringVar, filedialog
from tkinter import Entry
from tkinter.ttk import Combobox
from PIL import Image, ImageTk

from threading import Thread

class GearboxView (DeviceFrame):
    """Class containing the Gearbox's View

    """

    def __init__(self, view, frame, terminal, model, controller, name):
    #Constructor for the Gearbox's View

        DeviceFrame.__init__(self, frame, controller, terminal, model)

        self.controller.instrument.name = name
        self.view=view

        self.initFrame(text=self.controller.instrument.type)
        self.initAttributes()
                
        self.initLabelFrame()
        self.initFrameLine()
        self.initLabel()
        self.initButtons()
        self.initCombo()
        self.initVar()
        self.initEntries()

    def updateView(self, configuration=False):
    #This method refresh the content of the view
        self.renameInstrument()
    
    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage     
        self.state="CLOSED"

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument_version = Frame(self.labelFrame_instrument)
        self.frame_instrument_image= Frame(self.labelFrame_instrument)
        self.frame_instrument_button_server = Frame(self.labelFrame_instrument)
        self.frame_instrument_button_hipro = Frame(self.labelFrame_instrument)
        self.frame_instrument_connect = Frame(self.labelFrame_instrument)

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name   : ")
        self.label_instrumentVersion = Label(self.frame_instrument_version, text="Version : ")
        self.label_instrumentImage = Label(self.frame_instrument_image, text="Image   : ")
        self.label_instrumentConnect = Label(self.frame_instrument_connect, text="Gearbox : ")
        self.label_instrumentHipro = Label(self.frame_instrument_connect, text="HiPro2     : ")

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentImage = StringVar()   

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName, width=30)
        self.entry_instrumentImage = Entry(self.frame_instrument_image, textvariable=self.stringvar_instrumentImage, width=30)

        self.combo_instrumentVersion = Combobox(self.frame_instrument_version, values=[""], state="readonly", width=27)

        self.button_set_server = Button(self.frame_instrument_button_server, text='Start Gearbox', command=self.button_set_server_callback)
        self.button_close_server = Button(self.frame_instrument_button_server, text='Close Gearbox', command=self.button_close_server_callback)

        self.button_set_hipro = Button(self.frame_instrument_button_hipro, text='Connect HiPro', command=self.button_set_hipro_callback)
        self.button_close_hipro = Button(self.frame_instrument_button_hipro, text='Disconnect HiPro', command=self.button_close_hipro_callback)

        self.img = Image.open("Images/gearbox.png")
        self.img = self.img.resize((250, 250), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.breakpointImg = Image.open("Images/breakpoint.png")
        self.breakpointImg = self.breakpointImg.resize((15, 15), Image.ANTIALIAS)
        self.breakpointImg = ImageTk.PhotoImage(self.breakpointImg)
        self.connect_point = Label(self.frame_instrument_connect, image=self.breakpointImg, bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.hipro_point = Label(self.frame_instrument_connect, image=self.breakpointImg, bg=self.model.parameters_dict['backgroundColorInstrumentData'])

        self.connectImg = Image.open("Images/connect.png")
        self.connectImg = self.connectImg.resize((15, 15), Image.ANTIALIAS)
        self.connectImg = ImageTk.PhotoImage(self.connectImg)
             
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=5, fill="y")
        
        self.panel.pack(fill = "both", expand = "yes")

    def initFrameLine(self):
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument_version.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_version.pack(fill="both", pady=3)

        self.frame_instrument_image.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_image.pack(fill="both", pady=3)

        self.frame_instrument_button_server.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_button_server.pack(fill="both", pady=5)

        self.frame_instrument_button_hipro.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_button_hipro.pack(fill="both", pady=5)

        self.frame_instrument_connect.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_connect.pack(fill="both", pady=5)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentName.pack(side="left")

        self.label_instrumentVersion.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentVersion.pack(side="left")

        self.label_instrumentImage.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentImage.pack(side="left")

        self.label_instrumentConnect.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentConnect.pack(side="left")

        self.connect_point.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.connect_point.pack(side="left", pady=5, padx=5, fill="y")

        self.label_instrumentHipro.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentHipro.pack(side="left")

        self.hipro_point.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.hipro_point.pack(side="left", pady=5, padx=5, fill="y")
        
    def initButtons(self):
    #This methods instanciates all the Label
        self.button_set_server.pack(side="left", pady=2, padx=2, expand="true")
        self.button_close_server.pack(side="left", pady=2, padx=2, expand="true")

        self.button_set_hipro.pack(side="left", pady=2, padx=2, expand="true")
        self.button_close_hipro.pack(side="left", pady=2, padx=2, expand="true")

    def initCombo(self):
    #This methods instanciates all the combobox
        #self.combo_temperatureSource.bind("<<ComboboxSelected>>", self.combo_temperatureSource_callback)
        list=[]
        for dir in listdir("C:\\toolsuites\\gearbox\\gearboxj"):
            list.append(dir)

        self.combo_instrumentVersion.configure(values=list, background='white')
        self.combo_instrumentVersion.current(0)
        self.combo_instrumentVersion.pack(side="right", padx=5)
        
    def initVar(self):
    #This methods instanciates all the Var
        self.stringvar_instrumentName.set(self.controller.instrument.name) 

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_instrumentImage.bind("<Double-Button-1>", self.entry_instrumentImage_callback)
        self.entry_instrumentImage.pack(side='right', padx=5)

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

    def entry_instrumentImage_callback(self, arg=None, newName=None):
    #This method calls the view to change instrument name
        path = filedialog.askopenfilename(title = "Select file", filetypes = (("Corona files","*.corona"), ("Metax files","*.metax"),("all files","*.*")))
        self.stringvar_instrumentImage.set(path)
 
    def button_set_server_callback(self):
    #This method call the controller to change output state 
        if self.stringvar_instrumentImage.get() != "":        
            sys.stdout("\nTrying to open Gearbox Server...\n")
            tmp = self.controller.Start_Server(gearbox=self.combo_instrumentVersion.get(), image=self.stringvar_instrumentImage.get())
            if tmp:
                self.connect_point.configure(image=self.connectImg)  
                self.state="CONNECTED"

            else :
                self.connect_point.configure(image=self.breakpointImg)  
                self.hipro_point.configure(image=self.breakpointImg)  

        else: 
            self.view.sendError("200")
 
    def button_close_server_callback(self):
    #This method call the controller to change output state 
        if self.state == "CONNECTED":
            self.controller.Stop_Server()
            self.state= "CLOSE"
            self.connect_point.configure(image=self.breakpointImg)  
            self.hipro_point.configure(image=self.breakpointImg)  
 
    def button_set_hipro_callback(self):
    #This method call the controller to change output state 
        if self.state == "CONNECTED":
            self.controller.Open_connection()
            self.hipro_point.configure(image=self.connectImg)  

        else :
            self.hipro_point.configure(image=self.breakpointImg)  
 
    def button_close_hipro_callback(self):
    #This method call the controller to change output state 
        if self.state == "CONNECTED":
            self.controller.Close_connection()
            self.hipro_point.configure(image=self.breakpointImg)  

    def close(self):
        if self.state == "CONNECTED":
            self.controller.Stop_Server()
