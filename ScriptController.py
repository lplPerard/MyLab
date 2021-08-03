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
        self.listeCommand = self.view.getListeCommand().copy()
        command=None
        
        for item in self.listeCommand:
            command=None
            if item.combo_choice1 == "WAIT":
                self.generateWaitCommand(item.entry_attribute1)
                item.combo_choice1 = "PASS"

            elif item.combo_choice1 == "FOR":
                self.generateForCommand(self.listeCommand.index(item))
                item.combo_choice1 = "PASS"

            elif item.combo_choice1 != "PASS":
                self.getInstrument(name = item.combo_choice1)
                self.listeExecutable.append([getattr(self.instrument, item.combo_instrCommand), self.getArgs(command=item)])
                item.combo_choice1 = "PASS"
                
    def generateWaitCommand(self, duration):
    #This method generates a for fucntion    

        def func(args=[duration]) :
            print("I wait for : " + duration)
            time.sleep(float(duration))
            print("I waited for : " + duration)

        args=[duration]
        self.listeExecutable.append([func, args])

    def generateForCommand(self, index=None):
    #This method generate a For function
        end = 0
        endIndex = None

        for item in self.listeCommand[index+1:]:
            ind=self.listeCommand.index(item)
            print(ind)
            if item.combo_choice1 == "FOR":
                command = self.generateForCommand(ind)
                self.listeCommand[ind].combo_choice1 = "PASS"

            elif item.combo_choice1 == "END":
                self.listeCommand[ind].combo_choice1 = "PASS"
                endIndex = ind
                end = 1
                break

        if end != 0:
            subListeCommand = self.listeCommand[index+1:endIndex]

            start = float(self.listeCommand[index].entry_attribute1)
            step = float(self.listeCommand[index].entry_attribute2)
            num = float(self.listeCommand[index].entry_attribute3)
            togothrough = arange(0,num)*step+start

            for globals()[self.listeCommand[index].combo_instrCommand] in togothrough:
                for item in subListeCommand :
                    print(item.combo_choice1)
                    if item.combo_choice1 == "WAIT":
                        self.generateWaitCommand(item.entry_attribute1)

                    elif item.combo_choice1 != "PASS":
                        self.listeExecutable.append([getattr(self.instrument, item.combo_instrCommand), self.getArgs(command=item)])
                
            for item in subListeCommand :
                item.combo_choice1 = "PASS"

            self.listeCommand[index+1:endIndex] = subListeCommand

        else :
            self.root.sendError("101")

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
        args = [14]
        listeVariable = ["Temperature", "Voltage", "Current", "Frequency", "A", "B", "C", "D", "E", "F", "G"]

        index = listeVariable.index(command.entry_attribute1)
        if index != ValueError:
            args[0] = globals()[listeVariable[index]]
        else:
            args[0] = float(command.entry_attribute1)

        index = listeVariable.index(command.entry_attribute2)
        if index != ValueError:
            args[1] = globals()[listeVariable[index]]
        else:
            args[1] = float(command.entry_attribute2)

        index = listeVariable.index(command.entry_attribute3)
        if index != ValueError:
            args[2] = globals()[listeVariable[index]]
        else:
            args[2] = float(command.entry_attribute3)

        index = listeVariable.index(command.entry_attribute4)
        if index != ValueError:
            args[3] = globals()[listeVariable[index]]
        else:
            args[3] = float(command.entry_attribute4)

        index = listeVariable.index(command.entry_attribute5)
        if index != ValueError:
            args[4] = globals()[listeVariable[index]]
        else:
            args[4] = float(command.entry_attribute5)

        index = listeVariable.index(command.entry_attribute6)
        if index != ValueError:
            args[5] = globals()[listeVariable[index]]
        else:
            args[5] = float(command.entry_attribute6)

        index = listeVariable.index(command.entry_attribute7)
        if index != ValueError:
            args[6] = globals()[listeVariable[index]]
        else:
            args[6] = float(command.entry_attribute7)

    def runScript(self):
    #This method generates the executable liste and run it
        self.analyzeCommand()

        for item in self.listeExecutable:    
            item[0](item[1])    
        

