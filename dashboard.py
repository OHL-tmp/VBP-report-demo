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
                                    "Open collapse",
                                    #id="collapse-button",
                                    className="mb-3",
                                    color="primary",
                                ),
                            ],
                        ),
                        
                    ]
                )
            )

def card_sub1_volumn_based_measures(volumn_measure):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="20%"), width=1, align="start", style={"margin-right":"-20px", "margin-top":"-4px"}),
                                dbc.Col(html.H6(volumn_measure)),
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="20%"), width=1, align="start"),
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
            )


def card_sub2_volumn_based_measures(volumn_measure):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="20%"), width=1, align="start", style={"margin-right":"-20px", "margin-top":"-4px"}),
                                dbc.Col(html.H6(volumn_measure)),
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="20%"), width=1, align="start"),
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
            )


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
                                dbc.Col([dbc.Button("Open collapse", className="mb-3", color="primary")], width=3),
                                dbc.Col(
                                    [
                                     dbc.Button("Open collapse", className="mb-3", color="primary"),
                                     dbc.Button("Open collapse", className="mb-3", color="primary"),
                                     dbc.Button("Open collapse", className="mb-3", color="primary"),
                                    ], 
                                    width="100%",
                                ),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
            )


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
                                html.Img(src=app.get_asset_url("logo-demo.png"), width="100%"),
                                html.Img(src=app.get_asset_url("logo-demo.png"), width="100%"),
                            ]
                        ),
                    ]
                ),
                className="mb-3",
            )


app.layout = create_layout()




if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True)

