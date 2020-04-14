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


@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal_dashboard_domain_selection(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

##Domain 1
@app.callback(
    [Output("collapse-1", "is_open"), Output("collapse-button-1","children")],
    [Input("collapse-button-1", "n_clicks")],
    [State("collapse-1", "is_open")],
)
def toggle_collapse_domain_selection_measures(n, is_open):
    if n and n%2 == 1:
        return not is_open, "Confirm"
    elif n and n%2 == 0:
        return not is_open, "Edit"
    return is_open, "Select"


@app.callback(
    [Output("dashboard-card-domain-selection-1", "color"),
    Output("dashboard-card-selected-domain-1", "children")],
    [Input("checklist-domain-measures-lv1-1", "value"), Input("collapse-button-1", "n_clicks")],
)
def toggle_collapse_domain_selection_measures(v, n):
    if len(v) > 0 and n%2 == 0: 
        return  "info", u"Domain 1 ( {} measures selected) ".format(len(v))
    return "light", ""
    

@app.callback(
    Output("checklist-domain-measures-lv2-container-1", "children"),
    [
        Input("checklist-domain-measures-lv1-1", "value"),
    ],
)
def on_form_change(checklist_value):
    
    checked = len(checklist_value)
    
    if checked > 0:
        return checklist_domain_measures_lv2()
    return ""


##Domain 2
@app.callback(
    [Output("collapse-2", "is_open"), Output("collapse-button-2","children")],
    [Input("collapse-button-2", "n_clicks")],
    [State("collapse-2", "is_open")],
)
def toggle_collapse_domain_selection_measures(n, is_open):
    if n and n%2 == 1:
        return not is_open, "Confirm"
    elif n and n%2 == 0:
        return not is_open, "Edit"
    return is_open, "Select"


@app.callback(
    [Output("dashboard-card-domain-selection-2", "color"),
    Output("dashboard-card-selected-domain-2", "children")],
    [Input("checklist-domain-measures-lv1-2", "value"), Input("collapse-button-2", "n_clicks")],
)
def toggle_collapse_domain_selection_measures(v, n):
    if len(v) > 0 and n%2 == 0: 
        return  "info", u"Domain 2 ( {} measures selected) ".format(len(v))
    return "light", ""
    

@app.callback(
    Output("checklist-domain-measures-lv2-container-2", "children"),
    [
        Input("checklist-domain-measures-lv1-2", "value"),
    ],
)
def on_form_change(checklist_value):
    
    checked = len(checklist_value)
    
    if checked > 0:
        return checklist_domain_measures_lv2()
    return ""



##Domain 3
@app.callback(
    [Output("collapse-3", "is_open"), Output("collapse-button-3","children")],
    [Input("collapse-button-3", "n_clicks")],
    [State("collapse-3", "is_open")],
)
def toggle_collapse_domain_selection_measures(n, is_open):
    if n and n%2 == 1:
        return not is_open, "Confirm"
    elif n and n%2 == 0:
        return not is_open, "Edit"
    return is_open, "Select"


@app.callback(
    [Output("dashboard-card-domain-selection-3", "color"),
    Output("dashboard-card-selected-domain-3", "children")],
    [Input("checklist-domain-measures-lv1-3", "value"), Input("collapse-button-3", "n_clicks")],
)
def toggle_collapse_domain_selection_measures(v, n):
    if len(v) > 0 and n%2 == 0: 
        return  "info", u"Domain 3 ( {} measures selected) ".format(len(v))
    return "light", ""
    

@app.callback(
    Output("checklist-domain-measures-lv2-container-3", "children"),
    [
        Input("checklist-domain-measures-lv1-3", "value"),
    ],
)
def on_form_change(checklist_value):
    
    checked = len(checklist_value)
    
    if checked > 0:
        return checklist_domain_measures_lv2()
    return ""



##Domain 4
@app.callback(
    [Output("collapse-4", "is_open"), Output("collapse-button-4","children")],
    [Input("collapse-button-4", "n_clicks")],
    [State("collapse-4", "is_open")],
)
def toggle_collapse_domain_selection_measures(n, is_open):
    if n and n%2 == 1:
        return not is_open, "Confirm"
    elif n and n%2 == 0:
        return not is_open, "Edit"
    return is_open, "Select"


@app.callback(
    [Output("dashboard-card-domain-selection-4", "color"),
    Output("dashboard-card-selected-domain-4", "children")],
    [Input("checklist-domain-measures-lv1-4", "value"), Input("collapse-button-4", "n_clicks")],
)
def toggle_collapse_domain_selection_measures(v, n):
    if len(v) > 0 and n%2 == 0: 
        return  "info", u"Domain 4 ( {} measures selected) ".format(len(v))
    return "light", ""
    

@app.callback(
    Output("checklist-domain-measures-lv2-container-4", "children"),
    [
        Input("checklist-domain-measures-lv1-4", "value"),
    ],
)
def on_form_change(checklist_value):
    
    checked = len(checklist_value)
    
    if checked > 0:
        return checklist_domain_measures_lv2()
    return ""



##Domain 5
@app.callback(
    [Output("collapse-5", "is_open"), Output("collapse-button-5","children")],
    [Input("collapse-button-5", "n_clicks")],
    [State("collapse-5", "is_open")],
)
def toggle_collapse_domain_selection_measures(n, is_open):
    if n and n%2 == 1:
        return not is_open, "Confirm"
    elif n and n%2 == 0:
        return not is_open, "Edit"
    return is_open, "Select"


@app.callback(
    [Output("dashboard-card-domain-selection-5", "color"),
    Output("dashboard-card-selected-domain-5", "children")],
    [Input("checklist-domain-measures-lv1-5", "value"), Input("collapse-button-5", "n_clicks")],
)
def toggle_collapse_domain_selection_measures(v, n):
    if len(v) > 0 and n%2 == 0: 
        return  "info", u"Domain 5 ( {} measures selected) ".format(len(v))
    return "light", ""
    

@app.callback(
    Output("checklist-domain-measures-lv2-container-5", "children"),
    [
        Input("checklist-domain-measures-lv1-5", "value"),
    ],
)
def on_form_change(checklist_value):
    
    checked = len(checklist_value)
    
    if checked > 0:
        return checklist_domain_measures_lv2()
    return ""



##Domain 6
@app.callback(
    [Output("collapse-6", "is_open"), Output("collapse-button-6","children")],
    [Input("collapse-button-6", "n_clicks")],
    [State("collapse-6", "is_open")],
)
def toggle_collapse_domain_selection_measures(n, is_open):
    if n and n%2 == 1:
        return not is_open, "Confirm"
    elif n and n%2 == 0:
        return not is_open, "Edit"
    return is_open, "Select"


@app.callback(
    [Output("dashboard-card-domain-selection-6", "color"),
    Output("dashboard-card-selected-domain-6", "children")],
    [Input("checklist-domain-measures-lv1-6", "value"), Input("collapse-button-6", "n_clicks")],
)
def toggle_collapse_domain_selection_measures(v, n):
    if len(v) > 0 and n%2 == 0: 
        return  "info", u"Domain 6 ( {} measures selected) ".format(len(v))
    return "light", ""
    

@app.callback(
    Output("checklist-domain-measures-lv2-container-6", "children"),
    [
        Input("checklist-domain-measures-lv1-6", "value"),
    ],
)
def on_form_change(checklist_value):
    
    checked = len(checklist_value)
    
    if checked > 0:
        return checklist_domain_measures_lv2()
    return ""


##Domain 7
@app.callback(
    [Output("collapse-7", "is_open"), Output("collapse-button-7","children")],
    [Input("collapse-button-7", "n_clicks")],
    [State("collapse-7", "is_open")],
)
def toggle_collapse_domain_selection_measures(n, is_open):
    if n and n%2 == 1:
        return not is_open, "Confirm"
    elif n and n%2 == 0:
        return not is_open, "Edit"
    return is_open, "Select"


@app.callback(
    [Output("dashboard-card-domain-selection-7", "color"),
    Output("dashboard-card-selected-domain-7", "children")],
    [Input("checklist-domain-measures-lv1-7", "value"), Input("collapse-button-7", "n_clicks")],
)
def toggle_collapse_domain_selection_measures(v, n):
    if len(v) > 0 and n%2 == 0: 
        return  "info", u"Domain 7 ( {} measures selected) ".format(len(v))
    return "light", ""
    

@app.callback(
    Output("checklist-domain-measures-lv2-container-7", "children"),
    [
        Input("checklist-domain-measures-lv1-7", "value"),
    ],
)
def on_form_change(checklist_value):
    
    checked = len(checklist_value)
    
    if checked > 0:
        return checklist_domain_measures_lv2()
    return ""



if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True, port = 8051)
