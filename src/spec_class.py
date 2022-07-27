# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:06:14 2021

@author: mmaduar
"""

from pathlib import (Path)
import numpy as np

from specparms_class import SpecParms
# from spec_graphics_class import SpecGraphics


class Spec:
    """ Spectrum class. """

    def __init__(self, f_name):
        """
        Initialize a minimal members set from a read spectrum file.

        :param kind: Optional "kind" of ingredients.
        :type kind: list[str] or None
        :raise lumache.InvalidKindError: If the kind is invalid.
        :return: The ingredients list.
        :rtype: list[str]

        """
        self.f_name = f_name
        self.sufx = Path(f_name).suffix.casefold()
        #
        self.spec_parms = SpecParms(self.f_name, self.sufx)
        # self.spec_graphics = SpecGraphics()
        self.pkl_file = Path(self.f_name).with_suffix('.xz')

    @staticmethod
    def curr_h_win(n_ch, i_ch):
        """ Find the current half windows. """
        _a = 0.00125
        _b = 0.00075 * n_ch
        h_win = np.int(np.round(_a * i_ch + _b))
        return h_win

    def total_analysis(self, k_sep_pk=2.0, smoo=3000.0, widths_range=(4.0, 20.0)):
        """Analyze thoroughly a spectrum."""
        self.spec_parms.total_analysis(k_sep_pk, smoo, widths_range)

    def plot_graphics(self, graph_nos):
        """Plot graphics (?)."""
        # self.spec_graphics.plot_graphics(self.spec_parms, graph_nos)
        pass
