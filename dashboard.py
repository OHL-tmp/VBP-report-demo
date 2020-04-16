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
from figure import bargraph_overall,waterfall_overall,tbl_utilizer,piechart_utilizer,bargraph_h,bargraph_stack3,bubblegraph,bargraph_perform

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()


app = dash.Dash(__name__, url_base_pathname='/demo-report/', external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

## load data
df_overall = pd.read_csv("data/overall_performance.csv")
df_waterfall = pd.read_csv("data/overall_waterfall.csv")
df_utilizer= pd.read_csv("data/utilizer_tbl.csv")
df_util_split=pd.read_csv("data/util_split.csv")
df_script_per_util=pd.read_csv("data/script_per_util.csv")
df_tot_script_split=pd.read_csv("data/tot_script_split.csv")
df_tot_unit_split=pd.read_csv("data/tot_unit_split.csv")
df_domain_perform=pd.read_csv("data/domain_perform.csv")
df_measure_perform=pd.read_csv("data/measure_performance.csv")
df_tot_script=pd.DataFrame(df_tot_script_split.sum(axis=0)[1:4,],columns=['tot_script']).iloc[[2,1,0],]
df_tot_unit=pd.DataFrame(df_tot_unit_split.sum(axis=0)[1:4,],columns=['tot_unit']).iloc[[2,1,0],]

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
    bargraph_overall1=bargraph_overall(df_overall['month'],df_overall['base'],df_overall['adjusted'])
    waterfall_overall1=waterfall_overall(df_waterfall['label'] ,df_waterfall['base'], df_waterfall['adjusted'])
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
                                    dbc.Col(dcc.Graph(figure=bargraph_overall1), width=6),
                                    dbc.Col(dcc.Graph(figure=waterfall_overall1), width=6),
                                ],
                            ),
                        ] 
                    ),
                ]
            )

def card_main_volumn_based_measures():
    tbl_utilizer1=tbl_utilizer(df_utilizer)
    piechart_utilizer1=piechart_utilizer(df_util_split['Class'],df_util_split['%'])
    bargraph_script_per_util=bargraph_h(df_script_per_util['avg script'] , df_script_per_util['label'])
    bargraph_tot_script=bargraph_h(df_tot_script['tot_script'] , df_tot_script.index)
    bargraph_tot_script_split=bargraph_stack3(df_tot_script_split['dosage'], df_tot_script_split['YTD'], df_tot_script_split['Annualized'] ,df_tot_script_split['Plan Target'])
    bargraph_tot_unit_split=bargraph_stack3(df_tot_unit_split['dosage'], df_tot_unit_split['YTD'], df_tot_unit_split['Annualized'] ,df_tot_unit_split['Plan Target'])
    bargraph_tot_unit=bargraph_h(df_tot_unit['tot_unit'] , df_tot_unit.index)

    return dbc.Card(
                dbc.CardBody(
                    [
                        html.H2("Volumn Based Measures", className="mb-3",),
                        html.Div(
                            [
                                card_sub2_volumn_based_measures("Utilizer Count and Market Share",tbl_utilizer1,piechart_utilizer1),
                                card_sub1_volumn_based_measures("Avg Script (30-day adj) per Utilizer",bargraph_script_per_util),
                                card_sub2_volumn_based_measures("Total Script Count (30-day adj) by Dosage (in thousand)",bargraph_tot_script,bargraph_tot_script_split),
                                card_sub2_volumn_based_measures("Total Units by Dosage (Mn)",bargraph_tot_unit,bargraph_tot_unit_split),
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

def card_sub1_volumn_based_measures(volumn_measure,fig):
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
                                dbc.Col(dcc.Graph(figure=fig), width="100%"),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
            )


def card_sub2_volumn_based_measures(volumn_measure,fig1,fig2):
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
                                dbc.Col(dcc.Graph(figure=fig1), width=6),
                                dbc.Col(dcc.Graph(figure=fig2), width=6),
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
    bubble_graph_domain=bubblegraph(df_domain_perform['weight'] ,df_domain_perform['performance'] ,df_domain_perform['domain'])
    return dbc.Card(
                dbc.CardBody(
                    [
                       dcc.Graph(figure=bubble_graph_domain)
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
    waterfall_domain=waterfall_overall(df_waterfall['label'] ,df_waterfall['base'], df_waterfall['adjusted'])
    domain_perform=bargraph_perform(df_measure_perform['performance'], df_measure_perform['Measure'])
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
                                dcc.Graph(figure=waterfall_domain),
                                dcc.Graph(figure=domain_perform),
                            ]
                        ),
                    ]
                ),
                className="mb-3",
            )


app.layout = create_layout()




if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True)

