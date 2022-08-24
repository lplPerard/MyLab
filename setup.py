# -*- coding: utf-8 -*-

# A simple setup script to create an executable using Cx_Freeze.

#Execute : python setup.py build bdist_msi 

import sys
from cx_Freeze import setup, Executable

Developer = 'LucPerard'
product_version = '2.0'
product_name = 'MyLab'

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "MyLab",                  # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]MyLab.exe",   # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

extensions = [
        # open / print / view text files
        {
            "extension": "mylab",
            "verb": "open",
            "executable": "MyLab.exe",
            "context": "Open with MyLab",
        }
        ]

bdist_msi_options = {'upgrade_code': '{48B079F4-B598-438D-A62A-8A233A3F8901}',
                     'add_to_path': False,
                     'initial_target_dir': r'C:\%s' % (product_name),
                     'target_name': product_name,
                     'install_icon': 'Images/icon2.ico',
                     'extensions': extensions,
                     'data': {"Shortcut":shortcut_table}
                    }

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

includefiles = ['Configuration/',
                'Drivers/',
                'Results/',
                'Logs/',
                'Instruments/',
                'Images/']

executables = [
    Executable('MyLab.py', base=base, icon='Images/icon2.ico')
]

setup(name=product_name,
      version=product_version,
      author='Luc PERARD',
      options = {'build_exe': {'include_files':includefiles}, 'bdist_msi': bdist_msi_options},    
      executables=executables
      )