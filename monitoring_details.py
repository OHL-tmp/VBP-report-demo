#!/usr/bin/env python3

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
from utils import *
from figure import *


# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()


app = dash.Dash(__name__, url_base_pathname='/vbc-demo/monitor/')

server = app.server

def create_layout():
#    load_data()
    return html.Div(
                [ 
                    html.Div([Header_mgmt(app)], style={"height":"6rem"}),
                    
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(html.Div(
		                                    	[
		                                    		col_menu_drilldown(),
		                                    	]
		                                    ),
                                   		width=3),
                                    dbc.Col(col_content_drilldown(), width=9),
                                ]
                            ),
                        ],
                        className="mb-3",
                    ),
                    
                ],
                style={"padding-left":"3rem", "padding-right":"3rem", "background-color":"#f5f5f5"},
            )


def col_menu_drilldown():

	return html.Div(
				[
					card_menu_volumn_based_measure(),
					card_menu_outcome_based_measure(),
				]
			)


def card_menu_volumn_based_measure():
	return html.Div(
			[
				dbc.Card(
					[
						dbc.CardBody(
							[
								html.H2("Volume Based Measure"),
								html.H4("Volume Based Measure"),
								html.H4("Volume Based Measure"),
								html.H4("Volume Based Measure"),
							]
						)
					],
					className="mr-3",
					style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
				)
			],
			style={"padding-top":"1rem", "padding-bottom":"1rem"}
		)

def card_menu_outcome_based_measure():
	return html.Div(
			[
				dbc.Card(
					[
						dbc.CardBody(
							[
								html.H2("Outcome Based Measure"),
								html.H4("Outcome Based Measure"),
								html.H4("Outcome Based Measure"),
								html.H4("Outcome Based Measure"),
							]
						)
					],
					className="mr-3",
					style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
				)
			],
			style={"padding-top":"1rem", "padding-bottom":"1rem"}
		)



def col_content_drilldown():
	return html.Div(
			[
				dbc.Row(
					[
						dbc.Col(card_overview_drilldown()),
						dbc.Col(card_key_driver_drilldown()),
					]
				),
				card_confounding_factors(),
				card_graph1_performance_drilldown(),
				card_graph2_performance_drilldown(),
				card_table1_performance_drilldown(),
				card_table2_performance_drilldown(),
			]
		)


def card_overview_drilldown():
	return html.Div(
			[
				dbc.Row(
                        [
                            dbc.Col(html.H1("Average Episode Cost"), width="auto"),
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H3("worse than target", style={"font-size":"0.5rem", "color":"#fff"}),
                                        html.H2("8%", style={"font-size":"1.5rem", "margin-top":"-5px", "color":"#fff"}),
                                    ],
                                    style={"margin-top":"-16px"}
                                ),
                                style={"height":"3rem", "background-color":"#1357DD", "text-align":"center"},
                            ),
                        ]
                    ),
                    html.P("As of June 30th.", style={"color":"#000", "font-size":"0.8rem"}),
                    dbc.Row(
                        [
                            html.Img(src=app.get_asset_url("logo-demo.png")),
                        ],
                    ),
                ],
		)


def card_key_driver_drilldown():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
		                        dbc.Col(html.H4("Key Dribvers", style={"font-size":"1rem", "margin-left":"10px"})),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=6),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=6),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=6),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=6),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=6),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem"}
            )



def card_confounding_factors():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Confounding Factors Unaccounted for in the Contract", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=3),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=3),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=3),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=3),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def card_graph1_performance_drilldown():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Performance Drilldown by Patient Cohort: By Comorbidity Type", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"max-height":"80rem"})),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def card_graph2_performance_drilldown():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Performance Drilldown by Provider: By Physician Group", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"max-height":"80rem"})),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )



def card_table1_performance_drilldown():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Performance by Drilldown Service Categories", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"max-height":"80rem"})),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )



def card_table2_performance_drilldown():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Service Category Drilldown: By Condition", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"max-height":"80rem"})),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )



app.layout = create_layout()


if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True)









