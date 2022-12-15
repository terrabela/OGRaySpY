#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 14:13:51 2022

@author: marcelofm
"""

from ograyspy_class import Ograyspy

ogra = Ograyspy(batch_mode=False)
print('Objeto ogra: Ograyspy criado.')
print(f'ogra.info_plat: {ogra.info_plat}')
print(f'ogra.info_mach: {ogra.info_mach}')
print(f'ogra.info_syst: {ogra.info_syst}')
print(f'ogra.info_node: {ogra.info_node}')
print(f'ogra.home_path: {ogra.home_path}')

to_be_found = 'Genie_Transfer'
print('\nogra.define_files_folder(to_be_found)')
ogra.define_files_folder(to_be_found)

# 2022-out-7: Excelente espectro para testes, tenho usado ultimamente:
a_pattern = 'Si/SI2018/SI11318.Chn'
# 2022-nov-16: outros espectros:
# a_pattern = "Filtros/2022/Cci/CCI1603-I.Chn"
# a_pattern = "Eso_non_existe.Chn"

print(f'\n\nogra.select_spectrum({a_pattern})')
ogra.select_spectrum(a_pattern)
print(f'A spec name: {ogra.a_spec_name}')
print(f'Reduced file name: {ogra.reduced_f_name}')

# AQUI: ativar gener_dataframe qdo estiver pronto.
ogra.perform_total_analysis(gener_dataframe=True)
# print(ogra.a_spec.spec_pks_df)

ogra.call_graphics()

print('Terminated Ok.')
