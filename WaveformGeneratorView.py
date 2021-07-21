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

        self.frame_source_waveform = Frame(self.scrollframe_signal)
        self.frame_source_frequency = Frame(self.scrollframe_signal)
        self.frame_source_amplitude = Frame(self.scrollframe_signal)
        self.frame_source_offset = Frame(self.scrollframe_signal)
        self.frame_source_phase = Frame(self.scrollframe_signal)
        self.frame_source_dutyCycle = Frame(self.scrollframe_signal)
        self.frame_source_pulseWidth = Frame(self.scrollframe_signal)
        self.frame_source_riseTime = Frame(self.scrollframe_signal)
        self.frame_source_fallTime = Frame(self.scrollframe_signal)
        self.frame_source_symetry = Frame(self.scrollframe_signal)
        self.frame_source_bandwidth = Frame(self.scrollframe_signal)
        self.frame_source_modulate = Frame(self.scrollframe_signal)
        self.frame_source_sweep = Frame(self.scrollframe_signal)

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
        self.doubleVar_source_frequency = DoubleVar()
        self.doubleVar_source_amplitude = DoubleVar()
        self.doubleVar_source_offset = DoubleVar()
        self.doubleVar_source_phase = DoubleVar()
        self.doubleVar_source_dutyCycle = DoubleVar()
        self.doubleVar_source_pulseWidth = DoubleVar()
        self.doubleVar_source_riseTime = DoubleVar()
        self.doubleVar_source_fallTime = DoubleVar()
        self.doubleVar_source_symetry = DoubleVar()
        self.doubleVar_source_bandwidth = DoubleVar()
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

        self.label_source_waveform = Label(self.frame_source_waveform, text="Waveform :")
        self.label_source_frequency = Label(self.frame_source_frequency, text="Frequency :")
        self.label_source_amplitude = Label(self.frame_source_amplitude, text="Amplitude :")
        self.label_source_offset = Label(self.frame_source_offset, text="Offset :")
        self.label_source_phase = Label(self.frame_source_phase, text="Phase :")
        self.label_source_dutyCycle = Label(self.frame_source_dutyCycle, text="Duty Cycle :")
        self.label_source_symetry = Label(self.frame_source_symetry, text="Symetry :")
        self.label_source_pulseWidth = Label(self.frame_source_pulseWidth, text="Pulse Width :")
        self.label_source_riseTime = Label(self.frame_source_riseTime, text="Rise Time :")
        self.label_source_fallTime = Label(self.frame_source_fallTime, text="Fall Time :")
        self.label_source_bandwidth = Label(self.frame_source_bandwidth, text="Bandwidth :")
        self.label_source_modulate = Label(self.frame_source_modulate, text="Modulation : ")
        self.label_source_sweep = Label(self.frame_source_sweep, text="Sweep :      ")
        self.label_source_dutyCycle.after(1000, self.updateMonitoring)

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

        self.combo_source_waveform = Combobox(self.frame_source_waveform, state="readonly", width=17, values=["Sinus", "Square", "Ramp", "Pulse", "Noise", "Arbitrary"])
        self.combo_source_frequency = Combobox(self.frame_source_frequency, state="readonly", width=5, values=["Hz", "kHz", "MHz"])
        self.combo_source_amplitude = Combobox(self.frame_source_amplitude, state="readonly", width=5, values=["V", "mV"])
        self.combo_source_offset = Combobox(self.frame_source_offset, state="readonly", width=5, values=["V", "mV"])
        self.combo_source_phase = Combobox(self.frame_source_phase, state="readonly", width=5, values=["deg"])
        self.combo_source_dutyCycle = Combobox(self.frame_source_dutyCycle, state="readonly", width=5, values=["%"])
        self.combo_source_symetry = Combobox(self.frame_source_symetry, state="readonly", width=5, values=["%"])
        self.combo_source_pulseWidth = Combobox(self.frame_source_pulseWidth, state="readonly", width=5, values=["s", "ms", "µs", "ns"])
        self.combo_source_riseTime = Combobox(self.frame_source_riseTime, state="readonly", width=5, values=["s", "ms", "µs", "ns"])
        self.combo_source_fallTime = Combobox(self.frame_source_fallTime, state="readonly", width=5, values=["s", "ms", "µs", "ns"])
        self.combo_source_bandwidth = Combobox(self.frame_source_bandwidth, state="readonly", width=5, values=["Hz", "kHz", "MHz"])
        
        self.combo_modulate_type = Combobox(self.frame_modulate_type, state="readonly", width=20, values=["AM", "FM", "PM", "FSK", "BPSK"])
        self.combo_modulate_source = Combobox(self.frame_modulate_source, state="readonly", width=20, values=["Internal", "External"])
        self.combo_modulate_shape = Combobox(self.frame_modulate_shape, state="readonly", width=20, values=["Sinus", "Square", "UpRamp", "DownRamp", "Triangle", "Noise"])
        self.combo_sweep_type = Combobox(self.frame_sweep_type, state="readonly", width=16, values=["Linear", "Logarithmic"])
        self.combo_sweep_time = Combobox(self.frame_sweep_time, state="readonly", width=5, values=["s", "ms", "µs", "ns"])
        self.combo_sweep_startFrequency = Combobox(self.frame_sweep_startFrequency, state="readonly", width=5, values=["Hz", "kHz", "MHz"])
        self.combo_sweep_stopFrequency = Combobox(self.frame_sweep_stopFrequency, state="readonly", width=5, values=["Hz", "kHz", "MHz"])
        self.combo_sweep_holdTime = Combobox(self.frame_sweep_holdTime, state="readonly", width=5, values=["s", "ms", "µs", "ns"])
        self.combo_sweep_returnTime = Combobox(self.frame_sweep_returnTime, state="readonly", width=5, values=["s", "ms", "µs", "ns"])

        self.entry_instrumentName = Entry(self.frame_instrument_name, width=30, textvariable=self.stringvar_instrumentName)
        self.entry_instrumentaddress = Entry(self.frame_instrument_address, width=30, textvariable=self.stringvar_instrumentaddress, state="readonly")

        self.entry_source_frequency = Entry(self.frame_source_frequency, textvariable=self.doubleVar_source_frequency, width=10)
        self.entry_source_amplitude = Entry(self.frame_source_amplitude, textvariable=self.doubleVar_source_amplitude, width=10)
        self.entry_source_offset = Entry(self.frame_source_offset, textvariable=self.doubleVar_source_offset, width=10)
        self.entry_source_phase = Entry(self.frame_source_phase, textvariable=self.doubleVar_source_phase, width=10)
        self.entry_source_dutyCycle = Entry(self.frame_source_dutyCycle, textvariable=self.doubleVar_source_dutyCycle, width=10)
        self.entry_source_Symetry = Entry(self.frame_source_symetry, textvariable=self.doubleVar_source_symetry, width=10)
        self.entry_source_pulseWidth = Entry(self.frame_source_pulseWidth, textvariable=self.doubleVar_source_pulseWidth, width=10)
        self.entry_source_riseTime = Entry(self.frame_source_riseTime, textvariable=self.doubleVar_source_riseTime, width=10)
        self.entry_source_fallTime = Entry(self.frame_source_fallTime, textvariable=self.doubleVar_source_fallTime, width=10)
        self.entry_source_bandwidth = Entry(self.frame_source_bandwidth, textvariable=self.doubleVar_source_bandwidth, width=10)

        self.entry_sweep_time = Entry(self.frame_sweep_time, textvariable=self.doubleVar_sweep_time, width=10)
        self.entry_sweep_startFrequency = Entry(self.frame_sweep_startFrequency, textvariable=self.doubleVar_sweep_startFrequency, width=10)
        self.entry_sweep_stopFrequency = Entry(self.frame_sweep_stopFrequency, textvariable=self.doubleVar_sweep_stopFrequency, width=10)
        self.entry_sweep_holdTime = Entry(self.frame_sweep_holdTime, textvariable=self.doubleVar_sweep_holdTime, width=10)
        self.entry_sweep_returnTime = Entry(self.frame_sweep_returnTime, textvariable=self.doubleVar_sweep_returnTime, width=10)

        self.master_activate = Button(self.frame_master_button, text='Master ON/OFF', command=self.master_activate_callback)

        self.radio_modulateStateOFF = Radiobutton(self.frame_source_modulate, text='OFF', variable=self.intVar_radioValueModulate, value=1)
        self.radio_modulateStateON = Radiobutton(self.frame_source_modulate, text='ON', variable=self.intVar_radioValueModulate, value=2)

        self.radio_sweepStateOFF = Radiobutton(self.frame_source_sweep, text='OFF', variable=self.intVar_radioValueSweep, value=1)
        self.radio_sweepStateON = Radiobutton(self.frame_source_sweep, text='ON', variable=self.intVar_radioValueSweep, value=2)

        self.radio_outputStateHigh = Radiobutton(self.frame_output_state, text='High Z', variable=self.intVar_radioValueState, value=1)
        self.radio_outputStateLoad = Radiobutton(self.frame_output_state, text='50Ω', variable=self.intVar_radioValueState, value=2)

        self.radio_masterStateOFF = Radiobutton(self.frame_master_radio, text='OFF', variable=self.intVar_radioValueMaster, value=1)
        self.radio_masterStateON = Radiobutton(self.frame_master_radio, text='ON', variable=self.intVar_radioValueMaster, value=2)
        
        self.img = None
        self.panel = Label(self.frame, bg=self.model.parameters_dict['backgroundColor'])
        
    def clearInstrument(self):
    #This method is used to clear every trace of this instrument before being deleted
        None

    def renameInstrument(self):
        i = 0
        for i in range(len(self.view.listInstruments)):
            if self.controller.instrument.name == self.view.listInstruments[i].controller.instrument.name:    
                newName = self.controller.instrument.name[:-2] + str(i) + ")"
                self.entry_instrumentName_callback(newName=newName)

    def updateView(self):
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

        self.frame_source_waveform.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_waveform.pack(fill="x", pady=5)

        self.frame_source_frequency.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_frequency.pack(fill="x", pady=5)

        self.frame_source_amplitude.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_amplitude.pack(fill="x", pady=5)

        self.frame_source_offset.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_offset.pack(fill="x", pady=5)

        self.frame_source_phase.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_phase.pack(fill="x", pady=5)

        self.frame_source_dutyCycle.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_dutyCycle.pack(fill="x",pady=5)

        self.frame_source_pulseWidth.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_pulseWidth.pack(fill="x",pady=5)

        self.frame_source_riseTime.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_riseTime.pack(fill="x",pady=5)

        self.frame_source_fallTime.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_fallTime.pack(fill="x",pady=5)

        self.frame_source_symetry.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_symetry.pack(fill="x",pady=5)

        self.frame_source_bandwidth.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_bandwidth.pack(fill="x",pady=5)

        self.frame_source_modulate.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_modulate.pack(fill="x",pady=5)

        self.frame_source_sweep.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frame_source_sweep.pack(fill="x",pady=5)

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

        self.doubleVar_source_frequency.set(1000)
        self.doubleVar_source_amplitude.set(1)
        self.doubleVar_source_offset.set(0)
        self.doubleVar_source_phase.set(0)
        self.doubleVar_source_dutyCycle.set(50)
        self.doubleVar_source_symetry.set(50)
        self.doubleVar_source_pulseWidth.set(1)
        self.doubleVar_source_riseTime.set(0)
        self.doubleVar_source_fallTime.set(0)
        self.doubleVar_source_bandwidth.set(1000)
        self.doubleVar_sweep_time.set(1)
        self.doubleVar_sweep_startFrequency.set(1)
        self.doubleVar_sweep_stopFrequency.set(1000)
        self.doubleVar_sweep_holdTime.set(0)
        self.doubleVar_sweep_returnTime.set(0)
        
    def initLabel(self):
    #This methods instanciates all the Label
        self.label_instrumentName.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentName.pack(side="left")

        self.label_instrumentaddress.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_instrumentaddress.pack(side="left")

        self.label_source_waveform.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_waveform.pack(side="left")

        self.label_source_frequency.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_frequency.pack(side="left")

        self.label_source_amplitude.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_amplitude.pack(side="left")

        self.label_source_offset.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_offset.pack(side="left")

        self.label_source_phase.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_phase.pack(side="left")

        self.label_source_dutyCycle.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_dutyCycle.pack(side="left")

        self.label_source_pulseWidth.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_pulseWidth.pack(side="left")

        self.label_source_riseTime.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_riseTime.pack(side="left")

        self.label_source_fallTime.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_fallTime.pack(side="left")

        self.label_source_symetry.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_symetry.pack(side="left")

        self.label_source_bandwidth.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_bandwidth.pack(side="left")

        self.label_source_modulate.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_modulate.pack(side="left")

        self.label_source_sweep.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_source_sweep.pack(side="left")

        self.label_function_modulation.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_function_modulation.pack(side="left")

        self.label_modulate_type.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_modulate_type.pack(side="left")

        self.label_modulate_source.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_modulate_source.pack(side="left")

        self.label_modulate_shape.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_modulate_shape.pack(side="left")

        self.label_function_sweep.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_function_sweep.pack(side="left")

        self.label_sweep_type.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_sweep_type.pack(side="left")

        self.label_sweep_time.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_sweep_time.pack(side="left")

        self.label_sweep_startFrequency.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_sweep_startFrequency.pack(side="left")

        self.label_sweep_stopFrequency.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_sweep_stopFrequency.pack(side="left")

        self.label_sweep_holdTime.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_sweep_holdTime.pack(side="left")

        self.label_sweep_returnTime.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_sweep_returnTime.pack(side="left")

        self.label_output_state.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.label_output_state.pack(side="left")

    def initCombo(self):
    #This methods instanciates all the combobox
        self.combo_source_waveform.bind("<<ComboboxSelected>>", self.combo_source_waveform_callback)
        self.combo_source_waveform.configure(background='white')
        self.combo_source_waveform.current(0)
        self.combo_source_waveform.pack(side="right")
        self.combo_source_waveform_callback()

        #self.combo_source_frequency.bind("<<ComboboxSelected>>", self.combo_source_frequency_callback)
        self.combo_source_frequency.configure(background='white')
        self.combo_source_frequency.current(0)
        self.combo_source_frequency.pack(side="right")
    
        #self.combo_source_amplitude.bind("<<ComboboxSelected>>", self.combo_source_amplitude_callback)
        self.combo_source_amplitude.configure(background='white')
        self.combo_source_amplitude.current(0)
        self.combo_source_amplitude.pack(side="right")
    
        #self.combo_source_offset.bind("<<ComboboxSelected>>", self.combo_source_offset_callback)
        self.combo_source_offset.configure(background='white')
        self.combo_source_offset.current(0)
        self.combo_source_offset.pack(side="right")
    
        #self.combo_source_phase.bind("<<ComboboxSelected>>", self.combo_source_phase_callback)
        self.combo_source_phase.configure(background='white')
        self.combo_source_phase.current(0)
        self.combo_source_phase.pack(side="right")
    
        #self.combo_source_phase.bind("<<ComboboxSelected>>", self.combo_source_phase_callback)
        self.combo_source_dutyCycle.configure(background='white')
        self.combo_source_dutyCycle.current(0)
        self.combo_source_dutyCycle.pack(side="right")

        #self.combo_source_symetry.bind("<<ComboboxSelected>>", self.combo_source_symetry_callback)
        self.combo_source_symetry.configure(background='white')
        self.combo_source_symetry.current(0)
        self.combo_source_symetry.pack(side="right")
    
        #self.combo_source_pulseWidth.bind("<<ComboboxSelected>>", self.combo_source_pulseWidth_callback)
        self.combo_source_pulseWidth.configure(background='white')
        self.combo_source_pulseWidth.current(0)
        self.combo_source_pulseWidth.pack(side="right")
    
        #self.combo_source_riseTime.bind("<<ComboboxSelected>>", self.combo_source_riseTime_callback)
        self.combo_source_riseTime.configure(background='white')
        self.combo_source_riseTime.current(0)
        self.combo_source_riseTime.pack(side="right")
    
        #self.combo_source_fallTime.bind("<<ComboboxSelected>>", self.combo_source_fallTime_callback)
        self.combo_source_fallTime.configure(background='white')
        self.combo_source_fallTime.current(0)
        self.combo_source_fallTime.pack(side="right")
    
        #self.combo_source_bandwidth.bind("<<ComboboxSelected>>", self.combo_source_bandwidth_callback)
        self.combo_source_bandwidth.configure(background='white')
        self.combo_source_bandwidth.current(0)
        self.combo_source_bandwidth.pack(side="right")
    
        #self.combo_modulate_type.bind("<<ComboboxSelected>>", self.combo_modulate_type_callback)
        self.combo_modulate_type.configure(background='white')
        self.combo_modulate_type.current(0)
        self.combo_modulate_type.pack(side="right")
    
        #self.combo_modulate_source.bind("<<ComboboxSelected>>", self.combo_modulate_source_callback)
        self.combo_modulate_source.configure(background='white')
        self.combo_modulate_source.current(0)
        self.combo_modulate_source.pack(side="right")
    
        #self.combo_modulate_shape.bind("<<ComboboxSelected>>", self.combo_modulate_shape_callback)
        self.combo_modulate_shape.configure(background='white')
        self.combo_modulate_shape.current(0)
        self.combo_modulate_shape.pack(side="right")
    
        #self.combo_sweep_type.bind("<<ComboboxSelected>>", self.combo_sweep_type_callback)
        self.combo_sweep_type.configure(background='white')
        self.combo_sweep_type.current(0)
        self.combo_sweep_type.pack(side="right")
    
        #self.combo_sweep_time.bind("<<ComboboxSelected>>", self.combo_sweep_time_callback)
        self.combo_sweep_time.configure(background='white')
        self.combo_sweep_time.current(0)
        self.combo_sweep_time.pack(side="right")
    
        #self.combo_sweep_startFrequency.bind("<<ComboboxSelected>>", self.combo_sweep_startFrequency_callback)
        self.combo_sweep_startFrequency.configure(background='white')
        self.combo_sweep_startFrequency.current(0)
        self.combo_sweep_startFrequency.pack(side="right")
    
        #self.combo_sweep_stopFrequency.bind("<<ComboboxSelected>>", self.combo_sweep_stopFrequency_callback)
        self.combo_sweep_stopFrequency.configure(background='white')
        self.combo_sweep_stopFrequency.current(0)
        self.combo_sweep_stopFrequency.pack(side="right")
    
        #self.combo_sweep_holdTime.bind("<<ComboboxSelected>>", self.combo_sweep_holdTime_callback)
        self.combo_sweep_holdTime.configure(background='white')
        self.combo_sweep_holdTime.current(0)
        self.combo_sweep_holdTime.pack(side="right")
    
        #self.combo_sweep_returnTime.bind("<<ComboboxSelected>>", self.combo_sweep_returnTime_callback)
        self.combo_sweep_returnTime.configure(background='white')
        self.combo_sweep_returnTime.current(0)
        self.combo_sweep_returnTime.pack(side="right")

    def initEntries(self):
    #This method instanciates the entries    
        self.entry_instrumentName.bind("<KeyRelease>", self.entry_instrumentName_callback)
        self.entry_instrumentName.pack(side='left', padx=5)

        self.entry_instrumentaddress.bind('<ButtonRelease-1>', self.view.menu2_Connections_callBack)
        self.entry_instrumentaddress.pack(side='left', padx=5)

        self.entry_source_frequency.bind("<Return>", self.entry_source_frequency_callback)
        self.entry_source_frequency.pack(side='right', padx=5)

        self.entry_source_amplitude.bind("<Return>", self.entry_source_amplitude_callback)
        self.entry_source_amplitude.pack(side='right', padx=5)

        self.entry_source_offset.pack(side='right', padx=5)

        self.entry_source_phase.pack(side='right', padx=5)

        self.entry_source_dutyCycle.pack(side='right', padx=5)

        self.entry_source_Symetry.pack(side='right', padx=5)

        self.entry_source_pulseWidth.pack(side='right', padx=5)

        self.entry_source_riseTime.pack(side='right', padx=5)

        self.entry_source_fallTime.pack(side='right', padx=5)

        self.entry_source_bandwidth.pack(side='right', padx=5)

        self.entry_sweep_time.pack(side='right', padx=5)

        self.entry_sweep_startFrequency.pack(side='right', padx=5)

        self.entry_sweep_stopFrequency.pack(side='right', padx=5)

        self.entry_sweep_holdTime.pack(side='right', padx=5)

        self.entry_sweep_returnTime.pack(side='right', padx=5)

    def initButton(self):
    #This method instanciates the buttons
        self.master_activate.pack(expand="yes")

        self.radio_sweepStateON.pack(side="right", expand="yes", fill="both")
        self.radio_sweepStateON.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.radio_sweepStateOFF.pack(side="right", expand="yes", fill="both")
        self.radio_sweepStateOFF.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.intVar_radioValueSweep.set(1)

        self.radio_modulateStateON.pack(side="right", expand="yes", fill="both")
        self.radio_modulateStateON.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.radio_modulateStateOFF.pack(side="right", expand="yes", fill="both")
        self.radio_modulateStateOFF.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.intVar_radioValueModulate.set(1)

        self.radio_outputStateHigh.pack(side="right", expand="yes", fill="both")
        self.radio_outputStateHigh.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.radio_outputStateLoad.pack(side="right", expand="yes", fill="both")
        self.radio_outputStateLoad.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.intVar_radioValueState.set(1)

        self.radio_masterStateON.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateON.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled", disabledforeground="black")
        self.radio_masterStateOFF.pack(side="top", expand="yes", fill="both")
        self.radio_masterStateOFF.configure(bg=self.model.parameters_dict['backgroundColor'], state="disabled", disabledforeground="black")
        self.intVar_radioValueMaster.set(1)

    def combo_source_waveform_callback(self, args=None):
    #This method is called when this combobow is selected
        if self.combo_source_waveform.get() == "Sinus":
            self.label_source_frequency.configure(state="normal")
            self.label_source_amplitude.configure(state="normal")
            self.label_source_offset.configure(state="normal")
            self.label_source_phase.configure(state="normal")
            self.label_source_dutyCycle.configure(state="disabled")
            self.label_source_symetry.configure(state="disabled")
            self.label_source_riseTime.configure(state="disabled")
            self.label_source_fallTime.configure(state="disabled")
            self.label_source_pulseWidth.configure(state="disabled")
            self.label_source_bandwidth.configure(state="disabled")
            
            self.entry_source_frequency.configure(state="normal")
            self.entry_source_amplitude.configure(state="normal")
            self.entry_source_offset.configure(state="normal")
            self.entry_source_phase.configure(state="normal")
            self.entry_source_dutyCycle.configure(state="disabled")
            self.entry_source_Symetry.configure(state="disabled")
            self.entry_source_riseTime.configure(state="disabled")
            self.entry_source_fallTime.configure(state="disabled")
            self.entry_source_pulseWidth.configure(state="disabled")
            self.entry_source_bandwidth.configure(state="disabled")

            self.combo_source_frequency.configure(state="normal")
            self.combo_source_amplitude.configure(state="normal")
            self.combo_source_offset.configure(state="normal")
            self.combo_source_phase.configure(state="normal")
            self.combo_source_dutyCycle.configure(state="disabled")
            self.combo_source_symetry.configure(state="disabled")
            self.combo_source_riseTime.configure(state="disabled")
            self.combo_source_fallTime.configure(state="disabled")
            self.combo_source_pulseWidth.configure(state="disabled")
            self.combo_source_bandwidth.configure(state="disabled")

        if self.combo_source_waveform.get() == "Square":
            self.label_source_frequency.configure(state="normal")
            self.label_source_amplitude.configure(state="normal")
            self.label_source_offset.configure(state="normal")
            self.label_source_phase.configure(state="normal")
            self.label_source_dutyCycle.configure(state="normal")
            self.label_source_symetry.configure(state="disabled")
            self.label_source_riseTime.configure(state="disabled")
            self.label_source_fallTime.configure(state="disabled")
            self.label_source_pulseWidth.configure(state="disabled")
            self.label_source_bandwidth.configure(state="disabled")
            
            self.entry_source_frequency.configure(state="normal")
            self.entry_source_amplitude.configure(state="normal")
            self.entry_source_offset.configure(state="normal")
            self.entry_source_phase.configure(state="normal")
            self.entry_source_dutyCycle.configure(state="normal")
            self.entry_source_Symetry.configure(state="disabled")
            self.entry_source_riseTime.configure(state="disabled")
            self.entry_source_fallTime.configure(state="disabled")
            self.entry_source_pulseWidth.configure(state="disabled")
            self.entry_source_bandwidth.configure(state="disabled")

            self.combo_source_frequency.configure(state="normal")
            self.combo_source_amplitude.configure(state="normal")
            self.combo_source_offset.configure(state="normal")
            self.combo_source_phase.configure(state="normal")
            self.combo_source_dutyCycle.configure(state="normal")
            self.combo_source_symetry.configure(state="disabled")
            self.combo_source_riseTime.configure(state="disabled")
            self.combo_source_fallTime.configure(state="disabled")
            self.combo_source_pulseWidth.configure(state="disabled")
            self.combo_source_bandwidth.configure(state="disabled")

        if self.combo_source_waveform.get() == "Ramp":
            self.label_source_frequency.configure(state="normal")
            self.label_source_amplitude.configure(state="normal")
            self.label_source_offset.configure(state="normal")
            self.label_source_phase.configure(state="normal")
            self.label_source_dutyCycle.configure(state="disabled")
            self.label_source_symetry.configure(state="normal")
            self.label_source_riseTime.configure(state="disabled")
            self.label_source_fallTime.configure(state="disabled")
            self.label_source_pulseWidth.configure(state="disabled")
            self.label_source_bandwidth.configure(state="disabled")
            
            self.entry_source_frequency.configure(state="normal")
            self.entry_source_amplitude.configure(state="normal")
            self.entry_source_offset.configure(state="normal")
            self.entry_source_phase.configure(state="normal")
            self.entry_source_dutyCycle.configure(state="disabled")
            self.entry_source_Symetry.configure(state="normal")
            self.entry_source_riseTime.configure(state="disabled")
            self.entry_source_fallTime.configure(state="disabled")
            self.entry_source_pulseWidth.configure(state="disabled")
            self.entry_source_bandwidth.configure(state="disabled")

            self.combo_source_frequency.configure(state="normal")
            self.combo_source_amplitude.configure(state="normal")
            self.combo_source_offset.configure(state="normal")
            self.combo_source_phase.configure(state="normal")
            self.combo_source_dutyCycle.configure(state="disabled")
            self.combo_source_symetry.configure(state="disabled")
            self.combo_source_riseTime.configure(state="disabled")
            self.combo_source_fallTime.configure(state="disabled")
            self.combo_source_pulseWidth.configure(state="disabled")
            self.combo_source_bandwidth.configure(state="disabled")

        if self.combo_source_waveform.get() == "Pulse":
            self.label_source_frequency.configure(state="normal")
            self.label_source_amplitude.configure(state="normal")
            self.label_source_offset.configure(state="normal")
            self.label_source_phase.configure(state="normal")
            self.label_source_dutyCycle.configure(state="disabled")
            self.label_source_symetry.configure(state="disabled")
            self.label_source_riseTime.configure(state="normal")
            self.label_source_fallTime.configure(state="normal")
            self.label_source_pulseWidth.configure(state="normal")
            self.label_source_bandwidth.configure(state="disabled")
            
            self.entry_source_frequency.configure(state="normal")
            self.entry_source_amplitude.configure(state="normal")
            self.entry_source_offset.configure(state="normal")
            self.entry_source_phase.configure(state="normal")
            self.entry_source_dutyCycle.configure(state="disabled")
            self.entry_source_Symetry.configure(state="disabled")
            self.entry_source_riseTime.configure(state="normal")
            self.entry_source_fallTime.configure(state="normal")
            self.entry_source_pulseWidth.configure(state="normal")
            self.entry_source_bandwidth.configure(state="disabled")

            self.combo_source_frequency.configure(state="normal")
            self.combo_source_amplitude.configure(state="normal")
            self.combo_source_offset.configure(state="normal")
            self.combo_source_phase.configure(state="normal")
            self.combo_source_dutyCycle.configure(state="disabled")
            self.combo_source_symetry.configure(state="disabled")
            self.combo_source_riseTime.configure(state="normal")
            self.combo_source_fallTime.configure(state="normal")
            self.combo_source_pulseWidth.configure(state="normal")
            self.combo_source_bandwidth.configure(state="disabled")

        if self.combo_source_waveform.get() == "Noise":
            self.label_source_frequency.configure(state="disabled")
            self.label_source_amplitude.configure(state="normal")
            self.label_source_offset.configure(state="normal")
            self.label_source_phase.configure(state="disabled")
            self.label_source_dutyCycle.configure(state="disabled")
            self.label_source_symetry.configure(state="disabled")
            self.label_source_riseTime.configure(state="disabled")
            self.label_source_fallTime.configure(state="disabled")
            self.label_source_pulseWidth.configure(state="disabled")
            self.label_source_bandwidth.configure(state="normal")
            
            self.entry_source_frequency.configure(state="disabled")
            self.entry_source_amplitude.configure(state="normal")
            self.entry_source_offset.configure(state="normal")
            self.entry_source_phase.configure(state="disabled")
            self.entry_source_dutyCycle.configure(state="disabled")
            self.entry_source_Symetry.configure(state="disabled")
            self.entry_source_riseTime.configure(state="disabled")
            self.entry_source_fallTime.configure(state="disabled")
            self.entry_source_pulseWidth.configure(state="disabled")
            self.entry_source_bandwidth.configure(state="normal")

            self.combo_source_frequency.configure(state="disabled")
            self.combo_source_amplitude.configure(state="normal")
            self.combo_source_offset.configure(state="normal")
            self.combo_source_phase.configure(state="disabled")
            self.combo_source_dutyCycle.configure(state="disabled")
            self.combo_source_symetry.configure(state="disabled")
            self.combo_source_riseTime.configure(state="disabled")
            self.combo_source_fallTime.configure(state="disabled")
            self.combo_source_pulseWidth.configure(state="disabled")
            self.combo_source_bandwidth.configure(state="normal")
        
        if self.combo_source_waveform.get() == "Arbitrary":
            self.label_source_frequency.configure(state="disabled")
            self.label_source_amplitude.configure(state="normal")
            self.label_source_offset.configure(state="normal")
            self.label_source_phase.configure(state="disabled")
            self.label_source_dutyCycle.configure(state="disabled")
            self.label_source_symetry.configure(state="disabled")
            self.label_source_riseTime.configure(state="disabled")
            self.label_source_fallTime.configure(state="disabled")
            self.label_source_pulseWidth.configure(state="disabled")
            self.label_source_bandwidth.configure(state="disabled")
            
            self.entry_source_frequency.configure(state="disabled")
            self.entry_source_amplitude.configure(state="normal")
            self.entry_source_offset.configure(state="normal")
            self.entry_source_phase.configure(state="disabled")
            self.entry_source_dutyCycle.configure(state="disabled")
            self.entry_source_Symetry.configure(state="disabled")
            self.entry_source_riseTime.configure(state="disabled")
            self.entry_source_fallTime.configure(state="disabled")
            self.entry_source_pulseWidth.configure(state="disabled")
            self.entry_source_bandwidth.configure(state="disabled")

            self.combo_source_frequency.configure(state="disabled")
            self.combo_source_amplitude.configure(state="normal")
            self.combo_source_offset.configure(state="normal")
            self.combo_source_phase.configure(state="disabled")
            self.combo_source_dutyCycle.configure(state="disabled")
            self.combo_source_symetry.configure(state="disabled")
            self.combo_source_riseTime.configure(state="disabled")
            self.combo_source_fallTime.configure(state="disabled")
            self.combo_source_pulseWidth.configure(state="disabled")
            self.combo_source_bandwidth.configure(state="disabled")
        
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

    def entry_source_frequency_callback(self, arg=None):
    #This method calls the controller to change the voltage
        voltage = self.doubleVar_source_frequency.get()        

    def entry_source_amplitude_callback(self, arg=None):
    #This method calls the controller to change the voltage
        current = self.doubleVar_source_amplitude.get()         

    def master_activate_callback(self):
    #This method call the controller to change output state 
        if self.controller.setMasterState() != -1:
            if (self.intVar_radioValueMaster.get() == 1) and (self.controller.instrument.address != ""):
                self.entry_source_amplitude_callback()
                self.entry_source_frequency_callback()

                self.intVar_radioValueMaster.set(2) 
                self.radio_masterStateON.select() 
                self.updateMonitoring()
            else:
                self.intVar_radioValueMaster.set(1)
                self.radio_masterStateOFF.select() 

    def updateMonitoring(self):
    #This method  updates the measurement content         
            None
            #self.label_source_dutyCycle.after(1000, self.updateMonitoring)