import numpy as np
from scipy.interpolate import splrep, splev
from scipy.fft import fft, fftfreq, fftshift
from scipy.signal import find_peaks
from peaksparms_class import PeaksParms


class GenericSeriesAnalysis:
    """
    Analyze a generic number series to find peaks, estimate their parameters
    and possibly find baseline.
    """

    def __init__(self, sp_counts, to_smooth, is_fft=False):
        self.spl_baseline = None
        self.eval_baseline = None
        self.y_s = np.array(sp_counts)
        self.nzero = self.y_s > 0
        self.n_ch = self.y_s.size
        self.final_baseline = np.zeros(self.n_ch)
        self.x_s = np.linspace(0, self.n_ch - 1, self.n_ch)
        self.chans_nzero = self.x_s[self.y_s > 0]
        self.counts_nzero = self.y_s[self.nzero]
        self.unc_y = np.sqrt(self.counts_nzero)
        self.y_smoothed = None
        if to_smooth:
            self.y_smoothed = self.eval_smoo_counts()
        self.fft_s = None
        if is_fft:
            self.fft_s = fft(self.y_s)

        # self.plotsteps_x = []
        # self.plotsteps_y = []

        self.is_reg = np.zeros(self.n_ch, dtype=bool)

        self.net_spec = np.zeros(self.n_ch)
        self.xs_all_mplets = []
        self.ys_all_mplets = []
        self.ys_all_steps = []

        self.chans_in_multiplets_list = []
        self.calculated_step_counts = []

        self.xs_bl_in_reg = np.array([])
        self.ys_bl_in_reg = np.array([])

        self.xs_bl_out_reg = np.array([])
        self.ys_bl_out_reg = np.array([])
        self.ws_bl_out_reg = np.array([])

        try:
            self.n_ch = self.ys.size
        except AttributeError:
            pass
        self.pk_parms = PeaksParms()
        self.fft_spec = np.array([])

    def eval_smoo_counts(self):
        if self.n_ch > 0:
            smoo_cts = splrep(x=self.chans_nzero,
                              y=self.counts_nzero,
                              w=1.0 / self.unc_y, k=3)
            evaluated = splev(self.x_s, smoo_cts)
            return evaluated

    def calculate_base_line(self, mix_regions, smoo):
        """Calculate baseline."""
        x_1 = self.chans_outof_regs()
        _first_nz = np.nonzero(self.y_s)[0][0]
        _init_fill = np.mean(self.y_s[_first_nz:_first_nz + 7]).astype(int)
        _y = self.counts_outof_regs()
        _y[0:_first_nz] = _init_fill
        _raiz_y = np.sqrt(_y)
        _raiz_y[_raiz_y < 2] = 1.0
        _w = 1.0 / _raiz_y
        self.spl_baseline = splrep(x=x_1, y=_y, w=_w, k=3, s=smoo)
        self.eval_baseline = splev(self.x_s, self.spl_baseline)
        self.xs_bl_out_reg = x_1
        self.ys_bl_out_reg = _y
        self.ws_bl_out_reg = _w

        self.xs_bl_in_reg = self.chans_in_regs()
        self.ys_bl_in_reg = self.counts_in_regs()

        for multiplet_region in mix_regions:
            _xs = self.x_s[slice(*multiplet_region)]
            _ys = self.y_s[slice(*multiplet_region)]
            _bl_in = splev(multiplet_region[0] - 1, self.spl_baseline)
            _bl_fi = splev(multiplet_region[1], self.spl_baseline)
            contin = np.zeros(_ys.size)
            gross_area = np.sum(_ys) + _bl_fi
            delta_y = _bl_fi - _bl_in
            delta_x = _ys.size
            for i in range(delta_x):
                sum_y = np.sum(_ys[0:i + 1])
                contin[i] = _bl_in + delta_y * sum_y / gross_area
            self.chans_in_multiplets_list.append(_xs)
            self.calculated_step_counts.append(contin)
            net_mplet = _ys - contin
            #    self.xs_all_mplets.extend(list(xs_mplet))
            #    self.xs_all_mplets.append( None )
            #    self.ys_all_mplets.extend(list(net_mplet))
            #    self.ys_all_mplets.append( None )
            #    self.ys_all_steps.extend(list(a_step))
            #    self.ys_all_steps.append( None )
            # self.net_spec[slice(*multiplet_region)] = np.where(net_mplet < 0.0, 0.0, net_mplet)
            # self.final_baseline = self.y_smoothed - self.net_spec

    def chans_in_regs(self):
        """ Channels in regions. """
        return self.x_s[self.is_reg]

    def counts_in_regs(self):
        """ Counts in regions. """
        return self.y_s[self.is_reg]

    def chans_outof_regs(self):
        """ Channels out of regions. """
        return self.x_s[~self.is_reg]

    def counts_outof_regs(self):
        """  Counts out of regions. """
        return self.y_s[~self.is_reg]

    def final_sums(self, pkp):
        print('Entrou em arrays')
        print(pkp.wide_regions)
        for i in pkp.wide_regions:
            print(self.y_s[i[0]:i[1] + 1])
        for i in pkp.fwhm_centr:
            print(i)
        for i in pkp.wide_regions:
            print(sum(self.y_s[i[0]:i[1] + 1]))

    def resolve_peaks_and_regions(self, k_sep_pk, smoo):
        self.peaks_search()
        print('resolve_peaks_and_regions:')
        self.redefine_widths_range()
        self.peaks_search(widths_range=self.widths_pair)
        self.define_multiplets_regions(k_sep_pk, smoo)
        self.baseline = self.calculate_base_line(mix_regions=self.pk_parms.mix_regions, smoo=smoo)

    def peaks_search(self, peak_sd_fact=3.0, widths_range=(None, None)):
        """Peaks search; use scipy.signal.find_peaks."""
        height = peak_sd_fact * np.sqrt(self.y_s)
        prominence = peak_sd_fact * np.sqrt(self.y_s)
        if widths_range == (None, None):
            widths_range = (self.n_ch * 0.0003, self.n_ch * 0.01)
        self.widths_range = widths_range
        peaks, propts = find_peaks(
            self.y_s,
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
                        self.is_reg[i_ch] = True

        comuta = np.zeros(self.n_ch)
        for i in range(1, self.n_ch):
            comuta[i] = self.is_reg[i].astype(int) - self.is_reg[i - 1].astype(int)

        # np.nonzero gera uma tupla, não sei por quê.
        inis = np.nonzero(comuta > 0)[0]
        # fins = np.append(np.nonzero(comuta<0), n)
        fins = np.nonzero(comuta < 0)[0]

        # Ajusta comprimento dos arrays. Têm de ser iguais.
        min_size = np.minimum(inis.size, fins.size)
        inis = inis[:min_size]
        fins = fins[:min_size]
        self.mix_regions = np.concatenate(np.array([[inis], [fins]])).T

        self.calculate_base_line(self.mix_regions, smoo)

        print('define_multiplets_regions completado. Define: self.mix_regions.')

    def calculate_net_spec(self, spec):
        """Calculate net spectrum."""
        net_spec = np.zeros(self.n_ch)
        for multiplet_region in self.mix_regions:
            xs_mplet = spec.spec_analysis.chans[slice(*multiplet_region)]
            ys_mplet = spec.y0s[slice(*multiplet_region)]
            ini_ch_mplet = multiplet_region[0]
            fin_ch_mplet = multiplet_region[1] - 1
            args = (ini_ch_mplet, fin_ch_mplet,
                    splev(ini_ch_mplet, spec.spec_analysis.spl_baseline),
                    splev(fin_ch_mplet, spec.spec_analysis.spl_baseline),
                    spec.y0s)
            a_step = step_baseline(*args)
            net_mplet = ys_mplet - a_step
            self.xs_all_mplets.extend(list(xs_mplet))
            self.xs_all_mplets.append(None)
            self.ys_all_mplets.extend(list(net_mplet))
            self.ys_all_mplets.append(None)
            self.ys_all_steps.extend(list(a_step))
            self.ys_all_steps.append(None)
            net_spec[slice(*multiplet_region)] = np.where(net_mplet < 0.0, 0.0, net_mplet)

# Ver onde chamar:
#        self.calculate_net_spec(spec)
