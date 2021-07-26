"""Copyleft Oticon Medical NICE

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
        self.initVar()
        self.initLabel()
        self.initCombo()
        self.initEntries()

    def initAttributes(self):
    #This methods initiates all attributes in the class. It is usefull to prevent double usage     
        self.state="freeze"   
        self.labelFrame_instrument = LabelFrame(self.frame, text="Instrument")
        self.labelFrame_signal = LabelFrame(self.frame, text="Signal")
        self.labelFrame_function = LabelFrame(self.frame, text="Functions")
        self.labelFrame_output = LabelFrame(self.frame, text="Output")

        self.canva_signal = Canvas(self.labelFrame_signal, scrollregion=(0,0,0,405), bd=0, highlightthickness=0, bg=self.model.parameters_dict['backgroundColor'])
        self.defilY_signal = Scrollbar(self.labelFrame_signal, orient='vertical', command=self.canva_signal.yview, bg=self.model.parameters_dict['backgroundColor'])
        
        self.canva_function = Canvas(self.labelFrame_function, scrollregion=(0,0,0,355), bd=0, highlightthickness=0, bg=self.model.parameters_dict['backgroundColor'])
        self.defilY_function = Scrollbar(self.labelFrame_function, orient='vertical', command=self.canva_function.yview, bg=self.model.parameters_dict['backgroundColor'])
        
        self.frame_instrument_name = Frame(self.labelFrame_instrument)
        self.frame_instrument_address = Frame(self.labelFrame_instrument)

        self.scrollframe_signal = Frame(self.canva_signal)
        self.scrollframe_function = Frame(self.canva_function)

        self.frame_signal_waveform = Frame(self.scrollframe_signal)
        self.frame_signal_frequency = Frame(self.scrollframe_signal)
        self.frame_signal_amplitude = Frame(self.scrollframe_signal)
        self.frame_signal_offset = Frame(self.scrollframe_signal)
        self.frame_signal_phase = Frame(self.scrollframe_signal)
        self.frame_signal_dutyCycle = Frame(self.scrollframe_signal)
        self.frame_signal_pulseWidth = Frame(self.scrollframe_signal)
        self.frame_signal_riseTime = Frame(self.scrollframe_signal)
        self.frame_signal_fallTime = Frame(self.scrollframe_signal)
        self.frame_signal_symetry = Frame(self.scrollframe_signal)
        self.frame_signal_bandwidth = Frame(self.scrollframe_signal)
        self.frame_signal_modulate = Frame(self.scrollframe_signal)
        self.frame_signal_sweep = Frame(self.scrollframe_signal)

        self.frame_function_modulation = Frame(self.scrollframe_function)
        self.frame_modulate_type = Frame(self.scrollframe_function)
        self.frame_modulate_source = Frame(self.scrollframe_function)
        self.frame_modulate_shape = Frame(self.scrollframe_function)
        self.frame_function_sweep = Frame(self.scrollframe_function)
        self.frame_sweep_type = Frame(self.scrollframe_function)
        self.frame_sweep_time = Frame(self.scrollframe_function)
        self.frame_sweep_startFrequency = Frame(self.scrollframe_function)
        self.frame_sweep_stopFrequency = Frame(self.scrollframe_function)
        self.frame_sweep_holdTime = Frame(self.scrollframe_function)
        self.frame_sweep_returnTime = Frame(self.scrollframe_function)
        
        self.frame_output_state = Frame(self.labelFrame_output)
        self.frame_master_button = Frame(self.labelFrame_output)
        self.frame_master_radio = Frame(self.labelFrame_output)


        self.stringvar_instrumentName = StringVar()    
        self.stringvar_instrumentaddress = StringVar()
        self.doubleVar_signal_frequency = DoubleVar()
        self.doubleVar_signal_amplitude = DoubleVar()
        self.doubleVar_signal_offset = DoubleVar()
        self.doubleVar_signal_phase = DoubleVar()
        self.doubleVar_signal_dutyCycle = DoubleVar()
        self.doubleVar_signal_pulseWidth = DoubleVar()
        self.doubleVar_signal_riseTime = DoubleVar()
        self.doubleVar_signal_fallTime = DoubleVar()
        self.doubleVar_signal_symetry = DoubleVar()
        self.doubleVar_signal_bandwidth = DoubleVar()
        self.doubleVar_sweep_time = DoubleVar()
        self.doubleVar_sweep_startFrequency = DoubleVar()
        self.doubleVar_sweep_stopFrequency = DoubleVar()
        self.doubleVar_sweep_holdTime = DoubleVar()
        self.doubleVar_sweep_returnTime = DoubleVar()
        self.intVar_radioValueModulate = IntVar()
        self.intVar_radioValueSweep = IntVar()
        self.intVar_radioValueState = IntVar()
        self.intVar_radioValueMaster = IntVar()

        self.label_instrumentName = Label(self.frame_instrument_name, text="Name :   ")
        self.label_instrumentaddress = Label(self.frame_instrument_address, text="Address :")

        self.label_signal_waveform = Label(self.frame_signal_waveform, text="Waveform :")
        self.label_signal_frequency = Label(self.frame_signal_frequency, text="Frequency :")
        self.label_signal_amplitude = Label(self.frame_signal_amplitude, text="Amplitude :")
        self.label_signal_offset = Label(self.frame_signal_offset, text="Offset :")
        self.label_signal_phase = Label(self.frame_signal_phase, text="Phase :")
        self.label_signal_dutyCycle = Label(self.frame_signal_dutyCycle, text="Duty Cycle :")
        self.label_signal_symetry = Label(self.frame_signal_symetry, text="Symetry :")
        self.label_signal_pulseWidth = Label(self.frame_signal_pulseWidth, text="Pulse Width :")
        self.label_signal_riseTime = Label(self.frame_signal_riseTime, text="Rise Time :")
        self.label_signal_fallTime = Label(self.frame_signal_fallTime, text="Fall Time :")
        self.label_signal_bandwidth = Label(self.frame_signal_bandwidth, text="Bandwidth :")
        self.label_signal_modulate = Label(self.frame_signal_modulate, text="Modulation : ")
        self.label_signal_sweep = Label(self.frame_signal_sweep, text="Sweep :      ")

        self.label_function_modulation = Label(self.frame_function_modulation, text="Modulation")
        self.label_modulate_type = Label(self.frame_modulate_type, text="Type :     ")
        self.label_modulate_source = Label(self.frame_modulate_source, text="Source : ")
        self.label_modulate_shape = Label(self.frame_modulate_shape, text="Shape :    ")
        self.label_function_sweep = Label(self.frame_function_sweep, text="\nSweep")
        self.label_sweep_type = Label(self.frame_sweep_type, text="Sweep Type :     ")
        self.label_sweep_time = Label(self.frame_sweep_time, text="Sweep Time :     ")
        self.label_sweep_startFrequency = Label(self.frame_sweep_startFrequency, text="Start Frequency : ")
        self.label_sweep_stopFrequency = Label(self.frame_sweep_stopFrequency, text="Stop Frequency : ")
        self.label_sweep_holdTime = Label(self.frame_sweep_holdTime, text="Hold Time :      ")
        self.label_sweep_returnTime = Label(self.frame_sweep_returnTime, text="Return Time :     ")
        
        self.label_output_state = Label(self.frame_output_state, text="Load :    ")

        self.combo_signal_waveform = Combobox(self.frame_signal_waveform, state="readonly", width=17, values=["Sinus", "Square", "Ramp", "Pulse", "Noise", "Arbitrary"])
        self.combo_signal_frequency = Combobox(self.frame_signal_frequency, state="readonly", width=5, values=["HZ", "KHZ", "MHZ"])
        self.combo_signal_amplitude = Combobox(self.frame_signal_amplitude, state="readonly", width=5, values=["VPP", "VRMS", "DBM"])
        self.combo_signal_offset = Combobox(self.frame_signal_offset, state="readonly", width=5, values=["V", "mV"])
        self.combo_signal_phase = Combobox(self.frame_signal_phase, state="readonly", width=5, values=["deg"])
        self.combo_signal_dutyCycle = Combobox(self.frame_signal_dutyCycle, state="readonly", width=5, values=["%"])
        self.combo_signal_symetry = Combobox(self.frame_signal_symetry, state="readonly", width=5, values=["%"])
        self.combo_signal_pulseWidth = Combobox(self.frame_signal_pulseWidth, state="readonly", width=5, values=["ms", "us", "s", "ns"])
        self.combo_signal_riseTime = Combobox(self.frame_signal_riseTime, state="readonly", width=5, values=["ns", "us"])
        self.combo_signal_fallTime = Combobox(self.frame_signal_fallTime, state="readonly", width=5, values=["ns", "us"])
        self.combo_signal_bandwidth = Combobox(self.frame_signal_bandwidth, state="readonly", width=5, values=["Hz", "kHz", "MHz"])
        
        self.combo_modulate_type = Combobox(self.frame_modulate_type, state="readonly", width=20, values=["AM", "FM", "PM", "FSK", "BPSK"])
        self.combo_modulate_source = Combobox(self.frame_modulate_source, state="readonly", width=20, values=["Internal", "External"])
        self.combo_modulate_shape = Combobox(self.frame_modulate_shape, state="readonly", width=20, values=["Sinus", "Square", "UpRamp", "DownRamp", "Triangle", "Noise"])
        self.combo_sweep_type = Combobox(self.frame_sweep_type, state="readonly", width=16, values=["Linear", "Logarithmic"])
        self.combo_sweep_time = Combobox(self.frame_sweep_time, state="readonly", width=5, values=["s", "ms", "us", "ns"])
        self.combo_sweep_startFrequency = Combobox(self.frame_sweep_startFrequency, state="readonly", width=5, values=["Hz", "kHz", "MHz"])
        self.combo_sweep_stopFrequency = Combobox(self.frame_sweep_stopFrequency, state="readonly", width=5, values=["Hz", "kHz", "MHz"])
        self.combo_sweep_holdTime = Combobox(self.frame_sweep_holdTime, state="readonly", width=5, values=["s", "ms", "us", "ns"])
        self.combo_sweep_returnTime = Combobox(self.frame_sweep_returnTime, state="readonly", width=5, values=["s", "ms", "us", "ns"])

        self.entry_instrumentName = Entry(self.frame_instrument_name, width=30, textvariable=self.stringvar_instrumentName)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, width=30, textvariable=self.stringvar_instrumentaddress, state="readonly")

        self.entry_signal_frequency = Entry(self.frame_signal_frequency, textvariable=self.doubleVar_signal_frequency, width=10)
        self.entry_signal_amplitude = Entry(self.frame_signal_amplitude, textvariable=self.doubleVar_signal_amplitude, width=10)
        self.entry_signal_offset = Entry(self.frame_signal_offset, textvariable=self.doubleVar_signal_offset, width=10)
        self.entry_signal_phase = Entry(self.frame_signal_phase, textvariable=self.doubleVar_signal_phase, width=10)
        self.entry_signal_dutyCycle = Entry(self.frame_signal_dutyCycle, textvariable=self.doubleVar_signal_dutyCycle, width=10)
        self.entry_signal_Symetry = Entry(self.frame_signal_symetry, textvariable=self.doubleVar_signal_symetry, width=10)
        self.entry_signal_pulseWidth = Entry(self.frame_signal_pulseWidth, textvariable=self.doubleVar_signal_pulseWidth, width=10)
        self.entry_signal_riseTime = Entry(self.frame_signal_riseTime, textvariable=self.doubleVar_signal_riseTime, width=10)
        self.entry_signal_fallTime = Entry(self.frame_signal_fallTime, textvariable=self.doubleVar_signal_fallTime, width=10)
        self.entry_signal_bandwidth = Entry(self.frame_signal_bandwidth, textvariable=self.doubleVar_signal_bandwidth, width=10)

        self.entry_sweep_time = Entry(self.frame_sweep_time, textvariable=self.doubleVar_sweep_time, width=10, state="disabled")
        self.entry_sweep_startFrequency = Entry(self.frame_sweep_startFrequency, textvariable=self.doubleVar_sweep_startFrequency, width=10, state="disabled")
        self.entry_sweep_stopFrequency = Entry(self.frame_sweep_stopFrequency, textvariable=self.doubleVar_sweep_stopFrequency, width=10, state="disabled")
        self.entry_sweep_holdTime = Entry(self.frame_sweep_holdTime, textvariable=self.doubleVar_sweep_holdTime, width=10, state="disabled")
        self.entry_sweep_returnTime = Entry(self.frame_sweep_returnTime, textvariable=self.doubleVar_sweep_returnTime, width=10, state="disabled")

        self.master_activate = Button(self.frame_master_button, text='Master ON/OFF', command=self.master_activate_callback)

        self.radio_modulateStateOFF = Radiobutton(self.frame_signal_modulate, text='OFF', variable=self.intVar_radioValueModulate, value=0, command=self.radio_modulateState_callback)
        self.radio_modulateStateON = Radiobutton(self.frame_signal_modulate, text='ON', variable=self.intVar_radioValueModulate, value=1, command=self.radio_modulateState_callback)

        self.radio_sweepStateOFF = Radiobutton(self.frame_signal_sweep, text='OFF', variable=self.intVar_radioValueSweep, value=0, command=self.radio_sweepState_callback)
        self.radio_sweepStateON = Radiobutton(self.frame_signal_sweep, text='ON', variable=self.intVar_radioValueSweep, value=1, command=self.radio_sweepState_callback)

        self.radio_outputStateLoad = Radiobutton(self.frame_output_state, text='50Ω', variable=self.intVar_radioValueState, value=0, command=self.radio_outputState_callback)
        self.radio_outputStateHigh = Radiobutton(self.frame_output_state, text='High Z', variable=self.intVar_radioValueState, value=1, command=self.radio_outputState_callback)

        self.radio_masterStateOFF = Radiobutton(self.frame_master_radio, text='OFF', variable=self.intVar_radioValueMaster, value=0)
        self.radio_masterStateON = Radiobutton(self.frame_master_radio, text='ON', variable=self.intVar_radioValueMaster, value=1)
        
        self.img = None
        self.panel = Label(self.frame, bg=self.model.parameters_dict['backgroundColor'])
        
    def clearInstrument(self):
    #This method is used to clear every trace of this instrument before being deleted
        None

    def renameInstrument(self):
        i = 0
        for i in range(len(self.view.listViews)):
            if self.controller.instrument.name == self.view.listViews[i].controller.instrument.name:    
                newName = self.controller.instrument.name[:-2] + str(i) + ")"
                self.entry_instrumentName_callback(newName=newName)

    def updateView(self, configuration=False):
    #This method refresh the content of the view
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)
        self.state="freeze" 
        found=0

        self.panel.destroy()

        for item in self.model.devices_dict:
            if (item in self.controller.instrument.address) and (self.model.devices_dict[item][1] == "Waveform Generator"):
                self.controller.instrument.id = item

                newName = self.model.devices_dict[item][0] + " (0)"
                self.entry_instrumentName_callback(newName=newName)

                if self.model.devices_dict[item][0] == "33500B":   
                    self.img = Image.open(self.model.devices_dict[item][2])
                    self.img = self.img.resize((200, 120), Image.ANTIALIAS)
                    self.img = ImageTk.PhotoImage(self.img)
                    self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColor'])
                    self.panel.pack(fill = "both", expand = "yes")

                if self.model.devices_dict[item][0] == "33600A":   
                    self.img = Image.open(self.model.devices_dict[item][2])
                    self.img = self.img.resize((200, 120), Image.ANTIALIAS)
                    self.img = ImageTk.PhotoImage(self.img)
                    self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColor'])
                    self.panel.pack(fill = "both", expand = "yes")

                if self.model.devices_dict[item][0] == "33210A":   
                    self.img = Image.open(self.model.devices_dict[item][2])
                    self.img = self.img.resize((200, 120), Image.ANTIALIAS)
                    self.img = ImageTk.PhotoImage(self.img)
                    self.panel = Label(self.frame, image = self.img, bg=self.model.parameters_dict['backgroundColor'])
                    self.panel.pack(fill = "both", expand = "yes")


                found=1
                break

        if (found==1) and (self.model.devices_dict[item][1] != "Waveform Generator"):
            self.view.menu5_callback(self)
            self.view.sendError('005')

        self.renameInstrument()

        if (found == 0) and (self.controller.instrument.address != ""):                
            self.term_text.insert(END, "\nUnknown device connected")

        if configuration == True:
            self.openConfiguration()
            
        if self.controller.instrument.address != "":
            self.controller.connectToDevice()
        
    def initLabelFrame(self):
    #This method instanciates all the LabelFrame
        self.labelFrame_instrument.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_instrument.pack(padx=5, pady=3)

        self.labelFrame_signal.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_signal.pack(padx=5, pady=3)
        
        self.labelFrame_function.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_function.pack(padx=5, pady=3)

        self.labelFrame_output.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.labelFrame_output.pack(padx=5, pady=3)

    def initFrameLine(self):
    #This method instanciates all the frame lines
        self.frame_instrument_name.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_instrument_name.pack(fill="both", pady=3)

        self.frame_instrument_address.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_instrument_address.pack(fill="both", pady=3)

        self.canva_signal.create_window(0, 0, anchor='nw', window=self.scrollframe_signal)
        self.scrollframe_signal.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.canva_signal.config(yscrollcommand= self.defilY_signal.set, height=125, width=220)
        self.canva_signal.pack(side="left", fill="both")
        self.defilY_signal.pack(fill="y", side='left', padx='5')        

        self.canva_function.create_window(0, 0, anchor='nw', window=self.scrollframe_function)
        self.scrollframe_function.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.canva_function.config(yscrollcommand= self.defilY_function.set, height=95, width=220)
        self.canva_function.pack(side="left", fill="both")
        self.defilY_function.pack(fill="y", side='left', padx='5')

        self.frame_signal_waveform.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_signal_waveform.pack(fill="x", pady=5)

        self.frame_signal_frequency.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_signal_frequency.pack(fill="x", pady=5)

        self.frame_signal_amplitude.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_signal_amplitude.pack(fill="x", pady=5)

        self.frame_signal_offset.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_signal_offset.pack(fill="x", pady=5)

        self.frame_signal_phase.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_signal_phase.pack(fill="x", pady=5)

        self.frame_signal_dutyCycle.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_signal_dutyCycle.pack(fill="x",pady=5)

        self.frame_signal_pulseWidth.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_signal_pulseWidth.pack(fill="x",pady=5)

        self.frame_signal_riseTime.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_signal_riseTime.pack(fill="x",pady=5)

        self.frame_signal_fallTime.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_signal_fallTime.pack(fill="x",pady=5)

        self.frame_signal_symetry.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_signal_symetry.pack(fill="x",pady=5)

        self.frame_signal_bandwidth.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_signal_bandwidth.pack(fill="x",pady=5)

        self.frame_signal_modulate.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_signal_modulate.pack(fill="x",pady=5)

        self.frame_signal_sweep.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_signal_sweep.pack(fill="x",pady=5)

        self.frame_function_modulation.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_function_modulation.pack(fill="both",pady=5)

        self.frame_modulate_type.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_modulate_type.pack(fill="both",pady=5)

        self.frame_modulate_source.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_modulate_source.pack(fill="both",pady=5)

        self.frame_modulate_shape.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_modulate_shape.pack(fill="both",pady=5)

        self.frame_function_sweep.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_function_sweep.pack(fill="both",pady=5)

        self.frame_sweep_type.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_sweep_type.pack(fill="both",pady=5)

        self.frame_sweep_time.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_sweep_time.pack(fill="both",pady=5)

        self.frame_sweep_startFrequency.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_sweep_startFrequency.pack(fill="both",pady=5)

        self.frame_sweep_stopFrequency.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_sweep_stopFrequency.pack(fill="both",pady=5)

        self.frame_sweep_holdTime.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_sweep_holdTime.pack(fill="both",pady=5)

        self.frame_sweep_returnTime.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_sweep_returnTime.pack(fill="both",pady=5)

        self.frame_output_state.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_output_state.pack(fill="both",pady=5)

        self.frame_master_button.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_master_button.pack(side="left", padx=5, pady=5, fill="y")

        self.frame_master_radio.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_master_radio.pack(side="left", padx=5, pady=5, fill="y")
    
    def initVar(self):
    #This methods instanciates all the Var
        self.stringvar_instrumentName.set(self.controller.instrument.name)    
        self.stringvar_instrumentaddress.set(self.controller.instrument.address)

        self.doubleVar_signal_frequency.set(1000)
        self.doubleVar_signal_amplitude.set(1)
        self.doubleVar_signal_offset.set(0)
        self.doubleVar_signal_phase.set(0)
        self.doubleVar_signal_dutyCycle.set(50)
        self.doubleVar_signal_symetry.set(50)
        self.doubleVar_signal_pulseWidth.set(1)
        self.doubleVar_signal_riseTime.set(10)
        self.doubleVar_signal_fallTime.set(10)
        self.doubleVar_signal_bandwidth.set(1000)
        self.doubleVar_sweep_time.set(1)
        self.doubleVar_sweep_startFrequency.set(1)
        self.doubleVar_sweep_stopFrequency.set(1000)
        self.doubleVar_sweep_holdTime.set(10)
        self.doubleVar_sweep_returnTime.set(10)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentName.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentaddress.pack(side="left")

        self.label_signal_waveform.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_signal_waveform.pack(side="left")

        self.label_signal_frequency.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_signal_frequency.pack(side="left")

        self.label_signal_amplitude.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_signal_amplitude.pack(side="left")

        self.label_signal_offset.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_signal_offset.pack(side="left")

        self.label_signal_phase.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_signal_phase.pack(side="left")

        self.label_signal_dutyCycle.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_signal_dutyCycle.pack(side="left")

        self.label_signal_pulseWidth.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_signal_pulseWidth.pack(side="left")

        self.label_signal_riseTime.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_signal_riseTime.pack(side="left")

        self.label_signal_fallTime.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_signal_fallTime.pack(side="left")

        self.label_signal_symetry.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_signal_symetry.pack(side="left")

        self.label_signal_bandwidth.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_signal_bandwidth.pack(side="left")

        self.label_signal_modulate.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_signal_modulate.pack(side="left")

        self.label_signal_sweep.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_signal_sweep.pack(side="left")

        self.label_function_modulation.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled")
        self.label_function_modulation.pack(side="left")

        self.label_modulate_type.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled")
        self.label_modulate_type.pack(side="left")

        self.label_modulate_source.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled")
        self.label_modulate_source.pack(side="left")

        self.label_modulate_shape.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled")
        self.label_modulate_shape.pack(side="left")

        self.label_function_sweep.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled")
        self.label_function_sweep.pack(side="left")

        self.label_sweep_type.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled")
        self.label_sweep_type.pack(side="left")

        self.label_sweep_time.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled")
        self.label_sweep_time.pack(side="left")

        self.label_sweep_startFrequency.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled")
        self.label_sweep_startFrequency.pack(side="left")

        self.label_sweep_stopFrequency.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled")
        self.label_sweep_stopFrequency.pack(side="left")

        self.label_sweep_holdTime.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled")
        self.label_sweep_holdTime.pack(side="left")

        self.label_sweep_returnTime.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled")
        self.label_sweep_returnTime.pack(side="left")

        self.label_output_state.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_output_state.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox
        self.combo_signal_waveform.bind("<<ComboboxSelected>>", self.combo_signal_waveform_callback)
        self.combo_signal_waveform.configure(background='white')
        self.combo_signal_waveform.current(0)
        self.combo_signal_waveform.pack(side="right")
        self.combo_signal_waveform_callback(init=True)

        self.combo_signal_frequency.bind("<<ComboboxSelected>>", self.combo_signal_frequency_callback)
        self.combo_signal_frequency.configure(background='white')
        self.combo_signal_frequency.current(0)
        self.combo_signal_frequency.pack(side="right")
    
        self.combo_signal_amplitude.bind("<<ComboboxSelected>>", self.combo_signal_amplitude_callback)
        self.combo_signal_amplitude.configure(background='white')
        self.combo_signal_amplitude.current(0)
        self.combo_signal_amplitude.pack(side="right")
    
        self.combo_signal_offset.bind("<<ComboboxSelected>>", self.combo_signal_offset_callback)
        self.combo_signal_offset.configure(background='white')
        self.combo_signal_offset.current(0)
        self.combo_signal_offset.pack(side="right")
    
        self.combo_signal_phase.bind("<<ComboboxSelected>>", self.combo_signal_phase_callback)
        self.combo_signal_phase.configure(background='white')
        self.combo_signal_phase.current(0)
        self.combo_signal_phase.pack(side="right")
    
        self.combo_signal_phase.bind("<<ComboboxSelected>>", self.combo_signal_phase_callback)
        self.combo_signal_dutyCycle.configure(background='white')
        self.combo_signal_dutyCycle.current(0)
        self.combo_signal_dutyCycle.pack(side="right")

        self.combo_signal_symetry.bind("<<ComboboxSelected>>", self.combo_signal_symetry_callback)
        self.combo_signal_symetry.configure(background='white')
        self.combo_signal_symetry.current(0)
        self.combo_signal_symetry.pack(side="right")
    
        self.combo_signal_pulseWidth.bind("<<ComboboxSelected>>", self.combo_signal_pulseWidth_callback)
        self.combo_signal_pulseWidth.configure(background='white')
        self.combo_signal_pulseWidth.current(0)
        self.combo_signal_pulseWidth.pack(side="right")
    
        self.combo_signal_riseTime.bind("<<ComboboxSelected>>", self.combo_signal_riseTime_callback)
        self.combo_signal_riseTime.configure(background='white')
        self.combo_signal_riseTime.current(0)
        self.combo_signal_riseTime.pack(side="right")
    
        self.combo_signal_fallTime.bind("<<ComboboxSelected>>", self.combo_signal_fallTime_callback)
        self.combo_signal_fallTime.configure(background='white')
        self.combo_signal_fallTime.current(0)
        self.combo_signal_fallTime.pack(side="right")
    
        self.combo_signal_bandwidth.bind("<<ComboboxSelected>>", self.combo_signal_bandwidth_callback)
        self.combo_signal_bandwidth.configure(background='white')
        self.combo_signal_bandwidth.current(0)
        self.combo_signal_bandwidth.pack(side="right")
    
        self.combo_modulate_type.bind("<<ComboboxSelected>>", self.combo_modulate_type_callback)
        self.combo_modulate_type.configure(background='white', state="disabled")
        self.combo_modulate_type.current(0)
        self.combo_modulate_type.pack(side="right")
    
        self.combo_modulate_source.bind("<<ComboboxSelected>>", self.combo_modulate_source_callback)
        self.combo_modulate_source.configure(background='white', state="disabled")
        self.combo_modulate_source.current(0)
        self.combo_modulate_source.pack(side="right")
    
        self.combo_modulate_shape.bind("<<ComboboxSelected>>", self.combo_modulate_shape_callback)
        self.combo_modulate_shape.configure(background='white', state="disabled")
        self.combo_modulate_shape.current(0)
        self.combo_modulate_shape.pack(side="right")
    
        self.combo_sweep_type.bind("<<ComboboxSelected>>", self.combo_sweep_type_callback)
        self.combo_sweep_type.configure(background='white', state="disabled")
        self.combo_sweep_type.current(0)
        self.combo_sweep_type.pack(side="right")
    
        self.combo_sweep_time.bind("<<ComboboxSelected>>", self.combo_sweep_time_callback)
        self.combo_sweep_time.configure(background='white', state="disabled")
        self.combo_sweep_time.current(0)
        self.combo_sweep_time.pack(side="right")
    
        self.combo_sweep_startFrequency.bind("<<ComboboxSelected>>", self.combo_sweep_startFrequency_callback)
        self.combo_sweep_startFrequency.configure(background='white', state="disabled")
        self.combo_sweep_startFrequency.current(0)
        self.combo_sweep_startFrequency.pack(side="right")
    
        self.combo_sweep_stopFrequency.bind("<<ComboboxSelected>>", self.combo_sweep_stopFrequency_callback)
        self.combo_sweep_stopFrequency.configure(background='white', state="disabled")
        self.combo_sweep_stopFrequency.current(0)
        self.combo_sweep_stopFrequency.pack(side="right")
    
        self.combo_sweep_holdTime.bind("<<ComboboxSelected>>", self.combo_sweep_holdTime_callback)
        self.combo_sweep_holdTime.configure(background='white', state="disabled")
        self.combo_sweep_holdTime.current(0)
        self.combo_sweep_holdTime.pack(side="right")
    
        self.combo_sweep_returnTime.bind("<<ComboboxSelected>>", self.combo_sweep_returnTime_callback)
        self.combo_sweep_returnTime.configure(background='white', state="disabled")
        self.combo_sweep_returnTime.current(0)
        self.combo_sweep_returnTime.pack(side="right")

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='left', padx=5)

        self.entry_instrumentaddress.bind('<Double-Button-1>', self.view.menu2_Connections_callBack)
        self.entry_instrumentaddress.pack(side='left', padx=5)

        self.entry_signal_frequency.bind("<Return>", self.entry_signal_frequency_callback)
        self.entry_signal_frequency.pack(side='right', padx=5)

        self.entry_signal_amplitude.bind("<Return>", self.entry_signal_amplitude_callback)
        self.entry_signal_amplitude.pack(side='right', padx=5)

        self.entry_signal_offset.bind("<Return>", self.entry_signal_offset_callback)
        self.entry_signal_offset.pack(side='right', padx=5)

        self.entry_signal_phase.bind("<Return>", self.entry_signal_phase_callback)
        self.entry_signal_phase.pack(side='right', padx=5)

        self.entry_signal_dutyCycle.bind("<Return>", self.entry_signal_dutyCycle_callback)
        self.entry_signal_dutyCycle.pack(side='right', padx=5)

        self.entry_signal_Symetry.bind("<Return>", self.entry_signal_symetry_callback)
        self.entry_signal_Symetry.pack(side='right', padx=5)

        self.entry_signal_pulseWidth.bind("<Return>", self.entry_signal_pulseWidth_callback)
        self.entry_signal_pulseWidth.pack(side='right', padx=5)

        self.entry_signal_riseTime.bind("<Return>", self.entry_signal_riseTime_callback)
        self.entry_signal_riseTime.pack(side='right', padx=5)

        self.entry_signal_fallTime.bind("<Return>", self.entry_signal_fallTime_callback)
        self.entry_signal_fallTime.pack(side='right', padx=5)

        self.entry_signal_bandwidth.bind("<Return>", self.entry_signal_bandwidth_callback)
        self.entry_signal_bandwidth.pack(side='right', padx=5)

        self.entry_sweep_time.bind("<Return>", self.entry_sweep_time_callback)
        self.entry_sweep_time.pack(side='right', padx=5)

        self.entry_sweep_startFrequency.bind("<Return>", self.entry_sweep_startFrequency_callback)
        self.entry_sweep_startFrequency.pack(side='right', padx=5)

        self.entry_sweep_stopFrequency.bind("<Return>", self.entry_sweep_stopFrequency_callback)
        self.entry_sweep_stopFrequency.pack(side='right', padx=5)

        self.entry_sweep_holdTime.bind("<Return>", self.entry_sweep_holdTime_callback)
        self.entry_sweep_holdTime.pack(side='right', padx=5)

        self.entry_sweep_returnTime.bind("<Return>", self.entry_sweep_returnTime_callback)
        self.entry_sweep_returnTime.pack(side='right', padx=5)

    def initButton(self):
    #This method instanciates the buttons
        self.master_activate.pack(expand="yes")

        self.radio_sweepStateON.pack(side="right", expand="yes", fill="both")
        self.radio_sweepStateON.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.radio_sweepStateOFF.pack(side="right", expand="yes", fill="both")
        self.radio_sweepStateOFF.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.intVar_radioValueSweep.set(0)

        self.radio_modulateStateON.pack(side="right", expand="yes", fill="both")
        self.radio_modulateStateON.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.radio_modulateStateOFF.pack(side="right", expand="yes", fill="both")
        self.radio_modulateStateOFF.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.intVar_radioValueModulate.set(0)

        self.radio_outputStateHigh.pack(side="right", expand="yes", fill="both")
        self.radio_outputStateHigh.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.radio_outputStateLoad.pack(side="right", expand="yes", fill="both")
        self.radio_outputStateLoad.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.intVar_radioValueState.set(0)

        self.radio_masterStateON.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateON.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled", disabledforeground="black")
        self.radio_masterStateOFF.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateOFF.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled", disabledforeground="black")
        self.intVar_radioValueMaster.set(0)

    def openConfiguration(self):
    #This method is called when the device is an opened configuration        
        self.doubleVar_signal_frequency.set(self.controller.instrument.signal_frequency)
        self.doubleVar_signal_amplitude.set(self.controller.instrument.signal_amplitude)
        self.doubleVar_signal_offset.set(self.controller.instrument.signal_offset)
        self.doubleVar_signal_phase.set(self.controller.instrument.signal_phase)
        self.doubleVar_signal_dutyCycle.set(self.controller.instrument.signal_dutyCycle)
        self.doubleVar_signal_pulseWidth.set(self.controller.instrument.signal_pulseWidth)
        self.doubleVar_signal_riseTime.set(self.controller.instrument.signal_riseTime)
        self.doubleVar_signal_fallTime.set(self.controller.instrument.signal_fallTime)
        self.doubleVar_signal_symetry.set(self.controller.instrument.signal_symetry)
        self.doubleVar_signal_bandwidth.set(self.controller.instrument.signal_bandwidth)
        self.doubleVar_sweep_time.set(self.controller.instrument.sweep_time)
        self.doubleVar_sweep_startFrequency.set(self.controller.instrument.sweep_startFrequency)
        self.doubleVar_sweep_stopFrequency.set(self.controller.instrument.sweep_stopFrequency)
        self.doubleVar_sweep_holdTime.set(self.controller.instrument.sweep_holdTime)
        self.doubleVar_sweep_returnTime.set(self.controller.instrument.sweep_returnTime)

        self.intVar_radioValueModulate.set(self.controller.instrument.signal_modulation_state)
        self.intVar_radioValueSweep.set(self.controller.instrument.signal_sweep_state)
        self.intVar_radioValueState.set(self.controller.instrument.output_state)
        if self.intVar_radioValueSweep.get() == 1:
            self.radio_sweepState_callback()
        if self.intVar_radioValueModulate.get() == 1:
            self.radio_modulateState_callback()

        self.combo_signal_waveform.set(self.controller.instrument.signal_waveform)
        self.combo_signal_waveform_callback(init=False)
        self.combo_signal_frequency.set(self.controller.instrument.signal_frequency_caliber)
        self.combo_signal_amplitude.set(self.controller.instrument.signal_amplitude_caliber)
        self.combo_signal_offset.set(self.controller.instrument.signal_offset_caliber)
        self.combo_signal_phase.set(self.controller.instrument.signal_phase_caliber)
        self.combo_signal_dutyCycle.set(self.controller.instrument.signal_dutyCycle_caliber)
        self.combo_signal_symetry.set(self.controller.instrument.signal_symetry_caliber)
        self.combo_signal_pulseWidth.set(self.controller.instrument.signal_pulseWidth_caliber)
        self.combo_signal_riseTime.set(self.controller.instrument.signal_riseTime_caliber)
        self.combo_signal_fallTime.set(self.controller.instrument.signal_fallTime_caliber)
        self.combo_signal_bandwidth.set(self.controller.instrument.signal_bandwidth_caliber)
        self.combo_modulate_type.set(self.controller.instrument.modulation_type)
        #self.combo_modulate_type_callback()
        self.combo_modulate_source.set(self.controller.instrument.modulation_source)
        #self.combo_modulate_source_callback()
        self.combo_modulate_shape.set(self.controller.instrument.modulation_shape)
        #self.combo_modulate_shape_callback()
        self.combo_sweep_type.set(self.controller.instrument.sweep_type)
        self.combo_sweep_time.set(self.controller.instrument.sweep_time_caliber)
        self.combo_sweep_startFrequency.set(self.controller.instrument.sweep_startFrequency_caliber)
        self.combo_sweep_stopFrequency.set(self.controller.instrument.sweep_stopFrequency_caliber)
        self.combo_sweep_holdTime.set(self.controller.instrument.sweep_holdTime_caliber)
        self.combo_sweep_returnTime.set(self.controller.instrument.sweep_returnTime_caliber)

    def combo_signal_waveform_callback(self, args=None, init=False):
    #This method is called when this combobow is selected
        if init == True:
            self.combo_signal_waveform.set(self.controller.instrument.signal_waveform)

        self.controller.instrument.signal_waveform = self.combo_signal_waveform.get()

        if self.combo_signal_waveform.get() == "Sinus":
            self.label_signal_frequency.configure(state="normal")
            self.label_signal_amplitude.configure(state="normal")
            self.label_signal_offset.configure(state="normal")
            self.label_signal_phase.configure(state="normal")
            self.label_signal_dutyCycle.configure(state="disabled")
            self.label_signal_symetry.configure(state="disabled")
            self.label_signal_riseTime.configure(state="disabled")
            self.label_signal_fallTime.configure(state="disabled")
            self.label_signal_pulseWidth.configure(state="disabled")
            self.label_signal_bandwidth.configure(state="disabled")
            
            self.entry_signal_frequency.configure(state="normal")
            self.entry_signal_amplitude.configure(state="normal")
            self.entry_signal_offset.configure(state="normal")
            self.entry_signal_phase.configure(state="normal")
            self.entry_signal_dutyCycle.configure(state="disabled")
            self.entry_signal_Symetry.configure(state="disabled")
            self.entry_signal_riseTime.configure(state="disabled")
            self.entry_signal_fallTime.configure(state="disabled")
            self.entry_signal_pulseWidth.configure(state="disabled")
            self.entry_signal_bandwidth.configure(state="disabled")

            self.combo_signal_frequency.configure(state="normal")
            self.combo_signal_amplitude.configure(state="normal")
            self.combo_signal_offset.configure(state="normal")
            self.combo_signal_phase.configure(state="normal")
            self.combo_signal_dutyCycle.configure(state="disabled")
            self.combo_signal_symetry.configure(state="disabled")
            self.combo_signal_riseTime.configure(state="disabled")
            self.combo_signal_fallTime.configure(state="disabled")
            self.combo_signal_pulseWidth.configure(state="disabled")
            self.combo_signal_bandwidth.configure(state="disabled")

        if self.combo_signal_waveform.get() == "Square":
            self.label_signal_frequency.configure(state="normal")
            self.label_signal_amplitude.configure(state="normal")
            self.label_signal_offset.configure(state="normal")
            self.label_signal_phase.configure(state="normal")
            self.label_signal_dutyCycle.configure(state="normal")
            self.label_signal_symetry.configure(state="disabled")
            self.label_signal_riseTime.configure(state="disabled")
            self.label_signal_fallTime.configure(state="disabled")
            self.label_signal_pulseWidth.configure(state="disabled")
            self.label_signal_bandwidth.configure(state="disabled")
            
            self.entry_signal_frequency.configure(state="normal")
            self.entry_signal_amplitude.configure(state="normal")
            self.entry_signal_offset.configure(state="normal")
            self.entry_signal_phase.configure(state="normal")
            self.entry_signal_dutyCycle.configure(state="normal")
            self.entry_signal_Symetry.configure(state="disabled")
            self.entry_signal_riseTime.configure(state="disabled")
            self.entry_signal_fallTime.configure(state="disabled")
            self.entry_signal_pulseWidth.configure(state="disabled")
            self.entry_signal_bandwidth.configure(state="disabled")

            self.combo_signal_frequency.configure(state="normal")
            self.combo_signal_amplitude.configure(state="normal")
            self.combo_signal_offset.configure(state="normal")
            self.combo_signal_phase.configure(state="normal")
            self.combo_signal_dutyCycle.configure(state="normal")
            self.combo_signal_symetry.configure(state="disabled")
            self.combo_signal_riseTime.configure(state="disabled")
            self.combo_signal_fallTime.configure(state="disabled")
            self.combo_signal_pulseWidth.configure(state="disabled")
            self.combo_signal_bandwidth.configure(state="disabled")

        if self.combo_signal_waveform.get() == "Ramp":
            self.label_signal_frequency.configure(state="normal")
            self.label_signal_amplitude.configure(state="normal")
            self.label_signal_offset.configure(state="normal")
            self.label_signal_phase.configure(state="normal")
            self.label_signal_dutyCycle.configure(state="disabled")
            self.label_signal_symetry.configure(state="normal")
            self.label_signal_riseTime.configure(state="disabled")
            self.label_signal_fallTime.configure(state="disabled")
            self.label_signal_pulseWidth.configure(state="disabled")
            self.label_signal_bandwidth.configure(state="disabled")
            
            self.entry_signal_frequency.configure(state="normal")
            self.entry_signal_amplitude.configure(state="normal")
            self.entry_signal_offset.configure(state="normal")
            self.entry_signal_phase.configure(state="normal")
            self.entry_signal_dutyCycle.configure(state="disabled")
            self.entry_signal_Symetry.configure(state="normal")
            self.entry_signal_riseTime.configure(state="disabled")
            self.entry_signal_fallTime.configure(state="disabled")
            self.entry_signal_pulseWidth.configure(state="disabled")
            self.entry_signal_bandwidth.configure(state="disabled")

            self.combo_signal_frequency.configure(state="normal")
            self.combo_signal_amplitude.configure(state="normal")
            self.combo_signal_offset.configure(state="normal")
            self.combo_signal_phase.configure(state="normal")
            self.combo_signal_dutyCycle.configure(state="disabled")
            self.combo_signal_symetry.configure(state="disabled")
            self.combo_signal_riseTime.configure(state="disabled")
            self.combo_signal_fallTime.configure(state="disabled")
            self.combo_signal_pulseWidth.configure(state="disabled")
            self.combo_signal_bandwidth.configure(state="disabled")

        if self.combo_signal_waveform.get() == "Pulse":
            self.label_signal_frequency.configure(state="normal")
            self.label_signal_amplitude.configure(state="normal")
            self.label_signal_offset.configure(state="normal")
            self.label_signal_phase.configure(state="normal")
            self.label_signal_dutyCycle.configure(state="disabled")
            self.label_signal_symetry.configure(state="disabled")
            self.label_signal_riseTime.configure(state="normal")
            self.label_signal_fallTime.configure(state="normal")
            self.label_signal_pulseWidth.configure(state="normal")
            self.label_signal_bandwidth.configure(state="disabled")
            
            self.entry_signal_frequency.configure(state="normal")
            self.entry_signal_amplitude.configure(state="normal")
            self.entry_signal_offset.configure(state="normal")
            self.entry_signal_phase.configure(state="normal")
            self.entry_signal_dutyCycle.configure(state="disabled")
            self.entry_signal_Symetry.configure(state="disabled")
            self.entry_signal_riseTime.configure(state="normal")
            self.entry_signal_fallTime.configure(state="normal")
            self.entry_signal_pulseWidth.configure(state="normal")
            self.entry_signal_bandwidth.configure(state="disabled")

            self.combo_signal_frequency.configure(state="normal")
            self.combo_signal_amplitude.configure(state="normal")
            self.combo_signal_offset.configure(state="normal")
            self.combo_signal_phase.configure(state="normal")
            self.combo_signal_dutyCycle.configure(state="disabled")
            self.combo_signal_symetry.configure(state="disabled")
            self.combo_signal_riseTime.configure(state="normal")
            self.combo_signal_fallTime.configure(state="normal")
            self.combo_signal_pulseWidth.configure(state="normal")
            self.combo_signal_bandwidth.configure(state="disabled")

        if self.combo_signal_waveform.get() == "Noise":
            self.label_signal_frequency.configure(state="disabled")
            self.label_signal_amplitude.configure(state="normal")
            self.label_signal_offset.configure(state="normal")
            self.label_signal_phase.configure(state="disabled")
            self.label_signal_dutyCycle.configure(state="disabled")
            self.label_signal_symetry.configure(state="disabled")
            self.label_signal_riseTime.configure(state="disabled")
            self.label_signal_fallTime.configure(state="disabled")
            self.label_signal_pulseWidth.configure(state="disabled")
            self.label_signal_bandwidth.configure(state="normal")
            
            self.entry_signal_frequency.configure(state="disabled")
            self.entry_signal_amplitude.configure(state="normal")
            self.entry_signal_offset.configure(state="normal")
            self.entry_signal_phase.configure(state="disabled")
            self.entry_signal_dutyCycle.configure(state="disabled")
            self.entry_signal_Symetry.configure(state="disabled")
            self.entry_signal_riseTime.configure(state="disabled")
            self.entry_signal_fallTime.configure(state="disabled")
            self.entry_signal_pulseWidth.configure(state="disabled")
            self.entry_signal_bandwidth.configure(state="normal")

            self.combo_signal_frequency.configure(state="disabled")
            self.combo_signal_amplitude.configure(state="normal")
            self.combo_signal_offset.configure(state="normal")
            self.combo_signal_phase.configure(state="disabled")
            self.combo_signal_dutyCycle.configure(state="disabled")
            self.combo_signal_symetry.configure(state="disabled")
            self.combo_signal_riseTime.configure(state="disabled")
            self.combo_signal_fallTime.configure(state="disabled")
            self.combo_signal_pulseWidth.configure(state="disabled")
            self.combo_signal_bandwidth.configure(state="normal")
        
        if self.combo_signal_waveform.get() == "Arbitrary":
            self.label_signal_frequency.configure(state="disabled")
            self.label_signal_amplitude.configure(state="normal")
            self.label_signal_offset.configure(state="normal")
            self.label_signal_phase.configure(state="disabled")
            self.label_signal_dutyCycle.configure(state="disabled")
            self.label_signal_symetry.configure(state="disabled")
            self.label_signal_riseTime.configure(state="disabled")
            self.label_signal_fallTime.configure(state="disabled")
            self.label_signal_pulseWidth.configure(state="disabled")
            self.label_signal_bandwidth.configure(state="disabled")
            
            self.entry_signal_frequency.configure(state="disabled")
            self.entry_signal_amplitude.configure(state="normal")
            self.entry_signal_offset.configure(state="normal")
            self.entry_signal_phase.configure(state="disabled")
            self.entry_signal_dutyCycle.configure(state="disabled")
            self.entry_signal_Symetry.configure(state="disabled")
            self.entry_signal_riseTime.configure(state="disabled")
            self.entry_signal_fallTime.configure(state="disabled")
            self.entry_signal_pulseWidth.configure(state="disabled")
            self.entry_signal_bandwidth.configure(state="disabled")

            self.combo_signal_frequency.configure(state="disabled")
            self.combo_signal_amplitude.configure(state="normal")
            self.combo_signal_offset.configure(state="normal")
            self.combo_signal_phase.configure(state="disabled")
            self.combo_signal_dutyCycle.configure(state="disabled")
            self.combo_signal_symetry.configure(state="disabled")
            self.combo_signal_riseTime.configure(state="disabled")
            self.combo_signal_fallTime.configure(state="disabled")
            self.combo_signal_pulseWidth.configure(state="disabled")
            self.combo_signal_bandwidth.configure(state="disabled")

    def combo_signal_frequency_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_frequency_caliber = self.combo_signal_frequency.get()
        
    def combo_signal_amplitude_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_amplitude_caliber = self.combo_signal_amplitude.get()          

    def combo_signal_offset_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_offset_caliber = self.combo_signal_offset.get()   
        
    def combo_signal_phase_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_phase_caliber = self.combo_signal_phase.get()   
        
    def combo_signal_dutyCycle_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_dutyCycle_caliber = self.combo_signal_dutyCycle.get() 
        
    def combo_signal_pulseWidth_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_pulsewidth_caliber = self.combo_signal_pulseWidth.get()     
        
    def combo_signal_riseTime_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_riseTime_caliber = self.combo_signal_riseTime.get()     
        
    def combo_signal_fallTime_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_fallTime_caliber = self.combo_signal_fallTime.get() 
        
    def combo_signal_symetry_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_symetry_caliber = self.combo_signal_symetry.get()  
        
    def combo_signal_bandwidth_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_bandwidth_caliber = self.combo_signal_bandwidth.get()  
        
    def combo_modulate_type_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.modulation_type = self.combo_modulate_type.get() 
        self.view.sendError("404")    
        
    def combo_modulate_source_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.modulation_source = self.combo_modulate_source.get() 
        self.view.sendError("404")    
        
    def combo_modulate_shape_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.modulation_shape = self.combo_modulate_shape.get() 
        self.view.sendError("404")    
        
    def combo_sweep_type_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.sweep_type = self.combo_sweep_type.get()
        self.view.sendError("404")     
        
    def combo_sweep_time_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.sweep_time_caliber = self.combo_sweep_time.get() 
        
    def combo_sweep_startFrequency_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.sweep_startFrequency_caliber = self.combo_sweep_startFrequency.get()   
        
    def combo_sweep_stopFrequency_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.sweep_stopFrequency_caliber = self.combo_sweep_stopFrequency.get()  
        
    def combo_sweep_holdTime_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.sweep_holdTime_caliber = self.combo_sweep_holdTime.get() 
        
    def combo_sweep_returnTime_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.sweep_returnTime_caliber = self.combo_sweep_returnTime.get()  

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

    def entry_signal_frequency_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_frequency = self.doubleVar_signal_frequency.get()  
        self.updateWaveform()
        
    def entry_signal_amplitude_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_amplitude = self.doubleVar_signal_amplitude.get()   
        self.updateWaveform()
        
    def entry_signal_offset_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_offset = self.doubleVar_signal_offset.get()    
        self.updateWaveform()
        
    def entry_signal_phase_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_phase = self.doubleVar_signal_phase.get()  
        self.updateWaveform()
        
    def entry_signal_dutyCycle_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_dutyCycle = self.doubleVar_signal_dutyCycle.get()  
        self.updateWaveform()

    def entry_signal_pulseWidth_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_pulsewidth = self.doubleVar_signal_pulseWidth.get()    
        self.updateWaveform()

    def entry_signal_riseTime_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_riseTime = self.doubleVar_signal_riseTime.get()  
        self.updateWaveform()

    def entry_signal_fallTime_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_fallTime = self.doubleVar_signal_fallTime.get() 
        self.updateWaveform()

    def entry_signal_symetry_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_symetry = self.doubleVar_signal_symetry.get()   
        self.updateWaveform()

    def entry_signal_bandwidth_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.signal_bandwidth = self.doubleVar_signal_bandwidth.get()   
        self.updateWaveform()

    def entry_sweep_time_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.sweep_time = self.doubleVar_sweep_time.get()     
        self.view.sendError("404") 
        
    def entry_sweep_startFrequency_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.sweep_startFrequency = self.doubleVar_sweep_startFrequency.get()     
        self.view.sendError("404")            
        
    def entry_sweep_stopFrequency_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.sweep_stopFrequency = self.doubleVar_sweep_stopFrequency.get()     
        self.view.sendError("404")      
        
    def entry_sweep_holdTime_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.sweep_holdTime = self.doubleVar_sweep_holdTime.get()     
        self.view.sendError("404")    
        
    def entry_sweep_returnTime_callback(self, arg=None):
    #This method calls the controller to change the voltage
        self.controller.instrument.sweep_returnTime = self.doubleVar_sweep_returnTime.get()     
        self.view.sendError("404")     

    def radio_outputState_callback(self, args=None):
    #This method is called when modifying the output impedance state
        self.controller.instrument.output_state = self.intVar_radioValueState.get()   
        self.updateWaveform()
        if self.intVar_radioValueState.get() == 0:   
            self.radio_outputStateLoad.select()  
            self.controller.setOutputState(state=0)  
        else:          
            self.controller.setOutputState(state=1)  
            self.radio_outputStateHigh.select()
    
    def radio_modulateState_callback(self, args=None):
    #This methods activates or desactivates the modulation function
        self.controller.instrument.signal_modulation_state = self.intVar_radioValueModulate.get()
        if self.intVar_radioValueModulate.get() != 0:
            self.intVar_radioValueSweep.set(0)
            self.combo_modulate_shape.configure(state="normal")
            self.combo_modulate_source.configure(state="normal")
            self.combo_modulate_type.configure(state="normal")
            self.combo_sweep_type.configure(state="disabled")
            self.combo_sweep_time.configure(state="disabled")
            self.combo_sweep_startFrequency.configure(state="disabled")
            self.combo_sweep_stopFrequency.configure(state="disabled")
            self.combo_sweep_holdTime.configure(state="disabled")
            self.combo_sweep_returnTime.configure(state="disabled")

            self.label_function_modulation.configure(state="normal")
            self.label_modulate_shape.configure(state="normal")
            self.label_modulate_source.configure(state="normal")
            self.label_modulate_type.configure(state="normal")
            self.label_function_sweep.configure(state="disabled")
            self.label_sweep_type.configure(state="disabled")
            self.label_sweep_time.configure(state="disabled")
            self.label_sweep_startFrequency.configure(state="disabled")
            self.label_sweep_stopFrequency.configure(state="disabled")
            self.label_sweep_holdTime.configure(state="disabled")
            self.label_sweep_returnTime.configure(state="disabled")

            self.entry_sweep_time.configure(state="disabled")
            self.entry_sweep_startFrequency.configure(state="disabled")
            self.entry_sweep_stopFrequency.configure(state="disabled")
            self.entry_sweep_holdTime.configure(state="disabled")
            self.entry_sweep_returnTime.configure(state="disabled")

        else:
            self.combo_modulate_shape.configure(state="disabled")
            self.combo_modulate_source.configure(state="disabled")
            self.combo_modulate_type.configure(state="disabled")
            self.combo_sweep_type.configure(state="disabled")
            self.combo_sweep_time.configure(state="disabled")
            self.combo_sweep_startFrequency.configure(state="disabled")
            self.combo_sweep_stopFrequency.configure(state="disabled")
            self.combo_sweep_holdTime.configure(state="disabled")
            self.combo_sweep_returnTime.configure(state="disabled")
            
            self.label_function_modulation.configure(state="disabled")
            self.label_modulate_shape.configure(state="disabled")
            self.label_modulate_source.configure(state="disabled")
            self.label_modulate_type.configure(state="disabled")
            self.label_function_sweep.configure(state="disabled")
            self.label_sweep_type.configure(state="disabled")
            self.label_sweep_time.configure(state="disabled")
            self.label_sweep_startFrequency.configure(state="disabled")
            self.label_sweep_stopFrequency.configure(state="disabled")
            self.label_sweep_holdTime.configure(state="disabled")
            self.label_sweep_returnTime.configure(state="disabled")

            self.entry_sweep_time.configure(state="disabled")
            self.entry_sweep_startFrequency.configure(state="disabled")
            self.entry_sweep_stopFrequency.configure(state="disabled")
            self.entry_sweep_holdTime.configure(state="disabled")
            self.entry_sweep_returnTime.configure(state="disabled")

    def radio_sweepState_callback(self, args=None):
    #This methods activates or desactivates the modulation function
        self.controller.instrument.signal_sweep_state = self.intVar_radioValueSweep.get()
        if self.intVar_radioValueSweep.get() != 0:
            self.intVar_radioValueModulate.set(0)
            self.combo_modulate_shape.configure(state="disabled")
            self.combo_modulate_source.configure(state="disabled")
            self.combo_modulate_type.configure(state="disabled")
            self.combo_sweep_type.configure(state="normal")
            self.combo_sweep_time.configure(state="normal")
            self.combo_sweep_startFrequency.configure(state="normal")
            self.combo_sweep_stopFrequency.configure(state="normal")
            self.combo_sweep_holdTime.configure(state="normal")
            self.combo_sweep_returnTime.configure(state="normal")

            self.label_function_modulation.configure(state="disabled")
            self.label_modulate_shape.configure(state="disabled")
            self.label_modulate_source.configure(state="disabled")
            self.label_modulate_type.configure(state="disabled")
            self.label_function_sweep.configure(state="normal")
            self.label_sweep_type.configure(state="normal")
            self.label_sweep_time.configure(state="normal")
            self.label_sweep_startFrequency.configure(state="normal")
            self.label_sweep_stopFrequency.configure(state="normal")
            self.label_sweep_holdTime.configure(state="normal")
            self.label_sweep_returnTime.configure(state="normal")

            self.entry_sweep_time.configure(state="normal")
            self.entry_sweep_startFrequency.configure(state="normal")
            self.entry_sweep_stopFrequency.configure(state="normal")
            self.entry_sweep_holdTime.configure(state="normal")
            self.entry_sweep_returnTime.configure(state="normal")

        else:
            self.combo_modulate_shape.configure(state="disabled")
            self.combo_modulate_source.configure(state="disabled")
            self.combo_modulate_type.configure(state="disabled")
            self.combo_sweep_type.configure(state="disabled")
            self.combo_sweep_time.configure(state="disabled")
            self.combo_sweep_startFrequency.configure(state="disabled")
            self.combo_sweep_stopFrequency.configure(state="disabled")
            self.combo_sweep_holdTime.configure(state="disabled")
            self.combo_sweep_returnTime.configure(state="disabled")
            
            self.label_function_modulation.configure(state="disabled")
            self.label_modulate_shape.configure(state="disabled")
            self.label_modulate_source.configure(state="disabled")
            self.label_modulate_type.configure(state="disabled")
            self.label_function_sweep.configure(state="disabled")
            self.label_sweep_type.configure(state="disabled")
            self.label_sweep_time.configure(state="disabled")
            self.label_sweep_startFrequency.configure(state="disabled")
            self.label_sweep_stopFrequency.configure(state="disabled")
            self.label_sweep_holdTime.configure(state="disabled")
            self.label_sweep_returnTime.configure(state="disabled")

            self.entry_sweep_time.configure(state="disabled")
            self.entry_sweep_startFrequency.configure(state="disabled")
            self.entry_sweep_stopFrequency.configure(state="disabled")
            self.entry_sweep_holdTime.configure(state="disabled")
            self.entry_sweep_returnTime.configure(state="disabled")

    def master_activate_callback(self):
    #This method call the controller to change output state
        self.updateWaveform() 
        if self.controller.setMasterState() != -1:
            if (self.intVar_radioValueMaster.get() == 0) and (self.controller.instrument.address != ""):
                self.intVar_radioValueMaster.set(1) 
                self.radio_masterStateON.select() 
            else:
                self.intVar_radioValueMaster.set(0)
                self.radio_masterStateOFF.select() 

    def updateWaveform(self):
    #This method  updates the measurement content
        amplitude = self.doubleVar_signal_amplitude.get()
        amplitudeType = self.combo_signal_amplitude.get()
        frequency = self.doubleVar_signal_frequency.get()
        frequencyUnit = self.combo_signal_frequency.get()
        offset = self.doubleVar_signal_offset.get()
        phase = self.doubleVar_signal_phase.get()
        bandwidth = self.doubleVar_signal_bandwidth.get()
        dutyCycle = self.doubleVar_signal_dutyCycle.get()
        pulseWidth = self.doubleVar_signal_pulseWidth.get()
        pulseWidthUnit = self.combo_signal_pulseWidth.get()
        symetry = self.doubleVar_signal_symetry.get()
        lead = self.doubleVar_signal_riseTime.get()
        leadUnit = self.combo_signal_riseTime.get()
        trail = self.doubleVar_signal_fallTime.get()
        trailUnit = self.combo_signal_fallTime.get()

        if self.combo_signal_waveform.get() == "Sinus":            
            self.controller.applySinus(amplitude=amplitude, amplitudeType=amplitudeType, frequency=frequency, frequencyUnit=frequencyUnit, offset=offset, phase=phase)    

        if self.combo_signal_waveform.get() == "Square":
            self.controller.applySquare(amplitude=amplitude, amplitudeType=amplitudeType, frequency=frequency, frequencyUnit=frequencyUnit, offset=offset, phase=phase, dutyCycle=dutyCycle)      

        if self.combo_signal_waveform.get() == "Ramp":
            self.controller.applyRamp(amplitude=amplitude, amplitudeType=amplitudeType, frequency=frequency, frequencyUnit=frequencyUnit, offset=offset, symetry=symetry, phase=phase)    

        if self.combo_signal_waveform.get() == "Pulse":
            self.controller.applyPulse(amplitude=amplitude, amplitudeType=amplitudeType, frequency=frequency, frequencyUnit=frequencyUnit, offset=offset, phase=phase, lead=lead, leadUnit=leadUnit, trail=trail, trailUnit=trailUnit, pulseWidth=pulseWidth, pulseWidthUnit=pulseWidthUnit)   
      
        if self.combo_signal_waveform.get() == "Noise":
            self.controller.applyNoise(amplitude=amplitude, amplitudeType=amplitudeType, bandwidth=bandwidth, offset=offset)   
      