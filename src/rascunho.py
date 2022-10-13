# 2021-Jul-08
# from lmfit import Model, Minimizer, minimize, Parameters, report_fit, fit_report, printfuncs

# https://lmfit.github.io/lmfit-py/
# builtin_models.html?highlight=peaks%20sum#example-3-
# fitting-multiple-peaks-and-using-prefixes
# from lmfit.models import ExponentialModel, GaussianModel

# https://lmfit.github.io/lmfit-py/builtin_models.html?highlight=peaks%20sum#example-3-fitting-
# multiple-peaks-and-using-prefixes

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


# 2022-Out-13
# Rascunho para implementar tox, algum dia.

# copied from https://github.com/pypa/sampleproject 2022-07-27

# this file is *not* meant to cover or endorse the use of tox or pytest or
# testing in general,
#
#  It's meant to show the use of:
#
#  - check-manifest
#     confirm items checked into vcs are in your sdist
#  - python setup.py check
#     confirm required package meta-data in setup.py
#  - readme_renderer (when using a ReStructuredText README)
#     confirms your long_description will render correctly on PyPI.
#
#  and also to help confirm pull requests to this project.

[tox]
# envlist = py{37,38,39,310}
envlist = py310

# Define the minimal tox version required to run;
# if the host tox is less than this the tool with create an environment and
# provision it with a tox that satisfies it under provision_tox_env.
# At least this version is needed for PEP 517/518 support.
minversion = 3.3.0

# Activate isolated build environment. tox will use a virtual environment
# to build a source distribution from the source tree. For build tools and
# arguments use the pyproject.toml file as specified in PEP-517 and PEP-518.
isolated_build = true

[testenv]
deps = pytest
    check-manifest >= 0.42
    # If your project uses README.rst, uncomment the following:
    # readme_renderer
    # flake8
    # pytest
commands = pytest
    # check-manifest --ignore 'tox.ini,tests/**'
    # This repository uses a Markdown long_description, so the -r flag to
    # `setup.py check` is not needed. If your project contains a README.rst,
    # use `python setup.py check -m -r -s` instead.
    # python setup.py check -m -s
    # flake8 .
    # py.test tests {posargs}

# [flake8]
# exclude = .tox,*.egg,build,data
# select = E,W,F
