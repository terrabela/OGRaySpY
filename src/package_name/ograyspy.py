#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:18:06 2020

@author: marcelo
"""

# import numpy as np

from src.spec_class import Spec
from src.spec_graphics_class import SpecGraphics

"""
spectrum_analysis.py
====================================
The core module of my example project
"""

# from scipy.signal import (cwt, ricker, find_peaks_cwt)
# from scipy.ndimage import label, generate_binary_structure, find_objects  # 2019-09-18
# import numpy.ma as ma  # masked array

# 2019-09-16: inseri.
# 2022-07-15: desativei por enquanto.
# from gauss_funcs import (gaus_fw, gaus_sig)


def about_me(your_name):
    """
    Return the most important thing about a person.

    Parameters
    ----------
    your_name
        A string indicating the name of the person.

    """
    return "The wise {} loves Python.".format(your_name)


class ExampleClass:
    """An example docstring for a class definition."""

    def __init__(self, name):
        """
        Blah blah blah.

        Parameters
        ---------
        name
            A string to assign to the `name` instance attribute.

        """
        self.name = name

    def about_self(self):
        """
        Return information about an instance created from ExampleClass.
        """
        return "I am a very smart {} object.".format(self.name)


a_spec_name = '../../Genie_Transfer/Filtros/2022/Cci/CCI1603-I.Chn'
a_raw_spec = Spec(a_spec_name)
a_raw_spec.total_analysis(k_sep_pk=2.0, smoo=4096, widths_range=(4.0, 20.0))

a_graphic_object = SpecGraphics(a_raw_spec.f_name, a_raw_spec.spec_parms)
a_graphic_object.plot_simple_scattergl()
