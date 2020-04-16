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



def modal_dashboard_domain_selection(n):
    return html.Div(
                [
                    dbc.Button("Open", id="open-centered"),
                    dbc.Button("EDIT", id="open-centered"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader([
                                dbc.Row([
                                     dbc.Col(html.Div("Select Domain")),
#                                    dbc.Card(id = "dashboard-card-selected-domain",
#                                            className="mb-3",),
                                ]),
                            ]),
                            dbc.ModalBody(
                                card_domain_selection(n)
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

def card_domain_selection(n):
    domain_card = []
    for i in range(n):
        card = dbc.Card(
                [
                    dbc.CardBody(
                        dbc.Row(
                            [

                                dbc.Col(collapse_domain_selection_measures(i)),
                            ]
                        )
                    ),
                ],
                id=u"dashboard-card-domain-selection-{}".format(i+1),
                className="mb-3"
            )
        domain_card.append(card)
    return html.Div(domain_card)

def collapse_domain_selection_measures(n):
    return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.Div(u'Domain {}'.format(n+1))),
                            dbc.Card(id = u"dashboard-card-selected-domain-{}".format(n+1),
                                    className="mb-3",
                                    color="info"),
                            dbc.Button(
                                children = "Select",
                                id=u"collapse-button-{}".format(n+1),
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
                                    eval("checklist_domain_measures_lv1_"+str(n+1)+"()"),
                                    html.Hr(className="my-2"),
                                    html.Div(id=u"checklist-domain-measures-lv2-container-{}".format(n+1)),
                                ]
                            )
                        ),
                        id=u"collapse-{}".format(n+1),
                    ),
                ]
            )

#domain 1
def checklist_domain_measures_lv1_1():
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
                        id="checklist-domain-measures-lv1-1",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2_1_1():
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
                        id="checklist-domain-measures-lv2-1",
                        inline=True,
                    ),
                ]
            )

#domain 2
def checklist_domain_measures_lv1_2():
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
                        id="checklist-domain-measures-lv1-2",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2_2_1():
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
                        id="checklist-domain-measures-lv2-2",
                        inline=True,
                    ),
                ]
            )

#domain 3
def checklist_domain_measures_lv1_3():
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
                        id="checklist-domain-measures-lv1-3",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2_3_1():
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
                        id="checklist-domain-measures-lv2-3",
                        inline=True,
                    ),
                ]
            )

#domain 4
def checklist_domain_measures_lv1_4():
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
                        id="checklist-domain-measures-lv1-4",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2_4_1():
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
                        id="checklist-domain-measures-lv2-4",
                        inline=True,
                    ),
                ]
            )

#domain 5
def checklist_domain_measures_lv1_5():
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
                        id="checklist-domain-measures-lv1-5",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2_5_1():
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
                        id="checklist-domain-measures-lv2-5",
                        inline=True,
                    ),
                ]
            )


#domain 6
def checklist_domain_measures_lv1_6():
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
                        id="checklist-domain-measures-lv1-6",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2_6_1():
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
                        id="checklist-domain-measures-lv2-6",
                        inline=True,
                    ),
                ]
            )

#domain 7
def checklist_domain_measures_lv1_7():
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
                        id="checklist-domain-measures-lv1-7",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2_7_1():
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
                        id="checklist-domain-measures-lv2-7",
                        inline=True,
                    ),
                ]
            )


app.layout = modal_dashboard_domain_selection(7)





if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True, port = 8051)
