# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 11:59:00 2021

@author: mmaduar
"""

import numpy as np
from numpy.polynomial import Polynomial as P  # 2020-09-06 Classe recomendada


class GenericCalib:
    """Calibrations superclass"""

    def get_calib_kind1(self):
        """Foo 1."""
        print("Preciso ver como obter isso 1.")
        return 1

    def get_calib_kind2(self):
        """Foo 2."""
        print("Preciso ver como obter isso 2.")
        return 2


class ChannelEnergyCalib(GenericCalib):
    """Energy - channel calibration."""

    def __init__(self,
                 coeffs_ch_en,
                 en_ch_calib=np.array([]),
                 chan_calib=np.array([])):
        super().__init__()
        self.calib_kind = "channel energy"

        self.p_en = np.array([])
        self.coeffs_ch_en = np.array(coeffs_ch_en)
        self.en_ch_calib = en_ch_calib
        self.chan_calib = chan_calib

        if (self.chan_calib.size >= 3) & (self.en_ch_calib.size == self.chan_calib.size):
            self.p_en = P.fit(self.chan_calib, self.en_ch_calib, deg=2)
        if np.any(self.coeffs_ch_en):
            self.p_en = P(np.flip(self.coeffs_ch_en))
        # print (self.coeffs_ch_en)

    def get_energy(self, chan):
        """Calculate energy for channel chan."""
        return self.p_en(chan)

    def is_set(self):
        """Say whether the calibration is set."""
        return np.any(self.coeffs_ch_en)


class EnergyFwhmCalib(GenericCalib):
    """Energy - FWHM calibration."""

    def __init__(self,
                 coeffs_en_fw,
                 en_fw_calib=np.array([]),
                 fwhm_calib=np.array([])):
        super().__init__()
        self.calib_kind = "energy fwhm"

        self.p_fw = np.array([])
        self.coeffs_en_fw = np.array(coeffs_en_fw)
        self.en_fw_calib = en_fw_calib
        self.fwhm_calib = fwhm_calib

        if (self.fwhm_calib.size >= 3) & (self.en_fw_calib.size == self.fwhm_calib.size):
            self.p_fw = P.fit(self.fwhm_calib, self.en_fw_calib, deg=2)
        if np.any(self.coeffs_en_fw):
            self.p_fw = P(np.flip(self.coeffs_en_fw))
        # print (self.coeffs_en_fw)

    def get_fwhm(self, engy):
        """Calculate FWHM for energy engy."""
        return self.p_fw(engy)

    def is_set(self):
        """Say whether the calibration is set."""
        return np.any(self.coeffs_en_fw)


class EnergyEfficiencyCalib(GenericCalib):
    """Energy - efficiency calibration."""

    def __init__(self,
                 coeffs_ef_en=np.array([]),
                 en_ef_calib=np.array([]),
                 effi_calib=np.array([])):
        super().__init__()
        self.calib_kind = "energy efficiency"

        self.p_ef = P(np.array([]))
        self.en_ef_calib = en_ef_calib
        self.effi_calib = effi_calib
        self.coeffs_ef_en = np.array(coeffs_ef_en)

    #        self.spec_calib1 = ChannelEnergyCalib(self.spec_parms.en_ch_calib,
    #                                              self.spec_parms.chan_calib)
    #        self.spec_calib2 = EnergyFwhmCalib(self.spec_parms.en_fw_calib,
    #                                              self.spec_parms.fwhm_calib)
    #        self.spec_calib3 = EnergyEfficiencyCalib(self.spec_parms.en_ef_calib,
    #                                              self.spec_parms.effi_calib)
    def get_effi(self, engy):
        """Calculate efficiency for energy engy."""
        return self.p_ef(engy)

    def is_set(self):
        """Say whether the calibration is set."""
        return np.any(self.coeffs_ef_en)
