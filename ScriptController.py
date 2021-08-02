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
        self.view=view
        self.root = self.view.root

    def analyzeCommand(self):
        self.listeCommand = self.view.getListeCommand().copy()
        command=None
        
        for item in self.listeCommand:
            if item.combo_choice1 == "WAIT":
                command = self.generateWaitCommand(item.entry_attribute1)
                item.combo_choice1 = "PASS"
            elif item.combo_choice1 == "FOR":
                command = self.generateForCommand(self.listeCommand.index(item))
                item.combo_choice1 = "PASS"
            elif item.combo_choice1 != "PASS":
                self.getInstrument(name = item.combo_choice1)
                command = [getattr(self.instrument, item.combo_instrCommand), self.getArgs(command=item)]
                item.combo_choice1 = "PASS"
                

            self.listeExecutable.append(command)

    def generateWaitCommand(self, duration):

        def func(args=[duration]) :
            print("I wait")
            time.sleep(float(duration))
            print("I waited")

        args=[duration]
        return([func, args])

    def generateForCommand(self, index=None):
        listeFor = []
        end = 0

        for item in self.listeCommand[index+1:]:
            index=self.listeCommand.index(item)
            if item.combo_choice1 == "FOR":
                command = self.generateForCommand(index + self.listeCommand[index+1:].index(item))
                self.listeCommand[index].combo_choice1 = "PASS"

            if item.combo_choice1 == "WAIT":
                command = self.generateWaitCommand(item.entry_attribute1)
                self.listeCommand[index].combo_choice1 = "PASS"

            elif item.combo_choice1 == "END":
                endIndex = self.listeCommand.index(item)
                self.listeCommand[index].combo_choice1 = "PASS"
                end = 1
                break

            elif item.combo_choice1 != "PASS":
                listeFor.append([getattr(self.instrument, item.combo_instrCommand), self.getArgs(command=item)])
                self.listeCommand[index].combo_choice1 = "PASS"

        if end != 0:
            def func(args=None):
                start=args[1]
                step=args[2]
                num=args[3]
                liste=arange(0,num)*step+start

                for globals()[args[0]] in liste:
                    index = liste.index(globals()[args[0]])
                    listeFor[index][0](listeFor[index][1])
            
            args = []

            return([func, args])

        else :
            self.root.sendError("101")

    def getInstrument(self, name=None):
        found=0
        for item in self.root.getControllerList():
            if item.instrument.name == name:
                self.instrument=item
                found = 1
                break

        if found == 0:
            self.root.sendError("100", name)

    def getArgs(self, command=None):
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
       self.analyzeCommand()

       for item in self.listeExecutable:
           print(item)
           item[0](item[1])    

