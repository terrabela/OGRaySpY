#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 17:53:26 2017

@author: marcelo
"""

import numpy as np
import matplotlib.pyplot as plt

# from test_lists import seqmatch

class CwtGraph:

# 2017-08-15 Fazer isso direito depois. Pra que pks???
#        def __init__(self, cnts, pks, cwtmatr ):
#        self.xchan = np.linspace(0, len(cnts)-1, len(cnts))
#        self.ycont = np.asarray( cnts )
#        self.pks = pks
#        self.cwtmatr = cwtmatr
    
    def __init__(self, cnts, cwtmatr ):
        self.xchan = np.linspace(0, len(cnts)-1, len(cnts))
        self.ycont = np.asarray( cnts )
        self.cwtmatr = cwtmatr

    def comparer(a1, a2, i1, i2, maxgap):
            return abs(a1[i1] - a2[i2]) <= maxgap
        
# 2017-08-15 Fazer isso direito depois. Quem sao xs, ys???
#    def plotlins(lins, codcolor):
#        for ili in range(len(lins)):
#            ptsinline = [[xs[ipt] for ipt in lins[ili]],
#                         [ ys[ipt] for ipt in lins[ili]]]
#            plt.plot( ptsinline[0], ptsinline[1], color=codcolor,
#                      linewidth=0.5, ls='-')
        # ======================================================================
        
        # Lembrar como escolher de que forma os plots devem aparecer no IPython:
        # %matplotlib inline
        # %matplotlib qt (= em nova janela)
        
    def plotcwtpeaks( self ):
        
        # ... e gr'afico
        # plt.figure(figsize=(12,8))
        # plt.plot(detre)
        # plt.title("Detren(ycont)")
        # plt.show
        
        # 2017-07-07: Reativar depois. Desativei os plots s'o para fazer benchmarking 
        # dos c'alculos
        
        plt.figure(figsize=(12,8))
        plt.plot(self.xchan, self.ycont)
        plt.plot(self.pks, self.ycont[self.pks], 'r^' )
        plt.title('Original spectrum')
        plt.show()
        
    def plotcwtmatrix( self ):

        # plt.plot(xchan_part, ycont_part)
        # plt.title("CWT-found peaks")
        # pyplot.plot(indicescwt5, ycont[indicescwt5], 'go', fillstyle='none', ms=15)
        # plt.plot(indicescwt+offs, ycont_part[indicescwt], 'r^', fillstyle='none', ms=10)

        # 2017-06-28 Gr'afico dos coeficiente cwt para dada escala
        # scalmin = 0 
        # scalmed = expect_width-1 
        # scalmax = 2*expect_width - 2

        # plt.plot(xchan, cwtmatr[scalmin], xchan_part, cwtmatr[scalmax], xchan_part, cwtmatr[scalmed])
        
        # grafico cwt: mapa de 
        plt.figure(figsize=(12,8))
        scals = 20
        #plt.imshow( self.cwtmatr, extent=[-1, 1, scals, 1], cmap='PRGn', aspect='auto', 
        #           vmax=abs( self.cwtmatr).max(), vmin=-abs(self.cwtmatr).max())
        plt.imshow( self.cwtmatr, extent=[-1, 1, scals, 1], cmap='gist_earth', aspect='auto', 
                   vmax=abs( self.cwtmatr).max(), vmin=-abs(self.cwtmatr).max())

    def grafcwt4k( self, arr ):
        scals = len(arr)
        plt.imshow(arr, extent=[0, 4095, scals, 1], cmap='PRGn', aspect='auto',
           vmax=abs(arr).max(), vmin=-abs(arr).max())
        
        # =====================================
        
##### 2017-08-08:
#### P.P. para testes

# totar = np.load('totar.npy')
# totar = np.load('totar_rf_tp.npy')
# totar = np.load('totar_ctp_17.npy')
        
# totar = np.load('totar_shifted.npy')

# scals = 20
# plt.imshow(totar, extent=[0, 4095, scals, 1], cmap='PRGn', aspect='auto',
#           vmax=abs(totar).max(), vmin=-abs(totar).max())
        