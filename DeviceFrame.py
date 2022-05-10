"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for DeviceFrame.

"""

from Instrument import Instrument
from tkinter import Button, LabelFrame
from tkinter import Label
from tkinter import Frame
from tkinter import Text
from tkinter import BOTH
from tkinter import YES
from tkinter import END
from tkinter.constants import NONE, TOP
from PIL import Image, ImageTk


class DeviceFrame():
    """Superclass containing the GUI for a typical testbench.

    """

    def __init__(self,  view=None, controller=None, terminal=None, model=None):
    #Constructor for the Sequence_view superclass
        
        self.view = view
        self.term_text = terminal
        self.model = model
        self.controller = controller
        self.frame = LabelFrame(view)

    def initFrame(self, text="", padx=15, pady=0):
    #This method generates the Frame's parameters for the sequence
        self.line = Frame(self.frame, bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.ident = Label(self.line, text=text, font=("bold", 16))
        self.ident.configure(bg=self.model.parameters_dict['backgroundColorInstrument'])
        self.ident.pack(expand="yes", side="left", anchor='w', padx=5, pady=5)

        self.deleteImg = Image.open("Images/delete.png")
        self.deleteImg = self.deleteImg.resize((15, 17), Image.ANTIALIAS)
        self.deleteImg = ImageTk.PhotoImage(self.deleteImg)

        self.button_delete = Button(self.line, image=self.deleteImg, command=self.button_delete_callback, bg="#797E84")
        self.button_delete.pack(expand="yes", side="right", anchor='e', padx=5, pady=5)

        self.frame.configure(labelwidget = self.line, padx=padx, pady=pady, bg=self.model.parameters_dict['backgroundColorInstrument'],
                                                                                 bd=self.model.parameters_dict['instrumentBorderwidth'])
        self.frame.pack(fill="y", expand="no", side="left", anchor='nw', pady=5)
        

        self.labelFrame_instrument = LabelFrame(self.frame, text="Instrument", bg=self.model.parameters_dict['backgroundColorInstrumentData'])

    def clearFrame(self):
    #This method delete the Sequence's frame from the grid
        self.labelFrame_instrument.destroy()
        self.frame.destroy()

    def button_delete_callback(self):
    #This method is called to delete the device from the list of devices
        self.view.menu5_callback(self)

    def clearInstrument(self):
        None   
      
    def generateArguments(self, args1="", args2="", args3="", args4="", args5="", args6="", args7="", args8="", args9="", args10="", args11="", args12="", args13="", args14=""):
    #This method generates a list of argument
        liste = [""]*14

        liste[0] = args1
        liste[1] = args2
        liste[2] = args3
        liste[3] = args4
        liste[4] = args5
        liste[5] = args6
        liste[6] = args7
        liste[7] = args8
        liste[8] = args9
        liste[9] = args10
        liste[10] = args11
        liste[11] = args12
        liste[12] = args13
        liste[13] = args14

        return(liste)

    def close(self):
        None
        
    def renameInstrument(self):
        for item in self.view.listViews:
            if self.controller.instrument.name == item.controller.instrument.name:  
                if (self != item):
                    index = int(item.controller.instrument.name[-2]) + 1
                    newName = self.controller.instrument.name[:-2] + str(index) + ")"
                    self.entry_instrumentName_callback(newName=newName)