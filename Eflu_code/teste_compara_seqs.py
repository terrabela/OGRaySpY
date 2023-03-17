# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 14:36:34 2017

@author: Marcelo
"""

# from spec_cwt import (SpecCwt)
import numpy as np
import matplotlib.pyplot as plt
import list_compars as lcmp

# 2017-08-13 
# P.P. para testes de comparacao de sequencias

def build_cwtpks( nscal, max_pkch):
    cwtpks = []
    for iscal in range(nscal):
        cwtpks.append( lcmp.buildseq( max_pkch ) )
    return cwtpks

def compare_peaks_thru_scales( cwtpks, maxgap, biuniv=0 ):
    pkmatches = []
    for isc in range( len(cwtpks)-1 ):
        # [1] para ter soh indices da matriz, nao os valores:
        sqm = lcmp.seqmatch( cwtpks[isc], cwtpks[isc+1], maxgap, biuniv)[1]
        # mas se quiser ter valores tamb'em:
        # sqm = lcmp.seqmatch( cwtpks[isc], cwtpks[isc+1], 2)
        pkmatches.append( sqm )
    return pkmatches

def ini_plot( cwtpks, mtchs ):
    plt.figure()
    for isca, sca in enumerate(cwtpks):
        plt.plot( sca, [isca for i in range(len(sca)) ], 'b.' )
    isca = 0
    for isca, mtchisca in enumerate(mtchs):
        for mtch in mtchisca:
            plt.plot( [ cwtpks[isca][mtch[0]], cwtpks[isca+1][mtch[1]] ],
                      [ isca, isca+1 ], 'r-' )

def build_ridges_by_match( pkmatches ):
    
    
    ridges = [ [0, [pkmt[0],pkmt[1]] ] for pkmt in pkmatches[0] ]
    ridgetails = [ rdge[1][-1] for rdge in ridges ]
    print ('tails: ', ridgetails)

#    id_open_rdgs = list (range(len(ridges)))
#    for isc in range( 1, len(pkmatches) ):
    for isc in range( 1, 2 ):
        print( ' pkmatches')
        for pkmt in pkmatches[isc]:
            print(pkmt)
            #pkmt0s = [pair[0] for pair in pkmt]
            #print( pkmt0s )
        # for pkmt in pkmatches[isc]:
            #irdg = 0
            #while pkmt[0] != ridges[irdg][1][-1]:
            #    irdg += 1
            # new_rdg = True
#            for irdg in id_open_rdgs:
#                if pkmt[0] == ridges[irdg][1][-1]:
#                    new_rdg = False
#                    ridges[irdg][1].append( pkmt[0] )
#                    break
#            else:
#                id_open_rdgs.append( len(ridges) )
#                ridges.append( [isc, pkmt] )
    return ridges 

def build_ridges_by_ridge( pkmatches ):
    #
    nsc = len (pkmatches )
    # 
    #ridges = [ [0, [pkmt[0],pkmt[1]] ] for pkmt in pkmatches[0] ]
    pkmatches_work = pkmatches.copy()
    # https://stackoverflow.com/questions/11264684/
    # flatten-list-of-lists
    npkm = len( [val for subl in pkmatches for val in subl] )
#    nsc = len(pkmatches)
    ipkm = 0
    isc = 0
    ridges = []
    while ipkm < npkm:
        for pkm in pkmatches_work[isc]:
            print (pkm)
 #           rdg = [isc, [ pkm[0]] ]
 #           isc2 = isc+1
 #           while ( isc2 <= nsc ):
 #               rdg[1].append[ pkm[isc2][1]]
 #               isc2 += 1
 #           ridges.append( rdg )
            ipkm += 1
            # find connections
            
        isc += 1    
    return ridges, npkm

def def2():
    # cwtmxs: 
    # Construindo ridges correspondentes a cwtlist
    
    
    #ridges = [ [ [0, spec.cwtmaxs[0][mtch[0]] ],
    #             [1, spec.cwtmaxs[1][mtch[1]] ] ] for mtch in mtchs[0] ]
    
    # Ativar depois
    # ridges = [ [ [0, mtch[0]], [1, mtch[1]] ] for mtch in mtchs[0] ]
    
    # print('ridges:')
    # print( ridges )
    nrdg = len(ridges)
    rdgfin = 0
    
    # print('mtchs a partir de 1:')
    for iconex in range(1,len(mtchs)):
    #    print ('mtchs, escala ', iconex, 'para seguinte' )
    #    print (mtchs[iconex])
        ipairant = 0
        for pair in mtchs[iconex]:
    #        print ( pair )
            if ipairant >= len(mtchs[iconex-1]):
                if pair[0] == mtchs[iconex-1][ipairant][1]:
    #                print ('bate:', pair, mtchs[iconex-1][ipairant])
                    ipairant += 1
    
    #plt.plot( mtchs[0], 'go' )
    #plt.show

    ridges = [ [mtch] for mtch in mtchs[0] ]
    ridgetails = [ rdge[0][1] for rdge in ridges ]
    inirdg = 0
    
    #for isca in range(1, len(mtchs)):
    #for isca in range(1, 2):
    #    print ('Scale ', isca)
    #    mtchisca = mtchs[isca]
    #    irdg = inirdg
    #    for mtch in mtchisca:
    #        print (mtch)
    #        if mtch[0] == ridgetails[irdg]:
    #            print ('Conectar ', mtch, ' com ridge ', ridges[irdg])
    #            irdg += 1
    #        else:
    #            print ('Iniciar novo ridge com ', mtch )
                
                
    #            ridges[irdg].append( mtch )
    #        else:
    #            ridges.append( [mtch] )
    #            irdg += 1
            # while ridgetails[irdg] == ridgetails[irdg+1]:
        
    # print('mtchs:')
    # print (mtchs)
    # para criar seqn natural
    # seq1 = np.arange(10)
    # seq2 = np.arange(10)
    
    ## ou
    
    # para criar seqn aleat'oria
    # seq1 = buildseq()
    # seq2 = buildseq()
    
    # spec = SpecCwt()
    # spec.c
    
########### 2017-08-16 Recomecando construcao dos ridges

# Fazendo uma cwtlist: list de nscal sequencias ordenadas

nscal = 5
max_pkch = 30
cwtpks = build_cwtpks(nscal, max_pkch)
# 2017-08-20 Para fazer correspondencia naum univoca:
# nao vou usar por enquanto.
# pkmatches = compare_peaks_thru_scales( cwtpks )
# ini_plot( cwtpks, pkmatches )

# 2017-08-20 Vou usar por hora correspondencia biunivoca:
# pkmatches = compare_peaks_thru_scales( cwtpks, 2, biuniv=1 )
# 2017-08-23 Construindo pkmatches from scratch
pkmatches = [[[0,0],[1,7],[2,9]],
             [[1,1],[3,2],[5,3],[7,4],[8,5],[9,6]],
             [[1,2],[2,3],[3,4],[5,6],[6,7]],
             [[1,0],[4,1],[6,2],[7,3]]]

# ini_plot( cwtpks, pkmatches )

# ridges, npkm = build_ridges_by_ridge ( pkmatches )
ridges = build_ridges_by_match ( pkmatches )


