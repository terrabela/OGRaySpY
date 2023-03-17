# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 13:49:30 2016

@author: Madu
"""

import numpy as np
from scipy.optimize import root
# from numpy import cosh, zeros_like, mgrid, zeros

def gaus(x):
    """Gaussian function.

    Args:
        x (float): variable.

    Returns:
        float: f(x), where f(x)=exp(-x**2).

    """
    return np.exp(-x**2)

def fb(b, y):
    dy = y[-1]-y[0]
    s = 0
    sl = []
    for i in range(1,len(y)-2):
        s += y[i]-b[i-1]
        sl.append(s)
    f = []
    ln1 = y[-2]-y[-1]
    for i in range(0,len(y)-3):
        f.append( sl[i] / (sl[-1]+ln1) * dy + y[0] - b[i] )
    return f

# AQUI, finalmente a emenda de baseline
    
def bline_estimate( iny ):
    bi_ini = np.linspace( iny[0], iny[-1], len(iny) )[1:-2]
#    sol_fb = root(fb, bi_ini, args=iny)
    fitres = root(fb, bi_ini, args=iny)
    listres = [ iny[0] ] + list(fitres.x) + iny[-2:]
    return listres
    
iny = [350, 402, 479, 500, 391, 279, 200]
print( bline_estimate( iny ) )

sol_fb = root(fb, np.linspace( iny[0], iny[-1], len(iny) )[1:-2], args=iny, jac=False, method='lm')
print( 'raiz fb: ', sol_fb.x )

print( sol_fb )
