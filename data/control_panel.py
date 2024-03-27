# 2024-03-26: from
# 100 simple examples of Dash components interacting with Plotly graphs
# https://dash-example-index.herokuapp.com
# through
# Dash in 20 minutes
# https://dash.plotly.com/tutorial

from pathlib import Path, PurePath
import pandas as pd
from dash import Dash, dcc, html, Input, Output, ctx, callback
import dash_mantine_components as dmc
import plotly.graph_objects as go

from ograyspy_class import Ograyspy
from spec_class import Spec
from spec_graphics_class import assemble_graph

rep_parts_list = ['short report', 'long report', 'spectrum graph']

to_be_found = 'Genie_Transfer'
ogra = Ograyspy(to_be_found)
print(ogra.info_node)
print(ogra.pkl_folder_files)
ogra.environment_df
ogra.spectra_names_df
test1 = ogra.spectra_path
test2 = ogra.spectra_names_df.reduced_names_files_list[0]
test3 = PurePath(test1, test2)
df =  ogra.spectra_names_df
spec_list = df.reduced_names_files_list.unique()




# Initialize the app - incorporate css
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = Dash(__name__, external_stylesheets=external_stylesheets)

# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dmc.Container([
    dmc.Title(f"Spectrum analysis control panel", color='blue', size='h3', align="center"),
    dmc.Grid([
        dmc.Col([
            html.Div("Spectrum file name rel. to working folder:"),
            dcc.Dropdown(
                id='spec_fnwf',
                options=spec_list,
                value=spec_list[0]
            ),
            html.Div("Choose the radius scale:"),
            dcc.RadioItems(
                id="bar-polar-app-x-radio-items",
                options=["Linear", "Logarithmic"],
                value="Logarithmic",
            ),
            html.Div("Smooth depth"),
            dcc.Slider(
                id='k_smoo', min=1, max=100, step=10, value=20
            ),
            html.Div("Min FWHMs for each peak in regions - gross spectrum"),
            dcc.Slider(
                id='n_fwhm_gro', min=3, max=13, step=2, value=5
            ),
            html.Div("Baseline determination by:"),
            dcc.Dropdown(
                id="b_line",
                options=['spline', 'Savitzky-Golay'],
                value="spline",
            ),
            html.Div("Min FWHMs for each peak in regions - net spectrum"),
            dcc.Slider(
                id='n_fwhm_net', min=3, max=9, step=2, value=3
            ),
            html.Div("Method for FWHM vs channel fit:"),
            dcc.Dropdown(
                id="meth_fwhm_fit",
                options=['linear sqrt', 'polynomial'],
                value='linear sqrt',
            ),
            html.Div("Nuclide library:"),
            dcc.Dropdown(
                id="nucl_bibl",
                options=['Natural', 'Pool Reactor'],
                value='Pool Reactor',
            ),
            html.Div("Results generation:"),
            dcc.Dropdown(
                id='report_parts',
                value=rep_parts_list,
                options=rep_parts_list,
                multi=True,
            )
        ], span=2),
        dmc.Col([
            dcc.Graph(id='gr-placeholder')
        ], span=10),
        ]),
    ], fluid=True)


@app.callback(
    Output("gr-placeholder", "figure"),
    Input("spec_fnwf", "value"),
    Input("bar-polar-app-x-radio-items", "value"),
    Input("k_smoo", "value"),
    Input("n_fwhm_gro", "value"),
    Input("b_line", "value"),
    Input("n_fwhm_net", "value"),
    Input('meth_fwhm_fit', 'value'),
    Input("nucl_bibl", "value"),
    Input('report_parts', 'value')
)
def update_graph(p1, p2, p3, p4, p5, p6, p7, p8, p9):
    ctx_clicked = ctx.triggered_id
    fig = go.Figure()
    if ctx_clicked == 'spec_fnwf':
        a_spec, counts_graphic = assemble_graph(p1, ogra.spectra_path, gen_html=False)
        fig = counts_graphic.figw1
        fig.update_layout(
            title=p1,
            autosize=True,
            height=700, width=1100, margin=dict(l=20, r=20, t=30, b=20)
        )
    elif ctx_clicked=='bar-polar-app-x-radio-items':
        a_spec, counts_graphic = assemble_graph(p1, ogra.spectra_path, gen_html=False)
        fig = counts_graphic.figw1
        fig.update_layout(
            title=p1,
            autosize=True,
            height=700, width=1100, margin=dict(l=20, r=20, t=30, b=20)
        )
        if p2 == 'Linear':
            fig.update_yaxes(type='linear')
        elif p2 == 'Logarithmic':
            fig.update_yaxes(type='log')
        else:
            pass
    elif ctx_clicked in ["k_smoo", "n_fwhm_gro", "b_line", "n_fwhm_net",
                         'meth_fwhm_fit', "nucl_bibl", "report_parts", ""]:
        pass
    else:
        pass
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
