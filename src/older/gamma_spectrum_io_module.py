import numpy as np
import struct as stru
from datetime import (datetime)

class SpecIO:
    
    def ti(self, by):
        return int.from_bytes(by, byteorder='little', signed=True)
    
    def tu(self, by):
        return int.from_bytes(by, byteorder='little', signed=False)
    
    def month_conv( self, month):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        try:
            month = months.index(month) + 1
        except ValueError:
            month = 0
        return month
    
    def readchnsp( self, fn ):
        if fn:
            self.cnts = []
            self.nonull_chan = []
            self.nonull_cnts = []
            self.nonull_unct = []
            try:
                fi = open(fn, 'rb')
            except (FileNotFoundError, IOError):
                print(r'Erro de arquivo CHN!!!')
                ret = -1
            else:
                ctn = fi.read()
                fi.close()
        
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

                self.inicounts = self.spChOffset + 32
                self.spCounts = [ self.tu( ctn[self.inicounts+i*4:self.inicounts+(i+1)*4] )
                    for i in range(self.spLngData) ]
                
                iBy = self.inicounts + 4*self.spLngData
                versChn = int.from_bytes(ctn[iBy:iBy+4], byteorder='little', signed=True)
                
                coeffs_ChEn_0 = stru.unpack('f', ctn[iBy+4:iBy+8])[0]
                coeffs_ChEn_1 = stru.unpack('f', ctn[iBy+8:iBy+12])[0]
                if versChn == -102:
                    coeffs_ChEn_2 = stru.unpack('f', ctn[iBy+12:iBy+16])
                else:
                    coeffs_ChEn_2 = 0.0
                self.coeffs_ChEn = [coeffs_ChEn_2, coeffs_ChEn_1, coeffs_ChEn_0 ]
                
                coeffs_EnFw_0 = stru.unpack('f', ctn[iBy+16:iBy+20])[0]
                coeffs_EnFw_1 = stru.unpack('f', ctn[iBy+20:iBy+24])[0]
                if versChn == -102:
                    coeffs_EnFw_2 = stru.unpack('f', ctn[iBy+24:iBy+28])
                else:
                    coeffs_EnFw_2 = 0.0
                self.coeffs_EnFw = [coeffs_EnFw_2, coeffs_EnFw_1, coeffs_EnFw_0 ]
                
                detDescrLen  = int(ctn[iBy+256])
                self.detDescr  = ctn[iBy+257:iBy+257+detDescrLen].decode('ascii')
                samDescrLen  = int(ctn[iBy+320])
                self.samDescr  = ctn[iBy+321:iBy+321+samDescrLen].decode('ascii')

                self.spRLTime = self.spRLTime20ms * 0.02
                self.spLVTime = self.spLVTime20ms * 0.02
                
                # 2-digit year specifications will be interpreted as years between 1980 and 2079.
                self.iyy = int(self.spyy)
                if self.iyy < 80:
                    self.iyy += 2000
                else:
                    self.iyy += 1900
                self.imo = self.month_conv(str(self.spMMM))
                self.diahora = datetime(self.iyy, self.month_conv(str(self.spMMM)),
                                        int(str(self.spdd)),
                                        int(str(self.sphh)),
                                        int(str(self.spmm)),
                                        int(str(self.spStartSec)) )
                
                self.sourceDatetime = 0
                
                # 2020-11-03 For CHN files, these members remain empty:
                self.enChcalib = np.array([])
                self.chancalib = np.array([])
                self.enFwcalib = np.array([])
                self.fwhmcalib = np.array([])
                self.enEfcalib = np.array([])
                self.efficalib = np.array([])
                ret = self.spLngData                
        else:
            ret = -2
        return ret    

    def convertSliceToDatetime( self, i, line2):
        yyyy = 0
        ret = 1
        try:
            dd = int( line2[ i  : i+2] )
            mo = int( line2[ i+3: i+5] )
            yy = int( line2[ i+6: i+8] )
            hh = int( line2[ i+9: i+11] )
            mi = int( line2[ i+12:i+14] )
            ss = int( line2[ i+15:i+17] )
        except ValueError:
            ret = 0
            return ret
        # 2-digit year specifications will be interpreted as years between 1980 and 2079.
        if yy < 80:
            yyyy += 2000
        else:
            yyyy += 1900
        try:
            ret = datetime(yyyy, mo, dd, hh, mi, ss)
        except ValueError:
            ret = 0
        return ret
    
    def readiecsp( self, fn ):
        if fn:
            self.cnts = []
            self.nonull_chan = []
            self.nonull_cnts = []
            self.nonull_unct = []
            try:
                fi = open(fn, 'r')
            except (FileNotFoundError, IOError):
                print(r'Erro de arquivo IEC !!!')
                ret = -1
            else:
                lins = fi.readlines()
                fi.close()
                inidat = 0
                inical = 0
                for ilin, lin in enumerate(lins):
                    if lin.find(r'A004SPARE') == 0:
                        inical = ilin+1
                    elif lin.find(r'A004USERDEFINED') == 0:
                        inidat = ilin+1
                        break
                self.spLVTime = float( lins[1][ 4:18] )
                self.spRLTime = float( lins[1][18:32] )
                self.spLngData = int( lins[1][32:38] )
                
                line2 = lins[2]
                self.diahora = self.convertSliceToDatetime( 4, line2 )
                self.sourceDatetime = self.convertSliceToDatetime( 22, line2 )

                # 2020-11-03 For IEC files, these members is set:
                self.enChcalib = []
                self.chancalib = []
                self.enFwcalib = []
                self.fwhmcalib = []
                self.enEfcalib = []
                self.efficalib = []
                #
                
                lstaux1 = []
                lstaux2 = []
                itr = list(range( inical, inical+12 ))
                for ilin in itr:
                    lstaux1.append( float(lins[ilin][ 4:20]) )
                    lstaux2.append( float(lins[ilin][20:36]) )
                    lstaux1.append( float(lins[ilin][36:52]) )
                    lstaux2.append( float(lins[ilin][52:68]) )
                self.enChcalib = np.trim_zeros(np.asarray(lstaux1),trim='b')
                self.chancalib = np.asarray(lstaux2[:len(self.enChcalib)])
                    
                lstaux1 = []
                lstaux2 = []
                itr = list(range( inical+12, inical+24 ))
                for ilin in itr:
                    lstaux1.append( float(lins[ilin][ 4:20]) )
                    lstaux2.append( float(lins[ilin][20:36]) )
                    lstaux1.append( float(lins[ilin][36:52]) )
                    lstaux2.append( float(lins[ilin][52:68]) )
                self.enFwcalib = np.trim_zeros(np.asarray(lstaux1),trim='b')
                self.fwhmcalib = np.asarray(lstaux2[:len(self.enFwcalib)])
                    
                lstaux1 = []
                lstaux2 = []
                itr = list(range( inical+24, inical+36 ))
                for ilin in itr:
                    lstaux1.append( float(lins[ilin][ 4:20]) )
                    lstaux2.append( float(lins[ilin][20:36]) )
                    lstaux1.append( float(lins[ilin][36:52]) )
                    lstaux2.append( float(lins[ilin][52:68]) )
                self.enEfcalib = np.trim_zeros(np.asarray(lstaux1),trim='b')
                self.efficalib = np.asarray(lstaux2[:len(self.enEfcalib)])
    
                self.cnts = [0]
                itr = list(range( inidat, len(lins) ))
                for ilin in itr:
                    self.cnts.append( int(lins[ilin][10:20]) )
                    self.cnts.append( int(lins[ilin][20:30]) )
                    self.cnts.append( int(lins[ilin][30:40]) )
                    self.cnts.append( int(lins[ilin][40:50]) )
                    self.cnts.append( int(lins[ilin][50:60]) )
                del itr
                del lins
                
                # 2020-11-03 For IEC files, these members remain empty:
                self.coeffs_ChEn = []
                self.coeffs_EnFw = []
                
                self.spCounts = self.cnts[:self.spLngData]
                ret = self.spLngData
        else:
            ret = -2
        return ret
    
    def writeiecsp( self, fn ):
        nlines = 
        if fn:
            self.cnts = []
            self.nonull_chan = []
            self.nonull_cnts = []
            self.nonull_unct = []
            try:
                fi = open(fn, 'r')
            except (FileNotFoundError, IOError):
                print(r'Erro de arquivo IEC !!!')
                ret = -1
            else:
                lins = fi.readlines()
                fi.close()
                inidat = 0
                inical = 0
                for ilin, lin in enumerate(lins):
                    if lin.find(r'A004SPARE') == 0:
                        inical = ilin+1
                    elif lin.find(r'A004USERDEFINED') == 0:
                        inidat = ilin+1
                        break
                self.spLVTime = float( lins[1][ 4:18] )
                self.spRLTime = float( lins[1][18:32] )
                self.spLngData = int( lins[1][32:38] )
                
                line2 = lins[2]
                self.diahora = self.convertSliceToDatetime( 4, line2 )
                self.sourceDatetime = self.convertSliceToDatetime( 22, line2 )

                # 2020-11-03 For IEC files, these members is set:
                self.enChcalib = []
                self.chancalib = []
                self.enFwcalib = []
                self.fwhmcalib = []
                self.enEfcalib = []
                self.efficalib = []
                #
                
                lstaux1 = []
                lstaux2 = []
                itr = list(range( inical, inical+12 ))
                for ilin in itr:
                    lstaux1.append( float(lins[ilin][ 4:20]) )
                    lstaux2.append( float(lins[ilin][20:36]) )
                    lstaux1.append( float(lins[ilin][36:52]) )
                    lstaux2.append( float(lins[ilin][52:68]) )
                self.enChcalib = np.trim_zeros(np.asarray(lstaux1),trim='b')
                self.chancalib = np.asarray(lstaux2[:len(self.enChcalib)])
                    
                lstaux1 = []
                lstaux2 = []
                itr = list(range( inical+12, inical+24 ))
                for ilin in itr:
                    lstaux1.append( float(lins[ilin][ 4:20]) )
                    lstaux2.append( float(lins[ilin][20:36]) )
                    lstaux1.append( float(lins[ilin][36:52]) )
                    lstaux2.append( float(lins[ilin][52:68]) )
                self.enFwcalib = np.trim_zeros(np.asarray(lstaux1),trim='b')
                self.fwhmcalib = np.asarray(lstaux2[:len(self.enFwcalib)])
                    
                lstaux1 = []
                lstaux2 = []
                itr = list(range( inical+24, inical+36 ))
                for ilin in itr:
                    lstaux1.append( float(lins[ilin][ 4:20]) )
                    lstaux2.append( float(lins[ilin][20:36]) )
                    lstaux1.append( float(lins[ilin][36:52]) )
                    lstaux2.append( float(lins[ilin][52:68]) )
                self.enEfcalib = np.trim_zeros(np.asarray(lstaux1),trim='b')
                self.efficalib = np.asarray(lstaux2[:len(self.enEfcalib)])
    
                self.cnts = [0]
                itr = list(range( inidat, len(lins) ))
                for ilin in itr:
                    self.cnts.append( int(lins[ilin][10:20]) )
                    self.cnts.append( int(lins[ilin][20:30]) )
                    self.cnts.append( int(lins[ilin][30:40]) )
                    self.cnts.append( int(lins[ilin][40:50]) )
                    self.cnts.append( int(lins[ilin][50:60]) )
                del itr
                del lins
                
                # 2020-11-03 For IEC files, these members remain empty:
                self.coeffs_ChEn = []
                self.coeffs_EnFw = []
                
                self.spCounts = self.cnts[:self.spLngData]
                ret = self.spLngData
        else:
            ret = -2
        return ret
    
# 2019-03-09 - Integrar essas 2 rotinas mais bem escritas a esta classe de io:

#    def bytes_from_file(filename, chunksize=8192):
#        with open(filename, "rb") as f:
#            while True:
#                chunk = f.read(chunksize)
#                if chunk:
#                    for b in chunk:
#                        yield b
#                else:
#                    break
                
#    def chunks_from_file(filename, chunksize=8192):
#        with open(filename, "rb") as f:
#            while True:
#                chunk = f.read(chunksize)
#                if chunk:
#                    yield chunk
#                else:
#                    break
                    
                    


    
