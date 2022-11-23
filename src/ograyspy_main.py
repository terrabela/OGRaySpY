#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 14:13:51 2022

@author: marcelofm
"""

from ograyspy_class import Ograyspy

ogra = Ograyspy(batch_mode=False)
print(ogra.a_spec_name)
to_be_found = 'Genie_Transfer'

# ogra.define_files_batch()
ogra.define_files_batch(to_be_found)

# 2022-out-7: Excelente espectro para testes, tenho usado ultimamente:
# a_pattern = 'Si/SI2018/SI11318.Chn'
# 2022-nov-16: outros espectros:
# a_pattern = "Filtros/2022/Cci/CCI1603-I.Chn"
# a_pattern = "Eso_non_existe.Chn"

# ogra.select_spectrum(a_pattern)
# ogra.perform_total_analysis(gener_dataframe=True)
# ogra.call_graphics()
print('Terminated Ok.')