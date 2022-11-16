# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 19:29:28 2021

@author: mmaduar
"""

import numpy as np
from scipy.interpolate import splrep, splev
# , splder, sproot

class CntArrayLike:
    """ Counts array alike vars class. """

    def __init__(self, n_ch, sp_counts):
        self.n_ch = n_ch
        self.x_s = np.linspace( 0, n_ch-1, n_ch )
        self.y0s = np.asarray(sp_counts)
        # self.terms_2nd_grade = np.zeros(self.n_ch)
        # self.terms_1st_grade = np.zeros(self.n_ch)
        # self.terms_0th_grade = np.zeros(self.n_ch)
        self.varnc_2nd_grade = np.zeros(n_ch)

        self.nzero = self.y0s > 0
        self.chans = self.x_s
        self.chans_nzero = self.x_s[self.y0s > 0]
        # Talvez melhor deixar 0.0 em vez de 0.9
        self.counts_nzero = self.y0s[self.nzero]
        self.unc_y = np.sqrt(self.counts_nzero)

        self.unc_y_4plot = np.where(self.unc_y < 1.4, 0.0, self.unc_y)

        smoo_cts = splrep(x=self.chans_nzero,
                          y=self.counts_nzero,
                          w=1.0/self.unc_y, k=3)
        self.eval_smoo_cts = splev(self.chans, smoo_cts)
        self.spl_baseline = np.array([])
        self.eval_baseline = np.array([])

        self.is_reg = np.zeros(n_ch, dtype=bool)
        self.is_net_reg = np.zeros(n_ch, dtype=bool)

        self.net_spec = np.zeros(n_ch)
        self.final_baseline = np.zeros(n_ch)
        self.xs_all_mplets = []
        self.ys_all_mplets = []
        self.ys_all_steps = []

    def chans_in_regs(self):
        """ Channels in regions. """
        return self.chans[self.is_reg]

    def counts_in_regs(self):
        """ Counts in regions. """
        return self.y0s[self.is_reg]

    def chans_outof_regs(self):
        """ Channels out of regions. """
        return self.chans[~self.is_reg]

    def counts_outof_regs(self):
        """  Counts out of regions. """
        return self.y0s[~self.is_reg]

    def correct_spec_begin(
            self, ct_arr, thresh_first_max=3.0, thresh_stable_var=1.0, ch_win=10):
        n_ct = ct_arr.size
        var_rel = np.array(
            [np.var(ct_arr[i:i + ch_win]) / (abs(np.mean(ct_arr[i:i + ch_win])) + 1)
             for i in range(n_ct - ch_win)]
        )
        loc_step = np.where(var_rel > thresh_first_max)[0][0]
        remaining_arr = var_rel[loc_step:]
        loc_stable_cts = np.where(remaining_arr < thresh_stable_var)[0][0] + loc_step
        return var_rel, loc_stable_cts
        # loc_stable_cts

    def calculate_base_line(self, mix_regions, smoo):
        """Calculate base line."""
        # _w = _raiz_y
        _aux_list = []
        for multiplet_region in mix_regions:
            _ys = self.y0s[slice(*multiplet_region)]
            _bl_in = splev(multiplet_region[0]-1, self.spl_baseline)
            _bl_fi = splev(multiplet_region[1], self.spl_baseline)
            _a_step = self.step_baseline( _bl_in, _bl_fi, _ys)
            _aux_list.append(_a_step)
            # print('multiplet_region: ', multiplet_region)
            # print('chans: ', _chans)
            # print('_ys: ', _ys)
            # print('_bl_in: ', _bl_in)
            # print('_bl_fi: ', _bl_fi)
            # print('a_step: ', _a_step)
            # print('============================')
            net_mplet = _ys - _a_step
        #    self.xs_all_mplets.extend(list(xs_mplet))
        #    self.xs_all_mplets.append( None )
        #    self.ys_all_mplets.extend(list(net_mplet))
        #    self.ys_all_mplets.append( None )
        #    self.ys_all_steps.extend(list(a_step))
        #    self.ys_all_steps.append( None )
            self.net_spec[slice(*multiplet_region)] = np.where(net_mplet < 0.0, 0.0, net_mplet)
        #    self.final_baseline = self.y0s - self.net_spec

        if len(_aux_list) != 0:
            self.calculated_step_counts = np.concatenate(_aux_list)

