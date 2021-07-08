"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Controller.

"""


from View import View
from Model import Model

class Controller():
    """Class containing the Controller for the CBRAM software.

    """

    def __init__(self):
    #Constructor for the Controller class

        self.view = View()
        self.view.mainloop()
        self.model = Model()
        self.__initModel()

    def __initModel(self):
    #This method initialize the Model
        print("bla")