"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the application's view

"""

from PowerSupplyView import PowerSupplyView
from tkinter import Tk   
from tkinter import Label
from tkinter import Menu 
from tkinter import Toplevel
from tkinter import Text
from tkinter import messagebox
from tkinter import BOTH
from tkinter import YES
from tkinter import END
from tkinter.constants import BOTTOM

from DeviceFrame import DeviceFrame
from ParametersTL import ParametersTL
from ConnectionsTL import ConnectionsTL
from WakeUpTL import WakeUpTL
from Model import Model

class View(Tk):
    """Class containing the GUI for the Mylab according to the MCV model.

    """

    def __init__(self, controller, model):
    #Constructor for the View class
        """
            Constructor for the class View. The class inherits from Tk from GUI management.
            The following attributes are  created :

        """
        Tk.__init__(self)
        
        self.model = model
        self.controller = controller

        self.topLevel_wakeUp = Toplevel(self) 
        self.topLevel_term = Toplevel(self)        
        self.topLevel_param = Toplevel(self)
        self.topLevel_connect = Toplevel(self)

        self.__initWidgets()

    def __initWidgets(self):
    #This method is used to encapsulate the creation of sequences and menues
        
        self.resizable(True, True)
        self.title("MyLab")
        self.geometry(self.model.parameters_dict['geometry'])
        self.attributes('-alpha', self.model.parameters_dict['backgroundAlpha'])
        self.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.topLevel_term.title("Terminal")
        self.topLevel_term.protocol('WM_DELETE_WINDOW', self.topLevel_term.withdraw)
        self.topLevel_term.transient()
        self.topLevel_term.withdraw()
        self.topLevel_term.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.topLevel_term.attributes('-alpha', self.model.parameters_dict['backgroundAlpha'], '-topmost', 'true')
        self.term_text = Text(self.topLevel_term, height=30, width=70, bg="black", fg="green")
        self.term_text.grid(column=0, row=0)
        self.term_text.insert(END, "You are running MyLab\n")        
        
        self.topLevel_wakeUp.title("Select Instrument")
        self.topLevel_wakeUp.protocol('WM_DELETE_WINDOW', self.topLevel_wakeUp.withdraw)
        self.topLevel_wakeUp.transient()
        self.topLevel_wakeUp.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.topLevel_wakeUp.geometry(self.model.parameters_dict['geometryWakeUpTL'])
        self.topLevel_wakeUp.attributes('-alpha', self.model.parameters_dict['backgroundAlpha'], '-topmost', 'true')
        self.wakeUpTL = WakeUpTL(self.topLevel_wakeUp, model=self.model, View=self)
        self.wakeUpTL.frame.pack()
        
        self.topLevel_param.title("Parameters")
        self.topLevel_param.protocol('WM_DELETE_WINDOW', self.topLevel_param.withdraw)
        self.topLevel_param.transient()
        self.topLevel_param.withdraw()
        self.topLevel_param.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.topLevel_param.attributes('-alpha', self.model.parameters_dict['backgroundAlpha'])
        self.parametersTL = ParametersTL(self.topLevel_param, model=self.model)
        self.parametersTL.frame.pack()
        
        self.topLevel_connect.title("Connections")
        self.topLevel_connect.resizable(False, True)
        self.topLevel_connect.protocol('WM_DELETE_WINDOW', self.topLevel_connect.withdraw)
        self.topLevel_connect.transient()
        self.topLevel_connect.withdraw()
        self.topLevel_connect.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.topLevel_connect.geometry(self.model.parameters_dict['geometryConnectionsTL'])
        self.topLevel_connect.attributes('-alpha', self.model.parameters_dict['backgroundAlpha'])
        self.connectionsTL = ConnectionsTL(self.topLevel_connect, view=self)
        self.connectionsTL.frame.pack()

        self.frame = DeviceFrame(self, terminal=self.term_text, model=self.model)
        self.frame.initFrame(text="Device Name", bg=self.model.parameters_dict['backgroundColor'])

        self.__initMenu()

        self.copyright = Label(self, text="Copyright Oticon Medical NICE", bg=self.model.parameters_dict['backgroundColor'])
        self.copyright.pack(side = BOTTOM, padx=5, pady=5)

    def changeDeviceFrame(self, deviceName):
    #This methods is used to change the device display
        if deviceName == "Power Supply":
                self.frame.clearFrame()
                self.frame = PowerSupplyView(self, terminal=self.term_text, model=self.model)
        if deviceName == "Oscilloscope":
                self.frame.clearFrame()
                self.frame = PowerSupplyView(self, terminal=self.term_text, model=self.model)
        if deviceName == "Source Meter":
                self.frame.clearFrame()
                self.frame = PowerSupplyView(self, terminal=self.term_text, model=self.model)
        if deviceName == "RLC Meter":
                self.frame.clearFrame()
                self.frame = PowerSupplyView(self, terminal=self.term_text, model=self.model)

    def sendError(self, error):
    #This method generates message boxes from error returns
        messagebox.showerror(title="Error : " + error, message=self.model.error_dict[error])

        
    def __initMenu(self):
    #This method generates a Menu bar which give access to the diffent software's tools
        self.menubar = Menu(self)

        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.menu1)
        self.menu1.add_command(label="Save", command=self.menu1_Save_callBack)
        self.menu1.add_command(label="Save as", command=self.menu1_SaveAs_callBack)
        self.menu1.add_command(label="Open", command=self.menu1_Open_callBack)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.menu2)        
        self.menu2.add_command(label="Parameters", command=self.menu2_Parameters_callBack)
        self.menu2.add_command(label="Connections", command=self.menu2_Connections_callBack)       

        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Display", menu=self.menu3)
        self.menu3.add_command(label="Terminal", command=self.menu3_Terminal_callBack)
        self.menu3.add_command(label="Change logs", command=self.menu3_logs_callBack)
        
        self.menu4 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Instruments", menu=self.menu4)
        self.menu4.add_command(label="Oscilloscope", command=self.menu4_Oscilloscope_callBack)
        self.menu4.add_command(label="Source Meter", command=self.menu4_SourceMeter_callBack)
        self.menu4.add_command(label="RLC Meter", command=self.menu4_RLCMeter_callBack)
        self.menu4.add_command(label="Power Supply", command=self.menu4_PowerSupply_callBack)
        self.menu4.add_command(label="Climatic Chamber", command=self.menu4_ClimaticChamber_callBack)

        self.config(menu=self.menubar)

    def menu1_Save_callBack(self):
    #Callback function for  menu1 1 option
        print("test")

    def menu1_SaveAs_callBack(self):
    #Callback function for menu1 2 option
        print("test")

    def menu1_Open_callBack(self):
    #Callback function for menu1 2 option
        print("test")

    def menu2_Parameters_callBack(self):
    #Callback function for menu2 1 option
        if self.topLevel_param.state() == "withdrawn":
            self.topLevel_param.deiconify()

        elif self.topLevel_param.state() == "normal":
            self.topLevel_param.withdraw()

    def menu2_Connections_callBack(self):
    #Callback function for menu2 2 option
        if self.topLevel_connect.state() == "withdrawn":
            self.topLevel_connect.deiconify()

        elif self.topLevel_connect.state() == "normal":
            self.topLevel_connect.withdraw()

    def menu3_Terminal_callBack(self):
    #Callback function for menu2 1 option
        if self.topLevel_term.state() == "withdrawn":
            self.topLevel_term.deiconify()

        elif self.topLevel_term.state() == "normal":
            self.topLevel_term.withdraw()

    def menu3_logs_callBack(self):
    #Callback function for menu2 2 option
        print("bla")

    def menu4_Oscilloscope_callBack(self):
    #Callback function for menu2 2 option
        mbox = messagebox.askyesno("Switch Instrument", "Do you want to switch instrument ?")
        if mbox == True:
            print("bla")
        else:
            print("bla")

    def menu4_SourceMeter_callBack(self):
    #Callback function for menu2 2 option
        mbox = messagebox.askyesno("Switch Instrument", "Do you want to switch instrument ?")
        if mbox == True:
            print("bla")
        else:
            print("bla")

    def menu4_RLCMeter_callBack(self):
    #Callback function for menu2 2 option
        mbox = messagebox.askyesno("Switch Instrument", "Do you want to switch instrument ?")
        if mbox == True:
            print("bla")
        else:
            print("bla")

    def menu4_PowerSupply_callBack(self):
    #Callback function for menu2 2 option
        mbox = messagebox.askyesno("Switch Instrument", "Do you want to switch instrument ?")
        if mbox == True:
            self.changeDeviceFrame("Power Supply")
        else:
            print("bla")

    def menu4_ClimaticChamber_callBack(self):
    #Callback function for menu2 2 option
        mbox = messagebox.askyesno("Switch Instrument", "Do you want to switch instrument ?")
        if mbox == True:
            print("bla")
        else:
            print("bla")
