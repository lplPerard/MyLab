"""Copyright Oticon Medical NICE

Developped by : Luc PERARD
Version : 1.2.1
Details : 
    - 2021/07/08 Software creation 

File description : Application Launcher

"""


from Controller import Controller
import sys

if __name__ == "__main__":

    path = ""
    
    if len(sys.argv) > 1:
        path = sys.argv[1]

    controller = Controller(path)