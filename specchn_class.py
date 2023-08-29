# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 16:13:36 2021

@author: mmaduar
"""

import struct as stru
from datetime import datetime
import re
import numpy as np


class SpecChn:
    """ CHN Spectrum class. """
    sufx = '.chn'

    def __init__(self, f_name):
        self.f_name = f_name
        self.n_ch = 0
        self.sp_counts = []
        self.source_datetime = datetime(1980, 1, 1)
        self.det_descr = ''
        self.sam_descr = ''
        self.rltime = 0
        self.lvtime = 0
        self.sp_type = 0
        self.sp_mca = 0
        self.sp_segm = 0
        self.sp_start_datetime = datetime(1980, 1, 1)
        self.coeffs_ch_en = []
        self.coeffs_en_fw = []

        self.read_chn_sp()

    @staticmethod
    def i_sign(a_byte):
        """Convert from signed byte"""
        return int.from_bytes(a_byte, byteorder='little', signed=True)

    @staticmethod
    def i_unsg(a_byte):
        """Convert from unsigned byte"""
        return int.from_bytes(a_byte, byteorder='little', signed=False)

    @staticmethod
    def month_conv(month):
        """Convert from Mmm-month"""
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        try:
            month = months.index(month) + 1
        except ValueError:
            month = 0
        return month

    def read_chn_sp(self):
        """Read a CHN file"""
        # print('arq ' + self.sufx)
        try:
            with open(self.f_name, 'rb') as f_file:
                ctn = f_file.read()
            self.sp_type = self.i_sign(ctn[0:2])
            self.sp_mca = self.i_sign(ctn[2:4])
            self.sp_segm = self.i_sign(ctn[4:6])
            sp_startsec = ctn[6:8].decode('ascii')
            sp_rltime_20ms = self.i_unsg(ctn[8:12])
            sp_lvtime_20ms = self.i_unsg(ctn[12:16])
            sp_dd = ctn[16:18].decode('ascii')
            sp_mmm = ctn[18:21].decode('ascii')
            sp_yy = ctn[21:23].decode('ascii')
            sp_hh = ctn[24:26].decode('ascii')
            sp_mm = ctn[26:28].decode('ascii')
            sp_ch_offset = self.i_unsg(ctn[28:30])
            self.n_ch = self.i_unsg(ctn[30:32])

            ini_counts = sp_ch_offset + 32
            self.sp_counts = [self.i_unsg(ctn[ini_counts + i * 4:ini_counts + (i + 1) * 4])
                              for i in range(self.n_ch)]
            i_by = ini_counts + 4 * self.n_ch
            vers_chn = int.from_bytes(ctn[i_by:i_by + 4], byteorder='little', signed=True)
            coeffs_chen0 = stru.unpack('f', ctn[i_by + 4:i_by + 8])[0]
            coeffs_chen1 = stru.unpack('f', ctn[i_by + 8:i_by + 12])[0]
            if vers_chn == -102:
                coeffs_chen2 = stru.unpack('f', ctn[i_by + 12:i_by + 16])
            else:
                coeffs_chen2 = 0.0
            self.coeffs_ch_en = [coeffs_chen2, coeffs_chen1, coeffs_chen0]
            coeffs_en_fw_0 = stru.unpack('f', ctn[i_by + 16:i_by + 20])[0]
            coeffs_en_fw_1 = stru.unpack('f', ctn[i_by + 20:i_by + 24])[0]
            if vers_chn == -102:
                coeffs_en_fw_2 = stru.unpack('f', ctn[i_by + 24:i_by + 28])
            else:
                coeffs_en_fw_2 = 0.0
            self.coeffs_en_fw = [coeffs_en_fw_2, coeffs_en_fw_1, coeffs_en_fw_0]
            # self.effi_calib = np.array([])
            len_det_descr = int(ctn[i_by + 256])
            self.det_descr = ctn[i_by + 257:i_by + 257 + len_det_descr].decode('ascii')
            len_sam_descr = int(ctn[i_by + 320])
            self.sam_descr_init = ctn[i_by + 321:i_by + 321 + len_sam_descr]
            self.sam_descr = self.sam_descr_init.decode('ascii', errors='ignore')
            self.rltime = sp_rltime_20ms * 0.02
            self.lvtime = sp_lvtime_20ms * 0.02
            # 2-digit year specifications will be interpreted as years between 1980 and 2079.
            i_yy = int(sp_yy)
            if i_yy < 80:
                i_yy += 2000
            else:
                i_yy += 1900
            self.sp_start_datetime = datetime(i_yy, self.month_conv(str(sp_mmm)),
                                              int(str(sp_dd)),
                                              int(str(sp_hh)),
                                              int(str(sp_mm)),
                                              int(str(sp_startsec)))
            ret_code = 0
        except FileNotFoundError:
            ret_code = -1
        return ret_code
