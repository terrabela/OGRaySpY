# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 11:42:20 2017

@author: Marcelo
"""

import sqlite3 as sqlite

# ========================================================================
# cria o db \wolkesicher\Python_Scripts\sqlite/spectrum1.db
# e conecta

class SpectrumDb():
#    def setUp(self):
    def __init__(self, dbname):
        self.con = sqlite.connect( dbname )
        self.cur = self.con.cursor()
        self.cur.execute("""
                         CREATE TABLE peaks (
                           id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                           pkCentroid FLOAT,
                           fwhm FLOAT,
                           height FLOAT,
                           fittedheight FLOAT,
                           isusedforcalib BOOL
                           );
                         """)
        print('Tabela criada com sucesso.')
        self.con.close()
