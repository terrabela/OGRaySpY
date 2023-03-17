# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

n = 11
parts = []
part = [n]
parts.append( part )

i=0
while part[0] != 1:
    try:
        mut = part.index(1)
    except ValueError:
        newpart = part[:-1] + [part[-1]-1, 1]
    else:
        newpart = part[:mut-1]
        r = n - sum( part[:mut] ) + 1
        k = part[mut-1]-1
        newpart.append(k)
        while r >= k:
            newpart.append(k)
            r -= k
        if r != 0:
            newpart.append(r)
    parts.append(newpart)
    part = newpart
    i += 1
 
print( parts )
print( parts [(i+1) // 2] )
