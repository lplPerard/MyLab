# -*- coding: utf-8 -*-

# A simple setup script to create an executable using Cx_Freeze.

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

includefiles = ['parameters.json', 'Metadata.json', 'Error.json', 'NIVISA_19.5']

executables = [
    Executable('MyLab.py', base=base)
]

setup(name='MyLab',
      version='0.0',
      author='Luc PERARD',
      options = {'build_exe': {'include_files':includefiles}},    
      executables=executables
      )