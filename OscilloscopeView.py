"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the Oscilloscope instrument's View.

"""

from tkinter.constants import END
from OscilloscopeController import OscilloscopeController
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

class OscilloscopeView (DeviceFrame):
    """Class containing the PowerSupply's View

    """

    def __init__(self, view, frame, terminal, model, controller, name):
    #Constructor for the PowerSupply's View

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
        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument) 

        self.frameline_channel = Frame(self.frame)
        self.frameline_configuration = Frame(self.frame)

        self.labelFrame_channel1 = LabelFrame(self.frameline_channel)
        self.canva_channel1 = Canvas(self.labelFrame_channel1, scrollregion=(0,0,0,190), bd=0, highlightthickness=0, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.defilY_channel1 = Scrollbar(self.labelFrame_channel1, orient='vertical', command=self.canva_channel1.yview, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.scrollframe_channel1 = Frame(self.canva_channel1)

        self.labelFrame_channel2 = LabelFrame(self.frameline_channel)
        self.canva_channel2 = Canvas(self.labelFrame_channel2, scrollregion=(0,0,0,190), bd=0, highlightthickness=0, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.defilY_channel2 = Scrollbar(self.labelFrame_channel2, orient='vertical', command=self.canva_channel2.yview, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.scrollframe_channel2 = Frame(self.canva_channel2)

        self.labelFrame_channel3 = LabelFrame(self.frameline_channel)
        self.canva_channel3 = Canvas(self.labelFrame_channel3, scrollregion=(0,0,0,190), bd=0, highlightthickness=0, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.defilY_channel3 = Scrollbar(self.labelFrame_channel3, orient='vertical', command=self.canva_channel3.yview, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.scrollframe_channel3 = Frame(self.canva_channel3)

        self.labelFrame_channel4 = LabelFrame(self.frameline_channel)
        self.canva_channel4 = Canvas(self.labelFrame_channel4, scrollregion=(0,0,0,190), bd=0, highlightthickness=0, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.defilY_channel4 = Scrollbar(self.labelFrame_channel4, orient='vertical', command=self.canva_channel4.yview, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.scrollframe_channel4 = Frame(self.canva_channel4)

        self.labelFrame_horizontal = LabelFrame(self.frameline_configuration, text="Horizontal")
        self.canva_horizontal = Canvas(self.labelFrame_horizontal, scrollregion=(0,0,0,190), bd=0, highlightthickness=0, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.defilY_horizontal = Scrollbar(self.labelFrame_horizontal, orient='vertical', command=self.canva_horizontal.yview, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.scrollframe_horizontal = Frame(self.canva_horizontal)

        self.labelFrame_trigger = LabelFrame(self.frameline_configuration, text="Trigger")
        self.canva_trigger = Canvas(self.labelFrame_trigger, scrollregion=(0,0,0,190), bd=0, highlightthickness=0, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.defilY_trigger = Scrollbar(self.labelFrame_trigger, orient='vertical', command=self.canva_trigger.yview, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.scrollframe_trigger = Frame(self.canva_trigger)

        self.frameline_channel1_caliber = Frame(self.scrollframe_channel1)
        self.frameline_channel1_coupling = Frame(self.scrollframe_channel1)
        self.frameline_channel1_bandwidth = Frame(self.scrollframe_channel1)
        self.frameline_channel1_offset = Frame(self.scrollframe_channel1)
        self.frameline_channel1_probe = Frame(self.scrollframe_channel1)
        self.frameline_channel1_activate = Frame(self.scrollframe_channel1)

        self.frameline_channel2_caliber = Frame(self.scrollframe_channel2)
        self.frameline_channel2_coupling = Frame(self.scrollframe_channel2)
        self.frameline_channel2_bandwidth = Frame(self.scrollframe_channel2)
        self.frameline_channel2_offset = Frame(self.scrollframe_channel2)
        self.frameline_channel2_probe = Frame(self.scrollframe_channel2)
        self.frameline_channel2_activate = Frame(self.scrollframe_channel2)

        self.frameline_channel3_caliber = Frame(self.scrollframe_channel3)
        self.frameline_channel3_coupling = Frame(self.scrollframe_channel3)
        self.frameline_channel3_bandwidth = Frame(self.scrollframe_channel3)
        self.frameline_channel3_offset = Frame(self.scrollframe_channel3)
        self.frameline_channel3_probe = Frame(self.scrollframe_channel3)
        self.frameline_channel3_activate = Frame(self.scrollframe_channel3)

        self.frameline_channel4_caliber = Frame(self.scrollframe_channel4)
        self.frameline_channel4_coupling = Frame(self.scrollframe_channel4)
        self.frameline_channel4_bandwidth = Frame(self.scrollframe_channel4)
        self.frameline_channel4_offset = Frame(self.scrollframe_channel4)
        self.frameline_channel4_probe = Frame(self.scrollframe_channel4)
        self.frameline_channel4_activate = Frame(self.scrollframe_channel4)

        self.frameline_captureWaveform = Frame(self.frame)

        self.frameline_horizontal_caliber = Frame(self.scrollframe_horizontal)
        self.frameline_horizontal_position = Frame(self.scrollframe_horizontal)
        self.frameline_horizontal_size = Frame(self.scrollframe_horizontal)
        self.frameline_horizontal_rate = Frame(self.scrollframe_horizontal)

        self.frameline_trigger_source = Frame(self.scrollframe_trigger)
        self.frameline_trigger_type = Frame(self.scrollframe_trigger)
        self.frameline_trigger_level = Frame(self.scrollframe_trigger)

        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentaddress = StringVar()
        self.doublevar_channel1_caliber = DoubleVar()
        self.doublevar_channel1_offset = DoubleVar()
        self.doublevar_channel2_caliber = DoubleVar()
        self.doublevar_channel2_offset = DoubleVar()
        self.doublevar_channel3_caliber = DoubleVar()
        self.doublevar_channel3_offset = DoubleVar()
        self.doublevar_channel4_caliber = DoubleVar()
        self.doublevar_channel4_offset = DoubleVar()
        self.doublevar_horizontal_caliber = DoubleVar()
        self.doublevar_horizontal_position = DoubleVar()
        self.doublevar_horizontal_size = DoubleVar()
        self.doublevar_trigger_level = DoubleVar()
        self.intVar_radioValue_channel1 = IntVar()
        self.intVar_radioValue_channel2 = IntVar()
        self.intVar_radioValue_channel3 = IntVar()
        self.intVar_radioValue_channel4 = IntVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :")
        self.label_instrumentaddress = Label(self.frame_instrument_address, text="Address :")

        self.label_channel1_caliber = Label(self.frameline_channel1_caliber, text="Caliber :     ")
        self.label_channel1_coupling = Label(self.frameline_channel1_coupling, text="Coupling :     ")
        self.label_channel1_bandwidth = Label(self.frameline_channel1_bandwidth, text="Bandwidth :  ")
        self.label_channel1_offset = Label(self.frameline_channel1_offset, text="Offset :      ")
        self.label_channel1_probe = Label(self.frameline_channel1_probe, text="Probe :          ")

        self.label_channel2_caliber = Label(self.frameline_channel2_caliber, text="Caliber :     ")
        self.label_channel2_coupling = Label(self.frameline_channel2_coupling, text="Coupling :     ")
        self.label_channel2_bandwidth = Label(self.frameline_channel2_bandwidth, text="Bandwidth :  ")
        self.label_channel2_offset = Label(self.frameline_channel2_offset, text="Offset :      ")
        self.label_channel2_probe = Label(self.frameline_channel2_probe, text="Probe :          ")

        self.label_channel3_caliber = Label(self.frameline_channel3_caliber, text="Caliber :     ")
        self.label_channel3_coupling = Label(self.frameline_channel3_coupling, text="Coupling :     ")
        self.label_channel3_bandwidth = Label(self.frameline_channel3_bandwidth, text="Bandwidth :  ")
        self.label_channel3_offset = Label(self.frameline_channel3_offset, text="Offset :      ")
        self.label_channel3_probe = Label(self.frameline_channel3_probe, text="Probe :          ")

        self.label_channel4_caliber = Label(self.frameline_channel4_caliber, text="Caliber :     ")
        self.label_channel4_coupling = Label(self.frameline_channel4_coupling, text="Coupling :     ")
        self.label_channel4_bandwidth = Label(self.frameline_channel4_bandwidth, text="Bandwidth :  ")
        self.label_channel4_offset = Label(self.frameline_channel4_offset, text="Offset :      ")
        self.label_channel4_probe = Label(self.frameline_channel4_probe, text="Probe :          ")

        self.label_trigger_type = Label(self.frameline_trigger_type, text="Type   :   ")
        self.label_trigger_source = Label(self.frameline_trigger_source, text="Source : ")
        self.label_trigger_level = Label(self.frameline_trigger_level, text="Level :     ")

        self.label_horizontal_caliber = Label(self.frameline_horizontal_caliber, text="Caliber :       ")
        self.label_horizontal_position = Label(self.frameline_horizontal_position, text="Position  :    ")
        self.label_horizontal_size = Label(self.frameline_horizontal_size, text="Sample size : ")
        self.label_horizontal_rate = Label(self.frameline_horizontal_rate, text="Sample rate  : ")

        self.combo_channel1 = Combobox(self.frameline_channel, width=10, values=["Channel 1", "Channel 2", "Channel 3", "Channel 4"], background=self.model.parameters_dict['backgroundColorInstrument'])
        self.combo_channel2 = Combobox(self.frameline_channel, width=10, values=["Channel 1", "Channel 2", "Channel 3", "Channel 4"], background=self.model.parameters_dict['backgroundColorInstrument'])
        self.combo_channel3 = Combobox(self.frameline_channel, width=10, values=["Channel 1", "Channel 2", "Channel 3", "Channel 4"], background=self.model.parameters_dict['backgroundColorInstrument'])
        self.combo_channel4 = Combobox(self.frameline_channel, width=10, values=["Channel 1", "Channel 2", "Channel 3", "Channel 4"], background=self.model.parameters_dict['backgroundColorInstrument'])

        self.combo_channel1_coupling = Combobox(self.frameline_channel1_coupling, width=15, values=["DC", "AC", "GROUND"], background=self.model.parameters_dict['backgroundColorInstrument'])
        self.combo_channel1_bandwidth = Combobox(self.frameline_channel1_bandwidth, width=15, values=["FULL", "200MHZ", "20MHZ"], background=self.model.parameters_dict['backgroundColorInstrument'])
        self.combo_channel1_probe = Combobox(self.frameline_channel1_probe, width=15, values=["1:1", "10:1", "100:1"], background=self.model.parameters_dict['backgroundColorInstrument'])

        self.combo_channel2_coupling = Combobox(self.frameline_channel2_coupling, width=15, values=["DC", "AC", "GROUND"], background=self.model.parameters_dict['backgroundColorInstrument'])
        self.combo_channel2_bandwidth = Combobox(self.frameline_channel2_bandwidth, width=15, values=["FULL", "200MHZ", "20MHZ"], background=self.model.parameters_dict['backgroundColorInstrument'])
        self.combo_channel2_probe = Combobox(self.frameline_channel2_probe, width=15, values=["1:1", "10:1", "100:1"], background=self.model.parameters_dict['backgroundColorInstrument'])

        self.combo_channel3_coupling = Combobox(self.frameline_channel3_coupling, width=15, values=["DC", "AC", "GROUND"], background=self.model.parameters_dict['backgroundColorInstrument'])
        self.combo_channel3_bandwidth = Combobox(self.frameline_channel3_bandwidth, width=15, values=["FULL", "200MHZ", "20MHZ"], background=self.model.parameters_dict['backgroundColorInstrument'])
        self.combo_channel3_probe = Combobox(self.frameline_channel3_probe, width=15, values=["1:1", "10:1", "100:1"], background=self.model.parameters_dict['backgroundColorInstrument'])

        self.combo_channel4_coupling = Combobox(self.frameline_channel4_coupling, width=15, values=["DC", "AC", "GROUND"], background=self.model.parameters_dict['backgroundColorInstrument'])
        self.combo_channel4_bandwidth = Combobox(self.frameline_channel4_bandwidth, width=15, values=["FULL", "200MHZ", "20MHZ"], background=self.model.parameters_dict['backgroundColorInstrument'])
        self.combo_channel4_probe = Combobox(self.frameline_channel4_probe, width=15, values=["1:1", "10:1", "100:1"], background=self.model.parameters_dict['backgroundColorInstrument'])

        self.combo_horizontal_rate = Combobox(self.frameline_horizontal_rate, width=15, values=["2.5Gsa/s", "125Msa/s"], background=self.model.parameters_dict['backgroundColorInstrument'])

        self.combo_trigger_source = Combobox(self.frameline_trigger_source, width=15, values=["Channel 1", "Channel 2", "Channel 3", "Channel 4", "External"], background=self.model.parameters_dict['backgroundColorInstrument'])
        self.combo_trigger_type = Combobox(self.frameline_trigger_type, width=15, values=["Rising Edge", "Falling Edge", "Both Edge", "Width"], background=self.model.parameters_dict['backgroundColorInstrument'])

        self.entry_instrumentName = Entry(self.frame_instrument_name, textvariable=self.stringvar_instrumentName)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, textvariable=self.stringvar_instrumentaddress, state="readonly")

        self.entry_channel1_caliber = Entry(self.frameline_channel1_caliber, textvariable=self.doublevar_channel1_caliber)
        self.entry_channel1_offset = Entry(self.frameline_channel1_offset, textvariable=self.doublevar_channel1_offset)

        self.entry_channel2_caliber = Entry(self.frameline_channel2_caliber, textvariable=self.doublevar_channel2_caliber)
        self.entry_channel2_offset = Entry(self.frameline_channel2_offset, textvariable=self.doublevar_channel2_offset)

        self.entry_channel3_caliber = Entry(self.frameline_channel3_caliber, textvariable=self.doublevar_channel3_caliber)
        self.entry_channel3_offset = Entry(self.frameline_channel3_offset, textvariable=self.doublevar_channel3_offset)

        self.entry_channel4_caliber = Entry(self.frameline_channel4_caliber, textvariable=self.doublevar_channel4_caliber)
        self.entry_channel4_offset = Entry(self.frameline_channel4_offset, textvariable=self.doublevar_channel4_offset)

        self.entry_trigger_level = Entry(self.frameline_trigger_level, textvariable=self.doublevar_trigger_level)

        self.entry_horizontal_caliber = Entry(self.frameline_horizontal_caliber, textvariable=self.doublevar_horizontal_caliber)
        self.entry_horizontal_position = Entry(self.frameline_horizontal_position, textvariable=self.doublevar_horizontal_position)
        self.entry_horizontal_size = Entry(self.frameline_horizontal_size, textvariable=self.doublevar_horizontal_size)

        self.button_channel1_activate = Button(self.frameline_channel1_activate, text='Channel ON/OFF')
        self.radio_channel1_StateON = Radiobutton(self.frameline_channel1_activate, text='ON', variable=self.intVar_radioValue_channel1, value=0)
        self.radio_channel1_StateOFF = Radiobutton(self.frameline_channel1_activate, text='OFF', variable=self.intVar_radioValue_channel1, value=1)

        self.button_channel2_activate = Button(self.frameline_channel2_activate, text='Channel ON/OFF')
        self.radio_channel2_StateON = Radiobutton(self.frameline_channel2_activate, text='ON', variable=self.intVar_radioValue_channel2, value=0)
        self.radio_channel2_StateOFF = Radiobutton(self.frameline_channel2_activate, text='OFF', variable=self.intVar_radioValue_channel2, value=1)

        self.button_channel3_activate = Button(self.frameline_channel3_activate, text='Channel ON/OFF')
        self.radio_channel3_StateON = Radiobutton(self.frameline_channel3_activate, text='ON', variable=self.intVar_radioValue_channel3, value=0)
        self.radio_channel3_StateOFF = Radiobutton(self.frameline_channel3_activate, text='OFF', variable=self.intVar_radioValue_channel3, value=1)

        self.button_channel4_activate = Button(self.frameline_channel4_activate, text='Channel ON/OFF')
        self.radio_channel4_StateON = Radiobutton(self.frameline_channel4_activate, text='ON', variable=self.intVar_radioValue_channel4, value=0)
        self.radio_channel4_StateOFF = Radiobutton(self.frameline_channel4_activate, text='OFF', variable=self.intVar_radioValue_channel4, value=1)

        self.button_captureWaveform1 = Button(self.frameline_captureWaveform, text='Capture Waveform')
        self.button_captureWaveform2 = Button(self.frameline_captureWaveform, text='Capture Waveform')
        self.button_captureWaveform3 = Button(self.frameline_captureWaveform, text='Capture Waveform')
        self.button_captureWaveform4 = Button(self.frameline_captureWaveform, text='Capture Waveform')
        
        self.img = None
        self.panel = Label(self.frame, bg=self.model.parameters_dict['backgroundColorInstrument'])
        
    def clearInstrument(self):
    #This method is used to clear every trace of this instrument before being deleted
        for i in range(len(self.controller.instrument.channelUsed)):
            if self.controller.instrument.channelUsed[i] == self.controller.instrument:
                self.controller.instrument.channelUsed[i]=""

    def renameInstrument(self):
        i = 0
        for item in self.view.listViews:
            if self.controller.instrument.name == item.controller.instrument.name:    
                newName = self.controller.instrument.name[:-2] + str(i) + ")"
                self.entry_instrumentName_callback(newName=newName)
                i = i+1

    def updateView(self, configuration=False):
    #This method refresh the content of the view
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        self.panel.destroy()
        found=0

        for item in self.model.devices_dict:
            if (item in self.controller.instrument.address):
                if self.model.devices_dict[item][1] == "Oscilloscope":
                    self.controller.instrument.id = item
                    self.controller.instrument.channelNumber = self.model.devices_dict[item][2]
                    self.combo_channel1.configure(values=self.controller.instrument.channelNumber)
                    self.combo_channel2.configure(values=self.controller.instrument.channelNumber)
                    self.combo_channel3.configure(values=self.controller.instrument.channelNumber)
                    self.combo_channel4.configure(values=self.controller.instrument.channelNumber)
                    self.controller.instrument.channelState = self.model.devices_dict[item][3]
                    self.controller.instrument.channelUsed = self.model.devices_dict[item][4]

                    newName = self.model.devices_dict[item][0] + " (0)"
                    self.entry_instrumentName_callback(newName=newName)

                    if self.model.devices_dict[item][0] == "HMO3004":   
                        self.img = Image.open(self.model.devices_dict[item][5])
                        self.img = self.img.resize((270, 140), Image.ANTIALIAS)
                        self.img = ImageTk.PhotoImage(self.img)
                        self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
                        self.panel.pack(fill = "both", expand = "yes")

                    elif self.model.devices_dict[item][0] == "RTM1054":   
                        self.img = Image.open(self.model.devices_dict[item][5])
                        self.img = self.img.resize((270, 135), Image.ANTIALIAS)
                        self.img = ImageTk.PhotoImage(self.img)
                        self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
                        self.panel.pack(fill = "both", expand = "yes")

                    elif self.model.devices_dict[item][0] == "RTM3004":   
                        self.img = Image.open(self.model.devices_dict[item][5])
                        self.img = self.img.resize((290, 150), Image.ANTIALIAS)
                        self.img = ImageTk.PhotoImage(self.img)
                        self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
                        self.panel.pack(fill = "both", expand = "yes")

                    elif self.model.devices_dict[item][0] == "MSO2014":   
                        self.img = Image.open(self.model.devices_dict[item][5])
                        self.img = self.img.resize((300, 150), Image.ANTIALIAS)
                        self.img = ImageTk.PhotoImage(self.img)
                        self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
                        self.panel.pack(fill = "both", expand = "yes")

                    elif self.model.devices_dict[item][0] == "DL9040":   
                        self.img = Image.open(self.model.devices_dict[item][5])
                        self.img = self.img.resize((270, 150), Image.ANTIALIAS)
                        self.img = ImageTk.PhotoImage(self.img)
                        self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColorInstrument'])
                        self.panel.pack(fill = "both", expand = "yes")

                    break

                found=1

        if (found==1) and (self.model.devices_dict[item][1] != "Oscilloscope"):
            self.view.menu5_callback(self)
            self.view.sendError('005')

        self.renameInstrument()

        if (found == 0) and (self.controller.instrument.address != ""):                
            self.term_text.insert(END, "\nUnknown device connected")
            used = 0
            for item in self.view.getInstrList():
                if (item.name != self.controller.instrument.name) and (item.address == self.controller.instrument.address):
                    self.controller.instrument.channelState = item.channelState
                    self.controller.instrument.channelUsed = item.channelUsed
                    used = used + 1

            if used == 0:           
                self.controller.instrument.channelState = [0, 0]
                self.controller.instrument.channelUsed = ["", ""]

        if configuration == True:
            None #add open configuration here
            
        if self.controller.instrument.address != "":
            self.controller.connectToDevice()
            #self.combo_instrumentChannel_callback()
        
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.pack(padx=5, pady=2, fill="y")

        self.labelFrame_channel1.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_channel1.configure(labelwidget=self.combo_channel1)
        self.labelFrame_channel1.pack(padx=5, pady=2, fill="y", side='left')

        self.labelFrame_channel2.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_channel2.configure(labelwidget=self.combo_channel2)
        self.labelFrame_channel2.pack(padx=5, pady=2, fill="y", side='left')

        self.labelFrame_channel3.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_channel3.configure(labelwidget=self.combo_channel3)
        self.labelFrame_channel3.pack(padx=5, pady=2, fill="y", side='left')

        self.labelFrame_channel4.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_channel4.configure(labelwidget=self.combo_channel4)
        self.labelFrame_channel4.pack(padx=5, pady=2, fill="y", side='left')

        self.labelFrame_horizontal.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_horizontal.pack(padx=5, pady=2, fill="y", side='left', expand='yes')

        self.labelFrame_trigger.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_trigger.pack(padx=5, pady=2, fill="y", side='left', expand='yes')

    def initFrameLine(self):
    #This method instanciates all the frameline
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.frame_instrument_address.pack(fill="both", pady=3)
        
        self.canva_channel1.create_window(0, 0, anchor='nw', window=self.scrollframe_channel1)
        self.scrollframe_channel1.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.canva_channel1.config(yscrollcommand= self.defilY_channel1.set, height=125, width=200)
        self.canva_channel1.pack(side="left", fill="both")
        self.defilY_channel1.pack(fill="y", side='left', padx='5')   
        
        self.canva_channel2.create_window(0, 0, anchor='nw', window=self.scrollframe_channel2)
        self.scrollframe_channel2.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.canva_channel2.config(yscrollcommand= self.defilY_channel2.set, height=125, width=200)
        self.canva_channel2.pack(side="left", fill="both")
        self.defilY_channel2.pack(fill="y", side='left', padx='5')   
        
        self.canva_channel3.create_window(0, 0, anchor='nw', window=self.scrollframe_channel3)
        self.scrollframe_channel3.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.canva_channel3.config(yscrollcommand= self.defilY_channel3.set, height=125, width=200)
        self.canva_channel3.pack(side="left", fill="both")
        self.defilY_channel3.pack(fill="y", side='left', padx='5')  
        
        self.canva_channel4.create_window(0, 0, anchor='nw', window=self.scrollframe_channel4)
        self.scrollframe_channel4.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.canva_channel4.config(yscrollcommand= self.defilY_channel4.set, height=125, width=200)
        self.canva_channel4.pack(side="left", fill="both")
        self.defilY_channel4.pack(fill="y", side='left', padx='5')  
        
        self.canva_horizontal.create_window(0, 0, anchor='nw', window=self.scrollframe_horizontal)
        self.scrollframe_horizontal.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.canva_horizontal.config(yscrollcommand= self.defilY_horizontal.set, height=95, width=200)
        self.canva_horizontal.pack(side="left", fill="both")
        self.defilY_horizontal.pack(fill="y", side='left', padx='5')     
        
        self.canva_trigger.create_window(0, 0, anchor='nw', window=self.scrollframe_trigger)
        self.scrollframe_trigger.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.canva_trigger.config(yscrollcommand= self.defilY_trigger.set, height=95, width=200)
        self.canva_trigger.pack(side="left", fill="both")
        self.defilY_trigger.pack(fill="y", side='left', padx='5')  

        self.frameline_channel.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel.pack(fill="both", pady=5)  

        self.frameline_captureWaveform.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_captureWaveform.pack(fill="both", pady=5)   

        self.frameline_configuration.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_configuration.pack(fill="both", pady=5)        

        self.frameline_channel1_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel1_caliber.pack(fill="both", pady=5)
        self.frameline_channel1_coupling.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel1_coupling.pack(fill="both", pady=5)
        self.frameline_channel1_bandwidth.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel1_bandwidth.pack(fill="both", pady=5)
        self.frameline_channel1_offset.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel1_offset.pack(fill="both", pady=5)
        self.frameline_channel1_probe.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel1_probe.pack(fill="both", pady=5)
        self.frameline_channel1_activate.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel1_activate.pack(fill="both", pady=5)

        self.frameline_channel2_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel2_caliber.pack(fill="both", pady=5)
        self.frameline_channel2_coupling.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel2_coupling.pack(fill="both", pady=5)
        self.frameline_channel2_bandwidth.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel2_bandwidth.pack(fill="both", pady=5)
        self.frameline_channel2_offset.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel2_offset.pack(fill="both", pady=5)
        self.frameline_channel2_probe.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel2_probe.pack(fill="both", pady=5)
        self.frameline_channel2_activate.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel2_activate.pack(fill="both", pady=5)

        self.frameline_channel3_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel3_caliber.pack(fill="both", pady=5)
        self.frameline_channel3_coupling.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel3_coupling.pack(fill="both", pady=5)
        self.frameline_channel3_bandwidth.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel3_bandwidth.pack(fill="both", pady=5)
        self.frameline_channel3_offset.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel3_offset.pack(fill="both", pady=5)
        self.frameline_channel3_probe.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel3_probe.pack(fill="both", pady=5)
        self.frameline_channel3_activate.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel3_activate.pack(fill="both", pady=5)

        self.frameline_channel4_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel4_caliber.pack(fill="both", pady=5)
        self.frameline_channel4_coupling.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel4_coupling.pack(fill="both", pady=5)
        self.frameline_channel4_bandwidth.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel4_bandwidth.pack(fill="both", pady=5)
        self.frameline_channel4_offset.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel4_offset.pack(fill="both", pady=5)
        self.frameline_channel4_probe.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel4_probe.pack(fill="both", pady=5)
        self.frameline_channel4_activate.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_channel4_activate.pack(fill="both", pady=5)

        self.frameline_horizontal_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_horizontal_caliber.pack(fill="both", pady=5)
        self.frameline_horizontal_position.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_horizontal_position.pack(fill="both", pady=5)
        self.frameline_horizontal_size.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_horizontal_size.pack(fill="both", pady=5)
        self.frameline_horizontal_rate.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_horizontal_rate.pack(fill="both", pady=5)
        
        self.frameline_trigger_source.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_trigger_source.pack(fill="both", pady=5)
        self.frameline_trigger_type.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_trigger_type.pack(fill="both", pady=5)
        self.frameline_trigger_level.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.frameline_trigger_level.pack(fill="both", pady=5)
    
    def initVar(self):
    #This methods instanciates all the Var
        self.stringvar_instrumentName.set(self.controller.instrument.name)    
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentName.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColorInstrumentData'])
        self.label_instrumentaddress.pack(side="left")

        self.label_channel1_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel1_caliber.pack(side="left")
        self.label_channel1_coupling.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel1_coupling.pack(side="left")
        self.label_channel1_bandwidth.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel1_bandwidth.pack(side="left")
        self.label_channel1_offset.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel1_offset.pack(side="left")
        self.label_channel1_probe.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel1_probe.pack(side="left")

        self.label_channel2_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel2_caliber.pack(side="left")
        self.label_channel2_coupling.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel2_coupling.pack(side="left")
        self.label_channel2_bandwidth.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel2_bandwidth.pack(side="left")
        self.label_channel2_offset.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel2_offset.pack(side="left")
        self.label_channel2_probe.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel2_probe.pack(side="left")

        self.label_channel3_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel3_caliber.pack(side="left")
        self.label_channel3_coupling.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel3_coupling.pack(side="left")
        self.label_channel3_bandwidth.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel3_bandwidth.pack(side="left")
        self.label_channel3_offset.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel3_offset.pack(side="left")
        self.label_channel3_probe.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel3_probe.pack(side="left")

        self.label_channel4_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel4_caliber.pack(side="left")
        self.label_channel4_coupling.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel4_coupling.pack(side="left")
        self.label_channel4_bandwidth.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel4_bandwidth.pack(side="left")
        self.label_channel4_offset.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel4_offset.pack(side="left")
        self.label_channel4_probe.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_channel4_probe.pack(side="left")

        self.label_horizontal_caliber.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_horizontal_caliber.pack(side="left")
        self.label_horizontal_position.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_horizontal_position.pack(side="left")
        self.label_horizontal_size.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_horizontal_size.pack(side="left")
        self.label_horizontal_rate.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_horizontal_rate.pack(side="left")

        self.label_trigger_source.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_trigger_source.pack(side="left")
        self.label_trigger_type.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_trigger_type.pack(side="left")
        self.label_trigger_level.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.label_trigger_level.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox
        self.combo_channel1.current(0)
        self.combo_channel2.current(1)
        self.combo_channel3.current(2)
        self.combo_channel4.current(3)

        self.combo_channel1_coupling.pack(side='left', padx=5)
        self.combo_channel1_coupling.current(0)
        self.combo_channel1_bandwidth.pack(side='left', padx=5)
        self.combo_channel1_bandwidth.current(0)
        self.combo_channel1_probe.pack(side='left', padx=5)
        self.combo_channel1_probe.current(0)

        self.combo_channel2_coupling.pack(side='left', padx=5)
        self.combo_channel2_coupling.current(0)
        self.combo_channel2_bandwidth.pack(side='left', padx=5)
        self.combo_channel2_bandwidth.current(0)
        self.combo_channel2_probe.pack(side='left', padx=5)
        self.combo_channel2_probe.current(0)

        self.combo_channel3_coupling.pack(side='left', padx=5)
        self.combo_channel3_coupling.current(0)
        self.combo_channel3_bandwidth.pack(side='left', padx=5)
        self.combo_channel3_bandwidth.current(0)
        self.combo_channel3_probe.pack(side='left', padx=5)
        self.combo_channel3_probe.current(0)

        self.combo_channel4_coupling.pack(side='left', padx=5)
        self.combo_channel4_coupling.current(0)
        self.combo_channel4_bandwidth.pack(side='left', padx=5)
        self.combo_channel4_bandwidth.current(0)
        self.combo_channel4_probe.pack(side='left', padx=5)
        self.combo_channel4_probe.current(0)
        
        self.combo_horizontal_rate.pack(side='left', padx=5)
        self.combo_horizontal_rate.current(0)
        
        self.combo_trigger_source.pack(side='left', padx=5)
        self.combo_trigger_source.current(0)
        self.combo_trigger_type.pack(side='left', padx=5)
        self.combo_trigger_type.current(0)

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='right', padx=5)

        self.entry_instrumentaddress.bind('<Double-Button-1>', self.view.menu2_Connections_callBack)
        self.entry_instrumentaddress.pack(side='right', padx=5)

        self.entry_channel1_caliber.pack(side='left', padx=5)
        self.entry_channel1_offset.pack(side='left', padx=5)

        self.entry_channel2_caliber.pack(side='left', padx=5)
        self.entry_channel2_offset.pack(side='left', padx=5)

        self.entry_channel3_caliber.pack(side='left', padx=5)
        self.entry_channel3_offset.pack(side='left', padx=5)

        self.entry_channel4_caliber.pack(side='left', padx=5)
        self.entry_channel4_offset.pack(side='left', padx=5)

        self.entry_horizontal_caliber.pack(side='left', padx=5)
        self.entry_horizontal_position.pack(side='left', padx=5)
        self.entry_horizontal_size.pack(side='left', padx=5)

        self.entry_trigger_level.pack(side='left', padx=5)

    def initButton(self):
    #This method instanciates the buttons
        self.button_channel1_activate.pack(side="left", expand="yes")

        self.radio_channel1_StateON.pack(side="left", expand="yes", fill="both")
        self.radio_channel1_StateON.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")
        self.radio_channel1_StateOFF.pack(side="left", expand="yes", fill="both")
        self.radio_channel1_StateOFF.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")

        self.intVar_radioValue_channel1.set(0)

        self.button_channel2_activate.pack(side="left", expand="yes")

        self.radio_channel2_StateON.pack(side="left", expand="yes", fill="both")
        self.radio_channel2_StateON.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")
        self.radio_channel2_StateOFF.pack(side="left", expand="yes", fill="both")
        self.radio_channel2_StateOFF.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")

        self.intVar_radioValue_channel2.set(0)

        self.button_channel3_activate.pack(side="left", expand="yes")

        self.radio_channel3_StateON.pack(side="left", expand="yes", fill="both")
        self.radio_channel3_StateON.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")
        self.radio_channel3_StateOFF.pack(side="left", expand="yes", fill="both")
        self.radio_channel3_StateOFF.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")

        self.intVar_radioValue_channel3.set(0)

        self.button_channel4_activate.pack(side="left", expand="yes")

        self.radio_channel4_StateON.pack(side="left", expand="yes", fill="both")
        self.radio_channel4_StateON.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")
        self.radio_channel4_StateOFF.pack(side="left", expand="yes", fill="both")
        self.radio_channel4_StateOFF.configure(bg=self.model.parameters_dict['backgroundColorInstrument'], state="disabled", disabledforeground="black")

        self.intVar_radioValue_channel4.set(0)

        self.button_captureWaveform1.pack(side="left", expand="yes")
        self.button_captureWaveform2.pack(side="left", expand="yes")
        self.button_captureWaveform3.pack(side="left", expand="yes")
        self.button_captureWaveform4.pack(side="left", expand="yes")

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
