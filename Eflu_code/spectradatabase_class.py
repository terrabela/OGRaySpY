# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 09:52:34 2021

@author: mmaduar
"""

from pathlib import (Path)
import numpy as np

import pandas as pd

from specparms_class import SpecParms

class SpectraDatabase:
    """ Spectrum class. """

    def __init__(self, db_name):
        """
        Initialize a spectra Pandas database.
        """
        self.db_name = db_name
        # self.sufx = Path(f_name).suffix.casefold()
        #
        # self.spec_parms = SpecParms(self.f_name, self.sufx)
        # self.pkl_file = Path(self.f_name).with_suffix('.xz')

    def spec_to_pickle(self, f_name, db_name):
        """Save single serialized spectrum xz-compressed."""
        # spec_dfr = pd.DataFrame({'fParms': self.spec_parms}, index=[self.pkl_file])
        # spec_dfr.to_pickle(self.pkl_file)

    def read_pickled(self):
        """Load single serialized spectrum xz-compressed."""
        return pd.read_pickle(self.pkl_file)
