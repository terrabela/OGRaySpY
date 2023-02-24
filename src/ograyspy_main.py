#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 14:13:51 2022

@author: marcelofm
"""

from PySide2 import sys
from PySide2.QtWidgets import QApplication, QMainWindow

from ograyspy_class import Ograyspy
from ui_ograyspy_main import Ui_MainWindow


def main2():
    ogra = Ograyspy(batch_mode=False)
    print('Objeto ogra: Ograyspy criado.')
    print(f'ogra.info_plat: {ogra.info_plat}')
    print(f'ogra.info_mach: {ogra.info_mach}')
    print(f'ogra.info_syst: {ogra.info_syst}')
    print(f'ogra.info_node: {ogra.info_node}')
    print(f'ogra.home_path: {ogra.home_path}')

    to_be_found = 'Genie_Transfer'
    # to_be_found = 'some_spectra'
    print('\nogra.define_files_folder(to_be_found)')
    ogra.define_files_folder(to_be_found)

    # 2022-out-7: Excelente espectro para testes, tenho usado ultimamente:
    a_pattern = 'Si/SI2018/SI11318.Chn'
    # 2022-nov-16: outros espectros:
    # a_pattern = "Filtros/2022/Cci/CCI1603-I.Chn"
    # a_pattern = "Filtros/2022/Cci/CCI2302-I.Chn"

    # a_pattern = "Eso_non_existe.Chn"

    print(f'\n\nogra.select_spectrum({a_pattern})')
    ogra.select_spectrum(a_pattern)
    print(f'A spec name: {ogra.a_spec_name}')
    print(f'Reduced file name: {ogra.reduced_f_name}')

    # AQUI: ativar gener_dataframe qdo estiver pronto.
    ogra.perform_total_analysis(peak_sd_fact=3.0, gener_dataframe=True)
    # print(ogra.a_spec.spec_pks_df)

    ogra.call_graphics()

    print('Terminated Ok.')


def main1():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    # sys.exit(app.exec_())
    app.exec_()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionE_xit.triggered.connect(QApplication.instance().closeAllWindows)
        self.action_Open_a_spectrum.triggered.connect(main2)

if __name__ == '__main__':
    main1()
    # main2()
