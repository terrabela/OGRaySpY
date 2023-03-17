#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 17:42:26 2017

@author: marcelo
"""

### 2017-08-04: Projeto corrente para analisar um espectro.
### 2017-08-07: Integrando busca de ridges por CWT

from teste_datas import (Spec)
from spec_cwt import (SpecCwt)
# from cwt_graph import (CwtGraph)

## P.P.

fn = 'spectra/Filtros/2016/ctp/ctp0402.Chn'
fn = 'spectra/Filtros/2017/RNP/prn3003.Chn'
spec = Spec()
#  Se espectro existe, ret = 0. Senao, -1 ou -2
ret = spec.readchnsp( fn )
print (ret)
if ret >= 0:
    # print ( spec.spCounts )
    
    speccwt = SpecCwt()

    peaks = speccwt.find_peaks( spec.spCounts, 1, 2 )
    print ( peaks )
    peaks = speccwt.find_peaks( spec.spCounts, 2, 3 )
    print ( peaks )
    peaks = speccwt.find_peaks( spec.spCounts, 20, 21 )
    print ( peaks )
    peaks = speccwt.find_peaks( spec.spCounts, 1, 4 )
    print ( peaks )
    
    nscal = 20
    
    a = speccwt.dopksarray( nscal )
    
    aa = speccwt.pksarray
    
    speccwt.build_cwt_matrix( spec.spCounts, 5, 11 )
    
    cwtgraph = CwtGraph( spec.spCounts, speccwt.indicescwt, speccwt.cwtmatr )
    
    
    cwtgraph.plotlins()
    cwtgraph.plotcwtpeaks()
    cwtgraph.plotcwtmatrix()
    
####