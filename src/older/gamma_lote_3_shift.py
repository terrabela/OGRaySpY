# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 16:30:02 2017

@author: mmaduar
"""

### 2017-08-07: Projeto corrente para analise graphless de 
### lotes de espectros para o INAC 2017

### 2017-08-15: Fork de gamma_lote para:
### Gravar todas as matrizes cwt previamente dos espectros
### 'as they are'.
###
### 

import numpy as np
from scipy import (signal)
from pathlib import (Path)
from teste_datas import (Spec)
from spec_cwt import (SpecCwt)
# from cwt_graph import (CwtGraph)
# from collections import (deque)

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

fb = FileBatch()
spec = Spec()


# O espectro
# spectra\Filters_by_fclty\ctp\2012\ctp\ctp3011.Chn
# gera array 'peaks' vazio, o que dah excecao ValueError

# 2017-08-15 Micro I...
fb.slotSetBatchCHN('C:/Users/mmaduar/Filtros')
# 2017-08-15 ... ou meu note:
# fb.slotSetBatchCHN('C:/Users/Marcelo/Espectros/Filtros')

print (fb.arqslist)
print (fb.numarqstxt, ' arquivos')

## totar = TOTal ARray
speccwt = SpecCwt()


idxs = []
parar = 1
erro = 0
nscal = 20
maxgap = 2
for fn in fb.lp:
    # print ( spec.spCounts )
    # Se espectro existe, ret = 0. Senao, -1 ou -2
    if spec.readchnsp( fn ) >= 0:
        print('==================')
        speccwt.setCounts(spec.spCounts)
        # peaks = speccwt.find_peaks( spec.spCounts, 7, 8 )
        # print ( peaks )
        try:
            speccwt.build_cwt_matrix( spec.spCounts, 1, 20 )
        except ValueError:
            erro = 1
            pass
        else:
            erro = 0
            # print (idx)
            # print (peaks[idx])
                
            ar = speccwt.dopksarray( 20 )
            speccwt.pksarray = np.zeros((nscal,len(speccwt.ycont)),
                                        dtype=np.int16 )
            
            # 2017-08-16 PAREI AQUI
            # usar os dados de dopksarray e cwtmatr para fazer os ridges
            matr = speccwt.cwtmatr
            # np.save( fn[:-4], matr )
            
            # speccwt.seqmatch
            
            #graf = CwtGraph( speccwt.ycont, peaks, ar_rot )
            #graf.grafcwt4k( ar_rot )
            #totar += ar_rot
            
            # totar += ar
            
            # speccwt.build_cwt_matrix( spec.spCounts, 5, 11 )
            # print(fn)
            # print(peaks)
    if parar == 10:
        break
    else:
        parar += 1
        print (parar)
        
            # Para plotar:
            # cwt_graf = CwtGraph( spec.cnts, speccwt.cwtmatr )
            # cwt_graf.plotcwtmatrix()



