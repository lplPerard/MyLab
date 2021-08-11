"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for ScriptView.

"""

import threading
from PIL import Image, ImageTk
from CommandLine import CommandLine
from Instrument import Instrument
from tkinter import Button, Canvas, Entry, Frame, LabelFrame, Scrollbar, IntVar
from tkinter import Label
from tkinter import Toplevel
from tkinter import Text
from tkinter import BOTH
from tkinter import YES
from tkinter import END
from tkinter.constants import NONE, TOP


class ScriptView():
    """Class containing the GUI for a typical scripts.

    """

    def __init__(self,  view=None, root=None, controller=None, terminal=None, model=None):
    #Constructor for the Sequence_view superclass
        
        self.view = view
        self.term_text = terminal
        self.model = model
        self.controller = controller
        self.root=root

        self.listeCommand = []
        self.scriptState = "STOP"

        self.dataFrame = LabelFrame(self.view)
        self.mainCanva= Canvas(self.view, scrollregion=(0,0,2500,2000), bd=0, highlightthickness=0, bg=self.model.parameters_dict['backgroundColor'])
        self.mainFrame= Frame(self.mainCanva, bg=self.model.parameters_dict['backgroundColor'])
        self.defilY_setup = Scrollbar(self.mainCanva, orient='vertical', command=self.mainCanva.yview, bg=self.model.parameters_dict['backgroundColor'])
        self.defilX_setup = Scrollbar(self.mainCanva, orient='horizontal', command=self.mainCanva.xview, bg=self.model.parameters_dict['backgroundColor'])

        self.frameline_insert = Frame(self.dataFrame, bg=self.model.parameters_dict['backgroundColorConfiguration'])
        self.frameline_buttons = Frame(self.dataFrame, bg=self.model.parameters_dict['backgroundColorConfiguration'])

        self.intvar_insertPos = IntVar()
        self.intvar_insertPos.set(0)

        self.playImg = Image.open("play.png")
        self.playImg = self.playImg.resize((15, 15), Image.ANTIALIAS)
        self.playImg = ImageTk.PhotoImage(self.playImg)

        self.pauseImg = Image.open("pause.png")
        self.pauseImg = self.pauseImg.resize((15, 15), Image.ANTIALIAS)
        self.pauseImg = ImageTk.PhotoImage(self.pauseImg)

        self.nextImg = Image.open("next.png")
        self.nextImg = self.nextImg.resize((15, 15), Image.ANTIALIAS)
        self.nextImg = ImageTk.PhotoImage(self.nextImg)

        self.stopImg = Image.open("stop.png")
        self.stopImg = self.stopImg.resize((15, 15), Image.ANTIALIAS)
        self.stopImg = ImageTk.PhotoImage(self.stopImg)

        self.button_addCommandLine = Button(self.dataFrame, text=" Add Command Line  ", command=self.addCommandLine)
        self.button_addCommandLine.bind_all('<Control-Key-n>', self.addCommandLine)
        self.button_insertCommandLine = Button(self.frameline_insert, text="Insert at ", command=lambda:self.addCommandLine(pos=self.intvar_insertPos.get()))
        self.button_clearCommandLine = Button(self.dataFrame, text=" Clear Script  ", command=self.clearCommandLine)
        self.button_stopScript = Button(self.frameline_buttons, image=self.stopImg, command=self.button_stopScript_callback)
        self.button_runScript = Button(self.frameline_buttons, image=self.playImg, command=self.button_runScript_callback)
        self.button_runScript.bind_all('<Control-Key-r>', self.button_runScript_callback)
        self.button_nextInScript = Button(self.frameline_buttons, image=self.nextImg, command=self.button_nextInScript_callback)

        self.entry_insertPos = Entry(self.frameline_insert, textvariable=self.intvar_insertPos, width=5)
        
    def initFrame(self, padx=10, pady=10):
    #This method generates the Frame's parameters for the sequence
        self.dataFrame.configure(text="Configuration", font=(12), padx=padx, pady=pady, bg=self.model.parameters_dict['backgroundColorConfiguration'])
        self.dataFrame.pack(fill="y", expand="no", side="left", anchor='nw')

        self.mainFrame.pack(fill="both", expand="yes", side="left", anchor='nw', padx=5, pady=5)

        self.mainCanva.create_window(0, 0, anchor='nw', window=self.mainFrame)
        self.mainCanva.bind_all("<MouseWheel>", self._on_mousewheel)
        self.mainFrame.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.mainCanva.config(yscrollcommand= self.defilY_setup.set, xscrollcommand= self.defilX_setup.set,height=2000)
        self.mainCanva.pack(fill="both", expand="yes", side="left", anchor='nw')
        self.defilX_setup.pack(fill="x", side='bottom', padx='3', pady=3) 
        #self.defilY_setup.pack(fill="y", side='right', padx='3', pady=3) 

        self.button_addCommandLine.pack(pady=2, padx=3)
        self.frameline_insert.pack()
        self.button_insertCommandLine.pack(side='left', anchor='nw', pady=2)
        self.entry_insertPos.pack(side='left', padx=3)
        self.button_clearCommandLine.pack(pady=2, padx=6)
        self.frameline_buttons.pack()
        self.button_stopScript.pack(side='left', ipadx=5, pady=2, padx=6)
        self.button_runScript.pack(side='left', ipadx=5, pady=2, padx=6)
        self.button_nextInScript.pack(side='left', ipadx=5, pady=2, padx=6)

    def addCommandLine(self, args=None, pos=None, command=None):
    #This method adds a new command line to be displayed by ScriptView
        if (pos == None) and (command == None):
            number = len(self.listeCommand)
            tamp = CommandLine(frame=self.mainFrame, root=self.root, script=self, terminal=self.term_text, model=self.model, number=number)
            self.listeCommand.append(tamp)
            self.term_text.insert(END, "New Command Line added at : " + str(number) + "\n")

        elif (pos != None) and (command == None):
            number = pos
            tamp = CommandLine(frame=self.mainFrame, root=self.root, script=self, terminal=self.term_text, model=self.model, number=number)
            self.listeCommand.insert(pos, tamp)
            for item in self.listeCommand:
                item.line.pack_forget()   
            for item in self.listeCommand:
                item.line.pack(fill="x", expand="no", side="top", anchor='nw', pady=2)        
            self.renumberLine()        

        elif (command != None):
            number = len(self.listeCommand)
            tamp = CommandLine(frame=self.mainFrame, root=self.root, script=self, terminal=self.term_text, model=self.model, number=number, command=command)
            self.listeCommand.append(tamp)
            self.term_text.insert(END, "New Command Line added at : " + str(number) + "\n")  

    def clearCommandLine(self):
    #This method clears all commandList
        for item in self.listeCommand:
            item.line.destroy()
        self.listeCommand.clear()

    def deleteCommandLine(self, commandLine=None):
    #This method is called to delete a line from ScriptView
        self.listeCommand.remove(commandLine)
        self.renumberLine()
    
    def renumberLine(self):
    #This method is called to change each line number in the list
        for index in range(len(self.listeCommand)):
            self.listeCommand[index].renumberLine(index)

    def getListeCommand(self):
    #This method returns the command for each item in listeCommand
        liste=[] 
        for item in self.listeCommand:
            liste.append(item.command)

        return(liste)

    def _on_mousewheel(self, event):
    #This method is called when playing with MousWheel on the script view
        self.mainCanva.yview_scroll(int(-1*(event.delta/120)), "units")

    def button_stopScript_callback(self, args=None):
    #This method is called when running the script
        self.scriptState = "STOP"

    def button_runScript_callback(self, args=None):
    #This method is called when running the script
        self.button_runScript.config(image=self.pauseImg)
        self.button_runScript.update_idletasks()

        if (self.scriptState != "RUN") and (self.scriptState != "PAUSE"):
            run = threading.Thread(target=self.controller.runScript)
            run.daemon = True
            run.start()

        elif self.scriptState == "RUN":
            self.scriptState = "PAUSE"
            self.button_runScript.config(image=self.playImg)

        elif self.scriptState == "PAUSE":
            self.scriptState = "RUN"
            self.button_runScript.config(image=self.pauseImg)

    def button_nextInScript_callback(self, args=None):
    #This method is called when clicking on the Next button

        if self.scriptState == "PAUSE":
            self.scriptState = "NEXT"
