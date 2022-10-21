import numpy as np
from scipy.interpolate import splrep, splev
from scipy.fft import fft, fftfreq, fftshift

class CountsSeriesArrays:
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
        if to_smooth:
            self.y_s = self.eval_smoo_counts()
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
        # _w = _raiz_y
        self.spl_baseline = splrep(x=x_1, y=_y, w=_w, k=3, s=smoo)
        # self.eval_baseline = splev(self.x_s, self.spl_baseline)
        self.eval_baseline = splev(self.x_s, self.spl_baseline)
        # self.eval_baseline = splev(x_1, self.spl_baseline)
        self.xs_bl_out_reg = x_1
        # print(x_1)
        self.ys_bl_out_reg = _y
        # print(_y)
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
            self.net_spec[slice(*multiplet_region)] = np.where(net_mplet < 0.0, 0.0, net_mplet)
            self.final_baseline = self.y_s - self.net_spec

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
