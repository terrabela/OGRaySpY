# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 10:39:10 2017

@author: Marcelo
"""

import numpy as np

def buildseq(rng):
    seq = []
    for i in range(rng):
        if np.random.randint(5) == 4: # pega 20% dos n'umeros
            seq.append(i)
    return seq
    
def eqseq( self, seq1, seq2 ):
    i1 = 0
    i2 = 0
    smatch = []
    while (i1 < len(seq1)) and (i2 < len(seq2)): 
        if seq1[i1] == seq2[i2]:
            smatch.append( seq1[i1] )
            i1 += 1
            i2 += 1
        elif seq1[i1] < seq2[i2]:
            i1 += 1
        else:
            i2 += 1
    return smatch

def seqmatch( seq1, seq2, maxgap, biunivocal = 0 ):
    i1 = 0
    i2 = 0
    smatch = []
    imatch = []
    if biunivocal == 0:
        while (i1 < len(seq1)) and (i2 < len(seq2)): 
            while seq1[i1] - seq2[i2] > maxgap:
                i2 += 1
                if i2 >= len(seq2): break
            if i2 >= len(seq2): break
            i2st = i2
            while abs( seq1[i1] - seq2[i2] ) <= maxgap:
                smatch.append( [seq1[i1], seq2[i2]] )
                imatch.append( [i1, i2] )
                i2 += 1
                if i2 >= len(seq2): break
            i1 += 1
            if i1 >= len(seq1): break
            i2 = i2st
    else:
        while (i1 < len(seq1)) and (i2 < len(seq2)):
            if ( abs(seq1[i1]-seq2[i2]) <= maxgap ):
                smatch.append( [seq1[i1], seq2[i2]] )
                imatch.append( [i1, i2] )
                i1 += 1
                i2 += 1
            elif (seq1[i1] > seq2[i2]):
                i2 += 1
            else:
                i1 += 1
    return (smatch, imatch)

def interseq( self, seq1, seq2, maxgap ):
    i1 = 0
    i2 = 0
    smatch = []
    while (i1 < len(seq1)) and (i2 < len(seq2)): 
        while seq1[i1] - seq2[i2] > maxgap:
            i2 += 1
            if i2 >= len(seq2): break
        if i2 >= len(seq2): break
        i2st = i2
        while abs( seq1[i1] - seq2[i2] ) <= maxgap:
            smatch.append( [seq1[i1], seq2[i2]] )
            i2 += 1
            if i2 >= len(seq2): break
        i1 += 1
        if i1 >= len(seq1): break
        i2 = i2st
    return smatch
   
def crit_gap(a, b, maxgap):
    return ( abs(a-b) <= maxgap )