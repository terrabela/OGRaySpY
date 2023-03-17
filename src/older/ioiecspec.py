# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 14:36:04 2016

@author: Madu
"""
from sys import platform
# from pathlib import Path, PurePath

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
        
    cnts = []
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

def writeiecsp( fnheader, fndestiny, cnts ):
    fhead = open(fnheader, 'r')
    lins = fi.readlines()
    fi.close()
    
    inidat = 1
    for lin in lins:
        if lin.find(r'A004USERDEFINED') == 0:
            break
        inidat += 1
        
    cnts = []
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
    return cnts

def SumSpectra( fnh, fn1, fn2, fns ):
    if platform == 'linux':
        fi = open(r'/home/' + fnh, 'r')
    else:
        fi = open(r'/Users/' + fnh, 'r')
  
    lins = fi.readlines()
    fi.close()

    header = []
    inidat = 1
    for lin in lins:
        inidat += 1
        header.append( lin )
        if lin.find(r'A004USERDEFINED') == 0:
            break

    cnts1, lt1, rt1 = readiecsp( fn1 )
    cnts2, lt2, rt2 = readiecsp( fn2 )
    
    ltstr = '{0:14.6f}'.format( lt1 + lt2 )
    rtstr = '{0:14.6f}'.format( rt1 + rt2 )      
    
    headerline1 = header[1][0:4] + ltstr + rtstr + header[1][32:]
        
    sums = []
    for i in range( len(cnts1) ):
        sums.append( cnts1[i] + cnts2[i] )

    formattedcounts = []
    nlin = len(cnts1) // 5
    i = 0
    for ilin in range( nlin ):
        lin = 'A004'
        lin += repr( ilin*5 ).rjust(6)
        for ifield in range(5):
            lin += repr( sums[i] ).rjust(10)
            # lin += '{0:10}'.format( sums[i] ) # works as well
            i += 1
        lin += '\n'
        formattedcounts.append( lin )

    if platform == 'linux':
        fo = open(r'/home/' + fns, 'w')
    else:
        fo = open(r'/Users/' + fns, 'w')
        
    fo.writelines( header[0] )
    fo.write( headerline1 )
    fo.writelines( header[2:] )
    fo.writelines( formattedcounts )    
    
    fo.close()
