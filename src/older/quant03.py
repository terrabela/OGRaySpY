# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# import numpy as np
import matplotlib.pyplot as pl 
from ioiecspec import readiecsp, SumSpectra

# counts = readiecsp(r'Madu/Python_Scripts/spyd1/ctp0303.IEC')

# fnheader = r'mmaduar/Python_Scripts/spyd1/lran12910.IEC'
# fnparcial1 =  r'mmaduar/Python_Scripts/spyd1/lran12910.IEC'
# fnparcial2 =  r'mmaduar/Python_Scripts/spyd1/lran12910.IEC'
# fnsum =  r'mmaduar/Python_Scripts/spyd1/lran12910double.IEC'

fnheader = r'mmaduar/Python_Scripts/spyd1/lixicubc.IEC'
fnparcial1 =  r'mmaduar/Python_Scripts/spyd1/lixicubc.IEC'
fnparcial2 =  r'mmaduar/Python_Scripts/spyd1/lixicubc2.IEC'
fnsum =  r'mmaduar/Python_Scripts/spyd1/lixicubsoma.IEC'

counts, lt, rt = readiecsp( fnparcial1 )

# counts = readiecsp(r'Madu/Python_Scripts/spyd1/lran12910.IEC')
SumSpectra ( fnheader, fnparcial1, fnparcial2, fnsum )

pl.figure()
pl.yscale('log')
pl.plot( counts )

nch = len( counts )
ch = list(range(nch))
