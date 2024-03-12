# Import packages
from dash import Dash, html, dcc, dash_table
import pandas as pd
import pathlib

# Initialize the app
app = Dash(__name__)
app.title = "Gamma-ray spectrum analysis"

server = app.server
app.config.suppress_callback_exceptions = True

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

# Read data
# df = pd.read_csv(DATA_PATH.joinpath("clinical_analytics.csv.gz"))
df = pd.read_pickle(DATA_PATH.joinpath("WindowsPedro-notebook.pkl"))

# App layout
# app.layout = html.Div([
#     html.Div(children='My First App with Data'),
#     dash_table.DataTable(data=df.to_dict('records'), page_size=10)
# ])

app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner1",
            className="banner1",
            children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
        ),
        # Left column

        # Right column
        html.Div(
            id="banner2",
            className="banner2",
            children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
        ),
    ],
)



# Run the app
if __name__ == '__main__':
    app.run(debug=True)

