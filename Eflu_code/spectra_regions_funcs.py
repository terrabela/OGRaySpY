# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 11:09:55 2018

@author: Marcelo
"""

from sys import platform
from platform import node
from scipy.signal import (find_peaks, find_peaks_cwt, peak_widths)
# port (find_peaks, peak_widths, cwt, ricker, find_peaks_cwt)
from scipy.fftpack import (fft, ifft)
from scipy.stats import (entropy)
# from pathlib import Path, PurePath
import numpy as np
from scipy.optimize import (curve_fit, root)
from copy import deepcopy
# from numpy import cosh, zeros_like, mgrid, zeros
# from test_lists import seqmatch

import base_line_funcs as blf

def readiecsp( fn ):
    fi = open(fn, 'r')
    lins = fi.readlines()
    fi.close()
    
    inidat = 1
    for lin in lins:
        if lin.find(r'A004USERDEFINED') == 0:
            break
        inidat += 1
        
    lt = float( lins[1][ 4:18] )
    rt = float( lins[1][18:32] )   
        
    cnts = [0]
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
    return cnts, lt, rt

def def_bline_regions( nch, regions ):

    ######################################
    
    # Define baseline regions (list 'blin')

    blin = []
    blin.append( [ 0, regions[0][0] ] )
    for i in range(len(regions)-1):
        blin.append( [regions[i][1], regions[i+1][0]] )
    blin.append( [ regions[-1][1], nch-1 ] )
    return blin

def blines_fit( blin, counts, regions):

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
    
    return xbl, ybl, zbl, xrg, yrg, zrg

def calc_centroid( xforplot, net_forplot ):
    somaxnety = []
    for j in range(len(xforplot)):
        somaxnety.append( xforplot [j] * net_forplot [j] )
    centroid = sum( somaxnety ) / sum( net_forplot )
    return centroid

def define_regions(indics, len_spc, side_extd=10, min_separ_pks=30):
    regions = []
    start = indics[0]-side_extd
    if start < 0:
        start = 0
    multiplet =[]
    multiplets = []
    for i in range(len(indics)-1):
        if indics[i+1] - indics[i] > min_separ_pks:
            regions.append([start, indics[i]+side_extd])
            multiplet.append(indics[i])
            multiplets.append(multiplet)
            start = indics[i+1]-side_extd
            multiplet = []
        else:
            multiplet.append(indics[i])
    final = indics[-1]+side_extd
    if final >= len_spc:
        final = len_spc - 1
    regions.append([indics[-1]-side_extd,final])
    multiplet.append(indics[-1])
    multiplets.append(multiplet)
    return regions, multiplets    

def scan_spectrum2( counts ):
    # expect_width = 7      # 2018-Jun-10: mudei pra 30; Jun-21: mudei para 5
    expect_width = 4
    widths = np.arange(1, expect_width)

    indicescwt = find_peaks_cwt(counts, widths, max_distances=widths,
                                       gap_thresh=2.0, min_snr=1.5)
    regions, multiplets = define_regions(indicescwt, len(counts), side_extd=13, min_separ_pks=30)
    print(r'expect_width:', expect_width)
    print(r'indicescwt:', indicescwt)
    return indicescwt, regions, multiplets

def total_analysis2(filename, **keywords):
    cts_spc, lt_spc, rt_spc = readiecsp(filename)
    xs = np.linspace(0, len(cts_spc)-1, len(cts_spc))
    indics, regions, multis = scan_spectrum2(cts_spc)
    # xs = list(range(len(cts_spc)))
    lx = [ list(range(region[0], region[1]+1)) for region in regions ]
    ly = [ [cts_spc[i] for i in xs] for xs in lx ] 
    
    blins = []
    if 'baseline' in keywords:
        if keywords['baseline']=='descendingthroughpeak':
            # 2018-07-16 Definir a baseline baseada em segmento movel
            ret = 'A definir.'
        else:
            # blins = [blf.bline_estimate_2(ys) for ys in ly ]
            ret = 'baseline is not ''descendingthroughpeak''. '
    else:
        blins = [blf.bline_estimate_2(ys) for ys in ly ]
    if blins:
        heis = [cts_spc[i] for i in indics]
        nety = [ [ gr-bl for gr, bl in zip(l1,l2) ] for l1,l2 in zip(ly,blins) ]
        ret = (cts_spc, lt_spc, rt_spc, xs, indics, regions, multis,
               lx, ly, blins, heis, nety)
    return ret
