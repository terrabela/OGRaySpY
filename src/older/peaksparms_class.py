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

        self.peaks_net = np.array([])
        self.propts_halfhe_net = np.array(1)

        self.width_heights_f = np.array([])
        self.left_ips_f = np.array([])
        self.right_ips_f = np.array([])

        self.width_heights = np.array([])
        self.left_ips = np.array([])
        self.right_ips = np.array([])
        self.pk_hei = np.array([])
        self.promns = np.array([])
        self.widths = np.array([])

        self.xs_fwhm_lines = np.array([])
        self.ys_fwhm_lines = np.array([])
        self.xs_fwb_lines = np.array([])
        self.ys_fwb_lines = np.array([])

        self.mix_regions = np.array([])
        self.width_range = (None, None)

        self.plateaux = np.array([])

        self.fwhm_ch_ini = np.array([])
        self.fwhm_ch_fin = np.array([])
        self.n_ch_fwhm = np.array([])

        self.fwhm_chans = []
        self.counts_gross = []
        self.counts_net = []
        self.sum_gross = np.array([])
        self.sum_net = np.array([])
        self.s_sum_net = np.array([])

        self.fwhm_ctrs = np.array([])

    def initial_peaks_search(self, n_ch, cts_to_search,
                             peak_sd_fact=3.0, width_range=(None, None),
                             areas_calc='under_fwhm'):
        """First peak search; use scipy.signal.find_peaks."""
        height = peak_sd_fact * np.sqrt(cts_to_search)
        prominence = peak_sd_fact * np.sqrt(cts_to_search)
        if width_range == (None, None):
            width_range = (n_ch * 0.0003, n_ch * 0.01)
        self.width_range = width_range
        self.peaks, propts_halfhe = find_peaks (
            cts_to_search,
            height=height,
            threshold=(None, None),
            prominence=prominence,
            width=width_range,
            rel_height=0.5)

        self.width_heights = propts_halfhe['width_heights']
        self.left_ips = propts_halfhe['left_ips']
        self.right_ips = propts_halfhe['right_ips']
        self.pk_hei = propts_halfhe['peak_heights']
        self.promns = propts_halfhe['prominences']
        self.widths = propts_halfhe['widths']

        self.plateaux = self.pk_hei -self.promns

        n_pk = self.peaks.size

        self.fwhm_ch_ini = np.ceil(self.left_ips).astype(int)
        self.fwhm_ch_fin = np.floor(self.right_ips).astype(int)
        self.n_ch_fwhm = self.fwhm_ch_fin - self.fwhm_ch_ini + 1

        self.counts_gross = [
            cts_to_search[ self.fwhm_ch_ini[i_pk]: self.fwhm_ch_fin[i_pk]+1]
            for i_pk in range(n_pk) ]
        self.counts_net = [
            self.counts_gross[i_pk] - self.plateaux[i_pk]
            for i_pk in range(n_pk) ]

        self.fwhm_chans = [
            np.array(range(self.fwhm_ch_ini[i_pk], self.fwhm_ch_fin[i_pk]+1))
            for i_pk in range(n_pk) ]

        self.sum_gross = np.array([np.sum(self.counts_gross[i_pk])
                                   for i_pk in range(n_pk)])
        self.sum_net = np.array([np.sum(self.counts_net[i_pk])
                          for i_pk in range(n_pk)])

        if areas_calc=='under_fwhm':
            # Centroids
            self.fwhm_ctrs = np.array([
                np.average(self.fwhm_chans[i_pk], weights=self.counts_net[i_pk])
                for i_pk in range(n_pk)
                ])
            # Uncertainties in areas
            self.s_sum_net = np.sqrt(self.sum_gross + self.n_ch_fwhm**2 * self.plateaux)

    def initial_width_lines(self):
        """Build width peaks related lines, just for plotting."""
        n_pk = self.peaks.size
        self.xs_fwhm_lines = np.concatenate(np.stack(
            (self.left_ips, self.right_ips, np.full(n_pk, None)), axis=1))
        self.ys_fwhm_lines = np.concatenate(np.stack(
            (self.width_heights, self.width_heights, np.full(n_pk, None)), axis=1))
        self.xs_fwb_lines = np.concatenate(np.stack(
            (self.fwhm_ch_ini, self.fwhm_ch_fin, np.full(n_pk, None)), axis=1))
        self.ys_fwb_lines = np.concatenate(np.stack(
            (self.plateaux, self.plateaux, np.full(n_pk, None)), axis=1))

    def define_multiplets_regions(self, n_ch, is_reg):
        """Define multiplet regions from already found peaks with proper widths."""
        # Fator de fwhm para separar picos de um multipleto
        k_sep_pk = 1.5

        # 2021-06-28
        if self.peaks.any():
            for i_pk, ch_pk in enumerate(self.peaks):
                if ((self.widths[i_pk] > self.width_range[0]) and
                    (self.widths[i_pk] < self.width_range[1])):
                    win_ini = ch_pk - np.round(k_sep_pk*self.widths[i_pk]).astype(int)
                    win_ini = max(win_ini, 0)
                    win_fin = ch_pk + np.round(k_sep_pk*self.widths[i_pk]).astype(int)
                    if win_fin >= n_ch:
                        win_fin = n_ch - 1
                    is_reg[win_ini:win_fin+1] = True
        print('define_multiplets_regions completado')

    def define_multiplets_limits(self, n_ch, is_reg):
        """Define multiplet limits from already defined regions."""

        # Com base nos canais marcados em is_reg,
        # define extremos das regiões, mix_regions

        comuta = np.zeros(n_ch)
        for i in range(1, n_ch):
            comuta[i] = is_reg[i].astype(int)-is_reg[i-1].astype(int)

        # np.nonzero gera uma tupla, não sei por quê.
        inis = np.nonzero(comuta>0)[0]
        # fins = np.append(np.nonzero(comuta<0), n)
        fins = np.nonzero(comuta<0)[0]

        # Ajusta comprimento dos arrays. Têm de ser iguais.
        min_size = np.minimum(inis.size, fins.size)
        inis = inis[:min_size]
        fins = fins[:min_size]
        self.mix_regions = np.concatenate(np.array([[inis], [fins]])).T

    def net_spec_peaks_search(self, net_spec):
        """Second peak search, now on the net spec; use scipy.signal.find_peaks."""

        # self.propts_fullhe = np.array(1)
        # self.propts_halfhe = np.array(1)
        width=(None, None)
        # Para o chn da piscina:
        height=50
        prominence=50
        # Para o iec da ALMERA:
        # height=25
        # prominence=25
        self.peaks_net, self.propts_halfhe_net = find_peaks (
            net_spec,
            height=height,
            threshold=(None, None),
            prominence=prominence,
            width=width, rel_height=0.5)
        width=(None, None)
