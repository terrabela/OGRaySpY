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


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec_()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionE_xit.triggered.connect(QApplication.instance().closeAllWindows)
        self.action_Open_a_spectrum.triggered.connect(self.process_example_spec)
        self.set_local_environ()

    def set_local_environ(self):
        self.ogra = Ograyspy(batch_mode=False)
        print('Objeto ogra: Ograyspy criado.')
        print(f'ogra.info_plat: {self.ogra.info_plat}')
        print(f'ogra.info_mach: {self.ogra.info_mach}')
        print(f'ogra.info_syst: {self.ogra.info_syst}')
        print(f'ogra.info_node: {self.ogra.info_node}')
        print(f'ogra.home_path: {self.ogra.home_path}')

        to_be_found = 'Genie_Transfer'
        # to_be_found = 'some_spectra'
        print('\nogra.define_files_folder(to_be_found)')
        self.ogra.define_files_folder(to_be_found)

    def process_example_spec(self):
        # 2022-out-7: Excelente espectro para testes, tenho usado ultimamente:
        a_pattern = 'Si/SI2018/SI11318.Chn'
        # 2022-nov-16: outros espectros:
        # a_pattern = "Filtros/2022/Cci/CCI1603-I.Chn"
        # a_pattern = "Filtros/2022/Cci/CCI2302-I.Chn"

        # a_pattern = "Eso_non_existe.Chn"

        print(f'\n\nogra.select_spectrum({a_pattern})')
        self.ogra.select_spectrum(a_pattern)
        print(f'A spec name: {self.ogra.a_spec_name}')
        print(f'Reduced file name: {self.ogra.reduced_f_name}')

        # AQUI: ativar gener_dataframe qdo estiver pronto.
        self.ogra.perform_total_analysis(peak_sd_fact=3.0, gener_dataframe=True)
        # print(ogra.a_spec.spec_pks_df)

        self.ogra.call_graphics()

        print('Processed an example spectrum. Ok.')


if __name__ == '__main__':
    main()
