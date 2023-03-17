# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as pl 

def gaus( x, k ):
    return np.exp( -k*x**2 )

def bline( yy ):
    ss = np.cumsum( yy)
    delta = ( yy[-1] - yy[0] ) / ( ss[-1] - ss[0] )
    return [ delta * (ss[i]-ss[0]) + ss[0] for i in ii ] 

ii = list(range(21))
xx = [ i-10.0 for i in ii ]

h = 1300

yy = [ h * gaus( x, 0.3 ) - 10*x + 300 for x in xx ]

# sn = np.sum( yy )

bb = bline( yy )
ll = [ yy[i]-bb[i] for i in ii ]

pl.figure()
# pl.yscale('log')
pl.plot( xx, yy, color='blue' )
pl.plot( xx, bb, color='magenta' )
pl.plot( xx, ll, color='green' )
