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
        self.radio_setupState_callback()
  
    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage     
        self.state="freeze"   

        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)

        self.labelFrame_source = LabelFrame(self.frame, text="Source")
        self.labelFrame_measure = LabelFrame(self.frame, text="Measure")

        self.frame_source1 = Frame(self.labelFrame_source)
        self.frame_source_voltage = Frame(self.frame_source1)
        self.frame_source_currentCompliance = Frame(self.frame_source1)
        self.frame_source2 = Frame(self.labelFrame_source)
        self.frame_source_current = Frame(self.frame_source2)
        self.frame_source_voltageCompliance = Frame(self.frame_source2)
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
        self.label_measure_voltage = Label(self.frame_measure_voltage, text="Voltage :")
        self.label_measure_current = Label(self.frame_measure_current, text="Current :")
        self.label_measure_resistance = Label(self.frame_measure_resistance, text="Resistance :")

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName, width=25)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentaddress, width=25, state="readonly")

        self.entry_source_voltage = Entry(self.frame_source_voltage, textvariable=self.doubleVar_source_voltage, state="readonly", width=10)
        self.entry_source_currentCompliance = Entry(self.frame_source_currentCompliance, textvariable=self.doubleVar_source_currentCompliance, state="readonly", width=10)
        self.entry_source_current = Entry(self.frame_source_current, textvariable=self.doubleVar_source_current, state="readonly", width=10)
        self.entry_source_voltageCompliance = Entry(self.frame_source_voltageCompliance, textvariable=self.doubleVar_source_voltageCompliance, state="readonly", width=10)
        self.entry_measure_voltage = Entry(self.frame_measure_voltage, textvariable=self.doubleVar_measure_voltage, state="readonly", width=10)
        self.entry_measure_current = Entry(self.frame_measure_current, textvariable=self.doubleVar_measure_current, state="readonly", width=10)
        self.entry_measure_resistance = Entry(self.frame_measure_resistance, textvariable=self.doubleVar_measure_resistance, state="readonly", width=10)

        self.combo_source_voltage = Combobox(self.frame_source_voltage, state="readonly", width=8, values=["V", "mV"])
        self.combo_source_currentCompliance = Combobox(self.frame_source_currentCompliance, state="readonly", width=8, values=["A", "mA"])
        self.combo_source_current = Combobox(self.frame_source_current, state="readonly", width=8, values=["A", "mA"])
        self.combo_source_voltageCompliance = Combobox(self.frame_source_voltageCompliance, state="readonly", width=8, values=["V", "mV"])
        self.combo_measure_voltage = Combobox(self.frame_measure_voltage, state="readonly", width=8, values=["V", "mV"])
        self.combo_measure_current = Combobox(self.frame_measure_current, state="readonly", width=8, values=["A", "mA"])        
        self.combo_measure_resistance = Combobox(self.frame_measure_resistance, state="readonly", width=8, values=["kΩ", "Ω", "MΩ"])

        self.img = None
        self.panel = Label(self.frame, bg=self.model.parameters_dict['backgroundColor'])
        
        self.radio_source1 = Radiobutton(self.frame_source1, variable=self.intVar_radio_source, value=0, command=self.radio_setupSource_callback)
        self.radio_source2 = Radiobutton(self.frame_source2, variable=self.intVar_radio_source, value=1, command=self.radio_setupSource_callback)

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
                    self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColor'])
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

        self.labelFrame_source.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_source.pack(padx=5, pady=5, fill="y")

        self.labelFrame_measure.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_measure.pack(padx=5, pady=5, fill="y")

    def initFrameLine(self):
    #This method instanciates all the frames used as lines
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_instrument_address.pack(fill="both", pady=3)

        self.frame_source_voltage.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_voltage.pack(fill="both", pady=5)

        self.frame_source_currentCompliance.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_currentCompliance.pack(fill="both", pady=5)

        self.frame_source_current.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_current.pack(fill="both", pady=5)

        self.frame_source_voltageCompliance.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_voltageCompliance.pack(fill="both", pady=5)        

        self.frame_measure_voltage.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_measure_voltage.pack(padx=5, pady=5, fill="y")

        self.frame_measure_current.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_measure_current.pack(side="left", padx=5, pady=5, fill="y")

        self.frame_measure_resistance.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_measure_resistance.pack(side="right", padx=5, pady=5, fill="y")
    
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
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentName.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentaddress.pack(side="left")

        self.label_source_voltage.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_voltage.pack(side="right", anchor='ne')

        self.label_source_currentCompliance.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_currentCompliance.pack(side="right", anchor='ne')

        self.label_source_current.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_current.pack(side="right")

        self.label_source_voltageCompliance.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_voltageCompliance.pack(side="right")

        self.label_measure_voltage.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_measure_voltage.pack(side="right")

        self.label_measure_current.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_measure_current.pack(side="right")

        self.label_measure_resistance.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_measure_resistance.pack(side="right")


    def initCombo(self):
    #This methods instanciates all the combobox
        #self.combo_source_voltage.bind("<<ComboboxSelected>>", self.combo_temperatureSource_callback)
        self.combo_source_voltage.configure(background='white')
        self.combo_source_voltage.current(0)
        self.combo_source_voltage.pack(side="right")
        
        self.combo_source_currentCompliance.configure(background='white')
        self.combo_source_currentCompliance.current(0)
        self.combo_source_currentCompliance.pack(side="right")
        
        self.combo_source_current.configure(background='white')
        self.combo_source_current.current(0)
        self.combo_source_current.pack(side="right")
        
        self.combo_source_voltageCompliance.configure(background='white')
        self.combo_source_voltageCompliance.current(0)
        self.combo_source_voltageCompliance.pack(side="right")
        
        self.combo_measure_voltage.configure(background='white')
        self.combo_measure_voltage.current(0)
        self.combo_measure_voltage.pack(side="right")
        
        self.combo_measure_current.configure(background='white')
        self.combo_measure_current.current(0)
        self.combo_measure_current.pack(side="right")
        
        self.combo_measure_resistance.configure(background='white')
        self.combo_measure_resistance.current(0)
        self.combo_measure_resistance.pack(side="right")

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_instrumentaddress.bind('<Double-Button-1>', self.entry_instrumentaddress_callback)
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
        self.radio_DCV.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_ACV.pack(side="left", expand="yes", fill="both")
        self.radio_ACV.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_DCI.pack(side="left", expand="yes", fill="both")
        self.radio_DCI.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_ACI.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_ACI.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_2WR.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_2WR.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_4WR.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_4WR.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_diode.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_diode.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_continuity.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_continuity.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_frequency.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_frequency.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_period.pack(side="left", expand="yes", fill="y", anchor='w')
        self.radio_period.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_caliberACmA.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberACmA.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_caliberDCmA.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberDCmA.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_caliberAC10A.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberAC10A.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_caliberDC10A.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberDC10A.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_caliberDiode5V.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberDiode5V.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_caliberDiode10V.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberDiode10V.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_caliberDiode01mA.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberDiode01mA.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.radio_caliberDiode1mA.pack(side="right", fill="both", anchor='ne')
        self.radio_caliberDiode1mA.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.measure_activate.pack(expand="yes")

        self.radio_masterStateON.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateON.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled", disabledforeground="black")
        self.radio_masterStateOFF.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateOFF.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled", disabledforeground="black")

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
        self.view.menu5.entryconfigure(indexMenu, label=name)

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
            if self.stringvar_instrumentaddress.get() != "":
                self.controller.setDCV()

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
                self.controller.setDCI(caliber=self.intVar_radioValueCaliberA.get())

        if self.intVar_radioValueSetup.get() == 3:      
            for child in self.frame_ACI.winfo_children():
                child.configure(state="normal")    
            for child in self.frame_ACI_caliber.winfo_children():
                child.configure(state="normal")
            self.radio_ACI.configure(fg="black")
            if self.stringvar_instrumentaddress.get() != "":
                self.controller.setACI(caliber=self.intVar_radioValueCaliberA.get())

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
                self.controller.setDiode(current=self.intVar_radioValueCaliberDiodeA.get(), voltage=self.intVar_radioValueCaliberDiodeV.get())

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
                self.controller.setDCI(caliber=self.intVar_radioValueCaliberA.get())

        if self.intVar_radioValueSetup.get() == 3:   
            if self.stringvar_instrumentaddress.get() != "":
                self.controller.setACI(caliber=self.intVar_radioValueCaliberA.get())

    def radio_caliberDiode_callback(self):
    #This method is called when clicking on caliber for diodes
        self.controller.setDiode(current=self.intVar_radioValueCaliberDiodeA.get(), voltage=self.intVar_radioValueCaliberDiodeV.get())

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
