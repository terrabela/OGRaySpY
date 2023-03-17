#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 18:46:42 2021

@author: maduar
"""

# main.py
import sys
from spec_class import Spec

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")
    f_name = '../../Genie_Transfer/Filtros/2021/Ctp/CTP0411 (6,13%).Chn'
    # f_name = sys.argv[1]
    if f_name:
        spec = Spec(f_name)
        spec.total_analysis()
        spec.plot_graphics([1,2,3,4,5,6])
    print('ograyspy.py completado')
