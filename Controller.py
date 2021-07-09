"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for Controller.

"""


from View import View
from Model import Model

class Controller():
    """Class containing the Controller for MyLab.

    """

    def __init__(self):
    #Constructor for the Controller class

        self.view = View()
        self.view.mainloop()
        self.model = Model()