# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 12:11:50 2021

@author: mmaduar
"""

import numpy as np
from scipy.signal import find_peaks


class PeaksParms:
    """Peaks set parameters (heights, widths etc)."""

    def __init__(self):
        self.peaks = np.array([])
        self.pk_hei = np.array([])
        self.widths = (None, None)
        # self.width_heights_f = np.array([])
        # self.left_ips_f = np.array([])
        # self.right_ips_f = np.array([])

        self.mix_regions = np.array([])

        self.plateaux = np.array([])
        self.fwhm_plateaux = np.array([])
        self.wide_regions = np.array([])
        self.fwhm_centr = np.array([])
        self.rough_sums = np.array([])
        

    def redefine_widths_range(self, widths_pair, gross):
        """Redefine widths range."""
        ws_min = np.percentile(self.propts_gro['widths'], 25) * 0.5
        ws_max = np.percentile(self.propts_gro['widths'], 75) * 2.0
        widths_pair = (ws_min, ws_max)
        
    def prepare_to_sum(self):
        fwhm_centr_ini = self.propts['left_ips']
        fwhm_centr_fin = self.propts['right_ips']
        fwhm_real = fwhm_centr_fin - fwhm_centr_ini
        fwhm_centr = 0.5 * (fwhm_centr_ini + fwhm_centr_fin)
        self.fwhm_centr = fwhm_centr
        self.wide_regions = np.array(([np.ceil(fwhm_centr  - 2 * fwhm_real).astype(int),
                                       np.floor(fwhm_centr + 2 * fwhm_real).astype(int)])).T
