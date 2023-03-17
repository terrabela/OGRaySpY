# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 17:47:35 2016

@author: marcelo
"""
import numpy as np
# import matplotlib.pyplot as plt

def buildseq():
    seq = []
    for i in range(100):
        if np.random.randint(5) == 4: # pega 20% dos n'umeros
            seq.append(i)
    return seq

def eqseq( seq1, seq2 ):
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

def seqmatch( seq1, seq2, maxgap ):
    i1 = 0
    i2 = 0
    smatch = []
    imatch = []
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
    return (smatch, imatch)

def interseq( seq1, seq2, maxgap ):
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
    
# para criar seqn natural
# seq1 = np.arange(10)
# seq2 = np.arange(10)

## ou

# para criar seqn aleat'oria
seq1 = buildseq()
seq2 = buildseq()

print(seq1)
print(seq2)

# Compara,c~ao com gap
       
print(r'Compara,c~ao com gap:')
smatch = seqmatch( seq1, seq2, 2 )
print( smatch ) 
print(r'Fim.')

transp1 = zip(*smatch)
print( *transp1 )

transp2 = map(list, zip(*smatch))
print( *transp2 )

transp3 = [list(i) for i in zip(*smatch)]
print( *transp3 )

print(r'Intersec,c~ao:')
intersc = set.intersection( set(seq1), set(seq2) )
print( intersc )

print(r'Diferen,ca:')
differn = set.difference( set(seq1), set(seq2) )
print( differn )
