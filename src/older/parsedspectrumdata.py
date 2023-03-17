# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 10:31:55 2016

@author: Marcelo
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 22:50:36 2016

@author: Marcelo
"""

from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QTextEdit)
from copy import deepcopy
import numpy as np
from specific_math_funcs import (bline_estimate)

class ParsedSpectrumData(QTextEdit):

    def __init__(self):
        super(ParsedSpectrumData, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.isUntitled = True
        self.lt = 0.0
        self.rt = 0.0

    def readiecsp( self, fn ):
        self.cnts = []
        self.nonull_chan = []
        self.nonull_chan = []
        self.nonull_cnts = []
        self.nonull_unct = []
        fi = open(fn, 'r')
        lins = fi.readlines()
        fi.close()
        
        # 2017-07-20 fill the text field
        # Obs. .join is reportedly the fastest
        self.setPlainText(''.join(lins))
        
        inidat = 1
        for lin in lins:
            if lin.find(r'A004USERDEFINED') == 0:
                break
            inidat += 1
            
        self.lt = float( lins[1][ 4:18] )
        self.rt = float( lins[1][18:32] )   
            
        itr = list(range( inidat, len(lins) ))
        for ilin in itr:
            self.cnts.append( int(lins[ilin][10:20]) )
            self.cnts.append( int(lins[ilin][20:30]) )
            self.cnts.append( int(lins[ilin][30:40]) )
            self.cnts.append( int(lins[ilin][40:50]) )
            self.cnts.append( int(lins[ilin][50:60]) )
        del itr
        del lins

        # set list without no-counts channels
        for i in range(len(self.cnts)):
            if self.cnts[i] > 0:
                self.nonull_chan.append( i )
                self.nonull_cnts.append( self.cnts[i] )
                self.nonull_unct.append( np.sqrt( self.cnts[i] ))

    def analyzeiecsp( self ):
        self.analyzeiecsp_step1()
        self.analyzeiecsp_step2()
        self.analyzeiecsp_step3()
        self.analyzeiecsp_finalstep()
        
    def analyzeiecsp_step1( self ):
        # ww: window width
        self.ww = 13
        self.chw = list( range(self.ww) )
        
        self.scale = 1.0e3
        self.thres = 1.7
        
        self.nch = len( self.cnts )
        self.ch = list(range(self.nch))
        
        self.covd = []
        self.covd00 = [ 0 for i in range(int(self.ww/2))]
        self.covd01 = [ 0 for i in range(int(self.ww/2))]
        self.covd11 = [ 0 for i in range(int(self.ww/2))]
        self.wstd = [ 0 for i in range(int(self.ww/2))]
        self.wpoly = []
        self.wmean = 0.0

        self.logcounts = []
        
        print ( 'Analyze iec spectrum: Step 1...' )
        print ('Fim do passo 1.')
        print ( 'Qt canais: ', self.nch, 'ww:', self.ww )
        
                
    def analyzeiecsp_step2( self ):                

        print ('Inihcio do passo 2.')        

        for i in range(len(self.cnts)):
            if self.cnts[i] <= 0:
                self.logcounts.append( 0.0 )
            else:
                self.logcounts.append( np.log( self.cnts[i] ) )

        for i in range( self.nch - self.ww - 200):
            # print (i)
            covd = np.cov( self.chw, self.cnts[i:i+self.ww] )
            # apagar depois esses print tudo...
            # print (self.chw)
            # print (self.cnts[i:i+self.ww])
            # print (covd)
            # print (self.covd00)
            # print (self.covd01)
            # print (self.covd11)
            self.covd00.append( covd[0,0] )
            self.covd01.append( covd[0,1] )
            self.covd11.append( covd[1,1] )
            # print (self.covd00)
            # print (self.covd01)
            # print (self.covd11)
            self.wmean = np.mean( self.cnts[i:i+self.ww] )
            if self.wmean == 0:
                self.wstd.append(0)
            else:
                self.wstd.append( self.scale * np.std( self.cnts[i:i+self.ww] )
                / np.sqrt( self.wmean ) )
            # print ('i, wmean: ', i, '   ', self.wmean )
            
            # 2017-03-28 O que eh isso mesmo???
            self.wpoly.append( np.polyfit( self.chw, self.logcounts[i:i+self.ww], 2) )
            # print ('wpoly[i]: ', self.wpoly[i] )

        self.wpoly0 = [ p[0]*10 for p in self.wpoly ]
        self.wpoly1 = [ p[1]    for p in self.wpoly ]
        self.wpoly2 = [ p[2]    for p in self.wpoly ]
        print ('Fim do passo 2.')
        
    def analyzeiecsp_step3( self ):                
        # Define peaks regions (list "regions")
            
        print ('Inihcio do passo 3 - anahlise.')

        self.regions = []
        self.limits = []
        inregion = False
        for i in range(len(self.wstd)):
            if not inregion and self.wstd[i] >= self.scale * self.thres:
                self.limits.append( i )
                inregion = True
            if inregion and self.wstd[i] < self.scale * self.thres:
                self.limits.append( i-1 )
                self.regions.append( self.limits )
                self.limits = []
                inregion = False
                
                
        cazzo = deepcopy( self.regions )
        i = 0
        while i < len(cazzo)-1:
            if cazzo[i+1][0]-cazzo[i][1] <= 7:
                print ('Emenda: ', cazzo[i], ',', cazzo[i+1])
                cazzo[i][1] = cazzo[i+1][1]
                cazzo.pop(i+1)
            else:
                i += 1
        self.regions = deepcopy( cazzo )
        del cazzo
        
        # Define baseline regions (list "blin")
        print ('Define baselines...')
       
        self.blin = []
        self.blin.append( [ 0, self.regions[0][0] ] )
        for i in range(len(self.regions)-1):
            self.blin.append( [self.regions[i][1], self.regions[i+1][0]] )
        self.blin.append( [ self.regions[-1][1], self.nch-1 ] )
        
        # eliminate regions shorter than 3 channels, without changing "blin"
        # newlist = []
        # for i in range(len(regions)):
        #     if regions[i][1]-regions[i][0] >= 2:
        #         newlist.append( regions[i] )
        # regions = [r for r in newlist]
        # del newlist     
        
        # Baseline fit between regions
        
        self.xbl = []
        self.ybl = []
        self.zbl = []
        for i in range(len(self.blin)):
            self.xbl.append( list( range( self.blin[i][0], self.blin[i][1]+1 ) ) )
            self.ybl.append( self.cnts[ self.blin[i][0]:self.blin[i][1]+1 ] )
            self.zbl.append( np.polyfit(self.xbl[i], self.ybl[i], 2) )
        
        # Baseline estimating inside regions
        print ('Estima baselines dentro das regioes...')
        
        self.xrg = []
        self.yrg = []
        self.zrg = []
        for i in range(len(self.regions)):
            self.xrg.append( list( range( self.regions[i][0], self.regions[i][1]+1 ) ) )
            self.yrg.append( self.cnts[ self.regions[i][0]:self.regions[i][1]+1 ] )
            self.deltay = self.yrg[i][-1] - self.yrg[i][0]
            # AQUI? VERIFICAR o que sumy, cumy 2016-12-04
            # sumy = sum( self.yrg[i] )
            # cumy = 0
            self.zrgi = []
            for j in range( len( self.yrg[i] ) ):
                self.zrgi.append( self.yrg[i][0] )
            self.zrg.append( np.polyfit(self.xrg[i], self.yrg[i], 2) )
            
        print ('Fim do passo 3 - anahlise.')

    def analyzeiecsp_finalstep( self ):                
        # final adjustments
        print ('Final step - os ajustes finais.')
        self.netareas = []
        self.centroids = []
        # Number of CHannels on each side to eXTenD the ReGion
        nchxtdrg = 3
        # print ('regions: ', self.regions, 'len: ', len(self.regions))
        # print ('yrg: ', self.yrg, 'len: ', len(self.yrg))
        # print ('zbl: ', self.zbl, 'len: ', len(self.zbl))
        for i in range(1, len(self.regions)):
            if len( self.yrg[i] ) >= 3:
                print('regiao maior que 3: ', i, 'compr: ', len( self.yrg[i]) )
                self.blest = bline_estimate( self.yrg[i] )
                p_bef = np.poly1d( self.zbl[i] )
                print('p_bef', p_bef)
                p_aft = np.poly1d( self.zbl[i+1] )     
                print('p_aft', p_aft)
                self.xforplot = list( range( self.regions[i][0]-nchxtdrg,
                    self.regions[i][1]+nchxtdrg+1 ) )
                print('xforplot', self.xforplot )
                self.yforfit  = list( p_bef( range(self.regions[i][0]-nchxtdrg,
                    self.regions[i][0]) )) + self.yrg[i] + list( p_aft(
                    range(self.regions[i][1]+1, self.regions[i][1] + nchxtdrg + 1)) )
                print('yforfit', self.yforfit )
                self.bl_forplot = bline_estimate( self.yforfit )
                print('bl_forplot', self.bl_forplot)
                self.net_forplot = []
                for j in range(len(self.yforfit)):
                    self.net_forplot.append( self.yforfit[j] - self.bl_forplot[j] )
                print('net_forplot', self.net_forplot)
        print ('FIM do Final step - os ajustes finais.')
