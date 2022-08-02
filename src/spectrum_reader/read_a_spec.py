#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:18:06 2020
@author: marcelo
"""

from src.spec_class import Spec

"""
read_a_spec.py
====================================
Read a gamma-ray spectrum
"""

# https://github.com/pypa/sampleproject

a_spec_name = '../../Genie_Transfer/Filtros/2022/Cci/CCI1603-I.Chn'
a_raw_spec = Spec(a_spec_name)
