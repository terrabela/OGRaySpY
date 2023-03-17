# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as pl 
from ioiecspec import readiecsp
from emendabaseline import bline_estimate
from sys import platform

# counts = readiecsp(r'Madu/Python_Scripts/spyd1/ctp0303.IEC')
# counts = readiecsp(r'Madu/Python_Scripts/spyd1/lran12910.IEC')
# counts = readiecsp(r'marcelo/Python_Scripts/spyd1/lran12910.IEC')

if platform == 'linux':
    flocalprefix = r'/home/marcelo/wolkesicher/ipen/Genie2k/Camfiles/Pni/2012_Ago/'
else:
#    flocalprefix = r'/Users/mmaduar/ownCloud/Python_Scripts/spyd1/'
#   # 2016-09-28 laptop novo
#   flocalprefix = r'/Users/Marcelo/ownCloud/ipen/Genie2k/Camfiles/PNI/2012_Ago/'
#   # 2017-03-07 nuvem MS-OneDrive no micro I... (mmaduar)
    flocalprefix = r'/Users/mmaduar/OneDrive/Documentos/Ipen/Espectros_IEC_diversos/'
#   # 2017-03-08 nuvem wolkesicher no laptop (Marcelo)
    # flocalprefix = r'/Users/Marcelo/wolkesicher/ipen/Genie2k/Camfiles/PNI/2012_Ago/'
    
# flocalname = flocalprefix + 'alm_qc_16.IEC'
# flocalname = flocalprefix + 'alm_samp1_F100_16_Cont-A.IEC'
# flocalname = flocalprefix + 'alm_samp1_spk_water_16.IEC'    
# flocalname = flocalprefix + 'alm_samp3(QC)_F100_16_Cont-A.IEC'    
# flocalname = flocalprefix + 'alm_samp3(QC)_F100_16_Cont-prelim.IEC'    
# flocalname = flocalprefix + 'alm_samp4_spruce_ndl_16.IEC'    
# flocalname = flocalprefix + 'alm_samp5_F100_16_Cont-A.IEC'    
# flocalname = flocalprefix + 'alm_samp5_sedim_16.IEC'    
# flocalname = flocalprefix + 'alm_samp5_sedim_cont#2_16.IEC'    
flocalname = flocalprefix + 'Veg_Lab_GF_#2.IEC'
# flocalname = flocalprefix + 'alm_samp3(QC)_F100_16_Cont-B.IEC'    

# 2016-07-14: lembrar que readiecsp devolve uma tupla counts, lt, rt:
counts, time_lt, time_rt = readiecsp( flocalname )

# counts = readiecsp(r'mmaduar/ownCloud/Python_Scripts/spyd1/lran12910.IEC')

pl.figure()
pl.yscale('log')
pl.plot( counts )

# ww: window width
ww = 13
chw = list( range(ww) )

scale = 1.0e3
thres = 1.7

nch = len( counts )
ch = list(range(nch))

covd00 = [ 0 for i in range(int(ww/2))]
covd01 = [ 0 for i in range(int(ww/2))]
covd11 = [ 0 for i in range(int(ww/2))]
wstd = [ 0 for i in range(int(ww/2))]
wpoly = []

logcounts = []
for i in range(len(counts)):
    if counts[i] <= 0:
        logcounts.append( 0 )
    else:
        logcounts.append( np.log( counts[i] ) )

for i in range( nch - ww):
    covd = np.cov( chw, counts[i:i+ww] )
    covd00.append( covd[0,0] )
    covd01.append( covd[0,1] )
    covd11.append( covd[1,1] )
    wmean = np.mean( counts[i:i+ww] )
    if wmean == 0:
        wstd.append(0)
    else:
        wstd.append( scale * np.std( counts[i:i+ww] ) / np.sqrt( wmean ) )
    wpoly.append( np.polyfit( chw, logcounts[i:i+ww], 2) )

wpoly0 = [ p[0]*10 for p in wpoly ]
wpoly1 = [ p[1]    for p in wpoly ]
wpoly2 = [ p[2]    for p in wpoly ]

# Define peaks regions (list "regions")
    
regions = []
limits = []
inregion = False
for i in range(len(wstd)):
    if not inregion and wstd[i] >= scale * thres:
        limits.append( i )
        inregion = True
    if inregion and wstd[i] < scale * thres:
        limits.append( i-1 )
        regions.append( limits )
        limits = []
        inregion = False

# 2017-03-08 Melhor conectar regioes proximas

# newlist = []
# for i in range(len(regions)):
#     if regions[i+1][0]-regions[i][1] <= 7:
#         combregion = [regions[i][0], regions[i+1][1]] 
#         newlist.append( combregion )
#         INCREMENTAR I e incluir regioes nao modificadas   
# regions = [r for r in newlist]
# del newlist    

# Define baseline regions (list "blin")

blin = []
blin.append( [ 0, regions[0][0] ] )
for i in range(len(regions)-1):
    blin.append( [regions[i][1], regions[i+1][0]] )
blin.append( [ regions[-1][1], nch-1 ] )

# 2017-03-08 Desabilitei, nao estah funcionando
# eliminate regions shorter than 3 channels, without changing "blin"

# newlist = []
# for i in range(len(regions)):
#     if regions[i][1]-regions[i][0] >= 2:
#         newlist.append( regions[i] )
# regions = [r for r in newlist]
# del newlist     

 

# Baseline fit between regions

xbl = []
ybl = []
zbl = []
for i in range(len(blin)):
    xbl.append( list( range( blin[i][0], blin[i][1]+1 ) ) )
    ybl.append( counts[ blin[i][0]:blin[i][1]+1 ] )
    zbl.append( np.polyfit(xbl[i], ybl[i], 2) )

# Baseline estimating inside regions

xrg = []
yrg = []
zrg = []
for i in range(len(regions)):
    xrg.append( list( range( regions[i][0], regions[i][1]+1 ) ) )
    yrg.append( counts[ regions[i][0]:regions[i][1]+1 ] )
    deltay = yrg[i][-1] - yrg[i][0]
    sumy = sum( yrg[i] )
    cumy = 0
    zrgi = []
    for j in range( len( yrg[i] ) ):
        zrgi.append( yrg[i][0] )
    zrg.append( np.polyfit(xrg[i], yrg[i], 2) )

# Plot analyzed spectrum

pl.figure()
# 2016-09-29 AQUI para mudar para escala log
# pl.yscale('log')
pl.plot( counts, label='counts', linewidth=0.5 )
pl.plot( wstd, label='sd/sqrt(mean)', linewidth=0.3 )
for i in range(len(regions)):
    x = list(range( regions[i][0], regions[i][1]+1 ))
    y = [ wstd[j] for j in x ]
    pl.plot( x, y, color='magenta', linewidth=2.0 )
    
# Color names: visit 
# http://www.w3schools.com/colors/colors_names.asp    

# plot regions fit
for i in range(len(regions)):
    print('Region fit: ', i)
    xp = np.linspace(regions[i][0], regions[i][1], 50)
    # 2016-06-30: PAREI AQUI agora tem que fazer o ajuste gaussiano
    # so' coloquei polinomial para testar
    p = np.poly1d( zrg[i] )
    pl.plot( xp, p(xp), color='Plum', linewidth=1.3 )
    
# plot baselines fit
for i in range(len(zbl)):
    print('Baseline fit: ', i)    
    xp = np.linspace(blin[i][0], blin[i][1], 50)
    p = np.poly1d( zbl[i] )
    pl.plot( xp, p(xp), color='Gold', linewidth=1.0)

# plot baselines inside regions fit

netareas = []
centroids = []
for i in range(len(regions)):
    if len( yrg[i] ) >= 3:
        # blest = bline_estimate( yrg[i] )
        p_bef = np.poly1d( zbl[i] )
        p_aft = np.poly1d( zbl[i+1] )     
        # Number of CHannels on each side to eXTenD the ReGion
        nchxtdrg = 3
        
        xforplot = list(
            range( regions[i][0]-nchxtdrg, regions[i][1]+nchxtdrg+1 ) )
        yforfit = list( p_bef( range(regions[i][0]-nchxtdrg,regions[i][0]) )) \
                + yrg[i]                                                      \
                + list( p_aft( range(regions[i][1]+1,regions[i][1]+nchxtdrg+1)) )
        bl_forplot = bline_estimate( yforfit )

        # blfit = yrg[i][:1] + list(blest.x) + yrg[i][-2:]
        # blfit = [ p_bef(blin[i][1]) ] + list(blest.x) + [ yrg[i][-2], p_aft( blin[i+1][0] ) ]
        # blfit = [ p_bef(blin[i][1]) ] + list(blest.x) + [ p_aft( blin[i+1][0] ) ] + [ p_aft( blin[i+1][0]-1 ) ]
        pl.plot( xforplot, bl_forplot, color='OrangeRed', linewidth=1.0)
        
        net_forplot = []
        for j in range(len(yforfit)):
            net_forplot.append( yforfit[j] - bl_forplot[j] )
        pl.plot( xforplot, net_forplot, color='Cyan', linewidth=1.0)
        
        somaxnety = []
        for j in range(len(xforplot)):
            somaxnety.append( xforplot [j] * net_forplot [j] )
        
            
        netareas.append( sum( net_forplot ))
        centroids.append( sum( somaxnety ) / sum( net_forplot ))
        