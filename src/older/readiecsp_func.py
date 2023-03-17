# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""

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