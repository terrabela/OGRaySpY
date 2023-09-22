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
from nuclide_analysis_class import NuclideAnalysis


# from spec_graphics_class import CountsGraphic, PeaksAndRegionsGraphic, BaselineGraphic

class Spec:
    """ Spectrum class. """

    def __init__(self, f_name='', reduced_f_name='', s_cond=None):
        """
        Initialize a minimal members set from a read spectrum file.

        :param f_name: Spectrum's complete file name.
        :type f_name: str
        :return: 0 if spectrum was successfully opened; -1 otherwise.
        :rtype: int
        and set spectrum parameters (count time, sample description etc.).

        """
        self.net_spec_ser_an = None
        self.final_composed_baseline = None
        self.f_name = f_name
        self.reduced_f_name = reduced_f_name
        self.sufx = Path(f_name).suffix.casefold()
        if self.sufx == '.chn':
            self.spec_io = SpecChn(f_name)
            self.lv_time = self.spec_io.lvtime
            self.rl_time = self.spec_io.rltime
            self.source_datetime = None

        elif self.sufx == '.iec':
            self.spec_io = SpecIec(f_name)
            self.lv_time = self.spec_io.lvtime
            self.rl_time = self.spec_io.rltime
            self.source_datetime = self.spec_io.source_datetime
        #
        self.pkl_file = Path('')

        # self.gross_spec_ser_an = GenericSeriesAnalysis(self.spec_io.sp_counts, to_smooth=True, s_cond=s_cond)
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

        self.nucl_an = NuclideAnalysis()

    @staticmethod
    def curr_h_win(n_ch, i_ch):
        """ Find the current half windows. """
        _a = 0.00125
        _b = 0.00075 * n_ch
        h_win = int(np.round(_a * i_ch + _b))
        return h_win

    def total_analysis(self, k_sep_pk=2.0, smoo=3000.0, widths_range=(4.0, 20.0),
                       peak_sd_fact=3.0, gener_dataframe=False, ):
        # Initialize a minimal members set from a read spectrum file.
        """Analyze thoroughly a spectrum.

        :param k_sep_pk: Spectrum's complete file name.
        :type k_sep_pk: float
        :param smoo: Smoothing factor
        :type smoo: float
        :param widths_range: WRITE
        :type widths_range: tuple
        :param peak_sd_fact: WRITE
        :type peak_sd_fact: float
        :param gener_dataframe: WRITE
        :type gener_dataframe: bool
        :returns: 0 if spectrum was successfully opened; -1 otherwise.
        :rtype: int
        """

        if self.origin_spec_ser_an.n_ch > 0:
            # print('k_sep_pk: ', k_sep_pk)
            # print('smoo: ', smoo)
            # print('widths_range: ', widths_range)
            # print('=================')
            # print('Exec peaks_search(gross=True), espectro ORIGINAL')
            print('Starting Spec.total_analysis...')
            self.origin_spec_ser_an.resolve_peaks_and_regions(
                k_sep_pk, peak_sd_fact=peak_sd_fact)
            # 2023-abr-29: MUDAR TUDO! excluí gross_spec_ser_an
            # 2023-mai-16: FEITO!
            self.origin_spec_ser_an.calculate_baseline(smoo=smoo)
            # 2022-nov-15: final composed baseline series
            self.final_composed_baseline = GenericSeriesAnalysis(self.origin_spec_ser_an.final_baseline)
            net_spec_array = np.where(
                self.origin_spec_ser_an.y_s - self.final_composed_baseline.y_s > 1,
                self.origin_spec_ser_an.y_s - self.final_composed_baseline.y_s,
                0.0
            )
            given_variance = np.where(
                self.origin_spec_ser_an.y_s + self.final_composed_baseline.y_s > 1,
                self.origin_spec_ser_an.y_s + self.final_composed_baseline.y_s,
                1.0
            )
            self.net_spec_ser_an = GenericSeriesAnalysis(
                net_spec_array,
                given_variance=given_variance
            )

            self.net_spec_ser_an.resolve_peaks_and_regions(
                k_sep_pk, peak_sd_fact=peak_sd_fact
            )
            self.net_spec_ser_an.pk_parms.prepare_to_sum(n_fwhms=3.0)
            self.net_spec_ser_an.perform_basic_net_area_calculation()

            if gener_dataframe:
                # 2023-Set-22 PAREI AQUI: CORRIGIR AQUI E EM OGRAYSPY_CLASS
                # DIRECIONAR RESULTADOS PARA CAMINHO LOCAL: 'data/results' +
                # + CAMINHO DO ARQUIVO.
                results_pkl_file = f_name.with_stem(f_name.stem + '_result').with_suffix('.pkl')
                self.generate_pandas_dataframe(results_pkl_file)

            print('Finish Spec.total_analysis!')
        else:
            print('Spec.total_analysis: No analysis applicable as spectrum is empty.')

    def generate_pandas_dataframe(self, pkl_results_path):
        # for this spectrum, generate a pd.Dataframe and save it as a pkl-file.
        """Generate a Dataframe and save it as pkl for this spectrum.

        """

        a_spec_vars = vars(self)
        campos = [a for a in a_spec_vars]
        valores = [a_spec_vars[a] for a in a_spec_vars]
        # spec_df_type1 = pd.DataFrame(data=valores, index=campos)
        # spec_df_type1.to_pickle(self.pkl_file)
        spec_df_type2 = pd.DataFrame(data=[valores], columns=campos)
        self.pkl_file = Path(self.f_name).with_suffix('.pkl')
        spec_df_type2.to_pickle(self.pkl_file)

    def identify_nuclides(self, nucl_iear1_df):
        print("Lets identify nuclides.")
        orig_ser = self.origin_spec_ser_an
        net_ser = self.net_spec_ser_an
        x_nz = orig_ser.chans_nzero
        y_nz = orig_ser.counts_nzero
        chans = net_ser.x_s
        ys_net_counts = net_ser.y_s
        peaks_net = net_ser.pk_parms.peaks
        peaks_orig = orig_ser.pk_parms.peaks
        counts = orig_ser.y_s
        chans_nzero = orig_ser.chans_nzero
        counts_nzero = orig_ser.counts_nzero
        unc_y = orig_ser.unc_y
        eval_y = orig_ser.y_smoothed
        eval_bl = orig_ser.eval_baseline
        fin_bl = orig_ser.final_baseline
        inis = orig_ser.pk_parms.propts['left_bases']
        fins = orig_ser.pk_parms.propts['right_bases']
        # 2023-Jun-15
        # CRUCIAL step: take the dict net_ser.pk_parms
        # keys/values and organize them as a pd.Dataframe
        vars_pkprms = vars(net_ser.pk_parms)
        keys_to_get = ['peaks', 'fwhm_centr', 'rough_sums', 'centroids', 'variances']
        prep_for_dict = [(key, vars_pkprms[key]) for key in keys_to_get]
        pks_dict = dict(prep_for_dict)
        peaks_df = pd.DataFrame.from_dict(pks_dict)
        pr_pk = dict([('pk_hei', net_ser.pk_parms.propts['peak_heights']),
                      ('lf_thr', net_ser.pk_parms.propts['left_thresholds']),
                      ('rg_thr', net_ser.pk_parms.propts['right_thresholds']),
                      ('promns', net_ser.pk_parms.propts['prominences']),
                      ('lf_bas', net_ser.pk_parms.propts['left_bases']),
                      ('rg_bas', net_ser.pk_parms.propts['right_bases']),
                      ('widths', net_ser.pk_parms.propts['widths']),
                      ('wi_hei', net_ser.pk_parms.propts['width_heights']),
                      ('lf_ips', net_ser.pk_parms.propts['left_ips']),
                      ('rg_ips', net_ser.pk_parms.propts['right_ips'])])
        pks_properties_df = pd.DataFrame(pr_pk)
        pks_comprehensive_df = pd.concat([peaks_df, pks_properties_df], axis=1)
        print(pks_comprehensive_df)

        def add_engy_to_pks_df(peaks_net_kev_df, func_en):
            peaks_net_kev_df['engy_pk_det'] = func_en(peaks_net_kev_df.centroids)

        add_engy_to_pks_df(pks_comprehensive_df, self.channel_energy_calib.get_energy)
        print(pks_comprehensive_df)

        # 2023-08-27 PAREI AQUI
        self.nucl_an.nuclide_identif(nucl_iear1_df, pks_comprehensive_df)

