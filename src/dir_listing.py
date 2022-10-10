# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 15:10:14 2022

@author: MFMáduar
"""

# 2022-09-08: AQUI provavelmente apagarei este arquivo.
from pathlib import Path


# https://docs.python.org/3/library/pathlib.html#basic-use
# https://realpython.com/working-with-files-in-python/
# https://www.inspiredpython.com/course/pattern-matching/python-pattern-matching-examples-working-with-paths-and-files

class DirectoryList:

    def __init__(self, entries_list=[]):
        entries = Path('./../../../OwnDrive/Genie_Transfer/Filtros/2022')
        self.entries_list = list(entries.glob('**/*.*'))
