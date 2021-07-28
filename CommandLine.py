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
        self.stringVar_defaultText1 = StringVar()
        self.stringVar_defaultText2 = StringVar()

        self.combo_attribute1 = Combobox(self.line, state="readonly", width=25, value=['Select'], postcommand=self.combo_choice1_update)
        self.combo_attribute2 = Combobox(self.line, state="readonly", width=25, value=['Select'], postcommand=self.combo_choice1_update)
        
        self.entry_attribute1 = Entry(self.line, textvariable=self.stringVar_defaultText1, fg="gainsboro")
        self.entry_attribute1.bind('<Button-1>', self.entry_attribute1_callback)
        self.entry_attribute2 = Entry(self.line, textvariable=self.stringVar_defaultText2, fg="gainsboro")
        self.entry_attribute2.bind('<Button-1>', self.entry_attribute2_callback)

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


    def combo_choice1_update(self):
    #This method update the line view according to the selected option
        liste = ['WAIT', 'FOR', 'END']
        for item in self.root.getInstrList():
            liste.insert(0, item.name)

        self.combo_choice1.configure(value=liste)

    def combo_choice1_callback(self, args=None):
    #This method update the line view according to the selected option
        self.combo_instrCommand.pack_forget()

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

    def button_deleteLine_callback(self, args=None):
    #This method is called when clicking on the quit button. It deletes the line.
        self.root.script.deleteCommandLine(self)
        self.line.destroy()

    def combo_instrCommand_callback(self, args=None):
    #This methods calls the appropriate attribute generator according to instrument type   
        if self.commandType == "WAIT":            
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.stringVar_defaultText1.set("delay (s)")
            
        elif self.commandType == "FOR":         
            self.generateForAttributes()   

        elif self.commandType == "Power Supply":
            None
        
        elif self.commandType  == "Multimeter":
            None

        elif self.commandType  == "Climatic Chamber":
            self.generateClimaticChamberAttributes()

    def generateForAttributes(self):
        self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
        self.stringVar_defaultText1.set("from (int)")
        self.entry_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
        self.stringVar_defaultText2.set("to (int)")

    def generateClimaticChamberAttributes(self):
        if self.combo_instrCommand.get() == "setTemperature":
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.stringVar_defaultText1.set("Temperature")