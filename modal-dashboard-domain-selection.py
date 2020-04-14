#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:10:52 2020

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


# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()


app = dash.Dash(__name__, url_base_pathname='/demo-report/', external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server



def modal_dashboard_domain_selection():
    return html.Div(
                [
                    dbc.Button("Open", id="open-centered"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Select Domain"),
                            dbc.ModalBody(
                                card_domain_selection()
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Close", id="close-centered", className="ml-auto"
                                )
                            ),
                        ],
                        id="modal-centered",
                        size='lg',
                        scrollable=True,
                    ),
                ]
            )

def card_domain_selection():
    return dbc.Card(
                [
                    dbc.CardBody(
                        dbc.Row(
                            [
                                
                                dbc.Col(collapse_domain_selection_measures()),
                            ]
                        )
                    ),
                ]
            )

def collapse_domain_selection_measures():
    return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.Div('Domain 1')),
                            dbc.Button(
                                "Open collapse",
                                id="collapse-button",
                                className="mb-3",
                                color="primary",
                            ),
                        ]
                    ),
                    
                    dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Choose Measures", className="card-title"),
                                    checklist_domain_measures_lv1(),
                                    html.Hr(className="my-2"),
                                    html.Div(id="checklist-domain-measures-lv2-container"),
                                ]
                            )
                        ),
                        id="collapse",
                    ),
                ]
            )

def checklist_domain_measures_lv1():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Option 1", "value": 1},
                            {"label": "Option 2", "value": 2},
                            {"label": "Option 3", "value": 3},
                            {"label": "Option 4", "value": 4},
                            {"label": "Option 5", "value": 5},
                            {"label": "Option 6", "value": 6},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv1",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Option 1", "value": 1},
                            {"label": "Option 2", "value": 2},
                            {"label": "Option 3", "value": 3},
                            {"label": "Option 4", "value": 4},
                            {"label": "Option 5", "value": 5},
                            {"label": "Option 6", "value": 6},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv2",
                        inline=True,
                    ),
                ]
            )



app.layout = modal_dashboard_domain_selection()


@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal_dashboard_domain_selection(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse_domain_selection_measures(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("checklist-domain-measures-lv2-container", "children"),
    [
        Input("checklist-domain-measures-lv1", "value"),
    ],
)
def on_form_change(checklist_value):
    
    checked = len(checklist_value)
    
    if checked > 0:
        return checklist_domain_measures_lv2()

    return str(checked)



if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True)
