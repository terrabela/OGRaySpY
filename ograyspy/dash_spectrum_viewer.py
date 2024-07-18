import dash
from dash.dependencies import Input, Output
from dash import html, dcc
import pandas as pd
from pathlib import PurePath

from ograyspy_class import Ograyspy
from spec_graphics_class import assemble_graph

# TRABALHAR NESTE: INSERIR OS CONTROLES DMC de CONTROL_PANEL_WITH_GO

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/stockdata.csv')

df['reference'] = df[df.columns[0]]

rep_parts_list = ['short report', 'long report', 'spectrum graph']

to_be_found = 'Genie_Transfer'
ogra = Ograyspy(to_be_found)
print(ogra.info_node)
print(ogra.pkl_folder_files)
test1 = ogra.spectra_path
test2 = ogra.spectra_names_df.reduced_names_files_list[0]
test3 = PurePath(test1, test2)
spec_names_df =  ogra.spectra_names_df
spec_list = spec_names_df.reduced_names_files_list.unique()

app = dash.Dash(__name__)
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.layout = html.Div([
    html.Label('Color'),
    dcc.Dropdown(
        id='color',
        options=[
            {'label': 'Navy', 'value': '#001f3f'},
            {'label': 'Blue', 'value': '#0074D9'},
            {'label': 'Aqua', 'value': '#7FDBFF'},
            {'label': 'TEAL', 'value': '#39CCCC'},
            {'label': 'OLIVE', 'value': '#3D9970'},
            {'label': 'GREEN', 'value': '#2ECC40'},
            {'label': 'LIME', 'value': '#01FF70'},
            {'label': 'YELLOW', 'value': '#FFDC00'},
            {'label': 'ORANGE', 'value': '#FF851B'},
            {'label': 'RED', 'value': '#FF4136'},
            {'label': 'MAROON', 'value': '#85144b'},
            {'label': 'FUCHSIA', 'value': '#F012BE'},
            {'label': 'PURPLE', 'value': '#B10DC9'},
        ],
        value='#001f3f'
    ),

    html.Label('Reference'),
    dcc.RadioItems(
        id='reference',
        options=[{'label': i, 'value': i} for i in ['Display', 'Hide']],
        value='Display'
    ),

    html.Label('Dataset'),
    dcc.Dropdown(
        id='dataset',
        options=[{'label': i, 'value': i} for i in df.columns],
        value=df.columns[0]
    ),

    html.Label('Spectrum file name rel. to working folder:'),
    dcc.Dropdown(
        id='spec_fnwf',
        options=spec_list,
        value=spec_list[0]
    ),

    dcc.Graph(id='graph')
])


@app.callback(
    Output('graph', 'figure'),
    [Input('color', 'value'),
     Input('reference', 'value'),
     Input('dataset', 'value'),
     Input('spec_fnwf', 'value')])
def display_graph(color, reference, dataset, spec_fnwf):
    a_spec, counts_graphic = assemble_graph(spec_fnwf, ogra.spectra_path, gen_html=False)
    new_x = a_spec.origin_spec_ser_an.x_s
    new_y = a_spec.origin_spec_ser_an.y_s
    data = [{
        'x': new_x,
        'y': new_y,
        'mode': 'lines',
        'marker': {'color': color},
        'name': dataset
    }]
    if reference == 'Display':
        data.append({'x': df.index, 'y': df['reference'], 'mode': 'lines', 'name': 'Reference'})
    return {
        'data': data,
        'layout': {
            # `uirevsion` is where the magic happens
            # this key is tracked internally by `dcc.Graph`,
            # when it changes from one update to the next,
            # it resets all of the user-driven interactions
            # (like zooming, panning, clicking on legend items).
            # if it remains the same, then that user-driven UI state
            # doesn't change.
            # it can be equal to anything, the important thing is
            # to make sure that it changes when you want to reset the user
            # state.
            #
            # in this example, we *only* want to reset the user UI state
            # when the user has changed their dataset. That is:
            # - if they toggle on or off reference, don't reset the UI state
            # - if they change the color, then don't reset the UI state
            # so, `uirevsion` needs to change when the `dataset` changes:
            # this is easy to program, we'll just set `uirevision` to be the
            # `dataset` value itself.
            #
            # if we wanted the `uirevision` to change when we add the "reference"
            # line, then we could set this to be `'{}{}'.format(dataset, reference)`
            'uirevision': dataset,

            'legend': {'x': 0, 'y': 1}
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)