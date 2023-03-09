#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 14:13:51 2022

@author: marcelofm
"""

from PySide2 import sys
from PySide2.QtCore import QPoint, QSettings, QSize
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog

from ograyspy_class import Ograyspy
from spectrumform_class import SpectrumForm
from ui_ograyspy_main import Ui_MainWindow
from ui_languages import Ui_LanguageDlg


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec_()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionE_xit.triggered.connect(self.close_app)
        self.action_Open_a_spectrum.triggered.connect(self.process_example_spec)
        self.actionChoose_a_spectrum.triggered.connect(self.load_a_spectrum)
        self.actionLanguages.triggered.connect(self.set_interface_language)
        self.read_settings()
        self.set_local_environ()

    def read_settings(self):

        settings = QSettings('MFMaduar', 'OGRaySpY settings')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        lang = settings.value('language', 'en')
        self.move(pos)
        self.resize(size)
        self.curr_lang = lang

    def write_settings(self):
        settings = QSettings('MFMaduar', 'OGRaySpY settings')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
        settings.setValue('language', self.curr_lang)

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


    def load_a_spectrum(self):
        print('Chamou Choose a spectrum')
        path_to_file, _ = QFileDialog.getOpenFileName(self,
                                                      self.tr("Load spectrum"),
                                                      self.tr("~/Desktop/"),
                                                      self.tr("Spectra (*.chn *.iec)"))
        if path_to_file:
            print(f'Escolhido: {path_to_file} ')
            # Open the form to be populated
            spectrum_form = SpectrumForm(path_to_file)
            if spectrum_form.exec_():
                print('Viva!')
            else:
                print('Cancelou...')

        else:
            print(f'dialogo cancelado')
        # self.image_viewer = ImageViewer(path_to_file)
        # self.image_viewer.show()


    def set_interface_language(self):
        lang_dlg = LanguageDlg()
        if lang_dlg.exec_():
            print('Viva!')
            if lang_dlg.pt_BR_rbt.isChecked():
                self.curr_lang = 'pt_BR'
            else:
                self.curr_lang = 'en'
            print(self.curr_lang)
        else:
            print('Cancelou...')

    def close_app(self):
        self.write_settings()
        print('Gravou os settings e terminou. Tchau!')
        QApplication.instance().closeAllWindows()


class LanguageDlg(QDialog, Ui_LanguageDlg):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    main()
