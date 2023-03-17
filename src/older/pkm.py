# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 16:21:08 2017

@author: mmaduar
"""

pkmatches = [[[0,0],[1,7],[2,9]],
             [[1,1],[3,2],[5,3],[7,4],[8,5],[9,6]],
             [[1,2],[2,3],[3,4],[5,6],[6,7]],
             [[1,0],[4,1],[6,2],[7,3]]]

ridges = [ [0, [pkmt[0],pkmt[1]]] for pkmt in pkmatches[0]]
new_tails_values = [pkmt[1] for pkmt in pkmatches[0]]
# tails_ndxs   = list(range(len(ridges)))
new_tails_ndxs = list(range(len(ridges)))


nrdg = len(ridges)
for i, pksc in enumerate(pkmatches):
    if i < 3:
        new_ridges = []
        tails_ndxs = new_tails_ndxs.copy()
        tails_values = new_tails_values.copy()
        for pkmt in pkmatches[i+1]:
            try:
                pos = tails_values.index( pkmt[0] )
            except ValueError:
                new_ridges.append( [i+1, pkmt] )
                nrdg += 1
                new_tails_ndxs.append( nrdg )
                new_tails_values.append( pkmt[1] )
            else:
                print ('pos: ', pos)
                print ('ridge index: ', tails_ndxs[pos])
                new_tails_ndxs.append( tails_ndxs[pos] )
                new_tails_values.append( pkmt[1] )
                # 2017-08-23 PAREI AQUI indice invalido
                # print( ridges[tails_ndxs[pos]][1] )
                # ridges[tails_ndxs[pos]][1].append( pkmt[1])
        print ('new ndxs: ', new_tails_ndxs)
        ridges += new_ridges        
                
print (new_ridges)                