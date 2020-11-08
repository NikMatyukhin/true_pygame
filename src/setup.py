from cx_Freeze import setup, Executable

import os

executables = [Executable('main.py', targetName='Sein Kampf')]

includes = []
#pygame_path = list(importlib.import_module('pygame').__path__)[0]
excludes = ['email','html','http','PyQt5','unittest','test','xmlrpc','testpath','pydoc_data','notebook',
            '_pytest','asyncio','urllib3','requests','atomicwrites','certifi','cffi','defusedxml',
            'jupyter_client','jupyter_core','tornado','markupsafe','zmq','win32com','scipy','nbformat',
            'nbconvert','jedi','jinja2','IPython']

options = {
    'build_exe': {
        'includes': includes,
        'include_files': ['assets/', 'music/', 'sounds/'],# pygame_path],
        'excludes': excludes,
        'build_exe': 'Sein Kampf',
    }
}

setup(name='Sein Kampf',
      version = '1.0',
      description = 'super game',
      options = options,
      executables = executables)
