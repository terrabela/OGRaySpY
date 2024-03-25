from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

from ograyspy_class import Ograyspy
from spec_class import Spec
from spec_graphics_class import SpecGraphics, CountsGraphic

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Put here a folder in your system with spectra:
folder_to_find = 'Genie_Transfer/ALMERA22'
ogra = Ograyspy(folder_to_find=folder_to_find)

app.layout = html.Div([
    dcc.Dropdown(
        ogra.spectra_names_df['reduced_names_files_list'].unique(),
        id='red_fname_drpdn'),
    html.Div(id='dd-output-container-name'),
    html.Div(dcc.Slider(-5, 10, 1, value=-3, id='smooth-slidr')),
    html.Div([
        dcc.Graph(
            id='spectrum_plot'
        )])
])


@callback(
    Output('dd-output-container-name', 'children'),
    Input('red_fname_drpdn', 'value')
)
def update_output(value):
    # a_spec = Spec(value, value)
    print('Valor: ' + str(value))
    print('Indice: ') + str
    return f'You have selected {value}'


@callback(
    Output('spectrum_plot', 'figure'),
    Input('smooth-slidr', 'value')
)
def update_figure(value):
    fig = px.scatter(x=[1, 2, 3, 4, 5], y=[1, 2, 3, 4, 5])
    return fig


if __name__ == '__main__':
    app.run(debug=True)
