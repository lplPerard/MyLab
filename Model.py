"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for the application's Model

"""

import json

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

        with open("parameters.json") as f:
            self.parameters_dict = json.load(f)
            f.close()

        with open("Error.json") as f:
            self.error_dict = json.load(f)
            f.close()

    def actualizeModel(self):
    #This method actualize the parameters_dict 
        with open("parameters.json") as f:
            self.parameters_dict = json.load(f)
            f.close()

        with open("Error.json") as f:
            self.error_dict = json.load(f)
            f.close()