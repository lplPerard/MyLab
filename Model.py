"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the application's Model

"""
import json
import jsonpickle

class Model():
    """Class containing the Model for the Mylab according to the MCV model.

    """

    def __init__(self, controller):
    #Constructor for the Model class
        """
            Constructor for the class Model. 
            The following attributes are  created :

        """
        self.controller = controller

        with open("Error.json") as f:
            self.error_dict = json.load(f)
            f.close()

        with open("Metadata.json") as f:
            self.meta_dict = json.load(f)
            f.close()

        with open("Devices.json") as f:
            self.devices_dict = json.load(f)
            f.close()

        with open("Parameters.json") as f:
            self.parameters_dict = json.load(f)
            f.close()

    def actualizeModel(self):
    #This method actualize the parameters_dict 
        with open(self.parametersFile) as f:
            self.parameters_dict = json.load(f)
            f.close()

        with open("Error.json") as f:
            self.error_dict = json.load(f)
            f.close()

    def saveConfiguration(self, listeInstruments, listeCommand, path):
        listejson = [listeInstruments, listeCommand]
        if (path != "") and (path[-5:] != "mylab"):
            File  = open(path + ".mylab", 'w')                   
            listeInstrumentsJSON = jsonpickle.encode(listejson, unpicklable=True)
            json.dump(listeInstrumentsJSON, File, indent=4)   

        if (path != "") and (path[-5:] == "mylab"):  
            File  = open(path, 'w')         
            listeInstrumentsJSON = jsonpickle.encode(listejson, unpicklable=True)
            json.dump(listeInstrumentsJSON, File, indent=4)  

        File.close()
    
    def openConfiguration(self, path):
    #This method import a serialized object result into the software
        if path != "":
            File = open(path, 'r')
            listejson = json.load(File)
            File.close()
            
            listejson = jsonpickle.decode(listejson)
            return(listejson)
