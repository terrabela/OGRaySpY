#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 16:10:34 2017

@author: marcelo
"""

from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QTextEdit)
from datetime import (datetime)
from time import (time)

class ChnSpectrum(QTextEdit):

    def __init__(self):
        super(ChnSpectrum, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.isUntitled = True
        self.lt = 0.0
        self.rt = 0.0

    def ti(self, by):
        ret = int.from_bytes(by, byteorder='little', signed=True)
        return ret

    def tu(self, by):
        ret = int.from_bytes(by, byteorder='little', signed=False)
        return ret

    def month_conv(month):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return months.index(month) + 1

    def readchnsp( self, fn ):
        self.cnts = []
        self.nonull_chan = []
        self.nonull_chan = []
        self.nonull_cnts = []
        self.nonull_unct = []
        
        # 2017-08-02 PAREI AQUI
        # A partir daqui mudar de IEC para CHN
        
        fi = open(fn, 'rb')
        ctn = fi.read()
        fi.close()

        # 2017-08-02 PAREI AQUI
        # ctn = binascii.hexlify(ctn)
        # self.setPlainText( bytesinsidefile )
        
        # spType = int.from_bytes( ctn[0:2], byteorder='little', signed=False)
        self.spType = self.ti(ctn[0:2])
        self.spMCA  = self.ti(ctn[2:4])
        self.spSegm  = self.ti(ctn[4:6])
        self.spStartSec  = ctn[6:8].decode('ascii')
        self.spRLTime20ms = self.tu(ctn[8:12])
        self.spLVTime20ms = self.tu(ctn[12:16])
        self.spdd   = ctn[16:18].decode('ascii')
        self.spMMM  = ctn[18:21].decode('ascii')
        self.spyy  = ctn[21:23].decode('ascii')
        self.sphh  = ctn[24:26].decode('ascii')
        self.spmm  = ctn[26:28].decode('ascii')
        self.spChOffset  = self.tu(ctn[28:30])
        self.spLngData   = self.tu(ctn[30:32])
        
        lst = []
        lst.append( str (self.spType) + '\n')
        lst.append( str (self.spMCA) + '\n')
        lst.append( str (self.spSegm ) + '\n')
        lst.append( str (self.spStartSec )+ '\n')
        lst.append( str (self.spRLTime20ms )+ '\n')
        lst.append( str (self.spLVTime20ms )+ '\n')
        lst.append( str (self.spdd )+ '\n')
        lst.append( str (self.spMMM )+ '\n')
        lst.append( str (self.spyy )+ '\n')
        lst.append( str (self.sphh )+ '\n')
        lst.append( str (self.spmm )+ '\n')
        lst.append( str (self.spChOffset )+ '\n')
        lst.append( str (self.spLngData )+ '\n')
        
        # 2-digit year specifications will be interpreted as years between 1980 and 2079.
        self.iyy = int(self.spyy)
        if self.iyy < 80:
            self.iyy += 2000
        else:
            self.iyy += 1900
        self.imo = self.month_conv(str(self.spMMM))
        # self.diahora = datetime(self.iyy, self.month_conv(str(self.spMMM)),
        #                        int(str(self.spdd)),
        #                        int(str(self.sphh)),
        #                        int(str(self.spmm)),
        #                        int(str(self.spStartSec)) )
        lst.append( str (self.iyy)+ '\n')
        # lst.append( str (self.imo)+ '\n')
        #lst.append( str (self.diahora)+ '\n')
        
        jnd_lst = ''.join(lst)
        self.setPlainText( 'sdgsdfg')
        self.setPlainText( jnd_lst )
