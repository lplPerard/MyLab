"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the Multimeter instrument's View.

"""

from tkinter.constants import END
from MultimeterController import MultimeterController
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

import sys

class MultimeterView (DeviceFrame):
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
        self.radio_setupState_callback()
  
    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage     
        self.state="freeze"   
        self.labelFrame_setup = LabelFrame(self.frame, text="Setup")
        self.canva_setup = Canvas(self.labelFrame_setup, scrollregion=(0,0,0,470), bd=0, highlightthickness=0, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.defilY_setup = Scrollbar(self.labelFrame_setup, orient='vertical', command=self.canva_setup.yview, bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)
        self.scrollframe_setup = Frame(self.canva_setup)
        self.frame_measure = Frame(self.frame)

        self.frame_source_temperature = Frame(self.scrollframe_setup)
        self.frame_source_button = Frame(self.scrollframe_setup)
        self.frame_source_radio = Frame(self.scrollframe_setup)
        self.frame_DCV = Frame(self.scrollframe_setup)
        self.frame_ACV = Frame(self.scrollframe_setup)
        self.frame_DCI = Frame(self.scrollframe_setup)
        self.frame_DCI_caliber = Frame(self.scrollframe_setup)
        self.frame_ACI = Frame(self.scrollframe_setup)
        self.frame_ACI_caliber = Frame(self.scrollframe_setup)
        self.frame_2WR = Frame(self.scrollframe_setup)
        self.frame_4WR = Frame(self.scrollframe_setup)
        self.frame_diode = Frame(self.scrollframe_setup)
        self.frame_diode_caliber = Frame(self.scrollframe_setup) 
        self.frame_continuity = Frame(self.scrollframe_setup)
        self.frame_frequency = Frame(self.scrollframe_setup)
        self.frame_period = Frame(self.scrollframe_setup)
        self.frame_measure_button = Frame(self.frame_measure)
        self.frame_measure_radio = Frame(self.frame_measure)

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentaddress = StringVar()
        self.doubleVar_DCV = DoubleVar()
        self.doubleVar_ACV = DoubleVar()
        self.doubleVar_DCI = DoubleVar()
        self.doubleVar_ACI = DoubleVar()
        self.doubleVar_2WR = DoubleVar()
        self.doubleVar_4WR = DoubleVar()
        self.doubleVar_diode = DoubleVar()
        self.doubleVar_frequency = DoubleVar()
        self.doubleVar_period = DoubleVar()
        self.intVar_radioValueSetup = IntVar()
        self.intVar_radioValueCaliberA = IntVar()
        self.intVar_radioValueCaliberDiodeV = IntVar()
        self.intVar_radioValueCaliberDiodeA = IntVar()
        self.intVar_radioValuemeasure = IntVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_instrumentaddress = Label(self.frame_instrument_address, text="Address :")
        
        self.label_DCI_caliber = Label(self.frame_DCI_caliber, text="Caliber :")
        self.label_ACI_caliber = Label(self.frame_ACI_caliber, text="Caliber :")
        self.label_frequency_unit = Label(self.frame_frequency, text=" Hz")
        self.label_period_unit = Label(self.frame_period, text=" s   ")
        self.label_diode_unit = Label(self.frame_diode, text=" s   ")

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName, width=25)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentaddress, width=25, state="readonly")

        self.entry_DCV = Entry(self.frame_DCV, textvariable=self.doubleVar_DCV, state="readonly", width=10)
        self.entry_ACV = Entry(self.frame_ACV, textvariable=self.doubleVar_ACV, state="readonly", width=10)
        self.entry_DCI = Entry(self.frame_DCI, textvariable=self.doubleVar_DCI, state="readonly", width=10)
        self.entry_ACI = Entry(self.frame_ACI, textvariable=self.doubleVar_ACI, state="readonly", width=10)
        self.entry_2WR = Entry(self.frame_2WR, textvariable=self.doubleVar_2WR, state="readonly", width=10)
        self.entry_4WR = Entry(self.frame_4WR, textvariable=self.doubleVar_4WR, state="readonly", width=10)
        self.entry_diode = Entry(self.frame_diode, textvariable=self.doubleVar_diode, state="readonly", width=14)
        self.entry_frequency = Entry(self.frame_frequency, textvariable=self.doubleVar_frequency, state="readonly", width=14)
        self.entry_period = Entry(self.frame_period, textvariable=self.doubleVar_period, state="readonly", width=14)

        self.combo_DCV = Combobox(self.frame_DCV, state="readonly", width=8, values=["1V", "100mV", "1000V", "100V", "10V"])
        self.combo_ACV = Combobox(self.frame_ACV, state="readonly", width=8, values=["1V", "100mV", "750V", "100V", "10V"])
        self.combo_DCI = Combobox(self.frame_DCI, state="readonly", width=8, values=["1mA", "100uA", "400mA", "100mA", "10mA"])
        self.combo_ACI = Combobox(self.frame_ACI, state="readonly", width=8, values=["10mA", "400mA", "100mA"])
        self.combo_2WR = Combobox(self.frame_2WR, state="readonly", width=8, values=["1kΩ", "100Ω", "10kΩ", "100kΩ", "1MΩ", "10MΩ", "100MΩ"])
        self.combo_4WR = Combobox(self.frame_4WR, state="readonly", width=8, values=["1kΩ", "100Ω", "10kΩ", "100kΩ", "1MΩ", "10MΩ", "100MΩ"])
        
        self.diodeImg = Image.open("Images/diode.png")
        self.diodeImg = self.diodeImg.resize((30, 17), Image.ANTIALIAS)
        self.diodeImg = ImageTk.PhotoImage(self.diodeImg)
        self.diodeImg_grey = Image.open("Images/diode_grey.png")
        self.diodeImg_grey = self.diodeImg_grey.resize((30, 17), Image.ANTIALIAS)
        self.diodeImg_grey = ImageTk.PhotoImage(self.diodeImg_grey)

        self.continuityImg = Image.open("Images/continuity.png")
        self.continuityImg = self.continuityImg.resize((25, 15), Image.ANTIALIAS)
        self.continuityImg = ImageTk.PhotoImage(self.continuityImg)   
        self.continuityImg_grey = Image.open("Images/continuity_grey.png")
        self.continuityImg_grey = self.continuityImg_grey.resize((25, 15), Image.ANTIALIAS)
        self.continuityImg_grey = ImageTk.PhotoImage(self.continuityImg_grey)         

        self.img = None
        self.panel = Label(self.frame, bg=self.model.parameters_dict['backgroundColorInstrument'])
        
        self.radio_DCV = Radiobutton(self.frame_DCV, text='DC V', variable=self.intVar_radioValueSetup, value=0, command=self.radio_setupState_callback)
        self.radio_ACV = Radiobutton(self.frame_ACV, text='AC V', variable=self.intVar_radioValueSetup, value=1, command=self.radio_setupState_callback)
        self.radio_DCI = Radiobutton(self.frame_DCI, text='DC I', variable=self.intVar_radioValueSetup, value=2, command=self.radio_setupState_callback)
        self.radio_ACI = Radiobutton(self.frame_ACI, text='AC I', variable=self.intVar_radioValueSetup, value=3, command=self.radio_setupState_callback)
        self.radio_2WR = Radiobutton(self.frame_2WR, text='2W Ω', variable=self.intVar_radioValueSetup, value=4, command=self.radio_setupState_callback)
        self.radio_4WR = Radiobutton(self.frame_4WR, text='4W Ω', variable=self.intVar_radioValueSetup, value=5, command=self.radio_setupState_callback)
        self.radio_diode = Radiobutton(self.frame_diode, image=self.diodeImg, variable=self.intVar_radioValueSetup, value=6, command=self.radio_setupState_callback)
        self.radio_continuity = Radiobutton(self.frame_continuity, image=self.continuityImg, variable=self.intVar_radioValueSetup, value=7, command=self.radio_setupState_callback)
        self.radio_frequency = Radiobutton(self.frame_frequency, text='Frequency', variable=self.intVar_radioValueSetup, value=8, command=self.radio_setupState_callback)
        self.radio_period = Radiobutton(self.frame_period, text='Period     ', variable=self.intVar_radioValueSetup, value=9, command=self.radio_setupState_callback)

        self.radio_caliberACmA = Radiobutton(self.frame_ACI_caliber, text='mA', variable=self.intVar_radioValueCaliberA, value=0, command=self.radio_caliber_callback)
        self.radio_caliberDCmA = Radiobutton(self.frame_DCI_caliber, text='mA', variable=self.intVar_radioValueCaliberA, value=0, command=self.radio_caliber_callback)
        self.radio_caliberAC10A = Radiobutton(self.frame_ACI_caliber, text='10A', variable=self.intVar_radioValueCaliberA, value=1, command=self.radio_caliber_callback)
        self.radio_caliberDC10A = Radiobutton(self.frame_DCI_caliber, text='10A', variable=self.intVar_radioValueCaliberA, value=1, command=self.radio_caliber_callback)

        self.radio_caliberDiode5V = Radiobutton(self.frame_diode_caliber, text='5V', variable=self.intVar_radioValueCaliberDiodeV, value=0, command=self.radio_caliberDiode_callback)
        self.radio_caliberDiode10V= Radiobutton(self.frame_diode_caliber, text='10V', variable=self.intVar_radioValueCaliberDiodeV, value=1, command=self.radio_caliberDiode_callback)
        self.radio_caliberDiode1mA = Radiobutton(self.frame_diode_caliber, text='1mA', variable=self.intVar_radioValueCaliberDiodeA, value=0, command=self.radio_caliberDiode_callback)
        self.radio_caliberDiode01mA = Radiobutton(self.frame_diode_caliber, text='0.1mA', variable=self.intVar_radioValueCaliberDiodeA, value=1, command=self.radio_caliberDiode_callback)

        self.measure_activate = Button(self.frame_measure_button, text='Measure ON/OFF', command=self.measure_activate_callback)
        self.radio_masterStateOFF = Radiobutton(self.frame_measure_radio, text='OFF', variable=self.intVar_radioValuemeasure, value=0)
        self.radio_masterStateON = Radiobutton(self.frame_measure_radio, text='ON', variable=self.intVar_radioValuemeasure, value=1)

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

                if self.model.devices_dict[item][0] == "8845A":   
                    self.img = Image.open(self.model.devices_dict[item][2])
                    self.img = self.img.resize((200, 100), Image.ANTIALIAS)
                    self.img = ImageTk.PhotoImage(self.img)
                    self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
                    self.panel.pack(fill = "both", expand = "yes")

                found=1
                break

        if (found==1) and (self.model.devices_dict[item][1] != "Multimeter"):
            self.view.menu5_callback(self)
            self.view.sendError('005')

        if (found == 0) and (self.controller.instrument.address != ""):                
            sys.stdout("\nUnknown device connected")

        if (found == 0) and (self.controller.instrument.address == ""):  
            self.img = Image.open("Images/8845A.png")
            self.img = self.img.resize((200, 100), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)
            self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
            self.panel.pack(fill = "both", expand = "yes")

        self.renameInstrument()
                       
        if self.controller.instrument.address != "":
            self.controller.connectToDevice()
  
    def renameInstrument(self):
        for item in self.view.listViews:
            if self.controller.instrument.name == item.controller.instrument.name:  
                if (self != item):
                    index = int(item.controller.instrument.name[-2]) + 1
                    newName = self.controller.instrument.name[:-2] + str(index) + ")"
                    self.entry_instrumentName_callback(newName=newName)
             
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=5, fill="y")

        self.labelFrame_setup.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_setup.pack(padx=5, pady=5, fill="y")

    def initFrameLine(self):
    #This method instanciates all the frames used as lines
        self.canva_setup.create_window(0, 0, anchor='nw', window=self.scrollframe_setup)
        self.scrollframe_setup.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.canva_setup.config(yscrollcommand= self.defilY_setup.set, height=260, width=220)
        self.canva_setup.pack(side="left", fill="both")
        self.defilY_setup.pack(fill="y", side='left', padx='5')   

        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_address.pack(fill="both", pady=3)

        self.frame_source_temperature.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_temperature.pack(fill="both", pady=5)

        self.frame_DCV.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_DCV.pack(fill="both", pady=5)

        self.frame_ACV.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_ACV.pack(fill="both", pady=5)
        
        self.frame_DCI.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_DCI.pack(fill="both", pady=5)
        
        self.frame_DCI_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_DCI_caliber.pack(fill="both", pady=5)
        
        self.frame_ACI.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_ACI.pack(fill="both", pady=5)
        
        self.frame_ACI_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_ACI_caliber.pack(fill="both", pady=5)
        
        self.frame_2WR.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_2WR.pack(fill="both", pady=5)
        
        self.frame_4WR.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_4WR.pack(fill="both", pady=5)
        
        self.frame_diode.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_diode.pack(fill="both", pady=5)
        
        self.frame_diode_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_diode_caliber.pack(fill="both", pady=5)
        
        self.frame_continuity.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_continuity.pack(fill="both", pady=5)
        
        self.frame_frequency.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_frequency.pack(fill="both", pady=5)
        
        self.frame_period.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_period.pack(fill="both", pady=5)
        

        self.frame_source_button.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_button.pack(side="left", fill="both", pady=5)

        self.frame_source_radio.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_source_radio.pack(side="right", fill="both", pady=5)

        self.frame_measure.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_measure.pack(padx=5, pady=5, fill="y")

        self.frame_measure_button.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_measure_button.pack(side="left", padx=5, pady=5, fill="y")

        self.frame_measure_radio.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frame_measure_radio.pack(side="right", padx=5, pady=5, fill="y")
    
    def initVar(self):
    #This methods instanciates all the Var
        self.stringvar_instrumentName.set(self.controller.instrument.name)    
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        
        self.doubleVar_DCV.set(0)
        self.doubleVar_ACV.set(0)
        self.doubleVar_DCI.set(0)
        self.doubleVar_ACI.set(0)
        self.doubleVar_2WR.set(0)
        self.doubleVar_4WR.set(0)
        self.doubleVar_frequency.set(0)
        self.doubleVar_period.set(0)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentName.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentaddress.pack(side="left")

        self.label_DCI_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_DCI_caliber.pack(side="right", anchor='ne')

        self.label_ACI_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_ACI_caliber.pack(side="right", anchor='ne')

        self.label_diode_unit.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_diode_unit.pack(side="right")

        self.label_frequency_unit.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_frequency_unit.pack(side="right")

        self.label_period_unit.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_period_unit.pack(side="right")

    def initCombo(self):
    #This methods instanciates all the combobox
        #self.combo_temperatureSource.bind("<<ComboboxSelected>>", self.combo_temperatureSource_callback)
        self.combo_DCV.configure(background='white')
        self.combo_DCV.current(0)
        self.combo_DCV.pack(side="right")
        
        self.combo_ACV.configure(background='white')
        self.combo_ACV.current(0)
        self.combo_ACV.pack(side="right")
        
        self.combo_DCI.configure(background='white')
        self.combo_DCI.current(0)
        self.combo_DCI.pack(side="right")
        
        self.combo_ACI.configure(background='white')
        self.combo_ACI.current(0)
        self.combo_ACI.pack(side="right")
        
        self.combo_2WR.configure(background='white')
        self.combo_2WR.current(0)
        self.combo_2WR.pack(side="right")
        
        self.combo_4WR.configure(background='white')
        self.combo_4WR.current(0)
        self.combo_4WR.pack(side="right")

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_instrumentaddress.bind('<Double-Button-1>', lambda event, name=self : self.view.menu2_Connections_callBack(event, name))
        self.entry_instrumentaddress.pack(side='right', padx=5)

        self.entry_DCV.pack(side='right', padx=5)

        self.entry_ACV.pack(side='right', padx=5)
        
        self.entry_DCI.pack(side='right', padx=5)
        
        self.entry_ACI.pack(side='right', padx=5)
        
        self.entry_2WR.pack(side='right', padx=5)
        
        self.entry_4WR.pack(side='right', padx=5)
        
        self.entry_diode.pack(side='right', padx=5)
        
        self.entry_frequency.pack(side='right', padx=5)
        
        self.entry_period.pack(side='right', padx=5)
        #self.entry_temperatureSource.bind("<Return>", self.entry_temperatureSource_callback)

    def initButton(self):
    #This method instanciates the buttons
        self.radio_DCV.pack(side="left", expand="yes", fill="both")
        self.radio_DCV.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_ACV.pack(side="left", expand="yes", fill="both")
        self.radio_ACV.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_DCI.pack(side="left", expand="yes", fill="both")
        self.radio_DCI.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_ACI.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_ACI.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_2WR.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_2WR.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_4WR.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_4WR.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_diode.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_diode.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_continuity.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_continuity.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_frequency.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_frequency.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_period.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_period.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_caliberACmA.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberACmA.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_caliberDCmA.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberDCmA.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_caliberAC10A.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberAC10A.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_caliberDC10A.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberDC10A.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_caliberDiode5V.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberDiode5V.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_caliberDiode10V.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberDiode10V.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_caliberDiode01mA.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberDiode01mA.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.radio_caliberDiode1mA.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberDiode1mA.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.measure_activate.pack(expand="yes")

        self.radio_masterStateON.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateON.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")
        self.radio_masterStateOFF.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateOFF.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")

        self.intVar_radioValueSetup.set(0)
        self.intVar_radioValuemeasure.set(0)

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
        self.view.menu5.entryconfig(indexMenu, label=name)

    def entry_instrumentaddress_callback(self, arg=None):
    #This method is called when double click on the address
        self.controller.closeConnection()
        self.stringvar_instrumentaddress.set("")
        self.view.menu2_Connections_callBack()

    def radio_setupState_callback(self, args=None):
    #This methods activates or desactivates the modulation function
        for child in self.frame_DCV.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_ACV.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_DCI.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_DCI_caliber.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_ACI.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_ACI_caliber.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_2WR.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_4WR.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_diode.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_diode_caliber.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_continuity.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_frequency.winfo_children():
            child.configure(state="disabled")
        for child in self.frame_period.winfo_children():
            child.configure(state="disabled")
                
        self.radio_DCV.configure(fg="grey24")
        self.radio_ACV.configure(fg="grey24")
        self.radio_DCI.configure(fg="grey24")
        self.radio_ACI.configure(fg="grey24")
        self.radio_2WR.configure(fg="grey24")
        self.radio_4WR.configure(fg="grey24")
        self.radio_diode.configure(fg="grey24", image=self.diodeImg_grey)
        self.radio_continuity.configure(fg="grey24", image=self.continuityImg_grey)
        self.radio_frequency.configure(fg="grey24")
        self.radio_period.configure(fg="grey24")

        if self.intVar_radioValueSetup.get() == 0 :            
            for child in self.frame_DCV.winfo_children():
                child.configure(state="normal")
            self.radio_DCV.configure(fg="black")
            #if self.stringvar_instrumentaddress.get() != "":
                #self.controller.setDCV()

        if self.intVar_radioValueSetup.get() == 1:          
            for child in self.frame_ACV.winfo_children():
                child.configure(state="normal")
            self.radio_ACV.configure(fg="black")
            if self.stringvar_instrumentaddress.get() != "":
                self.controller.setACV()

        if self.intVar_radioValueSetup.get() == 2:      
            for child in self.frame_DCI.winfo_children():
                child.configure(state="normal")   
            for child in self.frame_DCI_caliber.winfo_children():
                child.configure(state="normal")
            self.radio_DCI.configure(fg="black")
            if self.stringvar_instrumentaddress.get() != "":
                if self.intVar_radioValueCaliberA.get() == 0:
                    self.controller.setDCI(self.generateArguments(args9="mA"))
                else:
                    self.controller.setDCI(self.generateArguments(args9="10A"))

        if self.intVar_radioValueSetup.get() == 3:      
            for child in self.frame_ACI.winfo_children():
                child.configure(state="normal")    
            for child in self.frame_ACI_caliber.winfo_children():
                child.configure(state="normal")
            self.radio_ACI.configure(fg="black")
            if self.stringvar_instrumentaddress.get() != "":
                if self.intVar_radioValueCaliberA.get() == 0:
                    self.controller.setACI(self.generateArguments(args9="mA"))
                else:
                    self.controller.setACI(self.generateArguments(args9="10A"))


        if self.intVar_radioValueSetup.get() == 4 :     
            for child in self.frame_2WR.winfo_children():
                child.configure(state="normal")
            self.radio_2WR.configure(fg="black")
            if self.stringvar_instrumentaddress.get() != "":
                self.controller.set2WR()

        if self.intVar_radioValueSetup.get() == 5:     
            for child in self.frame_4WR.winfo_children():
                child.configure(state="normal")
            self.radio_4WR.configure(fg="black")
            if self.stringvar_instrumentaddress.get() != "":
                self.controller.set4WR()

        if self.intVar_radioValueSetup.get() == 6:     
            for child in self.frame_diode.winfo_children():
                child.configure(state="normal")   
            for child in self.frame_diode_caliber.winfo_children():
                child.configure(state="normal")
            self.radio_diode.configure(fg="black", image=self.diodeImg)
            if self.stringvar_instrumentaddress.get() != "":
                current=self.intVar_radioValueCaliberDiodeA.get()
                voltage=self.intVar_radioValueCaliberDiodeV.get()
        
                if current == 0:
                    current="1mA"
                else:
                    current="0.1mA"

                if voltage == 0:
                    voltage="5V"
                else:
                    voltage="10V"

                self.controller.setDiode(self.generateArguments(args11=current, args10=voltage))

        if self.intVar_radioValueSetup.get() == 7:     
            for child in self.frame_continuity.winfo_children():
                child.configure(state="normal")
            self.radio_continuity.configure(fg="black", image=self.continuityImg)
            if self.stringvar_instrumentaddress.get() != "":
                self.controller.setContinuity()

        if self.intVar_radioValueSetup.get() == 8:     
            for child in self.frame_frequency.winfo_children():
                child.configure(state="normal")
            self.radio_frequency.configure(fg="black")
            if self.stringvar_instrumentaddress.get() != "":
                self.controller.setFrequency()

        if self.intVar_radioValueSetup.get() == 9:     
            for child in self.frame_period.winfo_children():
                child.configure(state="normal")
            self.radio_period.configure(fg="black")
            if self.stringvar_instrumentaddress.get() != "":
                self.controller.setPeriod()

        self.radio_DCV.configure(state='normal')
        self.radio_ACV.configure(state='normal')
        self.radio_DCI.configure(state='normal')
        self.radio_ACI.configure(state='normal')
        self.radio_2WR.configure(state='normal')
        self.radio_4WR.configure(state='normal')
        self.radio_diode.configure(state='normal')
        self.radio_continuity.configure(state='normal')
        self.radio_frequency.configure(state='normal')
        self.radio_period.configure(state='normal')

        self.radio_masterStateOFF.select() 
        self.controller.instrument.masterState = 0

    def radio_caliber_callback(self):
    #This method is called when the amp caliber is changed 
        if self.intVar_radioValueCaliberA.get() == 0:
            self.combo_DCI.configure(value=["1mA", "100uA", "400mA", "100mA", "10mA"])
            self.combo_DCI.current(0)
            self.combo_ACI.configure(value=["10mA", "400mA", "100mA"])
            self.combo_ACI.current(0)

        else:
            self.combo_DCI.configure(value=["1A", "3A", "10A"])
            self.combo_DCI.current(0)
            self.combo_ACI.configure(value=["1A", "3A", "10A"])
            self.combo_ACI.current(0)        

        if self.intVar_radioValueSetup.get() == 2:  
            if self.stringvar_instrumentaddress.get() != "":                
                if self.intVar_radioValueCaliberA.get() == 0:
                    self.controller.setDCI(self.generateArguments(args9="mA"))
                else:
                    self.controller.setDCI(self.generateArguments(args9="10A"))

        if self.intVar_radioValueSetup.get() == 3:   
            if self.stringvar_instrumentaddress.get() != "":
                if self.intVar_radioValueCaliberA.get() == 0:
                    self.controller.setDCI(self.generateArguments(args9="mA"))
                else:
                    self.controller.setDCI(self.generateArguments(args9="10A"))

    def radio_caliberDiode_callback(self):
    #This method is called when clicking on caliber for diodes
        current=self.intVar_radioValueCaliberDiodeA.get()
        voltage=self.intVar_radioValueCaliberDiodeV.get()

        if current == 0:
            current="1mA"
        else:
            current="0.1mA"

        if voltage == 0:
            voltage="5V"
        else:
            voltage="10V"

        self.controller.setDiode(self.generateArguments(args11=current, args10=voltage))

    def measure_activate_callback(self):
    #This method call the controller to change output state                  
        if (self.intVar_radioValuemeasure.get() == 0) and (self.controller.instrument.address != ""):
            self.radio_masterStateON.select() 
            self.controller.instrument.masterState = 1

            if self.intVar_radioValueSetup.get() == 0 :         
                self.controller.setDCV()                    
                thread = Thread(target=self.controller.measureDCV) 
                thread.start()

            if self.intVar_radioValueSetup.get() == 1: 
                self.controller.setACV()                  
                thread = Thread(target=self.controller.measureACV) 
                thread.start()

            if self.intVar_radioValueSetup.get() == 2:      
                self.controller.setDCI(caliber=self.intVar_radioValueCaliberA.get())                  
                thread = Thread(target=self.controller.measureDCI) 
                thread.start()

            if self.intVar_radioValueSetup.get() == 3:    
                self.controller.setACI(caliber=self.intVar_radioValueCaliberA.get())                  
                thread = Thread(target=self.controller.measureACI) 
                thread.start()

            if self.intVar_radioValueSetup.get() == 4 :  
                self.controller.set2WR()

            if self.intVar_radioValueSetup.get() == 5:     
                self.controller.set4WR()

            if self.intVar_radioValueSetup.get() == 6: 
                self.controller.setDiode(current=self.intVar_radioValueCaliberDiodeA.get(), voltage=self.intVar_radioValueCaliberDiodeV.get())

            if self.intVar_radioValueSetup.get() == 7:
                self.controller.setContinuity()

            if self.intVar_radioValueSetup.get() == 8:  
                self.controller.setFrequency()

            if self.intVar_radioValueSetup.get() == 9: 
                self.controller.setPeriod()
            
        else:
            self.radio_masterStateOFF.select() 
            self.controller.instrument.masterState = 0

        self.updateMonitoring()

    def updateMonitoring(self):
    #This method  updates the measurement content
        if self.intVar_radioValuemeasure.get() == 1: 
            self.doubleVar_DCV.set(self.controller.instrument.measure_DCV)
            self.doubleVar_ACV.set(self.controller.instrument.measure_ACV)
            self.doubleVar_DCI.set(self.controller.instrument.measure_DCI)
            self.doubleVar_ACI.set(self.controller.instrument.measure_ACI)

            self.label_instrumentName.after(500, self.updateMonitoring)

