# -*- coding: utf-8 -*-
"""
cx_freeze setup script
run 'python setup.py build' to use
"""


import sys
from cx_Freeze import setup, Executable

import config

build_exe_options = {
    "include_msvcr": True,  #skip error msvcr100.dll missing
    "include_files": ['lt.log',
                      'lt.db',
                      ('plugins/Hebrew.json', 'plugins/Hebrew.json'),
                      ('plugins/English.json','plugins/English.json')]
}

base = None

if sys.platform == 'win32':
    base = "WIN32GUI"

setup(
    name=config.appname,
    version=config.appversion,
    description=config.appname,
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)])