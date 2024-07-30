
from PySide2.QtWidgets import QDialog
from ui_spectrumform import Ui_Dialog
from spec_class import Spec

class SpectrumForm(QDialog, Ui_Dialog):
    def __init__(self, spectrum_path):
        super().__init__()
        self.setupUi(self)
        self.a_spec = Spec()
        self.populate_form()

    def populate_form(self):
        self.rawDataTed.setText(self.a_spec.f_name)
        # self.sampDescrTed.setText(self.a_spec.origin_spec_ser_an.y_s.tostring())
        self.startDte.setDate(self.a_spec.start_datetime)
        self.leLT_2.setText()
        self.leRT_2.setText()
        self. (self.a_spec.det_descr) # PAREI AQUI

    def perform_total_analysis(self, k_sep_pk=2.0, smoo=4096,
                               widths_range=(4.0, 20.0),
                               peak_sd_fact=3.0,
                               gener_dataframe=False):
        self.a_spec.total_analysis(k_sep_pk=k_sep_pk,
                                   smoo=smoo,
                                   widths_range=widths_range,
                                   peak_sd_fact=peak_sd_fact,
                                   gener_dataframe=gener_dataframe)
        print('Fez total analysis.')
        print(dir(self.a_spec))
