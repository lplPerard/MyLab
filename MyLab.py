"""Copyright Oticon Medical NICE

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2021/07/08 Software creation 

File description : Application Launcher

"""

from Controller import Controller
import sys
import os

if __name__ == "__main__":

    path = ""
    company_name = 'Oticon medical'
    product_version = '0.0'
    product_name = 'MyLab_V' + product_version
    
    if len(sys.argv) > 1:
        path = sys.argv[1]

    controller = Controller(path)
    