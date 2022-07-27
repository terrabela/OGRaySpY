# 2022-07-14 Rascunho criado

figw1.add_trace(
    go.Scattergl(x=chans[:-ch_win],
                 y=var_rel,
                 name='var_rel',
                 line=dict(color='blue', width=0.5)));

figw1.add_trace(
    go.Scattergl(
        x=xs_tail,
        y=ys_tail,
        mode='markers',
        marker=dict(
            color='cyan',
            symbol='star-triangle-down',
            size=10,
            opacity=0.5,
            line=dict(color='red', width=2.0)
        ),
        name='Left tail'
    )
);


def plot_graphics(self, spec_parms, graph_nos):
    # graphic #1

    chans_nzero = spec_parms.cnt_array_like.chans_nzero

    chans_nzero = spec_parms.cnt_array_like.chans_nzero
    counts_nzero = spec_parms.cnt_array_like.counts_nzero
    unc_y_4plot = spec_parms.cnt_array_like.unc_y_4plot
    chans = spec_parms.cnt_array_like.chans
    xs_bl_out_reg = spec_parms.cnt_array_like.xs_bl_out_reg
    ys_bl_out_reg = spec_parms.cnt_array_like.ys_bl_out_reg
    eval_smoo_cts = spec_parms.cnt_array_like.eval_smoo_cts
    # Initialize figure
    figw1 = go.FigureWidget()

    # Add Traces

    figw1.add_trace(
        go.Scatter(x=chans_nzero,
                   y=counts_nzero,
                   error_y=dict(
                       color='orange', width=3.0,
                       type='data',  # value of error bar given in data coordinates
                       array=unc_y_4plot,
                       visible=True),
                   name='Counts & uncertaintes',
                   line=dict(color='orange', width=0.3)))
    figw1.add_trace(
        go.Scatter(x=chans,
                   y=eval_smoo_cts,
                   name='Smoothed',
                   line=dict(color='navy', width=0.4)))

    # Set title and scale type
    figw1.update_layout(title_text='Fig 1: Gamma-ray spectrum with automatic smooth')
    figw1.update_yaxes(type='log');

    figw1.write_html('fig1w.html', auto_open=True)

    # graphic #2

    fig_widths = go.FigureWidget(figw1);

    fig_widths.add_trace(
        go.Scatter(x=spec_parms.peaks_parms.xs_fwhm_lines,
                   y=spec_parms.peaks_parms.ys_fwhm_lines,
                   name='FWHMs',
                   line=dict(color='blue', width=3.0)));
    fig_widths.add_trace(
        go.Scatter(x=spec_parms.peaks_parms.xs_fwb_lines,
                   y=spec_parms.peaks_parms.ys_fwb_lines,
                   name='FW at base',
                   line=dict(color='magenta', width=3.0)));
    fig_widths.add_trace(
        go.Scatter(x=spec_parms.peaks_parms.peaks,
                   y=spec_parms.peaks_parms.pk_hei,
                   name='peak_heights',
                   mode='markers',
                   line=dict(color='green', width=3.0)));

    fig_widths.add_trace(
        go.Scatter(x=spec_parms.peaks_parms.peaks,
                   y=spec_parms.peaks_parms.pk_hei - spec_parms.peaks_parms.promns,
                   name='pk_hei-promns',
                   mode='markers',
                   line=dict(color='cyan', width=3.0)));
    # Set title and scale type
    fig_widths.update_layout(title_text="Fig 2: Peaks widths")
    fig_widths.update_yaxes(type='log');
    fig_widths.write_html('fig_widths.html', auto_open=True)

    # graphic #3

    fig_is_reg = go.FigureWidget(fig_widths);

    fig_is_reg.add_trace(
        go.Scatter(x=spec_parms.cnt_array_like.chans_in_regs(),
                   y=spec_parms.cnt_array_like.counts_in_regs(),
                   name='Counts in regions',
                   mode='markers',
                   marker=dict(
                       color='LightSkyBlue',
                       size=6,
                       line=dict(color='MediumPurple', width=3)
                   )));
    fig_is_reg.add_trace(
        go.Scatter(x=spec_parms.cnt_array_like.chans_outof_regs(),
                   y=spec_parms.cnt_array_like.counts_outof_regs(),
                   name='Counts out of regions',
                   mode='markers',
                   marker=dict(
                       color='Pink',
                       size=5,
                       line=dict(color='LightGreen', width=2)
                   )));

    # Set title and scale type
    fig_is_reg.update_layout(title_text="Fig 3: Definition of regions")
    fig_is_reg.update_yaxes(type='log');
    fig_is_reg.write_html('fig_is_reg.html', auto_open=True)

    # graphic #4
    chans = spec_parms.cnt_array_like.chans
    counts = spec_parms.cnt_array_like.y0s
    nzero = spec_parms.cnt_array_like.nzero
    is_reg = spec_parms.cnt_array_like.is_reg
    xs_all_mplets = spec_parms.cnt_array_like.xs_all_mplets
    ys_all_mplets = spec_parms.cnt_array_like.ys_all_mplets
    ys_all_steps = spec_parms.cnt_array_like.ys_all_steps
    final_baseline = spec_parms.cnt_array_like.final_baseline
    peaks = spec_parms.peaks_parms.peaks
    pk_hei = spec_parms.peaks_parms.pk_hei

    # Initialize another figure
    figw4 = go.FigureWidget();

    # Add Traces

    figw4.add_trace(
        go.Scatter(x=chans_nzero,
                   y=counts_nzero,
                   error_y=dict(
                       color='orange', width=3.0,
                       type='data',  # value of error bar given in data coordinates
                       array=unc_y_4plot,
                       visible=True),
                   name='Counts & uncertaintes',
                   line=dict(color='orange', width=0.3)));
    figw4.add_trace(
        go.Scatter(x=xs_bl_out_reg,
                   y=ys_bl_out_reg,
                   name='eval_baseline',
                   line=dict(color='red', width=0.5)));
    figw4.add_trace(
        go.Scatter(x=peaks,
                   y=pk_hei,
                   name='peak_heights',
                   mode='markers',
                   line=dict(color='green', width=3.0)));

    # Set title and scale type
    figw4.update_layout(title_text='Fig 4: Base line')
    figw4.update_yaxes(type='log');
    figw4.write_html('figw4.html', auto_open=True)

    # graphic #5

    fig_steps = go.FigureWidget();
    fig_steps.add_trace(
        go.Scatter(x=chans[nzero & is_reg],
                   y=counts[nzero & is_reg],
                   name='Counts in regions',
                   line=dict(color='navy', width=0.3),
                   mode='markers'));
    fig_steps.add_trace(
        go.Scatter(x=chans[nzero & ~is_reg],
                   y=counts[nzero & ~is_reg],
                   name='Counts out of regions',
                   line=dict(color='orange', width=0.3),
                   mode='markers'));
    fig_steps.add_trace(
        go.Scatter(x=xs_all_mplets,
                   y=ys_all_steps,
                   name='ys_all_steps',
                   line=dict(color='brown', width=1.5)));
    fig_steps.add_trace(
        go.Scatter(x=xs_all_mplets,
                   y=ys_all_mplets,
                   name='ys_all_mplets',
                   line=dict(color='green', width=3.0)));
    fig_steps.add_trace(
        go.Scatter(x=chans,
                   y=final_baseline,
                   name='final_baseline',
                   line=dict(color='magenta', width=0.7)));
    fig_steps.add_trace(
        go.Scatter(x=peaks,
                   y=pk_hei,
                   name='peak_heights',
                   marker=dict(color='yellow',
                               symbol='circle',
                               size=10,
                               opacity=0.8,
                               line=dict(color='magenta', width=2.0)
                               ),
                   mode='markers',
                   line=dict(color='green', width=3.0)));
    # Set title and scale type
    fig_steps.update_layout(title_text='Fig 5: fig_steps')
    fig_steps.update_yaxes(type='log');
    fig_steps.write_html('fig_steps.html', auto_open=True)

    # graphic #6

    # peaks_net = spec_parms.peaks_parms.peaks_net
    # pk_hei_net = spec_parms.peaks_parms.propts_halfhe_net['peak_heights']

    # figw6 = go.FigureWidget(figw4);
    # figw6.add_trace(
    #    go.Scatter(x=peaks_net,
    #               y=pk_hei_net,
    #               name='pk_hei_net',
    #               marker=dict(color='yellow',
    #                           symbol='circle',
    #                           size=10,
    #                           opacity=0.8,
    #                           line=dict(color='magenta', width=2.0)
    #                          ),
    #               mode='markers',
    #               line=dict(color='green',width=3.0)));

    # Set title and scale type
    # figw6.update_layout(title_text='Fig 6: net spec analysis')
    # figw6.update_yaxes(type='log');
    # figw6.write_html('figw6.html', auto_open=True)

