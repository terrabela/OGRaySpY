# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 16:15:12 2021

@author: mmaduar
"""

from datetime import datetime
import numpy as np


class SpecIec:
    """ IEC Spectrum class. """
    sufx = '.iec'

    def __init__(self, f_name):
        self.f_name = f_name
        self.n_ch = 0
        self.lvtime = 0.0
        self.rltime = 0.0
        self.sam_descr = ''

        self.read_iec_sp()

    @staticmethod
    def convert_slice_to_datetime(i, line2):
        """ Convert a string slice starting at i into a datetime. """
        yyyy = 0
        ret = 1
        try:
            _dd = int(line2[i: i + 2])
            _mo = int(line2[i + 3: i + 5])
            _yy = int(line2[i + 6: i + 8])
            _hh = int(line2[i + 9: i + 11])
            _mi = int(line2[i + 12:i + 14])
            _ss = int(line2[i + 15:i + 17])
        except ValueError:
            ret = 0
            return ret
        # 2-digit year specifications will be interpreted as years between 1980 and 2079.
        if _yy < 80:
            yyyy = 2000 + _yy
        else:
            yyyy = 1900 + _yy
        try:
            ret = datetime(yyyy, _mo, _dd, _hh, _mi, _ss)
        except ValueError:
            ret = 0
        return ret

    def read_iec_sp(self):
        """Read an IEC file"""
        print('arq ' + self.sufx)
        with open(self.f_name, 'r') as f_file:
            lins = f_file.readlines()
        for ilin, lin in enumerate(lins):
            if lin.find(r'A004SPARE') == 0:
                inical = ilin + 1
            elif lin.find(r'A004USERDEFINED') == 0:
                inidat = ilin + 1
                break
        self.lvtime = float(lins[1][4:18])
        self.rltime = float(lins[1][18:32])
        self.n_ch = int(lins[1][32:38])
        line2 = lins[2]
        self.sp_start_datetime = self.convert_slice_to_datetime(4, line2)
        self.source_datetime = self.convert_slice_to_datetime(22, line2)
        for ilin in range(5, 8):
            self.sam_descr += lins[ilin][4:].strip() + '; '
        self.sam_descr += lins[8][4:].strip()
        lstaux1 = []
        lstaux2 = []
        itr = list(range(inical, inical + 12))
        for ilin in itr:
            lstaux1.append(float(lins[ilin][4:20]))
            lstaux2.append(float(lins[ilin][20:36]))
            lstaux1.append(float(lins[ilin][36:52]))
            lstaux2.append(float(lins[ilin][52:68]))
        self.en_ch_calib = np.trim_zeros(np.asarray(lstaux1), trim='b')
        self.chan_calib = np.asarray(lstaux2[:len(self.en_ch_calib)])

        lstaux1 = []
        lstaux2 = []
        itr = list(range(inical + 12, inical + 24))
        for ilin in itr:
            lstaux1.append(float(lins[ilin][4:20]))
            lstaux2.append(float(lins[ilin][20:36]))
            lstaux1.append(float(lins[ilin][36:52]))
            lstaux2.append(float(lins[ilin][52:68]))
        self.en_fw_calib = np.trim_zeros(np.asarray(lstaux1), trim='b')
        self.fwhm_calib = np.asarray(lstaux2[:len(self.en_fw_calib)])

        lstaux1 = []
        lstaux2 = []
        itr = list(range(inical + 24, inical + 36))
        for ilin in itr:
            lstaux1.append(float(lins[ilin][4:20]))
            lstaux2.append(float(lins[ilin][20:36]))
            lstaux1.append(float(lins[ilin][36:52]))
            lstaux2.append(float(lins[ilin][52:68]))
        self.en_ef_calib = np.trim_zeros(np.asarray(lstaux1), trim='b')
        self.effi_calib = np.asarray(lstaux2[:len(self.en_ef_calib)])

        cnts = [0]
        itr = list(range(inidat, len(lins)))
        for ilin in itr:
            cnts.append(int(lins[ilin][10:20]))
            cnts.append(int(lins[ilin][20:30]))
            cnts.append(int(lins[ilin][30:40]))
            cnts.append(int(lins[ilin][40:50]))
            cnts.append(int(lins[ilin][50:60]))
        del itr
        del lins
        self.sp_counts = cnts[:self.n_ch]

        # 2020-11-03 For IEC files, these members remain empty:
        self.coeffs_ch_en = []
        self.coeffs_en_fw = []

        #
        # self.ln_counts = np.log(self.y0snzc)
        # self.w_ln_counts = np.zeros(self.n_ch)
        # self.parab_spec = np.zeros((self.xsnzc).size)
        #

        # indFirstNonZero = y0s.nonzero()[0][0]
        # FirstNonZero = y0s[indFirstNonZero+23]
        # self.y0sCorr = np.array(self.y0s)
        # self.y0sCorr[:indFirstNonZero+23] = FirstNonZero

        # for y_nzc in self.y0snzc:
        #    if y_nzc < 2:
        #        self.ln_counts[i] = 0
        #        self.w_ln_counts[i] = 0
        #    else:
        #        self.ln_counts[i] = np.log(self.sp_counts[i])
        #        self.w_ln_counts[i] = np.sqrt(self.sp_counts[i])
