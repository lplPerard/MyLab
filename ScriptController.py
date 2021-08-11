"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for ScriptController.

"""

from ScriptView import ScriptView
from numpy import arange
import time



class ScriptController():
    """Class containing the decoder for scripts.

    """

    def __init__(self):

        self.listeCommand = []
        self.listeExecutable = []
        self.view=None
        self.instrument = None
        self.root = None

    def updateView(self, view):
    #this method the view and root attributes
        self.view=view
        self.root = self.view.root

    def analyzeCommand(self):
    #This method analyze the command line to generate the appropriate function
        error=0
        self.listeCommand.clear()
        self.listeExecutable.clear()
        self.listeCommand = self.view.getListeCommand()
        
        for item in self.listeCommand:
            command=None
            if (item.combo_choice1 == "WAIT") and (item.state != "RUN"):
                tmp = self.generateWaitCommand(item.entry_attribute1)                
                self.listeExecutable.append(tmp)
                item.state = "RUN"

            elif (item.combo_choice1 == "FOR") and (item.state != "RUN"):
                error = self.generateForCommand(self.listeCommand.index(item))
                item.state = "RUN"

            elif (item.state != "RUN") and (item.combo_choice1 != "END"):
                self.getInstrument(name = item.combo_choice1)
                self.listeExecutable.append([getattr(self.instrument, item.combo_instrCommand), self.getArgs(command=item)])
                item.state = "RUN"
                
        return(error)

    def generateWaitCommand(self, duration):
    #This method generates a for fucntion    
        listeVariable = ["Temperature", "Voltage", "Current", "Frequency", "A", "B", "C", "D", "E", "F", "G"]

        try :
            index = listeVariable.index(duration)
            duration = globals()[listeVariable[index]]
        except:
            duration = float(duration)

        def func(args=[duration]) :
            print(duration)
            time.sleep(duration)

        args=[duration]
        return([func, args])

    def generateForCommand(self, index=None, forstate=0):
    #This method generate a For function
        subListExe = []
        end = 0
        endIndex = None
        command=None

        for item in self.listeCommand[index+1:]:
            ind=self.listeCommand.index(item)
            if (item.combo_choice1 == "FOR") and (item.state != "RUN"):
                self.listeCommand[ind].state = "RUN"
                self.listeCommand[ind].forState = forstate
                command = self.generateForCommand(index=ind, forstate=forstate+1)

            elif (item.combo_choice1 == "END") and (item.state != "RUN"):
                self.listeCommand[ind].state = "RUN"
                self.listeCommand[ind].forState = forstate
                endIndex = ind
                end = 1
                break

            elif (item.state != "RUN") :
                self.listeCommand[ind].forState = forstate

        if end != 0:
            subListeCommand = self.listeCommand[index+1:endIndex]

            start = float(self.listeCommand[index].entry_attribute1)
            step = float(self.listeCommand[index].entry_attribute2)
            num = float(self.listeCommand[index].entry_attribute3)
            togothrough = arange(0,num)*step+start

            for item in subListeCommand:
                if item.forstate < forstate:
                    item.forstate=forstate

            for globals()[self.listeCommand[index].combo_instrCommand] in togothrough:
                for item in subListeCommand :
                    if (item.combo_choice1 == "WAIT") and (item.forstate == forstate):
                        tmp=self.generateWaitCommand(item.entry_attribute1)
                        subListExe.append(tmp)
                        
                    elif (item.combo_choice1 == "FOR") and (item.forstate == forstate):
                        subListExe.extend(command)

                    elif (item.state != "RUN") and (item.forstate == forstate):
                        self.getInstrument(name = item.combo_choice1)
                        subListExe.append([getattr(self.instrument, item.combo_instrCommand), self.getArgs(command=item)])
                
            for item in subListeCommand :
                item.state = "RUN"
                
            self.listeCommand[index+1:endIndex] = subListeCommand

            if forstate != 0:
                return(subListExe)
            else:
                self.listeExecutable.extend(subListExe)

        else :
            self.root.sendError("101")
            return(-1)

    def getInstrument(self, name=None):
    #This method return the instrument controller corresponding to name
        found=0
        for item in self.root.getControllerList():
            if item.instrument.name == name:
                self.instrument=item
                found = 1
                break

        if found == 0:
            self.root.sendError("100", name)

    def getArgs(self, command=None):
    #This methods generates an argument list
        args = []
        listeVariable = ["Temperature", "Voltage", "Current", "Frequency", "A", "B", "C", "D", "E", "F", "G"]

        try:
            listeVariable.index(command.entry_attribute1)
            args.append(globals()[command.entry_attribute1])
        except:
            if command.entry_attribute1 != '':
                args.append(float(command.entry_attribute1))
            else:
                args.append(command.entry_attribute1)
                

        try:
            listeVariable.index(command.entry_attribute2)
            args.append(globals()[command.entry_attribute2])
        except:
            if command.entry_attribute2 != '':
                args.append(float(command.entry_attribute2))
            else:
                args.append(command.entry_attribute2)

        try:
            listeVariable.index(command.entry_attribute3)
            args.append(globals()[command.entry_attribute3])
        except:
            if command.entry_attribute3 != '':
                args.append(float(command.entry_attribute3))
            else:
                args.append(command.entry_attribute3)

        try:
            listeVariable.index(command.entry_attribute4)
            args.append(globals()[command.entry_attribute4])
        except:
            if command.entry_attribute4 != '':
                args.append(float(command.entry_attribute4))
            else:
                args.append(command.entry_attribute4)

        try:
            listeVariable.index(command.entry_attribute5)
            args.append(globals()[command.entry_attribute5])
        except:
            if command.entry_attribute5 != '':
                args.append(float(command.entry_attribute5))
            else:
                args.append(command.entry_attribute5)

        try:
            listeVariable.index(command.entry_attribute6)
            args.append(globals()[command.entry_attribute6])
        except:
            if command.entry_attribute6 != '':
                args.append(float(command.entry_attribute6))
            else:
                args.append(command.entry_attribute6)

        try:
            listeVariable.index(command.entry_attribute7)
            args.append(globals()[command.entry_attribute7])
        except:
            if command.entry_attribute7 != '':
                args.append(float(command.entry_attribute7))
            else:
                args.append(command.entry_attribute7)

        args.append(command.combo_attribute1)
        args.append(command.combo_attribute2)
        args.append(command.combo_attribute3)
        args.append(command.combo_attribute4)
        args.append(command.combo_attribute5)
        args.append(command.combo_attribute6)
        args.append(command.combo_attribute7)

        return(args)

    def runScript(self, args=None):
    #This method generates the executable liste and run it
        result = ""

        if self.analyzeCommand() != -1:
            self.view.scriptState = "RUN"

            for item in self.listeExecutable:  
                while self.view.scriptState == "PAUSE":
                    None

                if self.view.scriptState == "NEXT":
                    self.view.scriptState = "PAUSE"
                    self.view.button_runScript.config(image=self.view.pauseImg)
                    result = item[0](item[1])  
                    self.view.button_runScript.config(image=self.view.playImg)

                elif self.view.scriptState == "STOP":
                    break
                
                else:
                    result = item[0](item[1])    

                if result == "ERROR":
                    break

            for item in self.listeCommand:
                item.state = "FREE"
                item.forstate = 0
    
        self.view.scriptState = "STOP"
        self.view.button_runScript.config(image=self.view.playImg)