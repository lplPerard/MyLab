"""
Developped by : Luc PERARD
Version : 2.0
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