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
    def __init__(self, f_name, home_path, graph_name, x_s, y_s, xs_parts, ys_parts):
        super().__init__(f_name)
        self.f_name = str(f_name)
        # Initialize figure
        self.fig = go.FigureWidget()
        self.united_step_lines(xs_parts, ys_parts)
        self.fig.add_trace(
            go.Scattergl(x=self.x_pl,
                         y=self.y_pl,
                         name='y_pl',
                         line=dict(color='magenta', width=0.4)))
        self.fig.add_trace(
            go.Scattergl(x=x_s,
                         y=y_s,
                         name='y_s',
                         line=dict(color='green', width=0.4)))
        # Set title and scale type
        self.fig.update_layout(title_text='Fig X: ' + f_name)
        self.fig.update_yaxes(type='log')
        self.fig.write_html(str(home_path) + '/' + graph_name + '.html')

    def united_step_lines(self, x_s, y_s):
        """Build concatenated arrays of step lines, just for plotting."""
        self.x_pl = np.concatenate([np.append(i, None) for i in x_s])
        self.y_pl = np.concatenate([np.append(i, None) for i in y_s])


class CountsGraphic(SpecGraphics):
    def __init__(self, f_name, ser_an, home_path, graph_name):
        super().__init__(f_name)
        self.f_name = str(f_name)
        self.chans_nzero = ser_an.chans_nzero
        self.counts_nzero = ser_an.counts_nzero
        self.unc_y_4plot = np.where(ser_an.unc_y < 1.4, 0.0, ser_an.unc_y)
        # Initialize figure
        self.figw1 = go.FigureWidget()
        self.plot_figw1(ser_an, home_path, graph_name=graph_name)

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
        self.figw1.write_html(str(home_path) + '/' + graph_name + '.html')


class PeaksAndRegionsGraphic(SpecGraphics):

    def __init__(self, f_name, ser_an, home_path, graph_name):
        super().__init__(f_name)
        self.f_name = str(f_name)
        self.chans_nzero = ser_an.chans_nzero
        self.counts_nzero = ser_an.counts_nzero
        self.unc_y_4plot = np.where(ser_an.unc_y < 1.4, 0.0, ser_an.unc_y)

        self.pk_parms = ser_an.pk_parms
        self.propts = ser_an.pk_parms.propts

        self.plateaux = self.propts['peak_heights'] - self.propts['prominences']
        self.pk_parms.fwhm_ch_ini = np.ceil(self.propts['left_ips']).astype(int)
        self.pk_parms.fwhm_ch_fin = np.floor(self.propts['right_ips']).astype(int)

        self.xs_fwhm_lines = np.array([])
        self.ys_fwhm_lines = np.array([])
        self.xs_fwb_lines = np.array([])
        self.ys_fwb_lines = np.array([])

        # Initialize figure
        self.fig_widths = go.FigureWidget()
        self.plot_fig_widths(ser_an, home_path, 'Peaks_Regions')

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

    def plot_fig_widths(self, spec_an, home_path, graph_name):
        self.define_width_lines()
        self.fig_widths.add_trace(
            go.Scattergl(x=self.chans_nzero,
                         y=self.counts_nzero,
                         mode='markers',
                         marker_size=3,
                         error_y=dict(
                             color='orange', width=3.0,
                             type='data',  # value of error bar given in data coordinates
                             array=self.unc_y_4plot),
                         name='Counts & uncertainties'))
        self.fig_widths.add_trace(
            go.Scattergl(x=spec_an.x_s,
                         y=spec_an.y_s,
                         name='y_s',
                         line=dict(color='magenta', width=0.4)))
        self.fig_widths.add_trace(
            go.Scattergl(x=spec_an.x_s,
                         y=spec_an.y_smoothed,
                         name='y_smoothed',
                         line=dict(color='navy', width=0.5)))
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
        self.fig_widths.update_layout(title_text='Fig 2: Pekas' + self.f_name)
        self.fig_widths.update_yaxes(type="log")
        self.fig_widths.write_html(str(home_path) + '/' + graph_name + '.html')


class BaselineGraphic(SpecGraphics):

    def __init__(self, f_name, ser_an, home_path):
        super().__init__(f_name)
        self.f_name = str(f_name)
        self.chans_nzero = ser_an.chans_nzero
        self.counts_nzero = ser_an.counts_nzero
        self.unc_y_4plot = np.where(ser_an.unc_y < 1.4, 0.0, ser_an.unc_y)
        self.eval_baseline = ser_an.eval_baseline
        self.final_baseline = ser_an.final_baseline
        # Initialize figure
        self.figbl = go.FigureWidget()
        self.plot_figbl(ser_an, home_path, 'Gross_counts__baseline')

    def plot_figbl(self, spec_an, home_path, graph_name):
        # self.united_step_baselines()
        self.figbl.add_trace(
            go.Scattergl(x=self.chans_nzero,
                         y=self.counts_nzero,
                         mode='markers',
                         marker_size=3,
                         error_y=dict(
                             color='orange', width=3.0,
                             type='data',  # value of error bar given in data coordinates
                             array=self.unc_y_4plot),
                         name='Counts & uncertainties'))
        self.figbl.add_trace(
            go.Scattergl(x=spec_an.x_s,
                         y=self.eval_baseline,
                         name='eval_baseline',
                         line=dict(color='blue', width=0.5)));

        self.figbl.add_trace(
            go.Scattergl(x=spec_an.x_s,
                         y=self.final_baseline,
                         name='final_baseline',
                         line=dict(color='magenta', width=0.6)));

        self.figbl.add_trace(
            go.Scattergl(x=spec_an.x_s,
                         y=spec_an.y_smoothed,
                         name='y_smoothed',
                         line=dict(color='red', width=0.6)));

        #        self.figbl.add_trace(
        #            go.Scattergl(x=spec_an.cnt_arrs.plotsteps_x,
        #                         y=spec_an.cnt_arrs.plotsteps_y,
        #                         name='calculated_step_counts',
        #                         line=dict(color='red', width=1.3)));

        # Set title and scale type
        self.figbl.update_layout(title_text='Baseline: ' + self.f_name)
        self.figbl.update_yaxes(type="log")
        self.figbl.write_html(str(home_path) + '/' + graph_name + '.html')


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
        self.figns.write_html(graph_name + '.html')

    def united_step_baselines_DELETE(self):
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
        self.fig_is_reg.write_html('fig_is_reg.html')


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
        self.figfft.write_html(graph_name + '.html')
