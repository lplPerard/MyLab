"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for ScriptController.

"""

from tkinter.constants import END
from datetime import datetime
from numpy import arange, array
import time
import csv
import sys
import os


class ScriptController():
    """Class containing the decoder for scripts.

    """

    def __init__(self):

        self.listeCommand = []
        self.listeExecutable = []
        self.view=None
        self.instrument = None
        self.root = None
        self.fileName = ""
        self.logArray = []

        self.progress = 0

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
            item.state = "FREE"
            item.ifstate = 0
            item.forstate = 0
        
        for item in self.listeCommand:
            command=None
            if (item.combo_choice1 == "WAIT") and (item.state != "RUN"):
                tmp = self.generateWaitCommand(item)                
                self.listeExecutable.append(tmp)
                item.state = "RUN"

            if (item.combo_choice1 == "STORE") and (item.state != "RUN"):
                tmp = self.generateStoreCommand(item)                
                self.listeExecutable.append(tmp)
                item.state = "RUN"

            if (item.combo_choice1 == "LOG") and (item.state != "RUN"):
                tmp = self.generateLogCommand(item)                
                self.listeExecutable.append(tmp)
                item.state = "RUN"

            if (item.combo_choice1 == "IF") and (item.state != "RUN"):
                error = self.generateIfCommand(self.listeCommand.index(item))            
                self.listeExecutable.append(error)
                item.state = "RUN"

            elif (item.combo_choice1 == "FOR") and (item.state != "RUN"):
                error = self.generateForCommand(self.listeCommand.index(item))         
                self.listeExecutable.extend(error)
                item.state = "RUN"

            elif (item.state != "RUN") and (item.combo_choice1 != "END"):
                self.getInstrument(name = item.combo_choice1)
                self.listeExecutable.append([getattr(self.instrument, item.combo_instrCommand), [item, "INSTR"]])
                item.state = "RUN"
        
        for item in self.listeCommand:
            item.ifstate = 0
            item.forstate = 0
                
        return(error)

    def generateWaitCommand(self, command):
    #This method generates a for fucntion    
        def func(args=[]) :
            try:
                duration = globals()[args[0]]
            except:
                duration = float(args[0])

            sys.stdout("I wait for : " + str(duration))
            time.sleep(duration)

        if (command.breakpoint == 0):
            args=[command.entry_attribute1, "", ""]
        elif (command.breakpoint == 1):
            args=[command.entry_attribute1, "", "BREAKPOINT"]

        return([func, args])

    def generateStoreCommand(self, command):
    #This method generates a store function  
        self.getInstrument(command.combo_instrCommand)

        def func(args=[]):
            sys.stdout("result from instr : " + str(self.instrument.instrument.result))            
            globals()[args[0]] = self.instrument.instrument.result
            sys.stdout("I stored : " + str(globals()[args[0]]))

        if (command.breakpoint == 0):
            args=[command.entry_attribute1, "", ""]
        elif (command.breakpoint == 1):
            args=[command.entry_attribute1, "", "BREAKPOINT"]

        return([func, args])

    def generateLogCommand(self, command):
    #This method generates a store function  
        def func(args=[]):       
            self.getInstrument(command.combo_instrCommand)
            
            try:
                data = globals()[args[0]]
            except:
                data = self.instrument.instrument.measure[args[0]]

            name = self.instrument.instrument.name + '-' + args[0]

            self.addData(data, name)

        if (command.breakpoint == 0):
            args=[command.combo_attribute1, "NOTE", ""]
        elif (command.breakpoint == 1):
            args=[command.combo_attribute1, "NOTE", "BREAKPOINT"]

        return([func, args])

    def initVariable(tmp, args=[]):
    #This function can init a variable in script during execution
        globals()[args[0]] = args[1]

    def incVariable(tmp, args=[]):
    #This function can increment a variable in script during execution
        globals()[args[0]] = globals()[args[0]] + args[1]

    def generateIfCommand(self, index=None, ifstate=0):
    #This method generate a IF functions 
        subListExe = []
        end = 0
        endIndex = index+1
        command=None
        
        for item in self.listeCommand[index+1:]:
            ind=self.listeCommand.index(item)
            if (item.combo_choice1 == "IF") and (self.listeCommand[ind].ifstate <= ifstate):
                self.listeCommand[ind].state = "RUN"
                self.listeCommand[ind].ifstate = ifstate
                command = self.generateIfCommand(index=ind, ifstate=ifstate+1)

            elif (item.combo_choice1 == "ENDIF") and (self.listeCommand[ind].ifstate <= ifstate):
                self.listeCommand[ind].state = "RUN"
                self.listeCommand[ind].ifstate = ifstate
                endIndex = ind
                end = 1
                break

            elif (self.listeCommand[ind].ifstate <= ifstate) :
                self.listeCommand[ind].ifstate = ifstate

        if end!=0:

            subListeCommand = self.listeCommand[index+1:endIndex]
            
            for item in subListeCommand :
                if item.ifstate < ifstate:
                    item.ifstate=ifstate
                    
                if (item.combo_choice1 == "WAIT") and (item.ifstate == ifstate):
                    tmp=self.generateWaitCommand(item)
                    subListExe.append(tmp)
                    
                elif (item.combo_choice1 == "IF") and (item.ifstate == ifstate):
                    subListExe.append(command)
                    
                elif (item.combo_choice1 == "FOR") and (item.ifstate == ifstate):
                    tmp=self.generateForCommand(self.listeCommand.index(item))
                    subListExe.extend(tmp)
                    
                elif (item.combo_choice1 == "STORE") and (item.ifstate == ifstate):
                    tmp = self.generateStoreCommand(item)                
                    subListExe.append(tmp)
                    
                elif (item.combo_choice1 == "LOG") and (item.ifstate == ifstate):
                    tmp = self.generateLogCommand(item)                
                    subListExe.append(tmp)
                    
                elif (item.combo_choice1 == "END") and (item.ifstate == ifstate):
                    None

                elif (item.ifstate == ifstate):
                    self.getInstrument(name = item.combo_choice1)
                    subListExe.append([getattr(self.instrument, item.combo_instrCommand), [item, "INSTR"]])
                                    
            for item in subListeCommand :
                item.state = "RUN"
                
            self.listeCommand[index+1:endIndex] = subListeCommand

            def func(args=[]):
                try:
                    variable1 = globals()[args[0]]
                except:
                    variable1 = float(args[0])

                try:
                    variable2 = globals()[args[1]]
                except:
                    variable2 = float(args[1])

                operator=args[2]

                if operator == "==":
                    if variable1 == variable2:
                        self.runSubScript(args[3])
                elif operator == "!=":
                    if variable1 != variable2:
                        self.runSubScript(args[3])
                elif operator == ">=":
                    if variable1 >= variable2:
                        self.runSubScript(args[3])
                elif operator == "<=":
                    if variable1 <= variable2:
                        self.runSubScript(args[3])
                elif operator == "<":
                    if variable1 < variable2:
                        self.runSubScript(args[3])
                elif operator == ">":
                    if variable1 > variable2:
                        self.runSubScript(args[3])

            if (self.listeCommand[index].breakpoint == 0):
                args=[self.listeCommand[index].entry_attribute1, self.listeCommand[index].entry_attribute2, self.listeCommand[index].combo_attribute1, subListExe, "", ""]
            elif (self.listeCommand[index].breakpoint == 1):
                args=[self.listeCommand[index].entry_attribute1, self.listeCommand[index].entry_attribute2, self.listeCommand[index].combo_attribute1, subListExe, "", "BREAKPOINT"]

            return([func, args])

        else :
            self.root.sendError("102")
            return(-1)

    def generateForCommand(self, index=None, forstate=0):
    #This method generate a For function
        subListExe = []
        end = 0
        endIndex = index+1
        commandFor=[]

        for item in self.listeCommand[index+1:]:
            ind=self.listeCommand.index(item)
            if (item.combo_choice1 == "FOR") and (self.listeCommand[ind].forstate <= forstate):
                self.listeCommand[ind].state = "RUN"
                self.listeCommand[ind].forstate = forstate
                commandFor.append(self.generateForCommand(index=ind, forstate=forstate+1))

            elif (item.combo_choice1 == "END") and (self.listeCommand[ind].forstate <= forstate):
                self.listeCommand[ind].state = "RUN"
                self.listeCommand[ind].forstate = forstate
                endIndex = ind
                end = 1
                break

            elif (self.listeCommand[ind].forstate <= forstate) :
                self.listeCommand[ind].forstate = forstate

        if end != 0:
            subListeCommand = self.listeCommand[index+1:endIndex]

            start = float(self.listeCommand[index].entry_attribute1)
            step = float(self.listeCommand[index].entry_attribute2)
            num = float(self.listeCommand[index].entry_attribute3)
            togothrough = arange(0,num)*step+start

            subListExe.append([self.initVariable, [self.listeCommand[index].combo_instrCommand, start, "", ""]])    

            for _ in togothrough:
                NbFor = 0
                for item in subListeCommand :
                    ind=self.listeCommand.index(item)

                    if (item.combo_choice1 == "WAIT") and (item.forstate == forstate) and (item.ifstate < 666):
                        tmp=self.generateWaitCommand(item)
                        subListExe.append(tmp)

                    elif (item.combo_choice1 == "IF") and (item.forstate == forstate) and (item.ifstate < 666):
                        tmp = self.generateIfCommand(index=ind, ifstate=666)
                        subListExe.append(tmp)

                    elif (item.combo_choice1 == "STORE") and (item.forstate == forstate) and (item.ifstate < 666):
                        tmp = self.generateStoreCommand(item)                
                        subListExe.append(tmp)

                    elif (item.combo_choice1 == "LOG") and (item.forstate == forstate) and (item.ifstate < 666):
                        tmp = self.generateLogCommand(item)                
                        subListExe.append(tmp)

                    elif (item.combo_choice1 == "ENDIF") and (item.forstate == forstate) and (item.ifstate < 666):
                        None
                        
                    elif (item.combo_choice1 == "FOR") and (item.forstate == forstate) and (item.ifstate < 666):
                        subListExe.extend(commandFor[NbFor])
                        NbFor+=1

                    elif (item.forstate == forstate) and (item.ifstate == 0):
                        self.getInstrument(name = item.combo_choice1)
                        subListExe.append([getattr(self.instrument, item.combo_instrCommand), [item, "INSTR"]])
                        
                subListExe.append([self.incVariable, [self.listeCommand[index].combo_instrCommand, step, "", ""]])   
                
            for item in subListeCommand :
                item.state = "RUN"
                
            self.listeCommand[index+1:endIndex] = subListeCommand

            if forstate != 0:
                return(subListExe)
            else:
                return(subListExe)

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
        listeVariable = ["Temperature", "Voltage", "Current", "Frequency", "Power", "Period", "Time", "Distance", "Temperature2", "Voltage2", "Current2", "Frequency2", "Power2", "Period2", "Time2", "Distance2", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "La_Réponse_D"]

        try:
            listeVariable.index(command.entry_attribute1)
            args.append(globals()[command.entry_attribute1])
        except:
            if type(command.entry_attribute1) != type(""):
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

        if (command.breakpoint == 0):
            args.append("")
            args.append("")
        elif (command.breakpoint == 1):
            args.append("")
            args.append("BREAKPOINT")

        return(args)

    def runScript(self, args=None):
    #This method generates the executable liste and run it
        listeVariable = ["Temperature", "Voltage", "Current", "Frequency", "Power", "Period", "Time", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "La_Réponse_D"]
        
        now = datetime.now()
        self.fileName = now.strftime(self.view.path + "%d-%m-%Y-%Hh%Mmn%Ss.csv")
        self.log = False

        for variable in listeVariable:
            globals()[variable] = 0

        result = ""

        if self.analyzeCommand() != -1:
            self.view.scriptState = "RUN"

            progressLength = len(self.listeExecutable)
            currentProgress = 0

            for item in self.listeExecutable:   
                self.progress = 1
                if item[1][-1] == "INSTR":
                    item[1] = self.getArgs(item[1][0])

                sys.stdout(item)
                sys.stdout("")

                if item[1][-1] == "BREAKPOINT":
                    self.view.scriptState = "PAUSE"
                    self.view.button_runScript.config(image=self.view.playImg)

                while self.view.scriptState == "PAUSE":
                    None

                if self.view.scriptState == "NEXT":
                    self.view.scriptState = "PAUSE"
                    self.view.button_runScript.config(image=self.view.pauseImg)
                    try:
                        result = item[0](item[1])  
                        if item[1][-2] != "":
                            self.log = True
                    except:
                        sys.stdout("\nProblem during execution")
                        sys.stdout("Script ended with problem during execution\n")
                        break
                    self.view.button_runScript.config(image=self.view.playImg)

                elif self.view.scriptState == "STOP":
                    break
                
                else:
                        result = item[0](item[1])  
                        if item[1][-2] != "":
                            self.log = True

                if result == "ERROR":
                    sys.stdout("\nAn error occured during exucution, please open terminal for more details\n")
                    break

                currentProgress = currentProgress + 1
                self.progress = (currentProgress/progressLength)*100
                sys.stdout("\n")

            for item in self.listeCommand:
                item.state = "FREE"
                item.forstate = 0

            self.progress = 0
    
        self.view.scriptState = "STOP"
        self.view.button_runScript.config(image=self.view.playImg)
        sys.stdout("\n-------------------------------------------Script ended-------------------------------------------\n")

        if self.log :
            self.export2CSV()
            self.logArray=[]

    def runSubScript(self, subListExe=[]):
    #This method execute a script from a specific execution list
        progressLength = len(subListExe)
        currentProgress = 0

        for item in subListExe:  
            if item[1][-1] == "INSTR":
                item[1] = self.getArgs(item[1][0])            

            sys.stdout(item)
            sys.stdout("\n")

            if item[1][-1] == "BREAKPOINT":
                self.view.scriptState = "PAUSE"
                self.view.button_runScript.config(image=self.view.playImg)

            while self.view.scriptState == "PAUSE":
                None

            if self.view.scriptState == "NEXT":
                self.view.scriptState = "PAUSE"
                self.view.button_runScript.config(image=self.view.pauseImg)
                try:
                    result = item[0](item[1])  
                    if item[1][-2] != "":
                        self.log = True
                except:
                    sys.stdout("\nProblem during sub-execution\n")
                    sys.stdout("\nScript execution ended with problem during execution\n")
                    break
                self.view.button_runScript.config(image=self.view.playImg)

            elif self.view.scriptState == "STOP":
                break
            
            else:
                try:
                    result = item[0](item[1]) 
                    if item[1][-2] != "":
                        self.log = True
                except:
                    sys.stdout("\nProblem during sub-execution\n")
                    sys.stdout("\nScript execution ended with a problem during execution\n")
                    break

            if result == "ERROR":
                break

            currentProgress = currentProgress + 1
            self.progress = (currentProgress/progressLength)*100
            sys.stdout("")

    def export2CSV(self):
    #This method is used to track data in output csv file      
        file = open(self.fileName, "w")
        
        try:
            writer = csv.writer(file)             

            length = len(self.logArray[0])
            for index in range(length) :
                line=[]
                for column in self.logArray:
                    line.append(column[index]) 
                writer.writerow(line)
                    
        finally:
            file.close()

    def addColumn(self, name):
        found = 0
        for column in self.logArray :
            if column[0] == name:
                found = 1
                break

        if found == 0:    
            self.logArray.append([name])
            length = len(self.logArray[0])
            for _ in range(length-1):
                self.logArray[-1].append('')

    def addData(self, data, name):
        self.addColumn(name)
        index=0

        for column in self.logArray :
            if column[0] == name:
                if column[-1] == '':
                    column[-1] = data
                else:                
                    for column1 in self.logArray :
                        if column1[0] != name:
                            column1.append('')
                        else:
                            column1.append(data)