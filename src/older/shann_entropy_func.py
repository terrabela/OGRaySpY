# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 12:30:04 2018

@author: Marcelo
"""

import numpy as np
# from scipy import signal

def negtozero(x):
    if x < 0:
        y=0
    else:
        y=x
    return y    

def nonullelements_cwtmatr( cwtmatr ):
    return np.asarray(
            [[negtozero(col) for col in row] for row in cwtmatr]
)
# nonullelements_cwtmatr.shape

def norm_arr( arr ):
    soma = sum(arr)
    return arr/soma

def cwt_norm( nonul ):
    return np.asarray(
            [ norm_arr(row) for row in nonul ]
            )
    