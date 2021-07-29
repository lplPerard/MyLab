"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for CommandLine

"""

from tkinter.ttk import Button, Combobox

from PIL import Image, ImageTk
from Instrument import Instrument
from tkinter import Canvas, DoubleVar, Entry, Frame, LabelFrame, Scrollbar, StringVar
from tkinter import Label
from tkinter import Toplevel
from tkinter import Text
from tkinter import BOTH
from tkinter import YES
from tkinter import END
from tkinter.constants import NONE, TOP


class CommandLine():
    """Class containing the GUI for a Command Lines in Scripts.

    """

    def __init__(self,  frame=None,  root=None, controller=None, script=None, terminal=None, model=None, number=999):
    #Constructor for the Sequence_view superclass
        
        self.frame = frame
        self.term_text = terminal
        self.model = model
        self.controller = controller
        self.number=number
        self.root=root
        self.script = script

        self.initAttributes()
        self.initLabel()
        self.initCombo()
        
    def initAttributes(self):
    #this method list all the attributes
        self.commandType = ""
        self.variablesList = ["A", "B", "C", "D", "E", "F", "G"]

        self.line = Frame(self.frame, bg=self.model.parameters_dict['backgroundColorCommandLine'])
        self.line.pack(fill="x", expand="no", side="top", anchor='nw', pady=2)

        self.deleteImg = Image.open("delete.png")
        self.deleteImg = self.deleteImg.resize((10, 10), Image.ANTIALIAS)
        self.deleteImg = ImageTk.PhotoImage(self.deleteImg)

        self.label_number = Label(self.line, text=str(self.number), bg=self.model.parameters_dict['backgroundColorCommandLine'])

        self.combo_choice1 = Combobox(self.line, state="readonly", width=25, value=['Select', 'WAIT', 'FOR', 'END'], postcommand=self.combo_choice1_update)
        self.combo_instrCommand = Combobox(self.line, state="readonly", width=25)

        self.stringVar_attribute1 = StringVar()
        self.stringVar_attribute2 = StringVar()
        self.stringVar_attribute3 = StringVar()
        self.stringVar_defaultText1 = StringVar()
        self.stringVar_defaultText2 = StringVar()
        self.stringVar_defaultText3 = StringVar()

        self.combo_attribute1 = Combobox(self.line, state="readonly", width=25, value=['Select'], postcommand=self.combo_choice1_update)
        self.combo_attribute2 = Combobox(self.line, state="readonly", width=25, value=['Select'], postcommand=self.combo_choice1_update)
        
        self.entry_attribute1 = Entry(self.line, textvariable=self.stringVar_defaultText1, fg="gainsboro")
        self.entry_attribute1.bind('<Button-1>', self.entry_attribute1_callback)
        self.entry_attribute2 = Entry(self.line, textvariable=self.stringVar_defaultText2, fg="gainsboro")
        self.entry_attribute2.bind('<Button-1>', self.entry_attribute2_callback)
        self.entry_attribute3 = Entry(self.line, textvariable=self.stringVar_defaultText3, fg="gainsboro")
        self.entry_attribute3.bind('<Button-1>', self.entry_attribute3_callback)

        self.label_attribute1 = Label(self.line)
        self.label_attribute2 = Label(self.line)

        self.button_deleteLine = Button(self.line, image=self.deleteImg, command=self.button_deleteLine_callback)
        self.button_deleteLine.pack(expand="no", side="right", anchor='ne', padx=2)

    def initLabel(self):
    #This method instanciates all labels
        self.label_number.pack(expand="no", side="left", anchor='nw', padx=2)

    def initCombo(self):
    #this method instanciates all Combobox
        self.combo_choice1.bind("<<ComboboxSelected>>", self.combo_choice1_callback)
        self.combo_choice1.configure(background='white')
        self.combo_choice1.current(0)
        self.combo_choice1.pack(expand="no", side="left", anchor='nw', padx=2)
        
        self.combo_instrCommand.bind("<<ComboboxSelected>>", self.combo_instrCommand_callback)
        self.combo_instrCommand.configure(background='white')

    def entry_attribute1_callback(self, args=None):
        self.entry_attribute1.config(textvariable=self.stringVar_attribute1, fg="black")

    def entry_attribute2_callback(self, args=None):
        self.entry_attribute2.config(textvariable=self.stringVar_attribute2, fg="black")

    def entry_attribute3_callback(self, args=None):
        self.entry_attribute3.config(textvariable=self.stringVar_attribute2, fg="black")

    def renumberLine(self, number):
    #This method changes the line number
        self.label_number.config(text=str(number))

    def button_deleteLine_callback(self, args=None):
    #This method is called when clicking on the quit button. It deletes the line.
        self.root.script.deleteCommandLine(self)
        self.line.destroy()

    def combo_choice1_update(self):
    #This method update the line view according to the selected option
        liste = ['WAIT', 'FOR', 'END']
        for item in self.root.getInstrList():
            liste.insert(0, item.name)

        self.combo_choice1.configure(value=liste)

    def combo_choice1_callback(self, args=None):
    #This method update the line view according to the selected option
        self.combo_instrCommand.pack_forget()  
        self.combo_instrCommand.configure(value=[])
        self.cleanAttributes()

        if self.combo_choice1.get() == 'WAIT':
            self.commandType = "WAIT"
            self.combo_instrCommand_callback()

        elif self.combo_choice1.get() == 'FOR':
            self.commandType = "FOR"
            self.combo_instrCommand.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_instrCommand.config(value=self.variablesList)

        elif self.combo_choice1.get() == 'END':
            self.commandType = "END"
            self.combo_instrCommand.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_instrCommand.config(value=self.variablesList)
        
        else:
            self.combo_instrCommand.pack(expand="no", side="left", anchor='nw', padx=2)
            for item in self.root.getInstrList():
                if item.name == self.combo_choice1.get():
                    self.combo_instrCommand.config(value=item.commandList)
                    self.commandType = item.type
                    break

    def combo_instrCommand_callback(self, args=None):
    #This methods calls the appropriate attribute generator according to instrument type   
        self.cleanAttributes()
        if self.commandType == "WAIT":            
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.stringVar_defaultText1.set("delay (s)")
            
        elif self.commandType == "FOR":         
            self.generateForAttributes()   

        elif self.commandType == "Power Supply":
            self.generatePowerSupplyAttributes()
        
        elif self.commandType  == "Multimeter":
            self.generateMultimeterAttributes()

        elif self.commandType  == "Climatic Chamber":
            self.generateClimaticChamberAttributes()

    def cleanAttributes(self):
    #This method unpacks all attributes
        self.entry_attribute1.pack_forget()
        self.stringVar_defaultText1.set("")
        self.entry_attribute2.pack_forget()
        self.stringVar_defaultText2.set("")
        self.entry_attribute3.pack_forget()
        self.stringVar_defaultText3.set("")

        self.combo_attribute1.pack_forget()
        self.combo_attribute1.configure(value=[])
        self.combo_attribute2.pack_forget()
        self.combo_attribute2.configure(value=[])

    def generateForAttributes(self):
    #This method generates the attributes for FOR command
        self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
        self.stringVar_defaultText1.set("from (int)")
        self.entry_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
        self.stringVar_defaultText2.set("to (int)")
        self.entry_attribute3.pack(expand="no", side="left", anchor='nw', padx=2)
        self.stringVar_defaultText3.set("step")

    def generateClimaticChamberAttributes(self):
    #This method generates the attributes for Climatic Chamber commands
        if self.combo_instrCommand.get() == "setTemperature":
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.stringVar_defaultText1.set("Temperature")

    def generatePowerSupplyAttributes(self):
    #This method generates the attributes for Power Supply commands
        if self.combo_instrCommand.get() == "setVoltageSource":
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.stringVar_defaultText1.set("Voltage")
        if self.combo_instrCommand.get() == "setCurrentSource":
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.stringVar_defaultText1.set("Current")
        if self.combo_instrCommand.get() == "setChannelState":
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["1","2"])
            self.combo_attribute1.current(0)
        if self.combo_instrCommand.get() == "setMasterState":
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["OFF","ON"])
            self.combo_attribute1.current(0)

    def generateMultimeterAttributes(self):
    #This method generates the attributes for Power Supply commands
        if self.combo_instrCommand.get() == "setDCV":
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["Auto Range", "1V", "100mV", "1000V", "100V", "10V"])
            self.combo_attribute1.current(0)
        if self.combo_instrCommand.get() == "setACV":
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["Auto Range", "1V", "100mV", "750V", "100V", "10V"])
            self.combo_attribute1.current(0)
        if self.combo_instrCommand.get() == "setDCI":
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["Auto Range", "1mA", "100uA", "400mA", "100mA", "10mA"])
            self.combo_attribute1.current(0)
            self.combo_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute2.config(value=["mA", "10A"])
            self.combo_attribute2.current(0)
        if self.combo_instrCommand.get() == "setACI":
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["Auto Range", "10mA", "400mA", "100mA"])
            self.combo_attribute1.current(0)
            self.combo_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute2.config(value=["mA", "10A"])
            self.combo_attribute2.current(0)
        if self.combo_instrCommand.get() == "set2WR":
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["Auto Range", "1kΩ", "100Ω", "10kΩ", "100kΩ", "1MΩ", "10MΩ", "100MΩ"])
            self.combo_attribute1.current(0)
        if self.combo_instrCommand.get() == "set4WR":
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["Auto Range", "1kΩ", "100Ω", "10kΩ", "100kΩ", "1MΩ", "10MΩ", "100MΩ"])
            self.combo_attribute1.current(0)