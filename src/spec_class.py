# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:06:14 2021

@author: mmaduar
"""

# https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#compile

from pathlib import Path
import numpy as np
import pandas as pd

from genericcalib_class import ChannelEnergyCalib, EnergyFwhmCalib
from specchn_class import SpecChn
from speciec_class import SpecIec
from generic_series_analysis_class import GenericSeriesAnalysis

# from spec_class import Spec
# from spec_graphics_class import CountsGraphic, PeaksAndRegionsGraphic, BaselineGraphic


class Spec:
    """ Spectrum class. """

    def __init__(self, f_name='', reduced_f_name=''):
        """
        Initialize a minimal members set from a read spectrum file.

        :param f_name: Spectrum's complete file name.
        :type f_name: str
        # :raise lumache.InvalidKindError: If the kind is invalid.
        :return: 0 if spectrum was successfully opened; -1 otherwise.
        :rtype: int
        and set spectrum parameters (count time, sample description etc)."

        """
        self.net_spec_ser_an = None
        self.final_composed_baseline = None
        self.f_name = f_name
        self.reduced_f_name = reduced_f_name
        self.sufx = Path(f_name).suffix.casefold()
        if self.sufx == '.chn':
            self.spec_io = SpecChn(f_name)
            self.lv_time = self.spec_io.chn_lvtime
            self.rl_time = self.spec_io.chn_rltime
            self.source_datetime = None

        elif self.sufx == '.iec':
            self.spec_io = SpecIec(f_name)
            self.lv_time = self.spec_io.iec_lvtime
            self.rl_time = self.spec_io.iec_rltime
            self.source_datetime = self.spec_io.source_datetime
        #
        self.pkl_file = Path(self.f_name).with_suffix('.pkl')

        # 2022-out-7:
        # Parei aqui: fazer bd do Pandas
        # self.spec_pks_df = pd.DataFrame()

        self.gross_spec_ser_an = GenericSeriesAnalysis(self.spec_io.sp_counts, to_smooth=True)
        self.origin_spec_ser_an = GenericSeriesAnalysis(self.spec_io.sp_counts, to_smooth=False)

        self.start_datetime = self.spec_io.sp_start_datetime
        self.det_descr = self.spec_io.det_descr
        self.sam_descr = self.spec_io.sam_descr

        # 2022-nov-3: pausa para recreio: ver como fica espectro fft:
        # self.fft_ser_an = GenericSeriesAnalysis(self.spec_io.sp_counts, to_smooth=False, is_fft=True)

        # 2022-out-6 Criando a espectro líquido:
        # self.net_spec_ser_an = GenericSeriesAnalysis(self.spec_io.sp_counts, to_smooth=False)
        #
        # self.channel_energy_calib = ChannelEnergyCalib(
        #     self.spec_io.en_ch_calib,
        #     self.spec_io.chan_calib,
        #     self.spec_io.coeffs_ch_en
        # )
        # 2023-jan-4 Lê calibração canal x energia implícita no espectro CHN
        self.channel_energy_calib = ChannelEnergyCalib(
            self.spec_io.coeffs_ch_en
        )
        #       self.energy_fwhm_calib = EnergyFwhmCalib(self.spec_io.en_fw_calib,
        #                                                self.spec_io.fwhm_calib,
        #                                                self.spec_io.coeffs_en_fw)
        # self.energy_fwhm_calib = EnergyFwhmCalib(self.spec_io.coeffs_en_fw)
        #        self.energy_efficiency_calib = EnergyEfficiencyCalib(self.spec_io.en_ef_calib,
        #                                                            self.spec_io.effi_calib)

        #        self.channel_energy_calib = ChannelEnergyCalib()
        #        self.energy_fwhm_calib = EnergyFwhmCalib()
#         try:  # 2022-Jun-23
#             self.spec_io.en_ef_calib
#         except AttributeError:
#             pass
#         else:
#             self.energy_efficiency_calib = EnergyEfficiencyCalib(self.spec_io.en_ef_calib)

        self.spec_io = None
        # self.spec_pks_df = pd.DataFrame()
        # print(vars(self))
        # print(vars(self.gross_spec_ser_an.cnt_arrs))


    @staticmethod
    def curr_h_win(n_ch, i_ch):
        """ Find the current half windows. """
        _a = 0.00125
        _b = 0.00075 * n_ch
        h_win = np.int(np.round(_a * i_ch + _b))
        return h_win

    def total_analysis(self, k_sep_pk=2.0, smoo=3000.0, widths_range=(4.0, 20.0),
                       peak_sd_fact=3.0, gener_dataframe=False):
        """Analyze thoroughly a spectrum."""
        # Initialize a minimal members set from a read spectrum file.

        # :param k_sep_pk: Spectrum's complete file name.
        # :type f_name: str
        # :raise lumache.InvalidKindError: If the kind is invalid.
        # :return: 0 if spectrum was successfully opened; -1 otherwise.
        # :rtype: int

        # seqquência:
        #    incia obj spec_parms
        #    initial_peaks_search: acha picos candidatos, põe em peaks_parms.peaks

        if self.gross_spec_ser_an.n_ch > 0:
            # print('k_sep_pk: ', k_sep_pk)
            # print('smoo: ', smoo)
            # print('widths_range: ', widths_range)
            # print('=================')
            # print('Exec peaks_search(gross=True), espectro ORIGINAL')
            print('Starting Spec.total_analysis...')
            self.gross_spec_ser_an.resolve_peaks_and_regions (
                k_sep_pk, peak_sd_fact=peak_sd_fact)
            self.gross_spec_ser_an.calculate_baseline (smoo=smoo)
            # 2022-nov-15: final composed baseline series
            self.final_composed_baseline = GenericSeriesAnalysis(self.gross_spec_ser_an.final_baseline)
            net_spec_array = np.where (
                self.gross_spec_ser_an.y_s - self.final_composed_baseline.y_s > 1,
                self.gross_spec_ser_an.y_s - self.final_composed_baseline.y_s,
                0.0
            )
            given_variance = np.where (
                self.gross_spec_ser_an.y_s + self.final_composed_baseline.y_s > 1,
                self.gross_spec_ser_an.y_s + self.final_composed_baseline.y_s,
                1.0
            )
            self.net_spec_ser_an = GenericSeriesAnalysis(
                net_spec_array,
                given_variance = given_variance
            )

            self.net_spec_ser_an.resolve_peaks_and_regions (
                k_sep_pk, peak_sd_fact=peak_sd_fact
            )
            self.net_spec_ser_an.pk_parms.prepare_to_sum (n_fwhms=3.0)
            self.net_spec_ser_an.perform_basic_net_area_calculation ()

            if gener_dataframe:
                self.generate_pandas_dataframe()

            print('Finish Spec.total_analysis!')
        else:
            print('Spec.total_analysis: No analysis applicable as spectrum is empty.')

    def generate_pandas_dataframe(self):
        a_spec_vars = vars(self)
        campos = [a for a in a_spec_vars]
        valores = [a_spec_vars[a] for a in a_spec_vars]
        # spec_df_type1 = pd.DataFrame(data=valores, index=campos)
        # spec_df_type1.to_pickle(self.pkl_file)
        spec_df_type2 = pd.DataFrame(data=[valores], columns=campos)
        spec_df_type2.to_pickle(self.pkl_file)
