"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for WakeUpTL.

"""

from tkinter import Canvas, DoubleVar, Entry, Frame, IntVar, LabelFrame, Radiobutton, Scrollbar, filedialog
from tkinter import Label
from tkinter.constants import BOTTOM, TOP
from tkinter.ttk import Combobox
from tkinter import Button

import numpy as np
from math import sin, pi

from Graph import Graph

class WaveformTL():
    """Class containing a GUI for Parameters attributes

    """

    def __init__(self, frame, view, model=None):
    #Constructor for the Paramaters class

        self.frame = frame
        self.view = view
        self.model = model

        self.frame.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.initAttributes()
                
        self.initFrame()
        self.initButton()
        self.initVar()
        self.initEntries()

    def initAttributes(self):
    #This method instancitaes all the attributes
        self.waveform = [0]
        self.waveform_editor = [0]
        self.timeBase = [0]
        self.timeBase_editor = [0]
        self.stepDelay = 0.0094

        self.frameline_top = Frame(self.frame, bg=self.model.parameters_dict['backgroundColor'])
        self.frameline_edit = Frame(self.frameline_top, width=470, bg=self.model.parameters_dict['backgroundColor'])
        self.frameline_sine = Frame(self.frameline_edit, bg=self.model.parameters_dict['backgroundColor'])
        self.frameline_ramp = Frame(self.frameline_edit, bg=self.model.parameters_dict['backgroundColor'])
        self.frameline_pulse = Frame(self.frameline_edit, bg=self.model.parameters_dict['backgroundColor'])
        self.frameline_button = Frame(self.frameline_edit, bg=self.model.parameters_dict['backgroundColor'])

        self.frameline_bottom = Frame(self.frame, bg=self.model.parameters_dict['backgroundColor'])

        self.labelFrame_editor = LabelFrame(self.frameline_top, text="Waveform Editor", bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.labelFrame_list = LabelFrame(self.frameline_top, text="Waveform List", bg=self.model.parameters_dict['backgroundColorInstrument'])

        self.graph_editor = Graph(self.frameline_top, self.model)
        self.graph_list = Graph(self.frameline_bottom, self.model, size=(13,5))

        self.intVar_waveform = IntVar()
        self.doublevar_sine_amplitude = DoubleVar()
        self.doublevar_sine_frequency = DoubleVar()
        self.doublevar_sine_offset = DoubleVar()
        self.doublevar_ramp_start = DoubleVar()
        self.doublevar_ramp_stop = DoubleVar()
        self.doublevar_ramp_duration = DoubleVar()
        self.doublevar_pulse_amplitude = DoubleVar()
        self.doublevar_pulse_duration = DoubleVar()

        self.entry_sine_amplitude = Entry(self.frameline_sine, textvariable=self.doublevar_sine_amplitude, width=11)
        self.entry_sine_frequency = Entry(self.frameline_sine, textvariable=self.doublevar_sine_frequency, width=11)
        self.entry_sine_offset = Entry(self.frameline_sine, textvariable=self.doublevar_sine_offset, width=11)
        
        self.entry_ramp_start = Entry(self.frameline_ramp, textvariable=self.doublevar_ramp_start, width=11)
        self.entry_ramp_stop = Entry(self.frameline_ramp, textvariable=self.doublevar_ramp_stop, width=11)
        self.entry_ramp_duration = Entry(self.frameline_ramp, textvariable=self.doublevar_ramp_duration, width=11)
        
        self.entry_pulse_amplitude = Entry(self.frameline_pulse, textvariable=self.doublevar_pulse_amplitude, width=11)
        self.entry_pulse_duration = Entry(self.frameline_pulse, textvariable=self.doublevar_pulse_duration, width=11)
        
        self.radio_sine = Radiobutton(self.frameline_sine, variable=self.intVar_waveform, value=0, text="Half Sine (Amp, Freq, Offset) : ", bg=self.model.parameters_dict['backgroundColor'], command=self.radio_waveform_callback)
        self.radio_ramp = Radiobutton(self.frameline_ramp, variable=self.intVar_waveform, value=1, text="Ramp (Start, Stop, Duration)  : ", bg=self.model.parameters_dict['backgroundColor'], command=self.radio_waveform_callback)
        self.radio_pulse = Radiobutton(self.frameline_pulse, variable=self.intVar_waveform, value=2, text="Pulse (Amplitude, Duration)  :                           ", bg=self.model.parameters_dict['backgroundColor'], command=self.radio_waveform_callback)

        self.button_add = Button(self.frameline_button, text="Add to Waveform", command=self.button_add_callback)
        self.button_clear = Button(self.frameline_button, text="Clear Waveform", command=self.button_clear_callback)
        self.button_save = Button(self.frameline_button, text="Save Waveform", command=self.button_save_callback)
        self.button_open = Button(self.frameline_button, text="Open Waveform", command=self.button_open_callback)

    def initFrame(self):
    #This method pack every frame        
        self.frameline_top.pack()
        self.frameline_edit.pack(side='left')
        self.frameline_sine.pack()
        self.frameline_ramp.pack()
        self.frameline_pulse.pack()
        self.frameline_button.pack()

        self.frameline_bottom.pack()

        self.graph_editor.frame.pack(side='left')
        self.graph_list.frame.pack()

    def initButton(self):
    #This method pack every button
        self.radio_sine.pack(side='left', pady=2)
        self.radio_ramp.pack(side='left', pady=2)
        self.radio_pulse.pack(side='left', pady=2)

        self.button_add.pack(side='left', pady=8, padx=5, expand='yes')
        self.button_add_callback()
        
        self.button_clear.pack(side='left', pady=8, padx=5, expand='yes')
        self.button_save.pack(side='left', pady=8, padx=5, expand='yes')
        self.button_open.pack(side='left', pady=8, padx=5, expand='yes')

    def initEntries(self):
    #This method pack every entry
        self.entry_sine_amplitude.pack(side="left",padx=3)
        self.entry_sine_amplitude.bind("<KeyRelease>", self.update_graph_editor)
        self.entry_sine_frequency.pack(side="left",padx=3)
        self.entry_sine_frequency.bind("<KeyRelease>", self.update_graph_editor)
        self.entry_sine_offset.pack(side="left",padx=3)
        self.entry_sine_offset.bind("<KeyRelease>", self.update_graph_editor)
        
        self.entry_ramp_start.pack(side="left",padx=3)
        self.entry_ramp_start.bind("<KeyRelease>", self.update_graph_editor)
        self.entry_ramp_stop.pack(side="left",padx=3)
        self.entry_ramp_stop.bind("<KeyRelease>", self.update_graph_editor)
        self.entry_ramp_duration.pack(side="left",padx=3)
        self.entry_ramp_duration.bind("<KeyRelease>", self.update_graph_editor)
        
        self.entry_pulse_amplitude.pack(side="left",padx=3)
        self.entry_pulse_amplitude.bind("<KeyRelease>", self.update_graph_editor)
        self.entry_pulse_duration.pack(side="left",padx=3)
        self.entry_pulse_duration.bind("<KeyRelease>", self.update_graph_editor)

    def initVar(self):
    #This methods instanciates all the Var    
        self.doublevar_sine_amplitude.set(1)
        self.doublevar_sine_frequency.set(1)
        self.doublevar_sine_offset.set(0)
        self.doublevar_ramp_start.set(0)
        self.doublevar_ramp_stop.set(1)
        self.doublevar_ramp_duration.set(1)
        self.doublevar_pulse_amplitude.set(1)
        self.doublevar_pulse_duration.set(1)

        self.radio_waveform_callback()

    def update_graph_editor(self, args=[]):
    #This method updates the vie of editor graph
        self.graph_editor.clearGraph()
        timeBase = []
        waveform = []

        if self.intVar_waveform.get() == 0:
            amplitude = self.doublevar_sine_amplitude.get()
            offset = self.doublevar_sine_offset.get()
            frequency = self.doublevar_sine_frequency.get()
            duration = 1/frequency

            if self.timeBase[-1] == 0:
                time_start = 0
            else:
                time_start = self.timeBase[-1] + self.stepDelay

            time_step = int(duration / self.stepDelay)
            time_stop = time_start + duration

            timeBase = np.linspace(time_start, time_stop, time_step)
            x = np.linspace(0, duration, time_step)
            waveform = amplitude * np.sin(2 * pi * frequency * x) + offset
            self.timeBase_editor = timeBase[:int(time_step/2)]
            self.waveform_editor = waveform[:int(time_step/2)]

        elif self.intVar_waveform.get() == 1:
            duration = self.doublevar_ramp_duration.get()
            start = self.doublevar_ramp_start.get()
            stop = self.doublevar_ramp_stop.get()

            ramp = (stop-start) / duration

            if self.timeBase[-1] == 0:
                time_start = 0
            else:
                time_start = self.timeBase[-1] + self.stepDelay

            time_step = int(duration / self.stepDelay)
            time_stop = time_start + duration

            self.timeBase_editor = np.linspace(time_start, time_stop, time_step)
            self.waveform_editor = ramp * np.linspace(0, duration, time_step) + start

        elif self.intVar_waveform.get() == 2:
            duration = self.doublevar_pulse_duration.get()
            amplitude = self.doublevar_pulse_amplitude.get()

            if self.timeBase[-1] == 0:
                time_start = 0
            else:
                time_start = self.timeBase[-1] + self.stepDelay

            time_step = int(duration / self.stepDelay)
            time_stop = time_start + duration

            self.timeBase_editor = np.linspace(time_start, time_stop, time_step)
            self.waveform_editor = amplitude * np.ones(time_step)

        self.graph_editor.addStepGraph(x=self.timeBase_editor, y=self.waveform_editor, xlabel='Time', ylabel='Amplitude', title='Waveform under edition')

    def radio_waveform_callback(self, args=[]):
    #This methods updates th view according to the radio_waveform state
        for child in self.frameline_sine.winfo_children():
            child.configure(state="disabled")
        for child in self.frameline_ramp.winfo_children():
            child.configure(state="disabled")
        for child in self.frameline_pulse.winfo_children():
            child.configure(state="disabled")
                
        self.radio_sine.configure(fg="grey24")
        self.radio_ramp.configure(fg="grey24")
        self.radio_pulse.configure(fg="grey24")

        if self.intVar_waveform.get() == 0:
            for child in self.frameline_sine.winfo_children():
                child.configure(state="normal")
            self.radio_sine.configure(fg="black")

        elif self.intVar_waveform.get() == 1:
            for child in self.frameline_ramp.winfo_children():
                child.configure(state="normal")
            self.radio_ramp.configure(fg="black")

        elif self.intVar_waveform.get() == 2:
            for child in self.frameline_pulse.winfo_children():
                child.configure(state="normal")
            self.radio_pulse.configure(fg="black")

        self.radio_sine.configure(state='normal')
        self.radio_ramp.configure(state='normal')
        self.radio_pulse.configure(state='normal')

        self.update_graph_editor()

    def button_add_callback(self):
    #this method is called when the button add is clicked.
        try:
            self.update_graph_editor()
        except:
            None
        self.graph_list.clearGraph()

        self.waveform.extend(self.waveform_editor)
        self.timeBase.extend(self.timeBase_editor)
        self.graph_list.addStepGraph(x=self.timeBase, y=self.waveform, xlabel='Time', ylabel='Amplitude', title="Full Waveform")

        try:
            self.update_graph_editor()
        except:
            None

    def button_clear_callback(self):
    #this method is called when the button clear is clicked.

        self.waveform = [0]
        self.waveform_editor = [0]
        self.timeBase = [0]
        self.timeBase_editor = [0]

        self.graph_list.clearGraph()
        self.graph_list.addStepGraph(x=self.timeBase, y=self.waveform, xlabel='Time', ylabel='Amplitude', title="Full Waveform")

        try:
            self.update_graph_editor()
        except:
            None

    def button_save_callback(self, args=None):
    #This method is called when the button save is clicked        
        self.path = filedialog.asksaveasfilename(title = "Select file", filetypes = (("all files","*.*"), ("Waveform files","*.waveform")))
        self.model.saveWaveform(path=self.path, waveform=self.waveform, timeBase=self.timeBase)

    def button_open_callback(self, args=None):
    #This method is called when the button open is clicked       
        self.path = filedialog.askopenfilename(title = "Select file", filetypes = (("all files","*.*"), ("Waveform files","*.waveform")))
        
        if self.path != "":                
            liste = self.model.openConfiguration(path=self.path)
            self.button_clear_callback()

            self.timeBase = liste[0]
            self.waveform = liste[1]

        self.graph_list.clearGraph()
        self.graph_list.addStepGraph(x=self.timeBase, y=self.waveform, xlabel='Time', ylabel='Amplitude', title="Full Waveform")

        try:
            self.update_graph_editor()
        except:
            None
