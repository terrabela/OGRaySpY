#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 12:54:36 2021

@author: maduar
"""

import numpy as np
import plotly.graph_objects as go


class SpecGraphics:
    def __init__(self, f_name):
        pass


class GenericGraphics(SpecGraphics):
    def __init__(self, f_name, x_s, y_s):
        super().__init__(f_name)
        self.f_name = str(f_name)
        self.figw = go.FigureWidget()
        self.figw.add_trace(
            go.Scattergl(x=x_s,
                         y=y_s))
        # Set title and scale type
        self.figw.update_layout(title_text='Fig 1: ' + self.f_name)
        self.figw.update_yaxes(type="log")
        self.figw.write_html(f_name + '.html', auto_open=True)


class GrossCountsGraphic(SpecGraphics):
    def __init__(self, f_name, ser_an):
        super().__init__(f_name)
        self.f_name = str(f_name)
        self.chans_nzero = ser_an.chans_nzero
        self.counts_nzero = ser_an.counts_nzero
        self.unc_y_4plot = np.where(ser_an.unc_y < 1.4, 0.0, ser_an.unc_y)
        # Initialize figure
        self.figw1 = go.FigureWidget()
        self.plot_figw1(ser_an, 'Gross_counts')

    def plot_figw1(self, spec_an, home_path, graph_name):
        self.figw1.add_trace(
            go.Scattergl(x=self.chans_nzero,
                         y=self.counts_nzero,
                         mode='markers',
                         marker_size=3,
                         error_y=dict(
                             color='orange', width=3.0,
                             type='data',  # value of error bar given in data coordinates
                             array=self.unc_y_4plot),
                         name='Counts & uncertainties'))
        self.figw1.add_trace(
            go.Scattergl(x=spec_an.x_s,
                         y=spec_an.y_s,
                         name='y_s',
                         line=dict(color='magenta', width=0.4)))
        self.figw1.add_trace(
            go.Scattergl(x=spec_an.x_s,
                         y=spec_an.y_smoothed,
                         name='y_smoothed',
                         line=dict(color='navy', width=0.5)))

        # Set title and scale type
        self.figw1.update_layout(title_text='Fig 1: ' + self.f_name)
        self.figw1.update_yaxes(type="log")
        self.figw1.write_html(str(home_path) + '/' + graph_name + '.html', auto_open=True)

class PeaksAndRegionsGraphic(SpecGraphics):

    def __init__(self, f_name, ser_an):
        super().__init__(f_name, ser_an)
        self.f_name = str(f_name)
        self.chans_nzero = ser_an.chans_nzero
        self.counts_nzero = ser_an.counts_nzero
        # Initialize figure
        self.figw2 = go.FigureWidget();

        # Initialize figure
        self.pk_parms = spec_an.pk_parms
        self.propts = self.pk_parms.propts

        self.plateaux = self.propts['peak_heights'] - self.propts['prominences']
        self.pk_parms.fwhm_ch_ini = np.ceil(self.propts['left_ips']).astype(int)
        self.pk_parms.fwhm_ch_fin = np.floor(self.propts['right_ips']).astype(int)

        self.fig_widths = go.FigureWidget();

        self.xs_fwhm_lines = np.array([])
        self.ys_fwhm_lines = np.array([])
        self.xs_fwb_lines = np.array([])
        self.ys_fwb_lines = np.array([])

    def define_width_lines(self):
        """Build width peaks related lines, just for plotting."""
        n_pk = self.pk_parms.peaks.size
        if n_pk != 0:
            self.xs_fwhm_lines = np.concatenate(np.stack(
                (self.propts['left_ips'], self.propts['right_ips'],
                 np.full(n_pk, None)), axis=1))
            self.ys_fwhm_lines = np.concatenate(np.stack(
                (self.propts['width_heights'],
                 self.propts['width_heights'],
                 np.full(n_pk, None)), axis=1))

            self.xs_fwb_lines = np.concatenate(np.stack(
                (self.propts['left_ips'], self.propts['right_ips'],
                 np.full(n_pk, None)), axis=1))
            self.ys_fwb_lines = np.concatenate(np.stack(
                (self.plateaux, self.plateaux, np.full(n_pk, None)), axis=1))

    def plot_figw2(self, spec_an, graph_name):
        self.figw2.add_trace(
            go.Scattergl(x=spec_an.x_s,
                         y=spec_an.y_s,
                         name='y_s',
                         line=dict(color='magenta', width=0.4)))
        # Set title and scale type
        self.figw2.update_layout(title_text='Fig 2: ' + self.f_name)
        self.figw2.update_yaxes(type="log")
        self.figw2.write_html(graph_name + '.html', auto_open=True)

    def net_width_lines_deletar(self):
        """Build width peaks related lines, just for plotting."""
        n_pk = self.peaks_net.size
        if n_pk != 0:
            self.net_xs_fwhm_lines = np.concatenate(np.stack(
                (self.propts_net['left_ips'], self.propts_net['right_ips'],
                 np.full(n_pk, None)), axis=1))
            self.net_ys_fwhm_lines = np.concatenate(np.stack(
                (self.propts_net['width_heights'],
                 self.propts_net['width_heights'],
                 np.full(n_pk, None)), axis=1))

    def plot_figw2(self, spec_an, graph_name):
        self.define_width_lines()
        self.fig_widths.add_trace(
            go.Scattergl(x=self.chans_nzero,
                         y=self.counts_nzero,
                         error_y=dict(
                             color='orange', width=3.0,
                             type='data',  # value of error bar given in data coordinates
                             array=self.unc_y_4plot,
                             visible=True),
                         name="Counts & uncertaintes",
                         line=dict(color='orange', width=0.7)));

        self.fig_widths.add_trace(
            go.Scattergl(x=self.xs_fwhm_lines,
                         y=self.ys_fwhm_lines,
                         name='FWHMs',
                         line=dict(color='blue', width=3.0)));
        self.fig_widths.add_trace(
            go.Scattergl(x=self.xs_fwb_lines,
                         y=self.ys_fwb_lines,
                         name='FW at base',
                         line=dict(color='magenta', width=3.0)));

        self.fig_widths.add_trace(
            go.Scattergl(x=self.pk_parms.peaks,
                         y=self.pk_parms.propts['peak_heights'],
                         name='peak_heights',
                         marker=dict(color='yellow',
                                     symbol='circle',
                                     size=10,
                                     opacity=0.8,
                                     line=dict(color='green', width=2.0)
                                     ),
                         mode='markers'));
        # Set title and scale type
        self.fig_widths.update_layout(title_text="Fig 2: Peaks widths")
        self.fig_widths.update_yaxes(type='log');
        self.fig_widths.write_html(graph_name + '.html', auto_open=True)


class BaselineGraphic(SpecGraphics):
    def __init__(self, f_name, spec_an):
        super().__init__(f_name, spec_an)
        self.f_name = f_name
        self.chans_nzero = spec_an.cnt_arrs.chans_nzero
        self.counts_nzero = spec_an.cnt_arrs.counts_nzero
        self.unc_y_4plot = np.where(spec_an.cnt_arrs.unc_y < 1.4,
                                    0.0,
                                    spec_an.cnt_arrs.unc_y)
        # Initialize figure
        self.figbl = go.FigureWidget();

    def plot_figbl(self, spec_an, graph_name):
        # self.united_step_baselines()
        self.figbl.add_trace(
            go.Scattergl(x=self.chans_nzero,
                         y=self.counts_nzero,
                         error_y=dict(
                             color='orange', width=3.0,
                             type='data',  # value of error bar given in data coordinates
                             array=self.unc_y_4plot,
                             visible=True),
                         name="Counts & uncertaintes",
                         line=dict(color='orange', width=0.7)));
        self.figbl.add_trace(
            go.Scattergl(x=spec_an.cnt_arrs.x_s,
                         y=spec_an.cnt_arrs.y_s,
                         name='y_s, eventually smoothed',
                         line=dict(color='navy', width=0.4)))

        self.figbl.add_trace(
            go.Scattergl(x=spec_an.cnt_arrs.x_s,
                         y=spec_an.cnt_arrs.eval_baseline,
                         name='eval_baseline',
                         line=dict(color='blue', width=0.5)));

        self.figbl.add_trace(
            go.Scattergl(x=spec_an.cnt_arrs.x_s,
                         y=spec_an.cnt_arrs.final_baseline,
                         name='final_baseline',
                         line=dict(color='red', width=0.6)));

        #        self.figbl.add_trace(
        #            go.Scattergl(x=spec_an.cnt_arrs.plotsteps_x,
        #                         y=spec_an.cnt_arrs.plotsteps_y,
        #                         name='calculated_step_counts',
        #                         line=dict(color='red', width=1.3)));

        # Set title and scale type
        self.figbl.update_layout(title_text='Baseline: ' + self.f_name)
        self.figbl.update_yaxes(type="log")
        self.figbl.write_html(graph_name + '.html', auto_open=True)


class NetSpecGraphic(SpecGraphics):

    def __init__(self, f_name, spec_an):
        super().__init__(f_name, spec_an)
        self.f_name = f_name
        # Initialize figure
        self.figns = go.FigureWidget();

    def plot_figns(self, spec_an, graph_name):
        # self.united_step_baselines()
        self.figns.add_trace(
            go.Scattergl(x=spec_an.cnt_arrs.x_s,
                         y=spec_an.cnt_arrs.net_spec,
                         name='net_spec',
                         line=dict(color='red', width=0.6)));
        # Set title and scale type
        # self.figns.update_layout(title_text='Net spec: ' + self.f_name)
        # self.figbl.update_yaxes(type="log")
        self.figns.write_html(graph_name + '.html', auto_open=True)

    def united_step_baselines(self):
        """Build concatenated arrays of step baselines, just for plotting."""
        self.ch_in_mu_li = self.spec_an.cnt_arrs.chans_in_multiplets_list
        self.calc_st_co = self.spec_an.cnt_arrs.calculated_step_counts
        self.plotsteps_x = np.concatenate([np.append(i, None) for i in self.ch_in_mu_li])
        self.plotsteps_y = np.concatenate([np.append(i, None) for i in self.calc_st_co])

    def plot_figw3(self):
        # graphic #3

        self.fig_is_reg = go.FigureWidget();

        self.fig_is_reg.add_trace(
            go.Scattergl(x=self.parms.cnt_array_like.chans_in_regs(),
                         y=self.parms.cnt_array_like.counts_in_regs(),
                         name='Counts in regions',
                         mode='markers',
                         marker=dict(
                             color='LightSkyBlue',
                             size=6,
                             line=dict(color='MediumPurple', width=3)
                         )));
        self.fig_is_reg.add_trace(
            go.Scattergl(x=self.parms.cnt_array_like.chans_outof_regs(),
                         y=self.parms.cnt_array_like.counts_outof_regs(),
                         name='Counts out of regions',
                         mode='markers',
                         marker=dict(
                             color='Pink',
                             size=5,
                             line=dict(color='LightGreen', width=2)
                         )));

        # Set title and scale type
        self.fig_is_reg.update_layout(title_text="Fig 3: Definition of regions")
        self.fig_is_reg.update_yaxes(type='log');
        self.fig_is_reg.write_html('fig_is_reg.html', auto_open=True)

class FftGraphic(SpecGraphics):
    def __init__(self, f_name, ser_an):
        super().__init__(f_name, ser_an)
        self.f_name = str(f_name)
        # self.chans_nzero = ser_an.chans_nzero
        # self.counts_nzero = ser_an.counts_nzero
        self.fft_s = ser_an.fft_s
        self.unc_y_4plot = np.where(ser_an.unc_y < 1.4, 0.0, ser_an.unc_y)
        # Initialize figure
        self.figfft = go.FigureWidget();

    def plot_fft(self, spec_an, graph_name):
        self.figfft.add_trace(
            go.Scattergl(x=spec_an.x_s,
                         y=self.fft_s,
                         name='fft',
                         line=dict(color='green', width=0.4)))
        # Set title and scale type
        self.figfft.update_layout(title_text='Fig fft: ' + self.f_name)
        self.figfft.update_yaxes(type="log")
        self.figfft.write_html(graph_name + '.html', auto_open=True)
