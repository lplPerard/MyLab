"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Climatic Chamber Controller.

"""


from ClimaticChamber import ClimaticChamber
import serial
import time
import string

class VT4002():
    """Class containing the PowerSupplyController for MyLab.

    """

    def __init__(self, view=None, term=None, instrument=None):
    #Constructor for the Controller class   

        self.view = view  
        self.term = term

        self.instrument = ClimaticChamber()
        if instrument != None:
            self.instrument = instrument
    
    def updateView(self, view):
    #Setter method for view attribute
        self.view = view

    def connectToDevice(self, adress):
        try:
            self.resource = serial.Serial(adress, 9600, timeout=3)
        
        except:
            self.view.sendError('010')

    def setTemperature(self, args=[]):
	#Sets the temperature as temp 
        try:
            nominal_temp_string = "$00E " + str(args[0]) + "\r\n"
            self.resource.write(nominal_temp_string.encode()) 
        except:
            self.view.view.sendError('011')
            return("ERROR")
        

    def getTemperature(self):
    #Gets the temperature in the climatic chamber
        try:
            tmp = "$00I\r\n"
            self.resource.write(tmp.encode())
            line = self.resource.readline()
            line = line.decode('utf-8')
            line = line.split(' ')
            self.instrument.result = float(line[1])
            self.instrument.measure["temperature"] = [float(line[1])]
            return(float(line[1]))

        except:
            self.view.view.sendError('011')
            return("ERROR")