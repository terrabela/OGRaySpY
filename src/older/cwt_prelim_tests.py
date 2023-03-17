# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from test_lists import seqmatch
from sys import platform

def comparer(a1, a2, i1, i2, maxgap):
    return abs(a1[i1] - a2[i2]) <= maxgap

def plotlins(lins, codcolor):
    for ili in range(len(lins)):
        ptsinline = [[xs[ipt] for ipt in lins[ili]],
                     [ ys[ipt] for ipt in lins[ili]]]
        plt.plot( ptsinline[0], ptsinline[1], color=codcolor,
                 linewidth=0.5, ls='-')
# ======================================================================

# 2016-mar: Comandos bahsicos para ler e imprimir um arq texto:
#

# fi = open(r'/Users/Marcelo/Dropbox/Python_Scripts/spyd1/lran12910.iec', 'r')
# fi = open(r'/home/marcelo/Dropbox/GENIE2K/CAMFILES/Si/si2016/si00716.iec', 'r')

# Lembrar como escolher de que forma os plots devem aparecer no IPython:
# %matplotlib inline
# %matplotlib qt (= em nova janela)

if platform == 'linux':
    fi = open(r'/home/marcelo/Dropbox/Python_Scripts/spyd1/lran12910.IEC', 'r')
else:
    fi = open(r'/Users/Marcelo/wolkesicher/Python_Scripts/OpenGRay/'
              'spyd1/lran12910.iec', 'r')

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

plt.figure(figsize=(12,8))
plt.plot(xchan, ycont)
plt.title("Original spectrum")
plt.show()

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

expect_width = 6
widths = np.arange(1, expect_width+1)
indicescwt = signal.find_peaks_cwt(ycont, widths, min_snr=3.0)
print(r'indicescwt:', expect_width, indicescwt)

expect_width = 5
widths = np.arange(1, expect_width+1)
indicescwt = signal.find_peaks_cwt(ycont, widths, min_snr=3.0)
print(r'indicescwt:', expect_width, indicescwt)

expect_width = 4
widths = np.arange(1, expect_width+1)
indicescwt = signal.find_peaks_cwt(ycont, widths, min_snr=3.0)
print(r'indicescwt:', expect_width, indicescwt)

expect_width = 3
widths = np.arange(1, expect_width+1)
indicescwt = signal.find_peaks_cwt(ycont, widths, min_snr=3.0)
print(r'indicescwt:', expect_width, indicescwt)

# ... e gr'afico
plt.figure(figsize=(12,8))
plt.plot(xchan, ycont)
plt.title("CWT-found peaks")
# pyplot.plot(indicescwt5, ycont[indicescwt5], 'go', fillstyle='none', ms=15)
plt.plot(indicescwt, ycont[indicescwt], 'r^', fillstyle='none', ms=10)

nscal = 31

# grafico cwt: mapa de 
plt.figure(figsize=(12,8))
scals = np.arange(1, nscal + 1)
cwtmatr = signal.cwt(ycont, signal.ricker, scals)
plt.imshow(cwtmatr, extent=[-1, 1, nscal, 1], cmap='PRGn', aspect='auto', 
           vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
plt.show()


plt.figure(figsize=(12,8))
plt.title(r'Todas as escalas')
plt.plot(xchan, ycont)
for isca in range(nscal):
    plt.plot(xchan, cwtmatr[isca])
plt.show()


plt.figure(figsize=(12,8))
plt.title(r'Escala a=1')
plt.plot(xchan, ycont)
plt.plot(xchan, cwtmatr[0])
plt.show()

plt.figure(figsize=(12,8))
plt.title(r'Escala a=N')
plt.plot(xchan, ycont)
plt.plot(xchan, cwtmatr[nscal-1])
plt.show()

plt.figure(figsize=(12,8))
plt.title(r'Local maxima')
# sca1 = signal.argrelmax( cwtmatr[nscal-1] )
cwtmaxs = []
for isca in range(nscal):
    cwtmaxs.append( signal.argrelmax( cwtmatr[isca] )[0] )
    # plt.plot( cwtmaxs[isca], cwtmatr[isca, cwtmaxs[isca]], 'go')
    plt.plot( cwtmaxs[isca], np.ones(len(cwtmaxs[isca])) * isca, 'go')
plt.show()

# 2016-mar: Pesquisa dos ridges:
# plt.figure(figsize=(12,8))
# plt.title(r'Ridges')
# sca1 = signal.argrelmax( cwtmatr[nscal-1] )
ridges = []
totalpts = 0
totalrids = 0

# 2016-03-28: PAREI AQUI. Est'a complicando...

seq1 = np.arange(10)
seq2 = np.arange(10)

print(r'Comparacao com gap:')
print( seqmatch( seq1, seq2, 3 ) )

# for ipt in range( len(cwtmaxs[nscal-1]) ):
#     chann = cwtmaxs[nscal-1][ipt]
#     ridges[0].append( [ nscal-1, chann, cwtmatr[nscal-1][chann] ] )
    
        
# monta pontos e pontosescalas      
    
pontos = []
pontosescalas = []
iponto = 0
for iscal in range( nscal-1, nscal-4, -1 ):
    pontosescalas.append( [] )
    for ipt in range( len(cwtmaxs[iscal]) ):
        ponto = [iscal, cwtmaxs[iscal][ipt]]
        pontos.append( ponto )
        pontosescalas[ nscal-iscal-1 ].append( iponto )
        iponto += 1

ridges = []
for iscal in range( nscal-1, nscal-4, -1 ):
    ridgetail = []
    for item in ridges:
        ridgetail.append( ridges[len(ridges)-1][1] )
    sqm = seqmatch( cwtmaxs[iscal], cwtmaxs[iscal-1], 2)
    
    testes = [ pontos[ipt] for ipt in pontosescalas[nscal-iscal-1]]
    # sqm2 = seqmatch( [ ponto[ipt] for ipt in pontosescalas[nscal-iscal-1]] )
    # matchprev = []
    # for ch in sqm: matchprev.append( sqm[0] )
    matchcurr = []
    for ch in sqm: matchcurr.append( sqm[1] )


#    cwtmaxs[iscal]
#    ridgetail = []
#    for item in ridges:
#        ridgetail.append( ridges[len(ridges)-1][1] )
#    sqm = seqmatch( cwtmaxs[iscal], cwtmaxs[iscal-1], 2)
#    matchprev = []
#    for ch in sqm: matchprev.append( sqm[0] )
#    matchcurr = []
#    for ch in sqm: matchcurr.append( sqm[1] )
    # for ipt in matchcurr:
        ## PAREI AQUI
        # indx = [i for i,x in enumerate(pt) if x==889]

    
# ridges = []
# for iscal in range( nscal-1, nscal-4, -1 ):
#    ridgetail = []
#    for item in ridges:
#        ridgetail.append( ridges[len(ridges)-1][1] )
#    sqm = seqmatch( cwtmaxs[iscal], cwtmaxs[iscal-1], 2)
# for ch in sqm: matchprev.append( sqm[0] )
#    matchcurr = []
#    for ch in sqm: matchcurr.append( sqm[1] )
    # for ipt in matchcurr:
        ## PAREI AQUI
        # indx = [i for i,x in enumerate(pt) if x==889]
     #   if ridgetail.index( ipt ):
     #       aaa = 1
     #   else:
     #       aaa = 2
    # se o maximo na escala atual ja estiver num ridge:
    
    # se o maximo na escala atual nao estiver num ridge existe,
    # criar um novo ridge:
#    for ipt in sqm:
#        ipt[0] = [ ipt[0], nscal   ]
#        ipt[1] = [ ipt[1], nscal-1 ]
#    ridges.append( sqm )
    
if 1==2:
    for iscal in range( nscal-2, 25, -1 ):
        for ipt in range( len(cwtmaxs[iscal]) ):
            chann = cwtmaxs[iscal][ipt]
            
            if np.abs( cwtmaxs[isca][ipt] - ridges[len(ridges)-1] ):
                # comparar com o 'ultimo elemento de cada ridge, o "rabo"
                ridges.append(1)
            for irid in range(len(ridges)):
                totalpts += 1
                if np.remainder(totalpts, 10) == 0:
                    ridges.append(totalpts)
                else:
                    ridges.append(7)
                
                # rid = []
                # rid.append( totalpts)
                # ridges.append( rid )
# plt.show()


# pyplot.show()
# =====================================