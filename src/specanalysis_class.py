# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 14:38:20 2021

@author: mmaduar
"""

import numpy as np
from scipy.interpolate import splrep, splev
# , splder, sproot

class SpecAnalysis:
    """Perform math analysis of spec."""

    def __init__(self, chans_nzero, counts_nzero, unc_y, chans):
        # self.peaks_parms = PeaksParms(self.eval_smoo_cts)
        smoo_cts = splrep(x=chans_nzero,
                          y=counts_nzero,
                          w=1.0/unc_y, k=3)
        self.eval_smoo_cts = splev(chans, smoo_cts)

    def calculate_net_spec(self, spec):
        """Calculate net spectrum."""
        net_spec = np.zeros(self.n_ch)
        for multiplet_region in self.mix_regions:
            xs_mplet = spec.spec_analysis.chans[slice(*multiplet_region)]
            ys_mplet = spec.y0s[slice(*multiplet_region)]
            ini_ch_mplet = multiplet_region[0]
            fin_ch_mplet = multiplet_region[1]-1
            args = (ini_ch_mplet, fin_ch_mplet,
                    splev(ini_ch_mplet, spec.spec_analysis.spl_baseline),
                    splev(fin_ch_mplet, spec.spec_analysis.spl_baseline),
                    spec.y0s)
            a_step = step_baseline(*args)
            net_mplet = ys_mplet - a_step
            self.xs_all_mplets.extend(list(xs_mplet))
            self.xs_all_mplets.append( None )
            self.ys_all_mplets.extend(list(net_mplet))
            self.ys_all_mplets.append( None )
            self.ys_all_steps.extend(list(a_step))
            self.ys_all_steps.append( None )
            net_spec[slice(*multiplet_region)] = np.where(net_mplet < 0.0, 0.0, net_mplet)

# Ver onde chamar:
#        self.calculate_net_spec(spec)
