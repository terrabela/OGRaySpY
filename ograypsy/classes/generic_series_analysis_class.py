import numpy as np
from scipy.interpolate import splrep, splev
from scipy.fft import fft, fftfreq, fftshift
from scipy.signal import find_peaks, savgol_filter
from scipy.special import erf


def step_baseline(y_s):
    """Calculate step baseline inside a region. Called just by calculate_baseline."""
    cts_cumsum = np.cumsum(y_s[1:])
    cts_cumsum.resize(y_s.size, refcheck=False)
    cts_cumsum = np.roll(cts_cumsum, 1)
    coeff = (y_s[-1] - y_s[0]) / cts_cumsum[-1]
    contin = cts_cumsum * coeff + y_s[0]
    return contin


class GenericSeriesAnalysis:
    """
    Analyze a generic number series to find peaks, estimate their parameters
    and possibly find baseline.
    """

    def __init__(self, sp_counts, to_smooth, smooth_method, smooth_on, smooth_cond,
                 is_fft=False, given_variance=None):
        """
        Initialize a generic series analysis object.
        :param sp_counts: data series counts
        :type sp_counts: np.array
        :param to_smooth: whether to smooth sp_counts
        :type to_smooth: bool
        :param smooth_method: method to smooth sp_counts ('spline' or 'sav_gol')
        :type smooth_method: str
        :param smooth_on: smooth on counts ('lin') or on their logs ('log')
        :type smooth_on: string
        :param smooth_cond: smoothing condition as defined in scipy.interpolate.splrep
        :type smooth_cond: float
        """

        self.mix_regions = None
        self.spl_baseline = None
        self.eval_baseline = None
        self.y_s = np.array(sp_counts)
        self.nzero = self.y_s > 0
        self.n_ch = self.y_s.size
        self.final_baseline = None
        self.x_s = np.linspace(0, self.n_ch - 1, self.n_ch)
        self.chans_nzero = self.x_s[self.y_s > 0]
        self.counts_nzero = self.y_s[self.nzero]
        if given_variance is None:
            self.unc_y = np.sqrt(self.counts_nzero)
            self.given_variance = self.y_s
        else:
            self.given_variance = given_variance
            self.unc_y = np.sqrt(given_variance)
        self.y_smoothed = None
        if to_smooth:
            self.y_smoothed = self.eval_smoo_counts(smooth_method, smooth_cond)
        else:
            self.y_smoothed = self.y_s
        self.fft_s = None
        if is_fft:
            self.fft_s = fft(self.y_s)

        # self.plotsteps_x = []
        # self.plotsteps_y = []

        self.is_reg = np.zeros(self.n_ch, dtype=bool)

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
        # self.pk_parms = PeaksParms()
        self.fft_spec = np.array([])
        # Maybe irrelevant: 4 FWHMs is almost the whole area:
        self.k_erf = erf(4*np.sqrt(np.log(2)))

    def resolve_peaks_and_regions(self, k_sep_pk, peak_sd_fact):
        self.peaks_search(peak_sd_fact=peak_sd_fact)
        print('resolve_peaks_and_regions:')
        self.redefine_widths_range()
        self.peaks_search(peak_sd_fact=peak_sd_fact,
                          widths_range=self.widths_pair)
        self.define_multiplets_regions(k_sep_pk)

    def peaks_search(self, peak_sd_fact=3.0, widths_range=(None, None)):
        """Peaks search; use scipy.signal.find_peaks."""
        height = peak_sd_fact * np.sqrt(self.given_variance)
        prominence = peak_sd_fact * np.sqrt(self.given_variance)
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

    def define_multiplets_regions(self, k_sep_pk):
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

        print('define_multiplets_regions completado. Define: self.mix_regions.')

    def eval_smoo_counts(self, smooth_method, smooth_cond):
        if self.n_ch > 0:
            if smooth_method == 'spline':
                if smooth_cond:
                    s = smooth_cond
                else:
                    n_datapts = self.chans_nzero.size
                    s = n_datapts-np.sqrt(2*n_datapts)
                smoo_cts = splrep(x=self.chans_nzero, y=self.counts_nzero,
                                  w=1.0/self.unc_y, k=3, s=s)
                evaluated = splev(self.x_s, smoo_cts)
            elif smooth_method == 'sav_gol':
                evaluated = savgol_filter(self.y_s, window_length=13, polyorder=3)
            else:
                evaluated = None
            return evaluated

    def calculate_baseline(self, smoo):
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
        self.final_baseline = np.array(self.eval_baseline)
        self.xs_bl_out_reg = x_1
        self.ys_bl_out_reg = _y
        self.ws_bl_out_reg = _w

        self.xs_bl_in_reg = self.chans_in_regs()
        self.ys_bl_in_reg = self.counts_in_regs()

        for a_region in self.mix_regions:
            _xs = self.x_s[slice(*a_region)]
            _ys = self.y_s[slice(*a_region)]
            assembled_to_step = np.zeros(a_region[1] - a_region[0])
            assembled_to_step[0] = self.eval_baseline[a_region[0]]
            assembled_to_step[-1] = self.eval_baseline[a_region[1] - 1]
            assembled_to_step[1:-2] = self.y_smoothed[slice(a_region[0] + 1, a_region[1] - 2)]
            continuum = step_baseline(assembled_to_step)
            self.chans_in_multiplets_list.append(_xs)
            self.calculated_step_counts.append(continuum)
            self.final_baseline[slice(*a_region)] = continuum

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

    def perform_basic_net_area_calculation(self):
        """Perform a very rough net area calculation"""
        self.pk_parms.rough_sums = [np.sum(self.y_s[i[0]:i[1] + 1]) for i in self.pk_parms.wide_regions]
        # 2022-12-14 Parei aqui: calcular centroides
        self.pk_parms.centroids = [np.average(np.linspace(i[0], i[1], num=i[1]-i[0] + 1),
                                              weights=self.y_s[i[0]:i[1]+1])
                                   for i in self.pk_parms.wide_regions]
        self.pk_parms.variances = [np.sum(self.given_variance[i[0]:i[1] + 1])
                                   for i in self.pk_parms.wide_regions]
        # self.pk_parms.net_areas = self.k_erf * self.pk_parms.rough_sums

    def perform_gauss_with_tail_net_area_calculation(self):
        """Perform net area calculation by fitting a Gaussian with exponential left tail."""
        # 2024-Feb-15: use lmfit
        for i in self.pk_parms.wide_regions:
            x_pk = np.linspace(i[0], i[1], num=i[1]-i[0]+1)
            y_pk = self.y_s[i[0]:i[1] + 1]
            print(x_pk)
            print(y_pk)
