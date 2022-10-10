import numpy as np
from scipy.signal import find_peaks
from src.peaksparms_class import PeaksParms


class GenericSeriesAnalysis:
    """Analyze a generic number series to find peaks, estimate their parameters and possibly find baseline."""

    def __init__(self, cnt_arrs):
        self.cnt_arrs = cnt_arrs
        self.ys = cnt_arrs.y_s
        self.n_ch = self.ys.size
        self.pk_parms = PeaksParms()

    def resolve_peaks_and_regions(self, k_sep_pk, smoo):
        self.peaks_search()
        print('resolve_peaks_and_regions:')
        self.redefine_widths_range()
        self.peaks_search(widths_range=self.widths_pair)
        self.define_multiplets_regions(k_sep_pk, smoo)
        self.baseline = self.cnt_arrs.calculate_base_line(
            mix_regions=self.pk_parms.mix_regions, smoo=smoo)

    def peaks_search(self, peak_sd_fact=3.0, widths_range=(None, None)):
        """Peaks search; use scipy.signal.find_peaks."""
        height = peak_sd_fact * np.sqrt(self.ys)
        prominence = peak_sd_fact * np.sqrt(self.ys)
        if widths_range == (None, None):
            widths_range = (self.n_ch * 0.0003, self.n_ch * 0.01)
        self.widths_range = widths_range
        peaks, propts = find_peaks(
            self.ys,
            height=height,
            threshold=(None, None),
            prominence=prominence,
            width=widths_range,
            rel_height=0.5)

        self.pk_parms.peaks = peaks
        self.pk_parms.propts = propts

    def redefine_widths_range(self):
        """Redefine widths range."""
        ws_min = np.percentile(self.pk_parms.propts['widths'], 25) * 0.5
        ws_max = np.percentile(self.pk_parms.propts['widths'], 75) * 2.0
        self.widths_pair = (ws_min, ws_max)


    def define_multiplets_regions(self, k_sep_pk, smoo):
        """Define multiplet regions from already found peaks with proper widths."""
        # k_sep_pk: Fator de fwhm para ampliar multipletos:
        # 2021-06-28
        # 2022-03-24 Vamos refatorar tudo:

        widths_extd = k_sep_pk * self.pk_parms.propts['widths']
        ini_extd = np.round(self.pk_parms.peaks - widths_extd).astype(int)
        fin_extd = np.round(self.pk_parms.peaks + widths_extd).astype(int)
        if self.pk_parms.peaks.any():
            for i_pk, ch_pk in enumerate(self.pk_parms.peaks):
                for i_ch in range(ini_extd[i_pk], fin_extd[i_pk] + 1):
                    if (i_ch >= 0) & (i_ch < self.n_ch):
                        self.cnt_arrs.is_reg[i_ch] = True

        comuta = np.zeros(self.n_ch)
        for i in range(1, self.n_ch):
            comuta[i] = self.cnt_arrs.is_reg[i].astype(int) - self.cnt_arrs.is_reg[i - 1].astype(int)

        # np.nonzero gera uma tupla, não sei por quê.
        inis = np.nonzero(comuta > 0)[0]
        # fins = np.append(np.nonzero(comuta<0), n)
        fins = np.nonzero(comuta < 0)[0]

        # Ajusta comprimento dos arrays. Têm de ser iguais.
        min_size = np.minimum(inis.size, fins.size)
        inis = inis[:min_size]
        fins = fins[:min_size]
        self.mix_regions = np.concatenate(np.array([[inis], [fins]])).T

        self.cnt_arrs.calculate_base_line(self.mix_regions, smoo)

        print('define_multiplets_regions completado. Define: self.mix_regions.')
