# Created on Fri Nov  5 12:00:42 2021

# @author: mmaduar
import numpy as np

from genericcalib_class import ChannelEnergyCalib, EnergyFwhmCalib, EnergyEfficiencyCalib
from specchn_class import SpecChn
from speciec_class import SpecIec
from cntarraylike_class import CntArrayLike
from peaksparms_class import PeaksParms


class SpecParms:
    """Given spectrum parameters (count time, sample description etc)."""

    def __init__(self, f_name, sufx):
        self.sufx = sufx
        if self.sufx == '.chn':
            self.spec_io = SpecChn(f_name)
        elif self.sufx == '.iec':
            self.spec_io = SpecIec(f_name)

        #
        n_ch = self.spec_io.n_ch

        self.cnt_array_like = CntArrayLike(n_ch, self.spec_io.sp_counts)
        self.peaks_parms = PeaksParms()

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
        try: # 2022-Jun-23
            self.spec_io.en_ef_calib
        except AttributeError:
            pass
        else:
            self.energy_efficiency_calib = EnergyEfficiencyCalib(self.spec_io.en_ef_calib)

#    def total_analysis(self, smoo, widths_range, k_sep_pk=5.0):
    def total_analysis(self, k_sep_pk, smoo, widths_ranges):
        """
        # sequência:
        #    incia obj spec_parms
        #    initial_peaks_search: acha picos candidatos, põe em peaks_parms.peaks
        #    define_multiplets_regions:
        #       em init do cnt_array_like, define eval_smoo_cts
        #       em define_multiplets_regions: define is_reg com base em bons picos
        #    em define_multiplets_limits: define mix_regions (lims reg)
        #    calculate_base_line
        #    calculate_net_spec
        #
        #
        #
        #
        """
#        dá pobrema fazer em eval_smoo_cts
#        self.peaks_parms.initial_peaks_search(self.cnt_array_like.n_ch,
#                                              self.cnt_array_like.eval_smoo_cts)
        # 2022-07-15: AQUI: ver como implementar isso:
        # assemble a local counts array with left tail substituted
        # counts_wo_ltail = np.concatenate(())
        self.peaks_parms.peaks_search (cts_to_search=self.cnt_array_like.y0s, gross=True)
        self.peaks_parms.redefine_widths_range()
        self.peaks_parms.peaks_search (cts_to_search=self.cnt_array_like.y0s, gross=True,
                                       widths_range=self.peaks_parms.widths_range)
        self.peaks_parms.initial_width_lines()

        print(self.cnt_array_like.is_reg)
        print(self.cnt_array_like.is_reg.size)
        print(k_sep_pk)

        self.peaks_parms.define_multiplets_regions(self.cnt_array_like.is_reg,
                                                   k_sep_pk=k_sep_pk)
        self.cnt_array_like.calculate_base_line(self.peaks_parms.mix_regions, smoo)

        self.peaks_parms.peaks_search(cts_to_search=self.cnt_array_like.net_spec, gross=False)
        self.peaks_parms.net_width_lines()
        self.peaks_parms.define_net_multiplets_regions(self.cnt_array_like.is_net_reg,
                                                       k_sep_pk=k_sep_pk)

    def chunks_from_file(self, chunksize=8192):
        """ Read file chunks. """
        file_chunks = []
        with open(self, "rb") as f_file:
            while True:
                chunk = f_file.read(chunksize)
                if chunk:
                    yield chunk
                    file_chunks.append(chunk)
                else:
                    break
        return file_chunks
