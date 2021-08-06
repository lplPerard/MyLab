"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the application's view

"""

from ScriptController import ScriptController
from OscilloscopeView import OscilloscopeView
from OscilloscopeController import OscilloscopeController
from SourcemeterView import SourcemeterView
from SourcemeterController import SourcemeterController
from ScriptView import ScriptView
from MultimeterView import MultimeterView
from MultimeterController import MultimeterController
from WaveformGeneratorView import WaveformGeneratorView
from WaveformGeneratorController import WaveformGeneratorController
from ClimaticChamberView import ClimaticChamberView
from ClimaticChamberController import ClimaticChamberController
from PowerSupplyController import PowerSupplyController
from PowerSupplyView import PowerSupplyView
from tkinter import Canvas, Frame, Scrollbar, Tk   
from tkinter import Label
from tkinter import Menu 
from tkinter import Toplevel
from tkinter import Text
from tkinter import messagebox
from tkinter import filedialog
from tkinter.constants import BOTH, YES, END, BOTTOM, RIGHT

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
        self.protocol("WM_DELETE_WINDOW", self.closeView)

        self.initAttributes()
        self.__initWidgets()

    def initAttributes(self):
    #This method instanciates all the attributes    
        self.listViews=[]

        self.path=""

        self.topLevel_wakeUp = Toplevel(self) 
        self.topLevel_term = Toplevel(self)        
        self.topLevel_param = Toplevel(self)
        self.topLevel_connect = Toplevel(self)
        
        self.term_text = Text(self.topLevel_term, height=30, width=70, bg="black", fg="green")

        self.wakeUpTL = WakeUpTL(frame=self.topLevel_wakeUp, model=self.model, view=self)
        self.parametersTL = ParametersTL(self.topLevel_param, model=self.model)
        self.connectionsTL = ConnectionsTL(self.topLevel_connect, view=self)

        self.menubar = Menu(self)
        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menu4 = Menu(self.menubar, tearoff=0)
        self.menu5 = Menu(self.menubar, tearoff=0)
        self.menu6 = Menu(self.menubar, tearoff=0)

        self.frameLine_instruments = Frame(self)
        self.frameLine_script = Frame(self)

        self.mainCanva= Canvas(self.frameLine_instruments, scrollregion=(0,0,4000,0), bd=0, highlightthickness=0, bg=self.model.parameters_dict['backgroundColor'])
        self.defilX_setup = Scrollbar(self.frameLine_instruments, orient='horizontal', command=self.mainCanva.xview, bg=self.model.parameters_dict['backgroundColor'], troughcolor=self.model.parameters_dict['backgroundColor'])
        self.mainFrame= Frame(self.mainCanva)

        controller = ScriptController()
        self.script = ScriptView(view=self.frameLine_script, root=self, model=self.model, terminal=self.term_text, controller=controller)
        controller.updateView(self.script)

    def __initWidgets(self):
    #This method is used to encapsulate the creation of sequences and menues
        
        self.resizable(True, True)
        self.title("MyLab")
        self.geometry(self.model.parameters_dict['geometry'])
        self.attributes('-alpha', self.model.parameters_dict['backgroundAlpha'])
        self.configure(bg=self.model.parameters_dict['viewColor'])
        
        self.frameLine_instruments.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frameLine_instruments.pack(padx=5, pady=5, fill="both")
        
        self.frameLine_script.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.frameLine_script.pack(padx=5, pady=5, fill="both", expand="yes")
        
        self.mainFrame.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.mainFrame.pack(padx=5, pady=5, fill="both", expand="yes")

        self.mainCanva.create_window(0, 0, anchor='nw', window=self.mainFrame, height=600, width=1920)
        self.mainFrame.configure(bg=self.model.parameters_dict['backgroundColor'])

        self.mainCanva.config(xscrollcommand= self.defilX_setup.set, height=605)
        self.mainCanva.pack(fill="both", expand="yes")
        self.defilX_setup.pack(fill="x", side='bottom', padx='5') 

        self.topLevel_term.title("Terminal")
        self.topLevel_term.resizable(True, True)
        self.topLevel_term.protocol('WM_DELETE_WINDOW', self.topLevel_term.withdraw)
        self.topLevel_term.transient()
        self.topLevel_term.withdraw()
        self.topLevel_term.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.topLevel_term.attributes('-alpha', self.model.parameters_dict['backgroundAlpha'], '-topmost', 'true')
        self.term_text.pack(fill="both", expand="yes")
        self.term_text.insert(END, "You are running MyLab" + self.model.meta_dict["version"] + "\n")    
        
        self.topLevel_wakeUp.title("Select Instrument")
        self.topLevel_wakeUp.protocol('WM_DELETE_WINDOW', self.topLevel_wakeUp.withdraw)
        self.topLevel_wakeUp.transient()
        self.topLevel_wakeUp.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.topLevel_wakeUp.geometry(self.model.parameters_dict['geometryWakeUpTL'])
        self.topLevel_wakeUp.attributes('-alpha', self.model.parameters_dict['backgroundAlpha'], '-topmost', 'true')
        self.wakeUpTL.frame.pack()
        
        self.topLevel_param.title("Parameters")
        self.topLevel_param.protocol('WM_DELETE_WINDOW', self.topLevel_param.withdraw)
        self.topLevel_param.transient()
        self.topLevel_param.withdraw()
        self.topLevel_param.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.topLevel_param.attributes('-alpha', self.model.parameters_dict['backgroundAlpha'])
        self.parametersTL.frame.pack()
        
        self.topLevel_connect.title("Connections")
        self.topLevel_connect.resizable(False, True)
        self.topLevel_connect.protocol('WM_DELETE_WINDOW', self.topLevel_connect.withdraw)
        self.topLevel_connect.transient()
        self.topLevel_connect.withdraw()
        self.topLevel_connect.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.topLevel_connect.geometry(self.model.parameters_dict['geometryConnectionsTL'])
        self.topLevel_connect.attributes('-alpha', self.model.parameters_dict['backgroundAlpha'])
        self.connectionsTL.frame.pack()

        self.__initMenu()

        self.script.initFrame()

    def closeView(self):
    #This method is called before the main windows is closed
        canClose = True
        for item in self.getInstrList():
            if item.masterState == 1:
                self.sendError("009")
                canClose = False

        if canClose == True:
            self.destroy()

    def getInstrList(self):
    #This method returns a list of instruments from listInstrument
        liste = []
        for item in self.listViews:
            liste.append(item.controller.instrument)

        liste.reverse()
        return(liste)
        
    def getControllerList(self):
    #This method returns a list of controller from listInstrument
        liste = []
        for item in self.listViews:
            liste.append(item.controller)

        liste.reverse()
        return(liste)
   
    def addDeviceFrame(self, deviceType=None, instrument=None, configuration=False):
    #This methods is used to change the device display
        if deviceType == "Power Supply":
            localController = PowerSupplyController(view=self, term=self.term_text, instrument=instrument)
            if len(self.listViews) < 15:
                pos = len(self.listViews)
                name= deviceType + " (" + str(pos) + ")"
                tamp = PowerSupplyView(self, frame=self.mainFrame, terminal=self.term_text, model=self.model, controller=localController, name=name)
                localController.updateView(tamp)
                self.listViews.insert(0, tamp)
                self.menu5.add_command(label=name, command=lambda: self.menu5_callback(tamp))
                tamp.updateView(configuration)
                self.term_text.insert(END, "New Power Supply added : " + deviceType + " (" + str(pos) + ")\n")
            else:
                self.sendWarning("W000")

        if deviceType == "Climatic Chamber":
            localController = ClimaticChamberController(view=self, term=self.term_text, instrument=instrument)
            if len(self.listViews) < 15:
                pos = len(self.listViews)
                name= deviceType + " (" + str(pos) + ")"
                tamp = ClimaticChamberView(self, frame=self.mainFrame, terminal=self.term_text, model=self.model, controller=localController, name=name)
                localController.updateView(tamp)
                self.listViews.insert(0, tamp)
                self.menu5.add_command(label=name, command=lambda: self.menu5_callback(tamp))
                tamp.updateView(configuration)
                self.term_text.insert(END, "New Climatic Chamber added : " + deviceType + " (" + str(pos) + ")\n")
            else:
                self.sendWarning("W000")

        if deviceType == "Waveform Generator":
            localController = WaveformGeneratorController(view=self, term=self.term_text, instrument=instrument)
            if len(self.listViews) < 15:
                pos = len(self.listViews)
                name= deviceType + " (" + str(pos) + ")"
                tamp = WaveformGeneratorView(self, frame=self.mainFrame, terminal=self.term_text, model=self.model, controller=localController, name=name)
                localController.updateView(tamp)
                self.listViews.insert(0, tamp)
                self.menu5.add_command(label=name, command=lambda: self.menu5_callback(tamp))
                tamp.updateView(configuration)
                self.term_text.insert(END, "New Waveform Generator added : " + deviceType + " (" + str(pos) + ")\n")
            else:
                self.sendWarning("W000")

        if deviceType == "Multimeter":
            localController = MultimeterController(view=self, term=self.term_text, instrument=instrument)
            if len(self.listViews) < 15:
                pos = len(self.listViews)
                name= deviceType + " (" + str(pos) + ")"
                tamp = MultimeterView(self, frame=self.mainFrame, terminal=self.term_text, model=self.model, controller=localController, name=name)
                localController.updateView(tamp)
                self.listViews.insert(0, tamp)
                self.menu5.add_command(label=name, command=lambda: self.menu5_callback(tamp))
                tamp.updateView(configuration)
                self.term_text.insert(END, "New Multimeter added : " + deviceType + " (" + str(pos) + ")\n")
            else:
                self.sendWarning("W000")

        if deviceType == "Sourcemeter":
            localController = SourcemeterController(view=self, term=self.term_text, instrument=instrument)
            if len(self.listViews) < 15:
                pos = len(self.listViews)
                name= deviceType + " (" + str(pos) + ")"
                tamp = SourcemeterView(self, frame=self.mainFrame, terminal=self.term_text, model=self.model, controller=localController, name=name)
                localController.updateView(tamp)
                self.listViews.insert(0, tamp)
                self.menu5.add_command(label=name, command=lambda: self.menu5_callback(tamp))
                tamp.updateView(configuration)
                self.term_text.insert(END, "New Sourcemeter added : " + deviceType + " (" + str(pos) + ")\n")
            else:
                self.sendWarning("W000")

        if deviceType == "Oscilloscope":
            localController = OscilloscopeController(view=self, term=self.term_text, instrument=instrument)
            if len(self.listViews) < 15:
                pos = len(self.listViews)
                name= deviceType + " (" + str(pos) + ")"
                tamp = OscilloscopeView(self, frame=self.mainFrame, terminal=self.term_text, model=self.model, controller=localController, name=name)
                localController.updateView(tamp)
                self.listViews.insert(0, tamp)
                self.menu5.add_command(label=name, command=lambda: self.menu5_callback(tamp))
                tamp.updateView(configuration)
                self.term_text.insert(END, "New Sourcemeter added : " + deviceType + " (" + str(pos) + ")\n")
            else:
                self.sendWarning("W000")

    def sendError(self, error="xxx", complement=""):
    #This method generates message boxes from error returns
        messagebox.showerror(title="Error : " + error, message=self.model.error_dict[error] + complement)
        self.term_text.insert(END, "\nError : " + error + "\n  " + self.model.error_dict[error] + "\n")  

    def sendWarning(self, warning):
    #This method generates message boxes from error returns
        messagebox.showwarning(title="Warning : " + warning, message=self.model.error_dict[warning])
        self.term_text.insert(END, "\nWarning : " + warning + "\n  " + self.model.error_dict[warning] + "\n")  

    def refresh(self):
    #This method refresh the view and its content     
        self.update_idletasks()
        for item in self.listViews:
            if item.controller.instrument.masterState == 0:
                item.updateView()

    def __initMenu(self):
    #This method generates a Menu bar which give access to the diffent software's tools
        self.menubar.add_cascade(label="File", menu=self.menu1)
        self.menu1.add_command(label="New", command=self.menu1_New_callBack)
        self.menu1.add_command(label="Save", command=self.menu1_Save_callBack)
        self.menu1.add_command(label="Save as", command=self.menu1_SaveAs_callBack)
        self.menu1.add_command(label="Open", command=self.menu1_Open_callBack)
        self.menu1.bind_all('<Control-Key-s>', self.menu1_Save_callBack)
        self.menu1.bind_all('<Control-Key-S>', self.menu1_SaveAs_callBack)
        self.menu1.bind_all('<Control-Key-o>', self.menu1_Open_callBack)

        self.menubar.add_cascade(label="Edit", menu=self.menu2)
        self.menu2.add_cascade(label="Add Instrument", menu=self.menu4)
        self.menu2.add_cascade(label="Add TestBench", menu=self.menu6)
        self.menu2.add_cascade(label="Delete", menu=self.menu5) 
        self.menu2.add_separator()
        self.menu2.add_command(label="Parameters", command=self.menu2_Parameters_callBack)
        self.menu2.add_command(label="Connections", command=self.menu2_Connections_callBack)
        self.menu2.bind_all('<Control-Key-a>', self.menu2_WakeUp_callBack)

        self.menubar.add_cascade(label="Display", menu=self.menu3)
        self.menu3.add_command(label="Terminal", command=self.menu3_Terminal_callBack)
        self.menu3.add_command(label="Script", command=self.menu3_Script_callBack)
        self.menu3.add_separator()
        self.menu3.add_command(label="Change logs", command=self.menu3_logs_callBack)  

        self.menu4.add_command(label="Configuration", command=self.menu4_Configuration_callBack)
        self.menu4.add_command(label="Climatic Chamber", command=self.menu4_ClimaticChamber_callBack) 
        self.menu4.add_command(label="Multimeter", command=self.menu4_Multimeter_callBack)
        self.menu4.add_command(label="Oscilloscope", command=self.menu4_Oscilloscope_callBack)
        self.menu4.add_command(label="Power Supply", command=self.menu4_PowerSupply_callBack)
        self.menu4.add_command(label="Sourcemeter", command=self.menu4_SourceMeter_callBack)
        self.menu4.add_command(label="Waveform Generator", command=self.menu4_WaveformGenerator_callBack)  
        
        self.menu6.add_command(label="HTOL", command=self.menu6_HTOL_callBack)
        self.menu6.add_command(label="Bode", command=self.menu6_Bode_callBack)
        self.menu6.add_command(label="I/V Characteristic", command=self.menu6_IV_callBack)
        
        self.config(menu=self.menubar)

    def menu1_New_callBack(self, args=None):
    #Callback function for menu1 new option
        mbox = messagebox.askyesno("New Configuration", "Do you want to start a new configuration ?\n Current configuration will be closed.")
        if mbox == True:
            self.menu1_Save_callBack()

            canClear = True
            for item in self.getInstrList():
                if item.masterState == 1:
                    self.sendError("008")
                    canClear = False

            if canClear == True:
                if self.listViews != []:
                    for item in self.listViews:
                        index = self.listViews.index(item)
                        self.listViews[index].clearInstrument()
                        self.listViews[index].clearFrame()
                        self.menu5.delete(self.listViews[index].controller.instrument.name)

                    self.listViews.clear()
                    self.script.clearCommandLine()
                    self.path = ""

    def menu1_Save_callBack(self, args=None):
    #Callback function for  menu1 1 option        
        canSave = True
        for item in self.getInstrList():
            if item.masterState == 1:
                self.sendError("007")
                canSave = False
            else:
                item.ressource = None

        if canSave == True:
            if self.path == "":
                self.path = filedialog.asksaveasfilename(title = "Select file", filetypes = (("all files","*.*"), ("MyLab files","*.mylab")))
                self.model.saveConfiguration(listeInstruments=self.getInstrList(), path=self.path, listeCommand=self.script.getListeCommand())
            else:
                self.model.saveConfiguration(listeInstruments=self.getInstrList(), path=self.path, listeCommand=self.script.getListeCommand())

    def menu1_SaveAs_callBack(self, args=None):
    #Callback function for menu1 2 option     
        canSave = True
        for item in self.getInstrList():
            if item.masterState == 1:
                self.sendError("007")
                canSave = False
            else:
                item.ressource = None

        if canSave == True:
            self.path = filedialog.asksaveasfilename(title = "Select file", filetypes = (("all files","*.*"), ("MyLab files","*.mylab")))
            self.model.saveConfiguration(listeInstruments=self.getInstrList(), path=self.path, listeCommand=self.script.getListeCommand())

    def menu1_Open_callBack(self, args=None):
    #Callback function for menu1 2 option
        canOpen = True
        for item in self.getInstrList():
            if item.masterState == 1:
                self.sendError("008")
                canOpen = False

        if canOpen == True:
            self.path = filedialog.askopenfilename(title = "Select file", filetypes = (("all files","*.*"), ("MyLab files","*.mylab")))
            if (self.listViews != []) and (self.path != ""):
                for item in self.listViews:
                    index = self.listViews.index(item)
                    self.listViews[index].clearInstrument()
                    self.listViews[index].clearFrame()
                    self.menu5.delete(self.listViews[index].controller.instrument.name)

                self.listViews.clear()
            
            if (self.script.listeCommand != []) and (self.path != ""):
                self.script.clearCommandLine()
            
            if self.path != "":                
                liste = self.model.openConfiguration(path=self.path)

                for item in liste[0]:
                    self.addDeviceFrame(deviceType=item.type, instrument=item, configuration=True)

                for item in liste[1]:
                    self.script.addCommandLine(command=item)
                
                for item in self.script.listeCommand:
                    item.updateLine()

    def menu2_Parameters_callBack(self, args=None):
    #Callback function for menu2 1 option
        if self.topLevel_param.state() == "withdrawn":
            self.topLevel_param.deiconify()

        elif self.topLevel_param.state() == "normal":
            self.topLevel_param.withdraw()

    def menu2_WakeUp_callBack(self, args=None):
    #Callback function for menu2 2 option
        if self.topLevel_wakeUp.state() == "withdrawn":
            self.topLevel_wakeUp.deiconify()

        elif self.topLevel_connect.state() == "normal":
            self.topLevel_connect.withdraw()

    def menu2_Connections_callBack(self, args=None):
    #Callback function for menu2 2 option
        if self.topLevel_connect.state() == "withdrawn":
            self.topLevel_connect.deiconify()
            self.connectionsTL.actualizeInstruments()

        elif self.topLevel_connect.state() == "normal":
            self.topLevel_connect.withdraw()

    def menu3_Terminal_callBack(self, args=None):
    #Callback function for menu2 1 option
        if self.topLevel_term.state() == "withdrawn":
            self.topLevel_term.deiconify()

        elif self.topLevel_term.state() == "normal":
            self.topLevel_term.withdraw()
            
    def menu3_Script_callBack(self, args=None):
    #Callback function for menu2 1 option
        if self.frameLine_script.winfo_ismapped() :
            self.frameLine_script.pack_forget()
        else:
            self.frameLine_script.pack(padx=5, pady=5, fill="both", expand="yes")

    def menu3_logs_callBack(self, args=None):
    #Callback function for menu2 2 option
        self.sendError("404")

    def menu4_Configuration_callBack(self, args=None):
    #Callback function for menu2 2 option
        canOpen = True
        for item in self.getInstrList():
            if item.masterState == 1:
                self.sendError("008")
                canOpen = False

        mbox = messagebox.askyesno("Add Instrument", "Do you want to add a Configuration ?")
        if (mbox == True) and (canOpen == True):
            self.path = filedialog.askopenfilename(title = "Select file", filetypes = (("all files","*.*"), ("MyLab files","*.mylab")))
            if self.path != "":
                
                liste = self.model.openConfiguration(path=self.path)

                for item in liste[0]:
                    self.addDeviceFrame(deviceType=item.type, instrument=item, configuration=True)
                for item in liste[1]:
                    self.script.addCommandLine(command=item)

    def menu4_WaveformGenerator_callBack(self, args=None):
    #Callback function for menu2 2 option
        mbox = messagebox.askyesno("Add Instrument", "Do you want to add a Waveform Generator?")
        if mbox == True:
            self.addDeviceFrame("Waveform Generator")

    def menu4_Multimeter_callBack(self, args=None):
    #Callback function for menu2 2 option
        mbox = messagebox.askyesno("Add Instrument", "Do you want to add a Multimeter ?")
        if mbox == True:
            self.addDeviceFrame("Multimeter")

    def menu4_Oscilloscope_callBack(self, args=None):
    #Callback function for menu2 2 option
        mbox = messagebox.askyesno("Add Instrument", "Do you want to add an Oscilloscope?")
        if mbox == True:
            self.addDeviceFrame("Oscilloscope")

    def menu4_SourceMeter_callBack(self, args=None):
    #Callback function for menu2 2 option
        mbox = messagebox.askyesno("Add Instrument", "Do you want to add Sourcemeter ?")
        if mbox == True:
            self.addDeviceFrame("Sourcemeter")

    def menu4_PowerSupply_callBack(self, args=None):
    #Callback function for menu2 2 option
        mbox = messagebox.askyesno("Add Instrument", "Do you want to add a Power Supply ?")
        if mbox == True:
            self.addDeviceFrame("Power Supply")

    def menu4_ClimaticChamber_callBack(self, args=None):
    #Callback function for menu2 2 option
        mbox = messagebox.askyesno("Add Instrument", "Do you want to add a Climatic Chamber ?")
        if mbox == True:
            self.addDeviceFrame("Climatic Chamber")

    def menu5_callback(self, instrView):
    #Callback function for menu5 delete option
        index = self.listViews.index(instrView)
        if self.listViews[index].controller.instrument.masterState == 0:
            self.menu5.delete(self.listViews[index].controller.instrument.name)
            self.term_text.insert(END, "An Instrument was deleted : " + self.listViews[index].controller.instrument.name +"\n")
            self.listViews[index].clearInstrument()
            self.listViews[index].clearFrame()
            del self.listViews[index]
        else:
            self.sendError("007")

    def menu6_HTOL_callBack(self, args=None):
    #Callback function for menu2 2 option
        self.sendError("404")

    def menu6_Bode_callBack(self, args=None):
    #Callback function for menu2 2 option
        self.sendError("404")

    def menu6_IV_callBack(self, args=None):
    #Callback function for menu2 2 option
        self.sendError("404")
