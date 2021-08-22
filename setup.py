# -*- coding: utf-8 -*-

# A simple setup script to create an executable using Cx_Freeze.

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

includefiles = ['Parameters.json', 'Metadata.json', 'Error.json', 'Devices.json',
                'NIVISA_19.5.exe', 'GPIB_Driver.exe','Keysight_Driver.exe''ReadMe.txt',
                'HMC8042.png', '2220-30-1.png', 'VT4002_EMC.png', '33500B.png', '8845A.png', 'E3642A.png', '2400.png',
                'RTM1054.png', 'RTM3004.png', 'MSO2014.png', 'HMO3004.png', 'DL9040.png',
                'icon.ico', 'diode.png', 'diode_grey.png', 'continuity.png', 'continuity_grey.png', 'delete.png', 'play.png', 'pause.png', 'next.png', 'stop.png', 'empty.png', 'breakpoint.png', 'sine.png', 'snapper.png']

executables = [
    Executable('MyLab.py', base=base, icon='icon2.ico')
]

setup(name='MyLab',
      version='0.0',
      author='Luc PERARD',
      options = {'build_exe': {'include_files':includefiles}},    
      executables=executables
      )