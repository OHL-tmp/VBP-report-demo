import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
import dash_bootstrap_components as dbc

def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Monitoring Dashboard",
                href="/vbc-demo/monitoring-dashboard",
                className="tab first",
            ),
            dcc.Link(
                "Mornitoring Details",
                href="/vbc-demo/mornitoring-details",
                className="tab",
            ),
            dcc.Link(
                "Contracting Decision Support",
                href="/vbc-dem/contracting-decision-support",
                className="tab",
            ),
            dcc.Link(
                "Measure Inventory", 
                href="/vbc-dem/measure-inventory", 
                className="tab"
            ),
        ],
        className="row all-tabs",
    )
    return menu
    

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

app.layout = html.Div([
   get_menu()
])


if __name__ == "__main__":
    app.run_server(debug=False, port = 8051)