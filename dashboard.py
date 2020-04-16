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
from utils import Header, make_dash_table


# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()


app = dash.Dash(__name__, url_base_pathname='/demo-report/', external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(__name__,  url_base_pathname='/demo-report/', external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server



def create_layout():
    return html.Div(
                [
                    html.Div([Header(app)], style={"height":"150px"}),
                    
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(jumbotron_year_to_date_metrics(), width=3),
                                    dbc.Col(jumbotron_overall_performance()),
                                ]
                            ),
                        ],
                        className="mb-3",
                    ),
                    
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(card_main_volumn_based_measures()),
                                    dbc.Col(card_main_value_based_measures()),
                                ]
                            ),
                        ],
                        className="mb-3",
                    )
                ],
                style={"padding-left":"50px", "padding-right":"50px"},
            )

def jumbotron_year_to_date_metrics():
    return html.Div(
                [
                    html.H5("Year to Date Metrics", style={"padding":"20px"}),
                    card_year_to_date_metrics("Total Patients", "1,000"),
                    card_year_to_date_metrics("Total Gross Scripts", "3,000"),
                    card_year_to_date_metrics("Total Scripts(30-day adjusted)", "4,000"),
                    card_year_to_date_metrics("Total Units(Tablets)", "120,000"),
                ],
                className="mb-3",
                style={"text-align":"center"},
            )


def card_year_to_date_metrics(title, value):
    return dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.P(title, style={"height":"10px"}),
                            html.H2(value, style={"height":"30px"}),
                        ],
                        style={"padding-top":"10px", "padding-bottom":"10px"},
                    )
                ],
                className="mb-3",
            )

def jumbotron_overall_performance():
    return html.Div(
                [
                    dbc.Jumbotron(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(html.H2("OVERALL PERFORMANCE")),
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.H6("Total Scripts(30-day adjusted)")),
                                                        dbc.Col(html.H2("4000")),
                                                    ]
                                                ),
                                            ],
                                            style={"padding-top":"8px", "padding-bottom":"8px"},
                                        ),
                                        style={"width": "30%"},
                                    ),
                                ]
                            ),
                            html.P("Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder "),
                            dbc.Row(
                                [
                                    dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6),
                                    dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6),
                                ],
                            ),
                        ] 
                    ),
                ]
            )

def card_main_volumn_based_measures():
    return dbc.Card(
                dbc.CardBody(
                    [
                        html.H2("Volumn Based Measures", className="mb-3",),
                        html.Div(
                            [
                                card_sub2_volumn_based_measures("Utilizer Count and Market Share"),
                                card_sub1_volumn_based_measures("Avg Script (30-day adj) per Utilizer"),
                                card_sub2_volumn_based_measures("Total Script Count (30-day adj) by Dosage (in thousand)"),
                                card_sub2_volumn_based_measures("Total Units by Dosage (Mn)"),
                            ],
                            className="mb-3",
                        ),
                        html.Div(
                            [
                                dbc.Button(
                                    "Edit",
                                    id="button-add-measure",
                                    className="mb-3",
                                    color="primary",
                                ),
                                dbc.Popover([
                                    dbc.PopoverHeader("Eidt Measures"),
                                    dbc.PopoverBody([
                                        dbc.Checklist(
                                            options = [{'label':"Utilizer Count and Market Share" , 'value':"Utilizer Count and Market Share" },
                                                      {'label':"Avg Script (30-day adj) per Utilizer" , 'value':"Avg Script (30-day adj) per Utilizer" },
                                                      {'label':"Total Script Count (30-day adj) by Dosage (in thousand)" , 'value':"Total Script Count (30-day adj) by Dosage (in thousand)" },
                                                      {'label':"Total Units by Dosage (Mn)", 'value': "Total Units by Dosage (Mn)"},],
                                            value = ["Utilizer Count and Market Share","Avg Script (30-day adj) per Utilizer","Total Script Count (30-day adj) by Dosage (in thousand)","Total Units by Dosage (Mn)"],
                                            labelCheckedStyle={"color": "red"},
                                            id = "checklist-add-measure"),
                                        dbc.Button("ADD", id = "add-button-add-measure")
                                    ]),
                                ],
                                id = "popover-add-measure",
                                is_open = False,
                                target = "button-add-measure",
                                placement = "top"),
                            ],
                        ),
                        
                    ]
                )
            )

def card_sub1_volumn_based_measures(volumn_measure):
    return html.Div([
        dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="20%"), width=1, align="start", style={"margin-right":"-20px", "margin-top":"-4px"}),
                                dbc.Col(html.H6(volumn_measure)),
    #                            dbc.Button([
    #                                "Close"
    #                            ], id = u"close-button-{}".format(volumn_measure),color = "light",size = "sm"),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), width="100%")),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
            )], id = u"card-container-{}".format(volumn_measure))


def card_sub2_volumn_based_measures(volumn_measure):
    return html.Div([
        dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="20%"), width=1, align="start", style={"margin-right":"-20px", "margin-top":"-4px"}),
                                dbc.Col(html.H6(volumn_measure)),
#                                dbc.Button([
#                                    "Close"
#                                ], id = u"close-button-{}".format(volumn_measure),color = "light",size = "sm"),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), width="100%"), width=6),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), width="100%"), width=6),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
            )], id = u"card-container-{}".format(volumn_measure))


def card_main_value_based_measures():
    return dbc.Card(
                dbc.CardBody(
                    [
                        html.H2("Volumn Based Measures", className="mb-3",),
                        html.Div(
                            [
                                card_overview_value_based_measures(),
                                card_modify_value_based_measures("Domain 1"),
                                card_sub_value_based_measures("Domain 1"),
                            ],
                            className="mb-3",
                        ),
                    ]
                )
            )

def card_overview_value_based_measures():
    return dbc.Card(
                dbc.CardBody(
                    [
                        html.Img(src=app.get_asset_url("logo-demo.png"), width="100%")
                    ]
                ),
                className="mb-3",
            )


def card_modify_value_based_measures(volumn_measure):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="20%"), width=1, align="start", style={"margin-right":"-20px", "margin-top":"-4px"}),
                                dbc.Col(html.H6(volumn_measure)),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
               #                 dbc.Col([dbc.Button("Open collapse", className="mb-3", color="primary")], width=3),
                                dbc.Col(modal_dashboard_domain_selection(7)),
                                dbc.Col(
                                    [
                                     card_buttonGroup_domain_selected(),
                                    ], 
                                    width="100%",
                                ),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
            )

def card_buttonGroup_domain_selected():
    return dbc.Card(
            dbc.CardBody([
                html.Div([dbc.Button("Domain 1", 
                                  id = "button-domain-1")],
                         id = "buttonGroup-domain-selected-1",
                         hidden = True),
                html.Div([dbc.Button("Domain 2", 
                                  id = "button-domain-2")],
                         id = "buttonGroup-domain-selected-2",
                         hidden = True),
                html.Div([dbc.Button("Domain 3", 
                                  id = "button-domain-3")],
                         id = "buttonGroup-domain-selected-3",
                         hidden = True),
                html.Div([dbc.Button("Domain 4", 
                                  id = "button-domain-4")],
                         id = "buttonGroup-domain-selected-4",
                         hidden = True),
                html.Div([dbc.Button("Domain 5", 
                                  id = "button-domain-5")],
                         id = "buttonGroup-domain-selected-5",
                         hidden = True),
                html.Div([dbc.Button("Domain 6", 
                                  id = "button-domain-6")],
                         id = "buttonGroup-domain-selected-6",
                         hidden = True),
                html.Div([dbc.Button("Domain 7", 
                                  id = "button-domain-7")],
                         id = "buttonGroup-domain-selected-7",
                         hidden = True),
            ],
            style = {"display": "flex"}),
            className="mb-3")


def card_sub_value_based_measures(volumn_measure):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.H6(volumn_measure)),
                                dbc.Col(dbc.Col(dbc.Button("Open collapse", className="mb-3", color="primary")), width=3),
                            ],
                        ),
                        html.Div(
                            [
                                dcc.Graph(id = "graph-container-domain-selected-1"),
                                dcc.Graph(id = "graph-container-domain-selected-2"),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
            )

app.layout = create_layout()


# add measure popover
@app.callback(
    Output("popover-add-measure","is_open"),
    [Input("button-add-measure","n_clicks"),
    Input("add-button-add-measure","n_clicks"),],
    [State("popover-add-measure", "is_open")],
)
def toggle_popover_add_measure(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open




# add/close measure card

states = {"Utilizer Count and Market Share": True, 
      "Avg Script (30-day adj) per Utilizer": True,
     "Total Script Count (30-day adj) by Dosage (in thousand)": True,
     "Total Units by Dosage (Mn)": True}

@app.callback(
    [Output("card-container-Utilizer Count and Market Share","hidden"),
    Output("card-container-Avg Script (30-day adj) per Utilizer","hidden"),
    Output("card-container-Total Script Count (30-day adj) by Dosage (in thousand)","hidden"),
    Output("card-container-Total Units by Dosage (Mn)","hidden"),],
    [Input("add-button-add-measure","n_clicks"),
    Input("checklist-add-measure","value")],
    [State("card-container-Utilizer Count and Market Share","hidden"),
    State("card-container-Avg Script (30-day adj) per Utilizer","hidden"),
    State("card-container-Total Script Count (30-day adj) by Dosage (in thousand)","hidden"),
    State("card-container-Total Units by Dosage (Mn)","hidden"),],
)
def add_close_measure_card( ad, v, h1, h2, h3, h4):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    edit = len([1 for i in triggered if i == "add-button-add-measure.n_clicks"])
    checked = v
    if edit:
        for p in ["Utilizer Count and Market Share", 
              "Avg Script (30-day adj) per Utilizer",
             "Total Script Count (30-day adj) by Dosage (in thousand)",
             "Total Units by Dosage (Mn)"]:
            if p in checked:
                states[p] = False
            else:
                states[p] = True
        return states["Utilizer Count and Market Share"], states["Avg Script (30-day adj) per Utilizer"],states["Total Script Count (30-day adj) by Dosage (in thousand)"],states["Total Units by Dosage (Mn)"]
    return h1, h2, h3, h4


# generate selected domain button

def generate_card_domain_button(d):
    if d:
        return False
    return True

for i in range(7):
    app.callback(
        Output(f"buttonGroup-domain-selected-{i+1}", "hidden"),
        [Input(f"dashboard-card-selected-domain-{i+1}", "children")]
    )(generate_card_domain_button)

    

# generate domain-related graph
@app.callback(
    [Output("graph-container-domain-selected-1", "figure"),
    Output("graph-container-domain-selected-2", "figure")],
    [Input("button-domain-1", "n_clicks"),
    Input("button-domain-2", "n_clicks"),
    Input("button-domain-3", "n_clicks"),
    Input("button-domain-4", "n_clicks"),
    Input("button-domain-5", "n_clicks"),
    Input("button-domain-6", "n_clicks"),
    Input("button-domain-7", "n_clicks")]
)
def generate_domain_related_graph(b1, b2, b3, b4, b5, b6, b7):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    fig1 = {}
    fig2 = {}
    if button_id == "button-domain-1":
        fig1 = fig1_1
        fig2 = fig2_1
    elif button_id == "button-domain-2":
        fig1 = fig1_2
        fig2 = fig2_2
    elif button_id == "button-domain-3":
        fig1 = fig1_3
        fig2 = fig2_3
    elif button_id == "button-domain-4":
        fig1 = fig1_4
        fig2 = fig2_4
    elif button_id == "button-domain-5":
        fig1 = fig1_5
        fig2 = fig2_5
    elif button_id == "button-domain-6":
        fig1 = fig1_6
        fig2 = fig2_6
    elif button_id == "button-domain-7":
        fig1 = fig1_7
        fig2 = fig2_7
    
    return fig1, fig2

## modal
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
    app.run_server(host="127.0.0.1",debug=True)

