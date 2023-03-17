# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 16:30:02 2017

@author: mmaduar
"""

### 2017-08-07: Projeto corrente para analise graphless de 
### lotes de espectros para o INAC 2017

### 2017-08-14: Fork de gamma_lote para:
### Fazer o drift do canal.
### Fazer coinicidir todos os picos 364 keV do I-131 no canal 411.
### 

import numpy as np
from pathlib import (Path)
from teste_datas import (Spec)
from spec_cwt import (SpecCwt)
from collections import (deque)

class FileBatch:
    
    def slotSetBatchIEC(self, locpath):

            #### 2017-07-31  PAREI AQUI. Agora hah varias coisas a fazer:
            ###
            ### - montar a lista de espectros para o INAC 2017:
            ### --- fazer a leitura de CHN !!!!
            ### --- usar CWT para ler os picos e pohr no SQLite

        # 2017-07-20 usando Path.glob
        self.p = Path( locpath )
        print( locpath )
        # lpp is a system-aware list of path p
        self.lpp = list( self.p.glob('**/*.[Ii][Ee][Cc]'))
        # lp is a list of strings from lpp
        self.lp = [ str(ip) for ip in self.lpp ]
            
        # https://docs.python.org/3.7/library/string.html
        self.arqslist = ''
        for ip in self.lp: self.arqslist += ip + '\n'
        self.numarqstxt  = 'Num de arquivos: {:>10} \n\n\n'.format(len(self.lp))
        self.anallogStr = '\n' + self.arqslist + '\n' + self.numarqstxt

    def slotSetBatchCHN(self, locpath):

            #### 2017-07-31  PAREI AQUI. Agora hah varias coisas a fazer:
            ###
            ### - montar a lista de espectros para o INAC 2017:
            ### --- fazer a leitura de CHN !!!!
            ### --- usar CWT para ler os picos e pohr no SQLite

        # 2017-07-20 usando Path.glob
        self.p = Path( locpath )
        print( locpath )
        # lpp is a system-aware list of path p
        self.lpp = list( self.p.glob('**/*.[Cc][Hh][Nn]'))
        # lp is a list of strings from lpp
        self.lp = [ str(ip) for ip in self.lpp ]
            
        # https://docs.python.org/3.7/library/string.html
        self.arqslist = ''
        for ip in self.lp: self.arqslist += ip + '\n'
        self.numarqstxt  = 'Num de arquivos: {:>10} \n\n\n'.format(len(self.lp))
        self.anallogStr = '\n' + self.arqslist + '\n' + self.numarqstxt


##################################################
## P.P.

# soh exemplos de fn
fn = 'spectra/Filtros/2016/ctp/ctp0402.Chn'
fn = 'spectra/Filtros/2017/RNP/prn3003.Chn'

fb = FileBatch()
spec = Spec()

# 2017-08-13 Teste com espectros recentes para diminuir
# tempo de execucao.
# Depois, voltar para set total.
# fb.slotSetBatchCHN('spectra/Filters_by_fclty/ctp/2017/CTP')
# fb.slotSetBatchCHN('spectra/Filters_by_fclty')
# fb.slotSetBatch('.')

# O espectro
# spectra\Filters_by_fclty\ctp\2012\ctp\ctp3011.Chn
# gera array 'peaks' vazio, o que dah excecao ValueError
fb.slotSetBatchCHN('spectra/Filters_by_fclty')

print (fb.numarqstxt)

print (fb.arqslist)

## totar = TOTal ARray
totar = np.zeros( (20,4096) ) 
speccwt = SpecCwt()


idxs = []
parar = 1
for fn in fb.lp:
    # print ( spec.spCounts )
    # Se espectro existe, ret = 0. Senao, -1 ou -2
    if spec.readchnsp( fn ) >= 0:
        print('==================')
        speccwt.setCounts(spec.spCounts)
        peaks = speccwt.find_peaks( spec.spCounts, 7, 8 )
        print ( peaks )
        
        try:
            idx = (np.abs(peaks-411)).argmin()
        except ValueError:
            break
        else:
            print (idx)
            print (peaks[idx])
            nrot = peaks[idx]-411
            print(nrot)
       
            if (nrot != 0):
                deq = deque(spec.spCounts)
                deq.rotate(-nrot)
                rotcounts = [c for c in deq]
                speccwt.setCounts( rotcounts )
                
            ar = speccwt.dopksarray( 20 )
            
            
            
            #graf = CwtGraph( speccwt.ycont, peaks, ar_rot )
            #graf.grafcwt4k( ar_rot )
            #totar += ar_rot
            
            totar += ar
            
            # speccwt.build_cwt_matrix( spec.spCounts, 5, 11 )
            # print(fn)
            # print(peaks)
    if parar == 4000:
        break
    else:
        parar += 1
        print (parar)
        
np.save('totar_shifted', totar)
####


