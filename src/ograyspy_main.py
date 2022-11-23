#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 14:13:51 2022

@author: marcelofm
"""

from ograyspy_class import Ograyspy

ogra = Ograyspy()
print(ogra.a_spec_name)
ogra.define_files_batch()
ogra.select_spectrum()
ogra.perform_total_analysis()
ogra.call_graphics()
print('Terminated Ok.')