"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Climatic Chamber Controller.

"""


from Autospacer import Autospacer
import serial
import time
import string

class AutospacerController():
    """Class containing the PowerSupplyController for MyLab.

    """

    def __init__(self, view=None, term=None, instrument=None, model=None):
    #Constructor for the Controller class   

        self.view = view  
        self.term = term
        self.model = model

        self.instrument = Autospacer()
        if instrument != None:
            self.instrument = instrument
    
    def updateView(self, view):
    #Setter method for view attribute
        self.view = view

    def connectToDevice(self, adress):
        try:
            self.resource = serial.Serial(adress[:5], 115200, timeout=1)
        
        except:
            self.view.view.sendError('010')


    def selectMagnet(self, args=[]):
	#decrements by 1 step
        try:
            tmp = "Magnet" + args[7]
            self.resource.write(tmp.encode())
            time.sleep(1)

            read = self.resource.readline()
            read = read.decode('utf-8')
            
            if(read[:3] != "ACK"):
                self.view.view.sendError('500')
                return("ERROR")

        except:
            self.view.view.sendError('011')
            return("ERROR")

    def placeMagnet(self, args=[]):
	#Launch autoZero procedure
        try:
            tmp = "Place" + args[7]
            self.resource.write(tmp.encode())
            time.sleep(1)

            read = self.resource.readline()
            read = read.decode('utf-8')
            
            if(read[:3] != "ACK"):
                self.view.view.sendError('500')
                return("ERROR")

        except:
            self.view.view.sendError('011')
            return("ERROR")

    def calibrate(self, args=[]):
	#define a new zero
        try:
            tmp = "calibration"
            self.resource.write(tmp.encode())
            time.sleep(1)

            read = self.resource.readline()
            read = read.decode('utf-8')
            
            if(read[:3] != "ACK"):
                self.view.view.sendError('500')
                return("ERROR")

        except:
            self.view.view.sendError('011')
            return("ERROR")

    def setDistance(self, args=[]):
	#go to a specific distance
        try:
            tmp = "Distance" + args[0]
            self.resource.write(tmp.encode())
            time.sleep(1)

            read = self.resource.readline()
            read = read.decode('utf-8')
            
            if(read[:3] != "ACK"):
                self.view.view.sendError('500')
                return("ERROR")

        except:
            self.view.view.sendError('011')
            return("ERROR")