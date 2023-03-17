# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import (fft, ifft)

from test_lists import seqmatch
from sys import platform
from platform import node

def comparer(a1, a2, i1, i2, maxgap):
    return abs(a1[i1] - a2[i2]) <= maxgap

def plotlins(lins, codcolor):
    for ili in range(len(lins)):
        ptsinline = [[xs[ipt] for ipt in lins[ili]],
                     [ ys[ipt] for ipt in lins[ili]]]
        plt.plot( ptsinline[0], ptsinline[1], color=codcolor,
                 linewidth=0.5, ls='-')
# ======================================================================

# Lembrar como escolher de que forma os plots devem aparecer no IPython:
# %matplotlib inline
# %matplotlib qt (= em nova janela)

if platform.startswith('linux'):
    flocalprefix = r'/home/marcelo/wolkesicher/ipen/Genie2k/Camfiles/Pni/2012_Ago/'
else:
    if node() == 'mmaduar-net3':
        flocalprefix = r'/Users/mmaduar/wolkesicher/Python_Scripts/OpenGRay/spyd1/'
    else:
        flocalprefix = r'/Users/Marcelo/wolkesicher/Python_Scripts/OpenGRay/spyd1/'
    
# flocalname = flocalprefix + 'lran12910.iec'
# flocalname = flocalprefix + 'ctp1404.iec'
flocalname = flocalprefix + 'ctp1508.iec'

fi = open(flocalname, 'r')

lins = fi.readlines()
fi.close()

inidat = 1
for lin in lins:
    if lin.find(r'A004USERDEFINED') == 0:
        break
    inidat += 1
    
cnts = []
itr = list(range( inidat, len(lins) ))
for ilin in itr:
    cnts.append( int(lins[ilin][10:20]) )
    cnts.append( int(lins[ilin][20:30]) )
    cnts.append( int(lins[ilin][30:40]) )
    cnts.append( int(lins[ilin][40:50]) )
    cnts.append( int(lins[ilin][50:60]) )
del itr
del lins

# x2 = range(len(cnts))
xchan = np.linspace(0, len(cnts)-1, len(cnts))
ycont = np.asarray(cnts)

# 2016-03-02: Usando funcoes de SciPy para picos e espectros:

# 2016-03-01 Bons valores para widths e min_snr

# C'alculo...
# detre = signal.detrend(ycont)
# ... e gr'afico
# plt.figure(figsize=(12,8))
# plt.plot(detre)
# plt.title("Detren(ycont)")
# plt.show

# C'alculo...
# Para os meus espectros, o par^ametro expect_width= 4 ou 5 
# s~ao os que d~ao mais picos

# 2017-

offs = 0
ends = 4000
ycont_part = ycont[offs:ends]
xchan_part = xchan[offs:ends]

expect_width = 7
widths = np.arange(1, 2*expect_width)

indicescwt = signal.find_peaks_cwt(ycont_part, widths, max_distances=widths/4,
                                   gap_thresh=2.0, min_snr=2.0)
print(r'indicescwt:', expect_width, indicescwt)

nscal = 2*expect_width-1
scals = np.arange(1, nscal + 1)
cwtmatr = signal.cwt(ycont_part, signal.ricker, scals)

# ... e gr'afico

# 2017-07-07: Reativar depois. Desativei os plots s'o para fazer benchmarking 
# dos c'alculos

# plt.figure(figsize=(12,8))
# plt.plot(xchan, ycont)
# plt.title("Original spectrum")
# plt.show()

# plt.figure(figsize=(12,8))
# plt.plot(xchan_part, ycont_part)
# plt.title("CWT-found peaks")
# pyplot.plot(indicescwt5, ycont[indicescwt5], 'go', fillstyle='none', ms=15)
# plt.plot(indicescwt+offs, ycont_part[indicescwt], 'r^', fillstyle='none', ms=10)
# 2017-06-28 Gr'afico dos coeficiente cwt para dada escala
scalmin = 0 
scalmed = expect_width-1 
scalmax = 2*expect_width - 2
# plt.plot(xchan_part, cwtmatr[scalmin], xchan_part, cwtmatr[scalmax], xchan_part, cwtmatr[scalmed])

# grafico cwt: mapa de 
# plt.figure(figsize=(12,8))
# plt.imshow(cwtmatr, extent=[-1, 1, nscal, 1], cmap='PRGn', aspect='auto', 
#           vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
# plt.show()

# =====================================