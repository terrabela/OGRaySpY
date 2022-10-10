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



    def plot_figw2(self):

    def plot_figw4(self):
        # Initialize another figure
        self.figw4 = go.FigureWidget(self.figw1);

        # Add Traces


        self.figw4.add_trace(
            go.Scattergl(x=self.parms.peaks_parms.peaks_gro,
                         y=self.parms.peaks_parms.propts_gro['peak_heights'],
                         name = 'peak_heights',
                         marker = dict(color='yellow',
                                       symbol='circle',
                                       size=10,
                                       opacity=0.8,
                                       line=dict(color='green', width=2.0)
                                       ),
                         mode = 'markers'));
        # Set title and scale type
        self.figw4.update_layout(title_text='Fig 4: Base line')
        self.figw4.update_yaxes(type='log');
        self.figw4.write_html('figw4.html', auto_open=True)

    def plot_figw5(self):

        # graphic #5

        self.fig_steps = go.FigureWidget();
        self.fig_steps.add_trace(
            go.Scattergl(x=self.chans[self.nzero & self.is_reg],
                         y=self.counts[self.nzero & self.is_reg],
                         name='Counts in regions',
                         line=dict(color='navy', width=0.3),
                         mode='markers'));
        self.fig_steps.add_trace(
            go.Scattergl(x=self.chans[self.nzero & ~self.is_reg],
                         y=self.counts[self.nzero & ~self.is_reg],
                         name='Counts out of regions',
                         line=dict(color='orange', width=0.3),
                         mode='markers'));
        self.fig_steps.add_trace(
            go.Scattergl(x=self.xs_all_mplets,
                         y=self.ys_all_steps,
                         name='ys_all_steps',
                         line=dict(color='brown', width=1.5)));
        self.fig_steps.add_trace(
            go.Scattergl(x=self.xs_all_mplets,
                         y=self.ys_all_mplets,
                         name='ys_all_mplets',
                         line=dict(color='green', width=3.0)));
        self.fig_steps.add_trace(
            go.Scattergl(x=self.chans,
                         y=self.final_baseline,
                         name='final_baseline',
                         line=dict(color='magenta', width=0.7)));
        self.fig_steps.add_trace(
            go.Scattergl(x=self.peaks_gro,
                         y=self.pk_hei_gro,
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
        self.fig_steps.update_layout(title_text='Fig 5: fig_steps')
        self.fig_steps.update_yaxes(type='log');
        self.fig_steps.write_html('fig_steps.html', auto_open=True)

    def plot_figw6(self):

    # graphic #6

        self.figw6 = go.FigureWidget();

        self.figw6.add_trace(
            go.Scattergl(x=self.parms.cnt_array_like.chans,
                         y=self.parms.cnt_array_like.net_spec,
                         name='net_spec',
                         line=dict(color='magenta', width=0.7)));

        self.figw6.add_trace(
            go.Scattergl(x=self.parms.peaks_parms.peaks_net,
                         y=self.parms.peaks_parms.propts_net['peak_heights'],
                         name='peak_heights',
                         marker=dict(color='orange',
                                     symbol='circle',
                                     size=10,
                                     opacity=0.8,
                                     line=dict(color='blue', width=2.0)
                                     ),
                         mode='markers'));
        # Set title and scale type
        self.figw6.update_layout(title_text='Fig 6: net spec analysis')
        # self.figw6.update_yaxes(type='log');
        self.figw6.write_html('figw6.html', auto_open=True)


