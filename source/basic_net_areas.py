import numpy as np

class BasicNetAreas:
    """ Class for very crude net area calculations. """

    def __init__(self):

        self.fwhm_ch_ini = np.array([])
        self.fwhm_ch_fin = np.array([])
        self.n_ch_fwhm = np.array([])

        self.fwhm_chans = []
        self.counts_gross = []
        self.counts_net = []
        self.sum_gross = np.array([])
        self.sum_net = np.array([])
        self.s_sum_net = np.array([])
        self.fwhm_ctrs = np.array([])

    def basic_net_area_calculation(self):
        #####################################
        # PAREI AQUI 24-Mar-2022
        #####################################

        ### FAZER já: criar nova classe e colocar a initialição do membros s_sum_net, etc..

        # self.net_fwhm_chans = [
        #    np.array(range(_net_fw_ch_ini[i_pk], self.fwhm_ch_fin[i_pk]+1))
        #    for i_pk in range(n_pk) ]

        #        if areas_calc=='under_fwhm':
        #            # NET Centroids
        #            self.net_fwhm_ctrs = np.array([
        ###                np.average(self.fwhm_chans[i_pk], weights=self.counts_net[i_pk])
        #                for i_pk in range(n_pk)
        #                ])
        # Uncertainties in areas
        #           self.s_sum_net = np.sqrt(self.sum_gross + self.n_ch_fwhm**2 * self.plateaux)
        pass

basic_area = BasicNetAreas()