import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def gaussianfunc(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

# ======================================================================

# 2016-mar: Espectro sint'etico:

npeaks = 6
nchans = 4100
maxhei = 10000.

# peaksigmas = np.random.random_sample(npeaks) * 20. + 0.5
# centroids = np.random.random_sample(npeaks) * (nchans-100) + 100
# heights = np.random.random_sample(npeaks) * maxhei + 10

peaksigmas = np.linspace(1.0, 50, num=npeaks)
centroids = np.linspace (200.0, 3500.0, num=npeaks)
heights = np.random.random_sample(npeaks) * maxhei + 10


synth = np.zeros(nchans)
for ipk in range(npeaks):
    for ict in range(nchans):
        synth[ict] += heights[ipk] * gaussianfunc(ict, centroids[ipk], peaksigmas[ipk])
    
plt.plot(synth) 

xchan = range(nchans)
ycont = synth

# C'alculo...
# Para esse espectro, o par^ametro 5 abaixo 'e que d'a mais picos
# expect_width = 15

expect_width = 4
widths = np.arange(1, expect_width+1)
indicescwt = signal.find_peaks_cwt(ycont, widths, min_snr=3.0)

print(r'indicescwt:', indicescwt)
# ... e gr'afico
plt.figure(figsize=(12,8))
plt.plot(xchan, ycont)
plt.title("CWT-found peaks")
# pyplot.plot(indicescwt5, ycont[indicescwt5], 'go', fillstyle='none', ms=15)
plt.plot(indicescwt, ycont[indicescwt], 'r^', fillstyle='none', ms=10)

# grafico cwt:

plt.figure(figsize=(12,8))
cwtmatr = signal.cwt(ycont, signal.ricker, widths)
plt.imshow(cwtmatr, extent=[-1, 1, 31, 1], cmap='PRGn', aspect='auto', 
           vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
plt.show()

plt.figure(figsize=(12,8))
# pyplot.plot(xchan, ycont)

for isca in range(expect_width):
    plt.plot(xchan, cwtmatr[isca])
plt.show()

# pyplot.show()

# =====================================   