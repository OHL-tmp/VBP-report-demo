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


app = dash.Dash(__name__, url_base_pathname='/demo-report/')

server = app.server



def create_layout():
    return html.Div(
                [
                    html.Div([Header(app)], style={"height":"6rem"}),
                    
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(div_year_to_date_metrics(), width=3),
                                    dbc.Col(div_overall_performance()),
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
                        style={"padding-top":"5rem"},
                    )
                ],
                style={"padding-left":"3rem", "padding-right":"3rem"},
            )

def div_year_to_date_metrics():
    return html.Div(
                [
                    html.H2("Year to Date Metrics", style={"padding-top":"2rem", "font-weight":"lighter", "font-size":"1rem"}),
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
                            html.H3(title, style={"height":"1rem", "font-size":"1rem"}),
                            html.H2(value, style={"height":"2rem"}),
                        ],
                        style={"padding-top":"0.8rem", "padding-bottom":"0.8rem"},
                    )
                ],
                className="mb-3",
                style={"background-color":"#efefef", "border":"none", "border-radius":"0.5rem"}
            )

def div_overall_performance():
    return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.H1("OVERALL PERFORMANCE"), width=9),
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H3("Total Scripts (30-day adjusted)", style={"font-size":"0.5rem", "color":"#fff"}),
                                        html.H2("4000", style={"font-size":"1.5rem", "margin-top":"-5px", "color":"#fff"}),
                                    ],
                                    style={"margin-top":"-16px"}
                                ),
                                style={"height":"3rem", "background-color":"#1357DD", "text-align":"center"},
                            ),
                        ]
                    ),
                    html.P("Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder Placeholder ", style={"color":"#000", "font-size":"0.8rem"}),
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6),
                            dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6),
                        ],
                    ),
                ],
                style={"padding":"1rem", "padding-right":"2rem"},
            )

def card_main_volumn_based_measures():
    return dbc.Card(
                dbc.CardBody(
                    [
                        html.H1("Volumn Based Measures", className="mb-3", style={"font-size":"1.5rem"}),
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
                                    "Edit Measure",
                                    #id="collapse-button",
                                    className="mb-3",
                                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},
                                ),
                            ],
                            style={"text-align":"center"},
                        ),
                        
                    ]
                ),
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
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
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
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
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )


def card_main_value_based_measures():
    return dbc.Card(
                dbc.CardBody(
                    [
                        html.H1("Volumn Based Measures", className="mb-3", style={"font-size":"1.5rem"}),
                        html.Div(
                            [
                                card_overview_value_based_measures(),
                                card_modify_value_based_measures(),
                                card_sub_value_based_measures("Domain 1"),
                            ],
                            className="mb-3",
                        ),
                    ]
                ),
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def card_overview_value_based_measures():
    return dbc.Card(
                dbc.CardBody(
                    [
                        html.Img(src=app.get_asset_url("logo-demo.png"), width="100%")
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )

def card_modify_value_based_measures():
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="20%"), width=1, align="start", style={"margin-right":"-20px", "margin-top":"-4px"}),
                                dbc.Col(html.H6("Domain Detail")),
                                dbc.Col([dbc.Button("Edit Domain", className="mb-3", color="primary", style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},)], width=3),
                            ],
                            no_gutters=True,
                        ),
                        html.Div(
                            [
                                
                                dbc.Button("Open collapseddddddddddd", className="mr-1", style={"background-color":"#fff", "border":"2px solid #1357DD", "border-radius":".5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem", "color":"#1357DD"}),
                                dbc.Button("Open ", className="mr-1", color="primary", style={"background-color":"#fff", "border":"2px solid #1357DD", "border-radius":".5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem", "color":"#1357DD"}),
                                dbc.Button("Open collapse", className="mr-1", color="primary", style={"background-color":"#fff", "border":"2px solid #1357DD", "border-radius":".5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem", "color":"#1357DD"}),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"border":"none", "border-radius":"0.5rem"}
            )


def card_sub_value_based_measures(volumn_measure):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.H6(volumn_measure)),
                                dbc.Col(dbc.Col(dbc.Button("Change Measure", className="mb-3", color="primary", style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"})), width=4),
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
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )


app.layout = create_layout()




if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True)

