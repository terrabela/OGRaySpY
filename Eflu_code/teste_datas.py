#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 16:10:34 2017

@author: marcelo
"""

from pathlib import (Path)
from datetime import (datetime)
import numpy as np
import numpy.ma as ma  # masked array

from scipy.signal import (cwt, ricker, find_peaks, find_peaks_cwt, peak_widths)
from scipy.ndimage import label, generate_binary_structure, find_objects  # 2019-09-18
# 2019-09-16
from gauss_funcs import gaus_fw, gaus_sig
# from csv import (DictReader, DictWriter)
# 2020-05-17
import struct

class Spec:

    def __init__(self):
        self.data = []

    def ti(self, by):
        return int.from_bytes(by, byteorder='little', signed=True)
    
    def tu(self, by):
        return int.from_bytes(by, byteorder='little', signed=False)

    # https://stackoverflow.com/questions/5415/convert-bytes-to-floating-point-numbers-in-python#73281
    def flo(self, by):
        return struct.unpack('f', by)[0]
    
    def month_conv( self, month):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        try:
            month = months.index(month) + 1
        except ValueError:
            month = 0
        return month
    
    # 2019-03-09 - Integrar essas 2 rotinas mais bem escritas a esta classe Spec.
    def bytes_from_file(filename, chunksize=8192):
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(chunksize)
                if chunk:
                    for b in chunk:
                        yield b
                else:
                    break
                
    def chunks_from_file(filename, chunksize=8192):
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(chunksize)
                if chunk:
                    yield chunk
                else:
                    break
                
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
                # 2020-05-17
                self.lastpart = self.inicounts + 4*self.spLngData 
                self.chnVersion = self.ti(ctn[self.lastpart:self.lastpart+2])
                self.enCalZinpt = self.flo(ctn[self.lastpart+4:self.lastpart+8])
                self.enCalSlope = self.flo(ctn[self.lastpart+8:self.lastpart+12])
                self.enCalQuadr = self.flo(ctn[self.lastpart+12:self.lastpart+16])
                self.pkShpZinpt = self.flo(ctn[self.lastpart+16:self.lastpart+20])
                self.pkShpSlope = self.flo(ctn[self.lastpart+20:self.lastpart+24])
                self.pkShpQuadr = self.flo(ctn[self.lastpart+24:self.lastpart+28])
                self.lenDetDesc = ctn[self.lastpart+256]
                self.detDesc = ctn[self.lastpart+257:self.lastpart+257+self.lenDetDesc].decode('ascii')
                self.lenSamDesc = ctn[self.lastpart+320]
                self.samDesc = ctn[self.lastpart+321:self.lastpart+321+self.lenSamDesc].decode('ascii')
                
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
                
                lst.append( str (self.iyy)+ '\n')
                lst.append( str (self.imo)+ '\n')
                lst.append( str (self.spRLTime) + '\n')
                lst.append( str (self.spLVTime) + '\n')
                lst.append( str (self.diahora)+ '\n')
                # lst.append( str (self.spCounts)+ '\n')
                
                self.jnd_lst = ''.join(lst)
                ret = 0
        else:
            ret = -2
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
                inidat = 1
                for lin in lins:
                    if lin.find(r'A004USERDEFINED') == 0:
                        break
                    inidat += 1
                    
                self.spLVTime = float( lins[1][ 4:18] )
                self.spRLTime = float( lins[1][18:32] )
                self.spLngData = int( lins[1][32:38] )
                self.samDesc = ''
                for i in range(5,9): self.samDesc += lins[i][4:].strip() + '; '
                self.samDesc = self.samDesc[:-2]+'.'

                #self.diahora = datetime(self.iyy, self.month_conv(str(self.spMMM)),
                #                        int(str(self.spdd)),
                #                        int(str(self.sphh)),
                #                        int(str(self.spmm)),
                #                        int(str(self.spStartSec)) )

                # 2-digit year specifications will be interpreted as years between 1980 and 2079.
                self.iyy = int(lins[2][10:12])
                if self.iyy < 80:
                    self.iyy += 2000
                else:
                    self.iyy += 1900
                
                self.diahora = datetime(self.iyy,int(lins[2][7:9]),int(lins[2][4:6]),
                                        int(lins[2][13:15]),int(lins[2][16:18]),int(lins[2][19:21]))
                
                #                        int(str(self.spdd)),
                #                        int(str(self.sphh)),
                #                        int(str(self.spmm)),
                #                        int(str(self.spStartSec)) )
                
                cnts = [0]
                itr = list(range( inidat, len(lins) ))
                for ilin in itr:
                    cnts.append( int(lins[ilin][10:20]) )
                    cnts.append( int(lins[ilin][20:30]) )
                    cnts.append( int(lins[ilin][30:40]) )
                    cnts.append( int(lins[ilin][40:50]) )
                    cnts.append( int(lins[ilin][50:60]) )
                del itr
                del lins
                
                self.spCounts = cnts[:self.spLngData]
                ret = 0
        else:
            ret = -2
        return ret    

    def readSp (self, fn ):
        ret = 0
        sufx = Path(fn).suffix.casefold()
        if sufx == '.chn':
            ret = self.readchnsp( fn )
        elif sufx == '.iec':
            ret = self.readiecsp( fn )
        else:
            ret = -1
        return ret
    
    def defRegsSpec(self, side_extd=13, min_separ_pks=30):
        regions = []
        ### pobrema aqui
        start = self.indicescwt[0]-side_extd
        if start < 0:
            start = 0
        multiplet =[]
        multiplets = []
        for i in range(len(self.indicescwt)-1):
            if self.indicescwt[i+1] - self.indicescwt[i] > min_separ_pks:
                regions.append([start, self.indicescwt[i]+side_extd])
                multiplet.append(self.indicescwt[i])
                multiplets.append(multiplet)
                start = self.indicescwt[i+1]-side_extd
                multiplet = []
            else:
                multiplet.append(self.indicescwt[i])
        final = self.indicescwt[-1]+side_extd
        if final >= self.spLngData:
            final = self.spLngData - 1
        regions.append([self.indicescwt[-1]-side_extd,final])
        multiplet.append(self.indicescwt[-1])
        multiplets.append(multiplet)
        return regions, multiplets    
    
    def scanSpec( self ):
        # expect_width = 7      # 2018-Jun-10: mudei pra 30; Jun-21: mudei para 5
        expect_width = 4
        widths = np.arange(1, expect_width)
        
        self.indicescwt = find_peaks_cwt(self.spCounts, widths, max_distances=widths,
                                           gap_thresh=2.0, min_snr=1.5)
        self.regions, self.multiplets = self.defRegsSpec()
        return self.indicescwt, self.regions, self.multiplets
    
    def defBlineRegionsSpec( self ):

        ######################################

        # Define baseline regions (list 'blin')

        self.blin = []
        self.blin.append( [ 0, self.regions[0][0] ] )
        for i in range(len(self.regions)-1):
            self.blin.append( [self.regions[i][1], self.regions[i+1][0]] )
        self.blin.append( [ self.regions[-1][1], self.spLngData-1 ] )
        return self.blin

    def defBlineRegionsSpec_B( self ):

        ######################################

        # 2019-05-21 Novo defBline
        # Define baseline regions (list 'blin')

        self.blin = []
        self.blin.append( [ 0, self.regions[0][0] ] )
        for i in range(len(self.regions)-1):
            self.blin.append( [self.regions[i][1], self.regions[i+1][0]] )
        self.blin.append( [ self.regions[-1][1], self.spLngData-1 ] )
        return self.blin

    def blinesFitSpec( self ):

    # Baseline fit between regions

        xbl = []
        ybl = []
        zbl = []
        for i in range(len(self.blin)):
            xbl.append( list( range( self.blin[i][0], self.blin[i][1]+1 ) ) )
            ybl.append( self.spCounts[ self.blin[i][0]:self.blin[i][1]+1 ] )
            zbl.append( np.polyfit(xbl[i], ybl[i], 2) )

        # Baseline estimating inside regions

        xrg = []
        yrg = []
        zrg = []
        for i in range(len(self.regions)):
            xrg.append( list( range( self.regions[i][0], self.regions[i][1]+1 ) ) )
            yrg.append( self.spCounts[ self.regions[i][0]:self.regions[i][1]+1 ] )
            deltay = yrg[i][-1] - yrg[i][0]
            sumy = sum( yrg[i] )
            cumy = 0
            zrgi = []
            for j in range( len( yrg[i] ) ):
                zrgi.append( yrg[i][0] )
            zrg.append( np.polyfit(xrg[i], yrg[i], 2) )

        # return xbl, ybl, zbl, xrg, yrg, zrg
        return 0

# 2019-11-04 Para cada fn2:
# Modificado em 2019-11-23

# Funcao Ricker:
# A (1 - x^2/a^2) exp(-x^2/2 a^2), onde
# A = 2/sqrt(3a)pi^1/4
# Fazendo anahlise no Maxima, descobri que o fator de escala "a"
# ohtimo eh sigma*sqrt(5):
        
# Lembrar que:
# sigma_experim = widthmax / np.sqrt(5)
# sigma_experim    

def analisa_um_fn(fn2):
    
    # widths = np.linspace(2,13,num=100)
    # para espectros 8k
    # widths = np.linspace(2,13,num=30)
    # para espectros 4k
    widths = np.linspace(2,7,num=30)
    n_side_chans = 11
    n_side_centr_ch = 5
    nsca_det = 5
    # constante k: ver no Maxima: (sqrt(3)*6^(3/2))/(2^(3/2)*5^(5/4)*%pi^(1/4));
    k = (np.sqrt(3)*6**(3/2))/(2**(3/2)*5**(5/4)*np.pi**(1/4))
    kfwhm = 2*np.sqrt(2*np.log(2))
    min_cwtpk = 13.0
    karea = np.sqrt(2*np.pi)
    # ~2.507
    spec2 = Spec()
    spec2.readSp( fn2 )
    # 2019-11-26 Preciso mudar esse remendo URGENTE!!
    spec2.spLngData = 4096
    xs = np.linspace(0,spec2.spLngData-1,spec2.spLngData)
    y0s = np.asarray(spec2.spCounts)

    ipks2 = find_peaks_cwt(y0s,widths=[widths[1]],wavelet=ricker,max_distances=widths/4,min_snr=1.0,noise_perc=10)
    ipks2

    pk_per_scal = []
    for wid in widths:
        pk_per_scal.append(find_peaks_cwt
                           (y0s,widths=[wid],wavelet=ricker,max_distances=widths/4,min_snr=1.0,noise_perc=10))

    pks_cwt_flatten = []
    for isc, pksc in enumerate(pk_per_scal):
        for pk in pksc:
            pks_cwt_flatten.append([pk,widths[isc]])
    len(pks_cwt_flatten)
    
    pks_cwt_flatten = []
    for isc, pksc in enumerate(pk_per_scal):
        for pk in pksc:
            pks_cwt_flatten.append([pk,widths[isc]])
    
    ar1 = np.asarray(pks_cwt_flatten)
    
    # imag1: imagem de pixels binahrios dos picos nas escalas
    imag1 = np.zeros((len(widths),len(xs)))
    for isc, pksc in enumerate(pk_per_scal):
        for pk in pksc:
            imag1[isc,pk] = 1
    stru_diag_also = generate_binary_structure(2,2)
    lblimag1, num_feat_imag1 = label(imag1,stru_diag_also)
    ridges = find_objects(lblimag1)
    ridges_rectangles = [lblimag1[loc] for loc in ridges]
    cwtmatr = cwt(y0s, ricker, widths)

    xpk = []
    ypk = []
    centrpk = []
    cwtpk = []
    nscpk = []
    regions_slcs = []
    for iridge, ridge in enumerate(ridges):
        lbl_ridge = iridge+1
        nscpk.append( ridge[0].stop - ridge[0].start)
        labeled = lblimag1[ridge]
        cwts_ridge = cwtmatr[ridge]
        retang3 = ma.masked_where(labeled!=lbl_ridge,cwts_ridge)
        maxim3 = np.max(retang3)
        flat_retang_ind = np.argmax(retang3)
        retang_indices = np.unravel_index(flat_retang_ind,np.shape(retang3))
        indices_max_in_ridge = tuple(map(lambda x, y: x + y, retang_indices, (ridge[0].start, ridge[1].start)))
        cwtpk.append(maxim3)
        xpk.append( indices_max_in_ridge[1] )
        ypk.append( widths[indices_max_in_ridge[0]] )
        region_slc = slice(xpk[-1]-n_side_chans, xpk[-1]+n_side_chans+1)
        regions_slcs.append(region_slc)
        # 2019-10-02 C'alculo de centroide
        region_centr = slice(xpk[-1]-n_side_centr_ch, xpk[-1]+n_side_centr_ch+1)
        centrpk.append( np.sum(xs[region_centr]*y0s[region_centr]) / np.sum(y0s[region_centr]))

    nscpk_ma = ma.masked_less(nscpk, nsca_det)
    cwtpk_ma = ma.masked_less(cwtpk, min_cwtpk)
    valid_peaks = ~(cwtpk_ma.mask | nscpk_ma.mask)
    regions_slcs_valid = np.asarray(regions_slcs)[valid_peaks]

    ypkregs = []
    fwhms = []
    gau_areas = []
    unc_gau_areas = []
    peak_constructed_spectrum = np.zeros(len(xs))
    for ipk, pk in enumerate(valid_peaks):
        if pk:
            # ypicoregio = gaus_sig(xs[regions_slcs[ipk2]],sigmamaximo,gau_hei,centroide)ypicoregio
            # subtrair o pica v'alido
            escalmaxima = ypk[ipk]
            maxcwt = cwtpk[ipk]
            centroide = centrpk[ipk]
            sigmamaximo = escalmaxima / np.sqrt(5)
            fwhm = kfwhm * sigmamaximo
            gau_hei = k * maxcwt / np.sqrt(sigmamaximo)
            gau_area = gau_hei * sigmamaximo * karea
            # print(escalmaxima, maxcwt, centroide, sigmamaximo, gau_hei)
            region_start = regions_slcs[ipk].start
            # print(region_start)
            ypicoregio = gaus_sig(xs[regions_slcs[ipk]],sigmamaximo,gau_hei,centroide)
            # print(ypicoregio)
            ypkregs.append(ypicoregio)
            fwhms.append(fwhm)
            gau_areas.append(gau_area)
            peak_constructed_spectrum[regions_slcs[ipk]] += ypicoregio
    # peak_constructed_spectrum
    baseline_spectrum = y0s - peak_constructed_spectrum
    len_bl = len(baseline_spectrum)
    bl_median_smoother = np.zeros(len_bl)
    bl_median_smoother[20:len_bl-20] = np.asarray(
        [np.median(baseline_spectrum[i-n_side_chans:i+n_side_chans+1]) for i in range(20,len_bl-20) ])
    
    for ipk,regio in enumerate(regions_slcs_valid):
        bline_cts = np.sum(bl_median_smoother[regio])
        unc_gau_area = np.sqrt(gau_areas[ipk]+bline_cts)
        # print ('gau_areas: ', gau_areas[ipk])
        # print ('unc_gau_area: ', unc_gau_area)
        # print ('bline_cts: ', bline_cts)
        # print ('------------------------')
        unc_gau_areas.append(unc_gau_area)
    y0s_xpk_valid = y0s[xpk][valid_peaks]
    y0s_xpk_invld = y0s[xpk][~valid_peaks]
    centrpk_valid = np.asarray(centrpk)[valid_peaks]
    centrpk_invld = np.asarray(centrpk)[~valid_peaks]
    # df2 = pd.DataFrame({'Centr': centrpk_valid,
    #                     'Fwhm': fwhms,
    #                     'Area': gau_areas,
    #                     'SArea': unc_gau_areas})
    return spec2, ar1, xpk, ypk, peak_constructed_spectrum, bl_median_smoother, y0s_xpk_valid, y0s_xpk_invld, \
    valid_peaks, regions_slcs_valid, centrpk_valid, centrpk_invld, fwhms, gau_areas, unc_gau_areas 