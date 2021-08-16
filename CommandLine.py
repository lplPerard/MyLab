"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for CommandLine

"""

from Command import Command
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

    def __init__(self,  frame=None,  root=None, controller=None, script=None, terminal=None, model=None, number=None, command=None):
    #Constructor for the Sequence_view superclass
        
        self.frame = frame
        self.term_text = terminal
        self.model = model
        self.controller = controller
        self.number=number
        self.root=root
        self.script = script

        if command == None:
            self.command = Command()
        else:
            self.command=command

        self.initAttributes()
        self.initLabel()
        self.initCombo()
        
    def initAttributes(self):
    #this method list all the attributes
        self.commandType = ""
        self.variablesList = ["Temperature", "Voltage", "Current", "Frequency", "A", "B", "C", "D", "E", "F", "G"]
        self.operatorsList = ["==", "!=", ">", ">=", "<=", "<"]

        self.line = Frame(self.frame, bg=self.model.parameters_dict['backgroundColorCommandLine'])
        self.line.pack(fill="x", expand="yes", side="top", anchor='nw', pady=2)

        self.deleteImg = Image.open("delete.png")
        self.deleteImg = self.deleteImg.resize((10, 12), Image.ANTIALIAS)
        self.deleteImg = ImageTk.PhotoImage(self.deleteImg)

        self.emptyImg = Image.open("empty.png")
        self.emptyImg = self.emptyImg.resize((10, 10), Image.ANTIALIAS)
        self.emptyImg = ImageTk.PhotoImage(self.emptyImg)

        self.breakpointImg = Image.open("breakpoint.png")
        self.breakpointImg = self.breakpointImg.resize((10, 10), Image.ANTIALIAS)
        self.breakpointImg = ImageTk.PhotoImage(self.breakpointImg)

        self.label_number = Label(self.line, text=str(self.number), bg=self.model.parameters_dict['backgroundColorCommandLine'])
        self.label_breakpoint = Label(self.line, image=self.emptyImg, bg=self.model.parameters_dict['backgroundColorCommandLine'])
        self.label_breakpoint.bind('<Button-1>', self.label_breakpoint_onClick_callback)

        self.combo_choice1 = Combobox(self.line, state="readonly", width=25, value=['Select', 'WAIT', 'FOR', 'END', 'STORE', 'IF', 'ENDIF'], postcommand=self.combo_choice1_update)
        self.combo_instrCommand = Combobox(self.line, state="readonly", width=25)

        self.stringVar_attribute1 = StringVar()
        self.stringVar_attribute1.set(self.command.entry_attribute1)
        self.stringVar_attribute2 = StringVar()
        self.stringVar_attribute2.set(self.command.entry_attribute2)
        self.stringVar_attribute3 = StringVar()
        self.stringVar_attribute3.set(self.command.entry_attribute3)
        self.stringVar_attribute4 = StringVar()
        self.stringVar_attribute4.set(self.command.entry_attribute4)
        self.stringVar_attribute5 = StringVar()
        self.stringVar_attribute5.set(self.command.entry_attribute5)
        self.stringVar_attribute6 = StringVar()
        self.stringVar_attribute6.set(self.command.entry_attribute6)
        self.stringVar_attribute7 = StringVar()
        self.stringVar_attribute7.set(self.command.entry_attribute7)
        self.stringVar_defaultText1 = StringVar()
        self.stringVar_defaultText2 = StringVar()
        self.stringVar_defaultText3 = StringVar()
        self.stringVar_defaultText4 = StringVar()
        self.stringVar_defaultText5 = StringVar()
        self.stringVar_defaultText6 = StringVar()
        self.stringVar_defaultText7 = StringVar()

        self.combo_attribute1 = Combobox(self.line, state="readonly", width=17, value=['Select'])
        self.combo_attribute2 = Combobox(self.line, state="readonly", width=17, value=['Select'])
        self.combo_attribute3 = Combobox(self.line, state="readonly", width=17, value=['Select'])
        self.combo_attribute4 = Combobox(self.line, state="readonly", width=17, value=['Select'])
        self.combo_attribute5 = Combobox(self.line, state="readonly", width=17, value=['Select'])
        self.combo_attribute6 = Combobox(self.line, state="readonly", width=17, value=['Select'])
        self.combo_attribute7 = Combobox(self.line, state="readonly", width=17, value=['Select'])
        
        self.entry_attribute1 = Entry(self.line, textvariable=self.stringVar_defaultText1, fg="gainsboro")
        self.entry_attribute1.bind('<KeyRelease>', self.entry_attribute1_onKey_callback)
        self.entry_attribute1.bind('<Button-1>', self.entry_attribute1_onClick_callback)
        self.entry_attribute2 = Entry(self.line, textvariable=self.stringVar_defaultText2, fg="gainsboro")
        self.entry_attribute2.bind('<KeyRelease>', self.entry_attribute2_onKey_callback)
        self.entry_attribute2.bind('<Button-1>', self.entry_attribute2_onClick_callback)
        self.entry_attribute3 = Entry(self.line, textvariable=self.stringVar_defaultText3, fg="gainsboro")
        self.entry_attribute3.bind('<KeyRelease>', self.entry_attribute3_onKey_callback)
        self.entry_attribute3.bind('<Button-1>', self.entry_attribute3_onClick_callback)
        self.entry_attribute4 = Entry(self.line, textvariable=self.stringVar_defaultText4, fg="gainsboro")
        self.entry_attribute4.bind('<KeyRelease>', self.entry_attribute4_onKey_callback)
        self.entry_attribute4.bind('<Button-1>', self.entry_attribute4_onClick_callback)
        self.entry_attribute5 = Entry(self.line, textvariable=self.stringVar_defaultText5, fg="gainsboro")
        self.entry_attribute5.bind('<KeyRelease>', self.entry_attribute5_onKey_callback)
        self.entry_attribute5.bind('<Button-1>', self.entry_attribute5_onClick_callback)
        self.entry_attribute6 = Entry(self.line, textvariable=self.stringVar_defaultText6, fg="gainsboro")
        self.entry_attribute6.bind('<KeyRelease>', self.entry_attribute6_onKey_callback)
        self.entry_attribute6.bind('<Button-1>', self.entry_attribute6_onClick_callback)
        self.entry_attribute7 = Entry(self.line, textvariable=self.stringVar_defaultText7, fg="gainsboro")
        self.entry_attribute7.bind('<KeyRelease>', self.entry_attribute7_onKey_callback)
        self.entry_attribute7.bind('<Button-1>', self.entry_attribute7_onClick_callback)

        self.label_attribute1 = Label(self.line)
        self.label_attribute2 = Label(self.line)

        self.button_deleteLine = Button(self.line, image=self.deleteImg, command=self.button_deleteLine_callback)
        self.button_deleteLine.pack(expand="no", side="left", anchor='ne', padx=2)

    def initLabel(self):
    #This method instanciates all labels
        self.label_breakpoint.pack(expand="no", side="left", anchor='w', padx=2)
        self.label_number.pack(expand="no", side="left", anchor='nw', padx=2)

    def initCombo(self):
    #this method instanciates all Combobox
        self.combo_choice1.bind("<<ComboboxSelected>>", self.combo_choice1_callback)
        self.combo_choice1.configure(background='white')
        self.combo_choice1.current(0)
        self.combo_choice1.pack(expand="no", side="left", anchor='nw', padx=2)
        
        self.combo_instrCommand.bind("<<ComboboxSelected>>", self.combo_instrCommand_callback)
        self.combo_instrCommand.configure(background='white')
        
        self.combo_attribute1.bind("<<ComboboxSelected>>", self.combo_attribute1_callback)
        self.combo_attribute1.configure(background='white')
        
        self.combo_attribute2.bind("<<ComboboxSelected>>", self.combo_attribute2_callback)
        self.combo_attribute2.configure(background='white')
        
        self.combo_attribute3.bind("<<ComboboxSelected>>", self.combo_attribute3_callback)
        self.combo_attribute3.configure(background='white')
        
        self.combo_attribute4.bind("<<ComboboxSelected>>", self.combo_attribute4_callback)
        self.combo_attribute4.configure(background='white')
        
        self.combo_attribute5.bind("<<ComboboxSelected>>", self.combo_attribute5_callback)
        self.combo_attribute5.configure(background='white')
        
        self.combo_attribute6.bind("<<ComboboxSelected>>", self.combo_attribute6_callback)
        self.combo_attribute6.configure(background='white')
        
        self.combo_attribute7.bind("<<ComboboxSelected>>", self.combo_attribute7_callback)
        self.combo_attribute7.configure(background='white')
   
    def combo_attribute1_callback(self, args=None):
    #Callback function for combo attribute 1
        self.command.combo_attribute1 = self.combo_attribute1.get()    

    def combo_attribute2_callback(self, args=None):
    #Callback function for combo attribute 2
        self.command.combo_attribute2 = self.combo_attribute2.get()  

    def combo_attribute3_callback(self, args=None):
    #Callback function for combo attribute 3
        self.command.combo_attribute3 = self.combo_attribute3.get()  

    def combo_attribute4_callback(self, args=None):
    #Callback function for combo attribute 4
        self.command.combo_attribute4 = self.combo_attribute4.get()  

    def combo_attribute5_callback(self, args=None):
    #Callback function for combo attribute 5
        self.command.combo_attribute5 = self.combo_attribute5.get()  

    def combo_attribute6_callback(self, args=None):
    #Callback function for combo attribute 6
        self.command.combo_attribute6 = self.combo_attribute6.get()  

    def combo_attribute7_callback(self, args=None):
    #Callback function for combo attribute 7
        self.command.combo_attribute7 = self.combo_attribute7.get()  

    def entry_attribute1_onClick_callback(self, args=None):
        self.entry_attribute1.config(textvariable=self.stringVar_attribute1, fg="black")

    def entry_attribute1_onKey_callback(self, args=None):
        self.command.entry_attribute1 = self.stringVar_attribute1.get()

    def entry_attribute2_onClick_callback(self, args=None):
        self.entry_attribute2.config(textvariable=self.stringVar_attribute2, fg="black")

    def entry_attribute2_onKey_callback(self, args=None):
        self.command.entry_attribute2 = self.stringVar_attribute2.get()

    def entry_attribute3_onClick_callback(self, args=None):
        self.entry_attribute3.config(textvariable=self.stringVar_attribute3, fg="black")
        
    def entry_attribute3_onKey_callback(self, args=None):
        self.command.entry_attribute3 = self.stringVar_attribute3.get()

    def entry_attribute4_onClick_callback(self, args=None):
        self.entry_attribute4.config(textvariable=self.stringVar_attribute4, fg="black")
        
    def entry_attribute4_onKey_callback(self, args=None):
        self.command.entry_attribute4 = self.stringVar_attribute4.get()

    def entry_attribute5_onClick_callback(self, args=None):
        self.entry_attribute5.config(textvariable=self.stringVar_attribute5, fg="black")
        
    def entry_attribute5_onKey_callback(self, args=None):
        self.command.entry_attribute5 = self.stringVar_attribute5.get()

    def entry_attribute6_onClick_callback(self, args=None):
        self.entry_attribute6.config(textvariable=self.stringVar_attribute1, fg="black")
        
    def entry_attribute6_onKey_callback(self, args=None):
        self.command.entry_attribute3 = self.stringVar_attribute3.get()

    def entry_attribute7_onClick_callback(self, args=None):
        self.entry_attribute7.config(textvariable=self.stringVar_attribute7, fg="black")
        
    def entry_attribute7_onKey_callback(self, args=None):
        self.command.entry_attribute7 = self.stringVar_attribute7.get()

    def label_breakpoint_onClick_callback(self, args=None):
    #Ths method adds a breakpoint to the command line
        if (self.command.breakpoint == 0) and (self.combo_choice1.get() not in ['FOR', 'END', 'ENDIF']):
            self.label_breakpoint.config(image=self.breakpointImg)    
            self.command.breakpoint = 1     

        else :
            self.label_breakpoint.config(image=self.emptyImg) 
            self.command.breakpoint = 0   

    def updateLine(self, args=None):
    #this method is called to load saved data
        if self.command.combo_choice1 != "":
            self.combo_choice1.set(self.command.combo_choice1)
            self.combo_choice1_callback(load=True)

            self.combo_instrCommand.set(self.command.combo_instrCommand)
            self.entry_attribute1.config(textvariable=self.stringVar_attribute1, fg='black')
            self.entry_attribute2.config(textvariable=self.stringVar_attribute2, fg='black')
            self.entry_attribute3.config(textvariable=self.stringVar_attribute3, fg='black')
            self.entry_attribute4.config(textvariable=self.stringVar_attribute4, fg='black')
            self.entry_attribute5.config(textvariable=self.stringVar_attribute5, fg='black')
            self.entry_attribute6.config(textvariable=self.stringVar_attribute6, fg='black')
            self.entry_attribute7.config(textvariable=self.stringVar_attribute7, fg='black')

            if self.command.combo_instrCommand != "":
                self.combo_instrCommand_callback(load=True)

    def renumberLine(self, number):
    #This method changes the line number
        self.label_number.config(text=str(number))

    def button_deleteLine_callback(self, args=None):
    #This method is called when clicking on the quit button. It deletes the line.
        self.root.script.deleteCommandLine(self)
        self.line.destroy()

    def combo_choice1_update(self):
    #This method update the line view according to the selected option
        liste = ['WAIT', 'FOR', 'END', 'STORE', 'IF', 'ENDIF']
        for item in self.root.getInstrList():
            liste.insert(0, item.name)

        self.combo_choice1.configure(value=liste)

    def combo_choice1_callback(self, args=None, load=False):
    #This method update the line view according to the selected option
        self.combo_instrCommand.pack_forget()  
        if load == False:
            self.combo_instrCommand.configure(value=[])
            self.cleanAttributes()
            self.command.combo_choice1 = self.combo_choice1.get()

        if self.combo_choice1.get() == 'WAIT':
            self.commandType = "WAIT"
            self.combo_instrCommand_callback(load=load)

        elif self.combo_choice1.get() == 'FOR':
            self.commandType = "FOR"
            self.combo_instrCommand.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_instrCommand.config(value=self.variablesList)

        elif self.combo_choice1.get() == 'END':
            self.commandType = "END"

        elif self.combo_choice1.get() == 'STORE':
            self.commandType = "STORE"      

            liste=[]
            for item in self.root.getInstrList():
                liste.insert(0, item.name)

            self.combo_instrCommand.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_instrCommand.config(value=liste)

        elif self.combo_choice1.get() == 'IF':
            self.commandType = "IF"
            self.combo_instrCommand_callback(load=load)

        elif self.combo_choice1.get() == 'ENDIF':
            self.commandType = "ENDIF"
        
        else:
            self.combo_instrCommand.pack(expand="no", side="left", anchor='nw', padx=2)
            for item in self.root.getInstrList():
                if item.name == self.combo_choice1.get():
                    self.combo_instrCommand.config(value=item.commandList)
                    self.commandType = item.type
                    break

    def combo_instrCommand_callback(self, args=None, load=False):
    #This methods calls the appropriate attribute generator according to instrument type  
        if load == False:
            self.cleanAttributes()

        if self.commandType == "WAIT":           
            self.generateWaitAttributes()         
            
        elif self.commandType == "FOR":         
            self.generateForAttributes()   

        elif self.commandType == "STORE":         
            self.generateStoreAttributes()  
            
        elif self.commandType == "IF":         
            self.generateIfAttributes()  

        elif self.commandType == "Power Supply":
            self.generatePowerSupplyAttributes()
        
        elif self.commandType  == "Multimeter":
            self.generateMultimeterAttributes()

        elif self.commandType  == "Climatic Chamber":
            self.generateClimaticChamberAttributes()

        elif self.commandType  == "Waveform Generator":
            self.generateWaveformGeneratorAttributes()

    def cleanAttributes(self):
    #This method unpacks all attributes
        self.entry_attribute1.config(textvariable=self.stringVar_defaultText1)
        self.entry_attribute1.pack_forget()
        self.stringVar_defaultText1.set("")
        self.entry_attribute2.config(textvariable=self.stringVar_defaultText2)
        self.entry_attribute2.pack_forget()
        self.stringVar_defaultText2.set("")
        self.entry_attribute3.config(textvariable=self.stringVar_defaultText3)
        self.entry_attribute3.pack_forget()
        self.stringVar_defaultText3.set("")
        self.entry_attribute4.config(textvariable=self.stringVar_defaultText4)
        self.entry_attribute4.pack_forget()
        self.stringVar_defaultText4.set("")
        self.entry_attribute5.config(textvariable=self.stringVar_defaultText5)
        self.entry_attribute5.pack_forget()
        self.stringVar_defaultText5.set("")
        self.entry_attribute6.config(textvariable=self.stringVar_defaultText6)
        self.entry_attribute6.pack_forget()
        self.stringVar_defaultText6.set("")
        self.entry_attribute7.config(textvariable=self.stringVar_defaultText7)
        self.entry_attribute7.pack_forget()
        self.stringVar_defaultText7.set("")

        self.combo_attribute1.pack_forget()
        self.combo_attribute1.configure(value=[])
        self.combo_attribute2.pack_forget()
        self.combo_attribute2.configure(value=[])
        self.combo_attribute3.pack_forget()
        self.combo_attribute3.configure(value=[])
        self.combo_attribute4.pack_forget()
        self.combo_attribute4.configure(value=[])
        self.combo_attribute5.pack_forget()
        self.combo_attribute5.configure(value=[])
        self.combo_attribute6.pack_forget()
        self.combo_attribute6.configure(value=[])
        self.combo_attribute7.pack_forget()
        self.combo_attribute7.configure(value=[])

    def generateForAttributes(self):
    #This method generates the attributes for FOR command
        self.command.combo_instrCommand = self.combo_instrCommand.get()

        self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
        self.stringVar_defaultText1.set("initial value")
        self.entry_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
        self.stringVar_defaultText2.set("step")
        self.entry_attribute3.pack(expand="no", side="left", anchor='nw', padx=2)
        self.stringVar_defaultText3.set("step number")

    def generateStoreAttributes(self):
    #This method generates the attributes for STORE command
        self.command.combo_instrCommand = self.combo_instrCommand.get()

        self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
        self.combo_attribute1.config(value=self.variablesList)

    def generateIfAttributes(self):
    #This method generates the attributes for IF command
        self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
        self.stringVar_defaultText1.set("Variable 1")

        self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
        self.combo_attribute1.config(value=self.operatorsList)

        self.entry_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
        self.stringVar_defaultText2.set("Variable 2")
        
    def generateWaitAttributes(self):
    #This method generates the attributes for END command
        self.stringVar_defaultText1.set("delay (s)")
        self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
        
    def generateClimaticChamberAttributes(self):
    #This method generates the attributes for Climatic Chamber commands
        self.command.combo_instrCommand = self.combo_instrCommand.get()

        if self.combo_instrCommand.get() == "setTemperature":
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.stringVar_defaultText1.set("Temperature")

    def generatePowerSupplyAttributes(self):
    #This method generates the attributes for Power Supply commands
        self.command.combo_instrCommand = self.combo_instrCommand.get()

        if self.combo_instrCommand.get() == "setVoltageSource":
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.stringVar_defaultText1.set("Voltage")
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["1","2"])
            self.combo_attribute1.current(0)

        if self.combo_instrCommand.get() == "setCurrentSource":
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.stringVar_defaultText1.set("Current")
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["1","2"])
            self.combo_attribute1.current(0)

        if self.combo_instrCommand.get() == "setChannelState":
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["1","2"])
            self.combo_attribute1.current(0)

        if self.combo_instrCommand.get() == "MeasureVoltage":
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["1","2"])
            self.combo_attribute1.current(0)

        if self.combo_instrCommand.get() == "setMasterState":
            None

    def generateMultimeterAttributes(self):
    #This method generates the attributes for Power Supply commands
        self.command.combo_instrCommand = self.combo_instrCommand.get()

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

    def generateWaveformGeneratorAttributes(self):
    #This method generates the attributes for Waveform Generator commands
        self.command.combo_instrCommand = self.combo_instrCommand.get()

        if self.combo_instrCommand.get() == "applySinus":
            self.stringVar_defaultText1.set("Frequency")
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["HZ", "KHZ", "MHZ"])
            self.combo_attribute1.current(0)

            self.stringVar_defaultText2.set("Amplitude")
            self.entry_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute2.config(value=["VPP", "VRMS", "DBM"])
            self.combo_attribute2.current(0)

            self.stringVar_defaultText3.set("Offset")
            self.entry_attribute3.pack(expand="no", side="left", anchor='nw', padx=2)

            self.stringVar_defaultText4.set("Phase (deg)")
            self.entry_attribute4.pack(expand="no", side="left", anchor='nw', padx=2)

        if self.combo_instrCommand.get() == "applySquare":
            self.stringVar_defaultText1.set("Frequency")
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["HZ", "KHZ", "MHZ"])
            self.combo_attribute1.current(0)

            self.stringVar_defaultText2.set("Amplitude")
            self.entry_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute2.config(value=["VPP", "VRMS", "DBM"])
            self.combo_attribute2.current(0)

            self.stringVar_defaultText3.set("Offset")
            self.entry_attribute3.pack(expand="no", side="left", anchor='nw', padx=2)

            self.stringVar_defaultText4.set("Phase (deg)")
            self.entry_attribute4.pack(expand="no", side="left", anchor='nw', padx=2)

            self.stringVar_defaultText5.set("Duty Cycle (%)")
            self.entry_attribute5.pack(expand="no", side="left", anchor='nw', padx=2)

        if self.combo_instrCommand.get() == "applyRamp":
            self.stringVar_defaultText1.set("Frequency")
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["HZ", "KHZ", "MHZ"])
            self.combo_attribute1.current(0)

            self.stringVar_defaultText2.set("Amplitude")
            self.entry_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute2.config(value=["VPP", "VRMS", "DBM"])
            self.combo_attribute2.current(0)

            self.stringVar_defaultText3.set("Offset")
            self.entry_attribute3.pack(expand="no", side="left", anchor='nw', padx=2)

            self.stringVar_defaultText4.set("Phase (deg)")
            self.entry_attribute4.pack(expand="no", side="left", anchor='nw', padx=2)

            self.stringVar_defaultText5.set("Symetry (%)")
            self.entry_attribute5.pack(expand="no", side="left", anchor='nw', padx=2)

        if self.combo_instrCommand.get() == "applyPulse":
            self.stringVar_defaultText1.set("Frequency")
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["HZ", "KHZ", "MHZ"])
            self.combo_attribute1.current(0)

            self.stringVar_defaultText2.set("Amplitude")
            self.entry_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute2.config(value=["VPP", "VRMS", "DBM"])
            self.combo_attribute2.current(0)

            self.stringVar_defaultText3.set("Offset")
            self.entry_attribute3.pack(expand="no", side="left", anchor='nw', padx=2)

            self.stringVar_defaultText4.set("Phase")
            self.entry_attribute4.pack(expand="no", side="left", anchor='nw', padx=2)

            self.stringVar_defaultText5.set("Pulse Width")
            self.entry_attribute5.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute5.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute5.config(value=["ms", "us", "s", "ns"])
            self.combo_attribute5.current(0)

            self.stringVar_defaultText6.set("Rise Time")
            self.entry_attribute6.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute6.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute6.config(value=["ns", "us"])
            self.combo_attribute6.current(0)

            self.stringVar_defaultText7.set("Fall Time")
            self.entry_attribute7.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute7.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute7.config(value=["ns", "us"])
            self.combo_attribute7.current(0)

        if self.combo_instrCommand.get() == "applyNoise":
            self.stringVar_defaultText1.set("Amplitude")
            self.entry_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["VPP", "VRMS", "DBM"])
            self.combo_attribute1.current(0)

            self.stringVar_defaultText2.set("Offset")
            self.entry_attribute2.pack(expand="no", side="left", anchor='nw', padx=2)

            self.stringVar_defaultText3.set("Bandwidth")
            self.entry_attribute3.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute3.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute3.config(value=["HZ", "KHZ", "MHZ"])
            self.combo_attribute3.current(0)

        if self.combo_instrCommand.get() == "setOutputState":
            self.combo_attribute1.pack(expand="no", side="left", anchor='nw', padx=2)
            self.combo_attribute1.config(value=["50Ω", "High Z"])
            self.combo_attribute1.current(0)

        if self.combo_instrCommand.get() == "setMasterState":
            None