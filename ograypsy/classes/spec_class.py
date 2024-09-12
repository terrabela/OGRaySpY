# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 16:06:14 2021
"""

# https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#compile

from pathlib import Path, PurePath
import numpy as np
import pandas as pd
from numpy.polynomial import Polynomial as Pol  # 2020-09-06 Esta é a nova classe recomendada

from ograypsy.classes.genericcalib_class import ChannelEnergyCalib  # 2023-Oct-26: Not yet in use: , EnergyFwhmCalib
from ograypsy.classes.specchn_class import SpecChn
from ograypsy.classes.speciec_class import SpecIec
from ograypsy.classes.generic_series_analysis_class import GenericSeriesAnalysis
from ograypsy.classes.nuclide_analysis_class import NuclideAnalysis

from sklearn import linear_model

# from spec_graphics_class import CountsGraphic, PeaksAndRegionsGraphic, BaselineGraphic


class Spec:
    """ Spectrum class. """

    # 2023-Oct-26: verify: s_cond is not used:
    def __init__(
            self, fpc_fname='', spectra_path='', to_smooth=False, smooth_method='spline',
            smooth_on='log', smooth_cond=0.0
    ):
        """
        Initialize a minimal members set from a read spectrum file.

        :param fpc_fname: final path component of the file name.
        :type fpc_fname: str
        :param spectra_path: path excluding file name.
        :type spectra_path: str
        :param to_smooth: whether to smooth the spectrum.
        :type to_smooth: bool
        :param smooth_method: method to smooth the spectrum.
        :type smooth_method: str
        :param smooth_on: whether to smooth on original counts or on their logarithms
        :type smooth_on: str
        :return: 0 if spectrum was successfully opened; -1 otherwise.
        :rtype: int
        and set spectrum parameters (count time, sample description etc.).

        """
        self.spec_io = None
        self.net_spec_ser_an = None
        self.final_composed_baseline = None
        f_name = PurePath(spectra_path, fpc_fname)
        self.reduced_f_name = fpc_fname
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
        # self.pkl_file = Path('')
        self.results_pkl_file = Path('')

        if self.spec_io:
            self.origin_spec_ser_an = GenericSeriesAnalysis(
                self.spec_io.sp_counts, to_smooth, smooth_method,
                smooth_on, smooth_cond
            )

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

            self.nucl_an = NuclideAnalysis()

    @staticmethod
    def curr_h_win(n_ch, i_ch):
        """ Find the current half windows. """
        _a = 0.00125
        _b = 0.00075 * n_ch
        h_win = int(np.round(_a * i_ch + _b))
        return h_win

    def en_eff(self, engy):
        return np.exp(self.p_eff(np.log(engy)))

    def define_result_pkl_name(self, results_path):
        red_fn = Path(self.reduced_f_name)
        reduced_pkl_file = red_fn.with_stem(red_fn.stem + '_result').with_suffix('.pkl')
        print(red_fn)
        print(reduced_pkl_file)
        self.results_pkl_file = Path.joinpath(Path(results_path), reduced_pkl_file)
        print('results_pkl_file')
        print(self.results_pkl_file)
        Path.mkdir(self.results_pkl_file.parent, parents=True, exist_ok=True)

    # 2023-Oct-26: verify: widths_range is not used:
    def total_analysis(self, k_sep_pk=2.0, smoo=3000.0, widths_range=(4.0, 20.0),
                       peak_sd_fact=3.0, gener_dataframe=False, results_path='.',
                       peak_area_calc_method='basic'):
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
        :param results_path: WRITE
        :type results_path: string
        :param peak_area_calc_method: WRITE
        :type peak_area_calc_method: string
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
            if peak_area_calc_method == 'basic':
                self.net_spec_ser_an.perform_basic_net_area_calculation()
            elif peak_area_calc_method == 'gaussian_with_tail':
                gener_dataframe = False
                self.net_spec_ser_an.perform_gauss_with_tail_net_area_calculation()
            if gener_dataframe:
                # 2023-Oct-17 PAREI AQUI: Create folders of pkls as needed.
                self.define_result_pkl_name(results_path)
                self.generate_pandas_dataframe()
            print('Finish Spec.total_analysis!')
        else:
            print('Spec.total_analysis: No analysis applicable as spectrum is empty.')
        return

    def generate_pandas_dataframe(self):
        # for this spectrum, generate a pd.Dataframe and save it as a pkl-file.
        """Generate a Dataframe and save it as pkl for this spectrum.

        """

        a_spec_vars = vars(self)
        campos = [a for a in a_spec_vars]
        valores = [a_spec_vars[a] for a in a_spec_vars]
        # spec_df_type1 = pd.DataFrame(data=valores, index=campos)
        # spec_df_type1.to_pickle(self.pkl_file)
        spec_df_type2 = pd.DataFrame(data=[valores], columns=campos)
        # self.pkl_file = Path(self.f_name).with_suffix('.pkl')
        spec_df_type2.to_pickle(self.results_pkl_file)

    def read_pkl_file(self):
        pass
        # Náo usar ainda, só para verificar se o pkl_file pode ser recuperado:
        # results_df = pd.read_pickle(self.results_pkl_file)
        # read_orig = results_df['origin_spec_ser_an'][0]
        # orig_ser = read_orig
        # read_net = results_df['net_spec_ser_an'][0]
        # net_ser = read_net
        # vars(net_ser)
        # 2023 - May - 26
        # Ok! Espectro gravado, depois lido, então vamos prosseguir
        # com a identificação dos nuclídeos.
        # Agora, posso ler e analisar um espectro, gravá-lo e depois, em outro momento,
        # ler o pkl com a análise.

    def identify_nuclides(self, nucl_iear1_df):
        print("Lets identify nuclides.")
        # orig_ser = self.origin_spec_ser_an
        net_ser = self.net_spec_ser_an
        # x_nz = orig_ser.chans_nzero
        # y_nz = orig_ser.counts_nzero
        # chans = net_ser.x_s
        # ys_net_counts = net_ser.y_s
        # peaks_net = net_ser.pk_parms.peaks
        # peaks_orig = orig_ser.pk_parms.peaks
        # counts = orig_ser.y_s
        # chans_nzero = orig_ser.chans_nzero
        # counts_nzero = orig_ser.counts_nzero
        # unc_y = orig_ser.unc_y
        # eval_y = orig_ser.y_smoothed
        # eval_bl = orig_ser.eval_baseline
        # fin_bl = orig_ser.final_baseline
        # inis = orig_ser.pk_parms.propts['left_bases']
        # fins = orig_ser.pk_parms.propts['right_bases']
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

        self.pks_comprehensive_df = pd.concat([peaks_df, pks_properties_df], axis=1)
        print(self.pks_comprehensive_df)

        self.add_engy_to_pks_df(self.pks_comprehensive_df, self.channel_energy_calib.get_energy)
        print(self.pks_comprehensive_df)

        # 2023-08-27 PAREI AQUI
        # self.nucl_an.nuclide_identif(nucl_iear1_df, pks_comprehensive_df)

    # 2023-Oct-23 FIX
    def add_engy_to_pks_df(self, pks_kev_df, func_en):
        pks_kev_df['engy_pk_det'] = func_en(pks_kev_df.centroids)

    def create_activities_df(self, nucl_df, results_path='.', must_be_key_gamma=False):
        en_toler_calib = 3.0
        en_toler_ident = 0.4
        if must_be_key_gamma:
            nucl_aux_df = pd.DataFrame(nucl_df.loc[nucl_df.is_key_gamma])
        else:
            nucl_aux_df = pd.DataFrame(nucl_df)
        cross_df_1 = pd.merge(self.pks_comprehensive_df, nucl_aux_df, how='cross')
        cross_df_1["delta_en"] = cross_df_1.engy_pk_det - cross_df_1.energy
        aux_2 = pd.DataFrame(cross_df_1.loc[np.abs(cross_df_1.delta_en) < en_toler_calib])
        x_energy = np.array(aux_2.energy).reshape(-1, 1)
        y_delta_en = np.array(aux_2.delta_en)
        # Robustly fit linear model with RANSAC algorithm
        ransac = linear_model.RANSACRegressor()
        ransac.fit(x_energy, y_delta_en)
        inlier_mask = ransac.inlier_mask_
        outlier_mask = np.logical_not(inlier_mask)
        aux_2["recalib_engy_ransac"] = aux_2.engy_pk_det - ransac.predict(x_energy)
        aux_2["new_delta_en"] = aux_2.recalib_engy_ransac - aux_2.energy
        aux_3 = aux_2.loc[abs(aux_2.new_delta_en) < 0.4]
        new_ch_en_calib = Pol.fit(aux_3.centroids, aux_3.energy, deg=2)

        self.pks_comprehensive_df['recalib_energy'] = new_ch_en_calib(self.pks_comprehensive_df.centroids)

        # 2023-Jun-14
        # Loading calibration pkl file:
        calib_pkl_name = 'data/f100_gmx_2021.pkl'
        calib_df = pd.read_pickle(calib_pkl_name)

        self.p_eff, _ = calib_df.effic_func[3]

        # 2023-Aug-18
        # AQUI escolher nucludeo que tiver mais picos identificados (Ag-110m tem mais que Cs-137)
        # Por enquanto, usar a calibracao robusta, que deve bastar.

        cross_df_2 = pd.merge(self.pks_comprehensive_df, nucl_df, how='cross')
        cross_df_2["delta_en"] = cross_df_2.recalib_energy - cross_df_2.energy
        df_result = pd.DataFrame(cross_df_2.loc[np.abs(cross_df_2.delta_en) < en_toler_ident])

        lv_time = self.lv_time
        # Sample size (L, kg, g etc.)
        samp_size = 0.1
        sam_descr = self.sam_descr
        source_datetime = self.source_datetime
        start_datetime = self.start_datetime

        df_result["disintegr"] = df_result.rough_sums / (self.en_eff(df_result.energy) * 1e-4 * df_result.intensity)
        df_result['activity_conc'] = df_result.disintegr / (self.lv_time * samp_size)
        # 2023-Sep-21:
        # AQUI: fazer a propagação de incerteza de activity_conc

        # df_result.dtypes
        df_result['acti_conc_unc'] = df_result.activity_conc * (np.sqrt(df_result.variances) / df_result.rough_sums) * (
            df_result.unc_i / df_result.intensity
        )

        # 2023-ago-4 PAREI AQUI. Fazer a indexação para o cálculo da atividade considerando a média das linhas
        # de cada nuclídeo
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#dataframe-column-selection-in-groupby
        d5_grouped = df_result.groupby("nuclide_name")[
            ['energy', 'intensity', 'centroids', 'rough_sums', 'variances', 'disintegr']]
        # d5_grouped = d5.groupby("nuclide_name")[['disintegr']]
        # sdfsdf = pd.DataFrame([[d5_grouped.mean(), d5_grouped.median()]])
        # sdfsdf

        df_result.groupby("nuclide_name")[['activity_conc']].describe()

        first_result = self.results_pkl_file.with_stem('first_result')
        cross_df_2.to_pickle(first_result)

        second_result = self.results_pkl_file.with_stem('second_result')
        df_result.to_pickle(second_result)

        df_result.groupby("nuclide_name")[['activity_conc']].describe()
        # 2023-Oct-26: NOTE: To locate a nuclide use
        # df_result.loc[df_result.nuclide_name == "110ag"]
        df_result['one_s2'] = 1.0 / df_result.acti_conc_unc ** 2.0
        df_result['x_s2'] = df_result.activity_conc * df_result.one_s2
        third_result = self.results_pkl_file.with_stem('third_result')
        df_result.to_pickle(third_result)

        # retomando
        grpd = df_result.groupby("nuclide_name")
        res_1 = pd.DataFrame(grpd[["one_s2", "x_s2"]].agg("sum"))
        res_1["avrg_xm"] = res_1.x_s2 / res_1.one_s2
        res_1["avrg_sd"] = 1.0 / np.sqrt(res_1.one_s2)
        # 2023-10-22 AQUI: MUDAR!!!!
        # final_activity_list_pkl_file = f_name.with_stem(f_name.stem + '_activ_list').with_suffix('.pkl')
        # final_activity_list_pkl_file
        red_fn = Path(self.reduced_f_name)
        final_pkl_file = red_fn.with_stem(red_fn.stem + '_final').with_suffix('.pkl')
        final_pkl_file = Path.joinpath(Path(results_path), final_pkl_file)
        Path.mkdir(self.results_pkl_file.parent, parents=True, exist_ok=True)
        res_1.to_pickle(final_pkl_file)

        return aux_3, self.pks_comprehensive_df, df_result, d5_grouped, res_1
