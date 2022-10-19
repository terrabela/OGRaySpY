# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:06:14 2021

@author: mmaduar
"""

# https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#compile

from pathlib import Path
import numpy as np
import pandas as pd

from genericcalib_class import ChannelEnergyCalib, EnergyFwhmCalib, EnergyEfficiencyCalib
from specchn_class import SpecChn
from speciec_class import SpecIec
from counts_series_arrays import CountsSeriesArrays
from generic_series_analysis_class import GenericSeriesAnalysis


class Spec:
    """ Spectrum class. """

    def __init__(self, f_name=''):
        """
        Initialize a minimal members set from a read spectrum file.

        :param f_name: Spectrum's complete file name.
        :type f_name: str
        # :raise lumache.InvalidKindError: If the kind is invalid.
        :return: 0 if spectrum was successfully opened; -1 otherwise.
        :rtype: int
        and set spectrum parameters (count time, sample description etc)."

        """
        self.f_name = f_name
        self.sufx = Path(f_name).suffix.casefold()
        if self.sufx == '.chn':
            self.spec_io = SpecChn(f_name)
        elif self.sufx == '.iec':
            self.spec_io = SpecIec(f_name)
        #
        self.pkl_file = Path(self.f_name).with_suffix('.xz')

        # 2022-out-7:
        # Parei aqui: fazer bd do Pandas
        self.spec_pks_df = pd.DataFrame()

        self.gross_spec_ser_an = GenericSeriesAnalysis(
            CountsSeriesArrays(self.spec_io.sp_counts, to_smooth=False)
        )

        self.smoo_gross_ser_an = GenericSeriesAnalysis(
            CountsSeriesArrays(self.spec_io.sp_counts, to_smooth=True)
        )
        # 2022-out-6 Criando a espectro líquido:
        self.net_spec_ser_an = GenericSeriesAnalysis(
            CountsSeriesArrays(self.spec_io.sp_counts, to_smooth=False)
        )
        #
        #        self.channel_energy_calib = ChannelEnergyCalib(self.spec_io.en_ch_calib,
        #                                                       self.spec_io.chan_calib,
        #                                                       self.spec_io.coeffs_ch_en)
        self.channel_energy_calib = ChannelEnergyCalib(self.spec_io.coeffs_ch_en)
        #       self.energy_fwhm_calib = EnergyFwhmCalib(self.spec_io.en_fw_calib,
        #                                                self.spec_io.fwhm_calib,
        #                                                self.spec_io.coeffs_en_fw)
        self.energy_fwhm_calib = EnergyFwhmCalib(self.spec_io.coeffs_en_fw)
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
        # print(vars(self))
        print(vars(self.gross_spec_ser_an.cnt_arrs))


    @staticmethod
    def curr_h_win(n_ch, i_ch):
        """ Find the current half windows. """
        _a = 0.00125
        _b = 0.00075 * n_ch
        h_win = np.int(np.round(_a * i_ch + _b))
        return h_win

    def total_analysis(self, k_sep_pk=2.0, smoo=3000.0, widths_range=(4.0, 20.0)):
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

        if self.gross_spec_ser_an.cnt_arrs.n_ch > 0:
            print('k_sep_pk: ', k_sep_pk)
            print('smoo: ', smoo)
            print('widths_range: ', widths_range)
            print('=================')
            print('Exec peaks_search(gross=True), espectro ORIGINAL')
            self.gross_spec_ser_an.resolve_peaks_and_regions (k_sep_pk, smoo)
            # 2022-out-4: Aqui faço a busca no suavizado, mas deixarei sem uso por enquanto
            print('Exec peaks_search(gross=True), espectro SMOOTHED')
            self.smoo_gross_ser_an.resolve_peaks_and_regions (k_sep_pk, smoo)
            #    define_multiplets_regions:
            #      em define_multiplets_regions: define is_reg com base em bons picos
            # 2022-out-5: Definindo multipletos no original spec (não no smoo)
            self.gross_spec_ser_an.define_multiplets_regions(k_sep_pk, smoo)

            # 2022-set-27 Aqui começam os cálculos em cima do espectro líquido
            self.net_spec_ser_an = GenericSeriesAnalysis(
                CountsSeriesArrays(self.gross_spec_ser_an.cnt_arrs.net_spec, to_smooth=False)
            )
            self.net_spec_ser_an.resolve_peaks_and_regions(k_sep_pk, smoo)
            self.net_spec_ser_an.define_multiplets_regions(k_sep_pk, smoo)

            self.spec_pks_df

            print('=================')
            # print('Exec peaks_search(gross=False)')
            # self.peaks_parms.peaks_search(cts_to_search=self.cnt_array_like.net_spec, gross=False,
            #                               widths_range=self.peaks_parms.net_widths)
            # print("self.peaks_parms.peaks_net: ", self.peaks_parms.peaks_net)
            # print("self.peaks_parms.propts_net: ", self.peaks_parms.propts_net)
            # print("self.peaks_parms.net_widths = (ws_min, ws_max): ", self.peaks_parms.net_widths)

            print('=================')
            # self.peaks_parms.define_width_lines(gross=False)

            # print(self.cnt_array_like.is_net_reg)
            # print(self.cnt_array_like.is_net_reg.size)

            # self.peaks_parms.define_net_multiplets_regions(self.cnt_array_like.is_net_reg,
            #                                                k_sep_pk=k_sep_pk)

            print('=================')
            # self.peaks_parms.define_width_lines(gross=False)
            # self.peaks_parms.net_width_lines()
            # self.peaks_parms.define_net_multiplets_regions(self.cnt_array_like.is_net_reg,
            #                                                k_sep_pk=k_sep_pk)
        else:
            print('No analysis applicable as spectrum is empty.')
        # print(vars(self.peaks_parms))


    def perform_basic_net_area_calculation(self):
        """Perform a very rough net area calculation"""
        # self.spec_parms.peaks_parms.basic_net_area_calculation()
        # self.spec_parms.ser_an.peaks_search()
        pass
