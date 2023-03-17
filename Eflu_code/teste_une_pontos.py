#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 22:31:27 2017

@author: marcelo
"""
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import pprint

# teste de unir pontos

# cnxs: pairs of connected points. Points IDs are in crescent order inside pairs. 
# 2017-09-23 TODO: Criar estrutura para os ridges.
# Talvez cada ridge como uma simples lista de conexoes
# Ou melhor, como uma lista de pontos. Vamos ver.

def build_pts( npt, xmax, ymax):
    xs = [ np.random.randint(xmax) for ipt in range(npt)]
    ys = [ np.random.randint(ymax) for ipt in range(npt)]
    return xs, ys

def tree(): return defaultdict(tree)

def add(t, path):
    for node in path:
        t = t[node]

def dicts(t): return {k: dicts(t[k]) for k in t}

npt = 100
xs, ys = build_pts(npt,300,200)
plt.plot( xs, ys, 'g.')
for ipt in range(npt):
    plt.text(xs[ipt], ys[ipt], ipt)

lingap = 10 # linear gap
cnxs = []
for ipt in range(npt):
    for jpt in range(ipt+1, npt):
        if abs(xs[jpt]-xs[ipt])<lingap and abs(ys[jpt]-ys[ipt])<lingap:
            #conx = [xs[ipt],xs[jpt]],[ys[ipt],ys[jpt]]
            conx = [ ipt, jpt ]
            cnxs.append (conx)

for conx in cnxs:
    plt.plot( [xs[conx[0]], xs[conx[1]]], [ys[conx[0]],ys[conx[1]]], 'r-')

# ridges = [ cnxs[0].copy() ]

ridges = []
ncx = len(cnxs)
for icx in range(ncx):
    # search at the end of each ridge
    for rdg in ridges:
        if cnxs[icx][0] == rdg[-1]:
            print ('atualz ridge: ', cnxs[icx][1])
            rdg.append(cnxs[icx][1])
            print ('novo ridge: ', rdg)
            
    for jcx in range(icx+1, ncx):
        if cnxs[icx][1] == cnxs[jcx][0]:
            print ('ridge: ', cnxs[icx][0], cnxs[icx][1], cnxs[jcx][1])
            ridges.append( [cnxs[icx][0], cnxs[icx][1], cnxs[jcx][1]] )
            
# 2017-10-01:       
# https://gist.github.com/hrldcpr/2012250        
        
taxonomy = tree()
taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Felidae']['Felis']['cat']
taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Felidae']['Panthera']['lion']
taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Canidae']['Canis']['dog']
taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Canidae']['Canis']['coyote']
taxonomy['Plantae']['Solanales']['Solanaceae']['Solanum']['tomato']
taxonomy['Plantae']['Solanales']['Solanaceae']['Solanum']['potato']
taxonomy['Plantae']['Solanales']['Convolvulaceae']['Ipomoea']['sweet potato']

add(taxonomy,
    'Animalia>Chordata>Mammalia>Cetacea>Balaenopteridae>Balaenoptera>blue whale'.split('>'))

verisso = dicts(taxonomy)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(verisso)

lista = [1,2,3,5,6,8,4,2,7,4,6,8,8]
while len(lista):
    print (lista)
    lista.pop()



# pprint(dicts(taxonomy))


#        if cnxs[icx][0] == cnxs[jcx][1]:
#            print ('ridge: ', cnxs[jcx][0], cnxs[jcx][1], cnxs[icx][1])

#ncx = len(cnxs) 
#for conx in cnxs:
#    print ('conx: ', conx)
#    tails = [rdg[-1] for rdg in ridges ]
#    try:
#        idx = tails.index( conx[0] )
#    except ValueError:
#        print ('nao ', conx[0], ' em ', tails )
#        ridges.append( conx.copy() )
#    else:
#        print ('SSIMMM ', conx[0], ' em ', tails )
#        ridges[idx].append( conx[1] )
        
    #    ridges.append( conx )
        
    #print ('ridges:', ridges)
    
#    for rdg in ridges:
#        try:
        #else:
        #    rdg.append( conx[1] )
            
    
    
    #for rdg in ridges:
    #    print('rdg:')
    #    print (conx[0], ' e ', rdg[-1])
    #    if conx[0] == rdg[-1]:
    #        print ('SIM')
    #        print( conx[0] ) 
    #        rdg.append( conx[1] ) # MODIFICA cnxs!!! Como ?
    #        break
    #else:
    #    print( 'nao')
    #    ridges.append( conx )
#    for conx in cnxs:
#        for 
