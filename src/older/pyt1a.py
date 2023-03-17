# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 13:17:38 2017

@author: Pedro
"""

# https://stackoverflow.com/questions/18326524/pass-tuple-as-input-argument-for-scipy-optimize-curve-fit
# https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/
# ver tambem como usa keyword p0
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html#scipy.optimize.curve_fit
import numpy as np 
from scipy.optimize import curve_fit

def expmaisk2(x,*args):
    locl = args
    d=locl[0]
    h=locl[1]
    k=locl[2]
    c=locl[3]
    print(13)
    print (args)
    return h*np.exp(k*(x-d))+c
    # return 29

def f(x, *p):
    return sum( [p[i]*x**i for i in range(len(p))] )

print(7)
print (expmaisk2(150.0, 50.0, 7.0, 0.02, 3.0))

aaa=f(2,0, 7, 34, 4, 3)
print(aaa)
