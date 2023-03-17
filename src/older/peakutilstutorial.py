# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# PeakUtils tutorial
# ==================

# This tutorial shows the basic usage of PeakUtils to detect the peaks of
# 1D data.

# Importing the libraries
# -----------------------

# .. code:: python

import numpy
import peakutils
from peakutils.plot import plot as pplot
from matplotlib import pyplot
from scipy.signal import find_peaks_cwt, spectrogram

# %matplotlib inline
    
# Preparing the data
# ------------------

# Now, lets generate some noisy data with two gaussians:

# .. code:: python

centers = (30.5, 72.3)
x = numpy.linspace(0, 120, 121)
y = (peakutils.gaussian(x, 5, centers[0], 3) +
    peakutils.gaussian(x, 7, centers[1], 10) +
    numpy.random.rand(x.size))
pyplot.figure(figsize=(10,6))
pyplot.plot(x, y)
pyplot.title("Data with noise")

# .. image:: _static/tut_a_1.png

# Getting a first estimate of the peaks
# -------------------------------------

# By using peakutils.indexes, we can get the indexes of the peaks from the
# data. Due to noise, it will be just a rough approximation.

# .. code:: python

indexes = peakutils.indexes(y, thres=0.5, min_dist=30)
print(r'Indices: ', indexes)
print(r'x:', x[indexes])
print(r'y:', y[indexes])
pyplot.figure(figsize=(10,6))
pplot(x, y, indexes)
pyplot.title('First estimate')

# .. parsed-literal::

#    [31 74]
#    [ 31.  74.] [ 5.67608909  7.79403394]

# .. image:: _static/tut_a_2.png


# Enhancing the resolution by interpolation
# -----------------------------------------

# We can enhance the resolution by interpolation. Here, we will try to fit
# a Gaussian near each peak that we have just detected.

# .. code:: python

peaks_x = peakutils.interpolate(x, y, ind=indexes)
print(peaks_x)

# .. parsed-literal::

#    [ 30.58270223  72.34348214]


# Estimating and removing the baseline
# ------------------------------------

# It is common for data to have a baseline that may not be desired.
# *PeakUtils* implements one function for estimating the baseline by using
# an iterative polynomial regression algorithm:

# .. code:: python

y2 = y + numpy.polyval([0.002,-0.08,5], x)
pyplot.figure(figsize=(10,6))
pyplot.plot(x, y2)
pyplot.title("Data with baseline")

# .. image:: _static/tut_a_3.png


# .. code:: python

base = peakutils.baseline(y2, 2)
pyplot.figure(figsize=(10,6))
pyplot.plot(x, y2-base)
pyplot.title("Data with baseline removed") 


# .. image:: _static/tut_a_4.png


# Related functionality in Scipy
# ------------------------------

# Scipy also implements functions that can be used for peak detection.
# Some examples:

# -  `scipy.signal.find\_peaks\_cwt 
#       <http://docs.scipy.org/doc/scipy/reference/generated/
#         scipy.signal.find_peaks_cwt.html>`__
# -  `scipy.signal.savgol\_filter
#       <http://docs.scipy.org/doc/scipy/reference/generated/
#         scipy.signal.savgol_filter.html>`__

# ======================================================================

# 2016-fev: Comandos b'asicos para ler e imprimir um arq texto:
#

fi = open(r'/Users/Marcelo/Dropbox/Python_Scripts/spyd1/lran12910.iec', 'r')
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

fig2, ax2 = pyplot.subplots()
ax2.scatter(range(len(cnts)), cnts)

ax2.set_xlabel(r'$\Delta_i$', fontsize=20)
ax2.set_ylabel(r'$\Delta_{i+1}$', fontsize=20)
ax2.set_title('Gamma-ray spectrum')

ax2.grid(True)
fig2.tight_layout()

pyplot.show()

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
pyplot.title('First estimate')

peaks_chan = peakutils.interpolate(xchan, ycont, ind=indexeschan)
print(r'peaks_chan:', peaks_chan)


# 2016-03-02: Usando funcoes de SciPy para picos e espectros:

# 2016-03-01 Bons valores para widths e min_snr
indicescwt = find_peaks_cwt(ycont, numpy.arange(1, 11), min_snr=3.0)
print(r'indicescwt:', indicescwt)

especgrama = spectrogram(ycont)

# 2016-03-02: Hah uma sugestao para usar rfft() para analisar sinal:
especrfft = numpy.fft.rfft(ycont)

pyplot.figure(figsize=(12,8))
pyplot.plot(especrfft.real)
pyplot.title(r'Parte real')

pyplot.figure(figsize=(12,8))
pyplot.plot(especrfft.imag)
pyplot.title(r'Parte imaginaria')

especirfft = numpy.fft.irfft(especrfft)

pyplot.figure(figsize=(12,8))
pyplot.plot(especirfft)
pyplot.title(r'Espectro reconstruido')

pyplot.figure(figsize=(12,8))
pyplot.plot(especirfft.imag)
pyplot.title(r'Parte imaginaria do reconstr')


ycont2 = ycont + numpy.polyval([0.002,-0.08,5], xchan)
pyplot.figure(figsize=(12,8))
pyplot.plot(xchan, ycont2)
pyplot.title("Data with baseline")

# 2016-03-01 Nao dah muito certo...
base2 = peakutils.baseline(ycont, deg=7)
