# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 16:30:02 2017

@author: mmaduar
"""

### 2017-08-07: Projeto corrente para analise graphless de 
### lotes de espectros para o INAC 2017

### 2017-08-13: Fork de gamma_lote para definir exatamente
### como farei a analise e como farei o shift dos espectros.

import numpy as np
from pathlib import (Path)
from teste_datas import (Spec)
from spec_cwt import (SpecCwt)

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
fb.slotSetBatchCHN('spectra/Filters_by_fclty/ctp/2017/CTP')
# fb.slotSetBatchCHN('spectra/Filters_by_fclty')
# fb.slotSetBatch('.')

print (fb.numarqstxt)

print (fb.arqslist)

## totar = TOTal ARray
totar = np.zeros( (20,4096) ) 

for fn in fb.lp:
    # print ( spec.spCounts )
    # Se espectro existe, ret = 0. Senao, -1 ou -2
    if spec.readchnsp( fn ) >= 0:
        speccwt = SpecCwt()
        peaks = speccwt.setCounts(spec.spCounts)
        
        ar = speccwt.dopksarray( 20 )
        totar += ar
        speccwt.build_cwt_matrix( spec.spCounts, 5, 11 )
        print(fn)
        # print(peaks)
np.save('totar_ctp_17', totar)
####
