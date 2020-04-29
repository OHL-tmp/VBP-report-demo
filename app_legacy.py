#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:36:08 2020

@author: yanchen
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import numpy as np

import pathlib
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from pages import (
    dashboard, launch_page
)


# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/vbc-demo/launch/":
        return launch_page.launch_layout()   
    elif pathname == "/vbc-demo/dashboard/":
        return dashboard.create_layout()
    elif pathname == "/vbc-demo/drilldown/":
        return drilldown.create_layout()
    elif pathname == "/vbc-demo/contract-simulation/":
        return simulation.create_layout()
    elif pathname == "/vbc-demo/metrics-library/":
        return metrics_library.create_layout()
    else:
        return launch_page.launch_layout()

if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=False, port = 8051)
