# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import numpy
import peakutils
from peakutils.plot import plot as pplot
from matplotlib import pyplot
from scipy.signal import cwt, find_peaks_cwt, ricker, spectrogram, detrend

# ======================================================================

# 2016-mar: Comandos bahsicos para ler e imprimir um arq texto:
#

# fi = open(r'/Users/Marcelo/Dropbox/Python_Scripts/spyd1/lran12910.iec', 'r')
fi = open(r'/GENIE2K/CAMFILES/Si/si2016/si00716.iec', 'r')
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
xchan = numpy.linspace(0, len(cnts)-1, len(cnts))
ycont = numpy.asarray(cnts)

pyplot.figure(figsize=(12,8))
pyplot.plot(xchan, ycont)
pyplot.title("Original spectrum")
pyplot.show()

indexeschan = peakutils.indexes(ycont, thres=0.05, min_dist=10)
print(r'Indices: ', indexeschan)
print(r'x:', xchan[indexeschan])
print(r'y:', ycont[indexeschan])
pyplot.figure(figsize=(10,6))
pplot(xchan, ycont, indexeschan)
pyplot.title(r'First estimate (by "peakutils"')

peaks_chan = peakutils.interpolate(xchan, ycont, ind=indexeschan)
print(r'peaks_chan:', peaks_chan)


# 2016-03-02: Usando funcoes de SciPy para picos e espectros:

# 2016-03-01 Bons valores para widths e min_snr
indicescwt = find_peaks_cwt(ycont, numpy.arange(1, 11), min_snr=3.0)
print(r'indicescwt:', indicescwt)

especgrama = spectrogram(ycont)

# 2016-03-02: Hah uma sugestao para usar rfft() para analisar sinal:

ycont = ycont[:-3]
especrfft = numpy.fft.rfft(ycont)

pyplot.figure(figsize=(12,8))
pyplot.plot(especrfft.real)
pyplot.title(r'Parte real')

pyplot.figure(figsize=(12,8))
pyplot.plot(especrfft.imag)
pyplot.title(r'Parte imaginaria')

# especrfft[0:50]= 0.0
especrfft[:20]= especrfft[:20].real - especrfft[:20].imag

especirfft = numpy.fft.irfft(especrfft)

detre = detrend(ycont)

pyplot.figure(figsize=(12,8))
pyplot.plot(ycont)
pyplot.plot(especirfft)
pyplot.plot(detre)
pyplot.scatter(indicescwt, ycont[indicescwt])

pyplot.title(r'Espectro reconstruido')

# pyplot.figure(figsize=(12,8))
# pyplot.plot(especirfft.imag)
# pyplot.title(r'Parte imaginaria do reconstr')

t = numpy.arange(-1, 2, .01)
s = numpy.sin(2*numpy.pi*t)

pyplot.figure(figsize=(12,8))

pyplot.plot(t, s)
# draw a thick red hline at y=0 that spans the xrange
l = pyplot.axhline(linewidth=4, color='r')

# draw a default hline at y=1 that spans the xrange
l = pyplot.axhline(y=1)

# draw a default vline at x=1 that spans the yrange
l = pyplot.axvline(x=1)

# draw a thick blue vline at x=0 that spans the upper quadrant of
# the yrange
l = pyplot.axvline(x=0, ymin=0.75, linewidth=4, color='b')

# draw a default hline at y=.5 that spans the middle half of
# the axes
l = pyplot.axhline(y=.5, xmin=0.25, xmax=0.75)

p = pyplot.axhspan(0.25, 0.75, facecolor='0.5', alpha=0.5)

p = pyplot.axvspan(1.25, 1.55, facecolor='g', alpha=0.5)

pyplot.axis([-1, 2, -1, 2])

# grafico cwt:


pyplot.figure(figsize=(10,6))
widths = numpy.arange(1, 11)
cwtmatr = cwt(ycont, ricker, widths)
pyplot.imshow(cwtmatr, extent=[-1, 1, 31, 1], cmap='PRGn', aspect='auto', 
           vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
pyplot.show()


# pyplot.show()


# =====================================