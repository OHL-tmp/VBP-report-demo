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

from modal_drilldown_tableview import *



# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()


app = dash.Dash(__name__, url_base_pathname='/vbc-demo/contract-optimizer/')

server = app.server


def create_layout():
#    load_data()
    return html.Div(
                [ 
                    html.Div([Header_mgmt(app, False, False, True, False)], style={"height":"6rem"}),
                    
                    html.Div(
                        [
                            dbc.Tabs(
							    [
							        dbc.Tab(tab_setup(), label="Contract Simulation Setup"),
							        dbc.Tab(tab_result(), label="Result"),
							        
							    ]
							)
                        ],
                        className="mb-3",
                    ),
                    
                ],
                style={"padding-left":"3rem", "padding-right":"3rem", "background-color":"#f5f5f5"},
            )


def tab_setup():
	return html.Div(
				[
					dbc.Row(
						[
							dbc.Col(html.H1("VBC Contract Simulation Setup/Edit Asumption")),
							dbc.Col(dbc.Button("Edit Assumption"))
						]
					),
					html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(html.H1("Performance Measure Setup", style={"color":"#f0a800", "font-size":"1rem","padding-top":"0.8rem"}), width=9),
                                    
                                ]
                            )
                        ],
                        style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#f7f7f7","margin-top":"2rem"}
                    ),
                    html.Div(
                        [
                        	card_performance_measure_setup(),
                        ]
                    ),
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(html.H1("Performance Measure Setup", style={"color":"#f0a800", "font-size":"1rem","padding-top":"0.8rem"}), width=9),
                                    
                                ]
                            )
                        ],
                        style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#f7f7f7","margin-top":"2rem"}
                    ),
                    html.Div(
                        [
                        	card_contractural_arrangement_setup(),
                        ]
                    ),
					
				]
			)


def card_performance_measure_setup():
	return dbc.Card(
                dbc.CardBody(
                    [
                        card_target_patient(),
                        card_outcome_measure(),
                        card_overall_likelihood_to_achieve(),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def card_target_patient():
	return dbc.Card(
                dbc.CardBody(
                    [
                    	dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Target Patient", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H3("Recommended", style={"font-size":"0.6rem"}),
                                        html.H3("Managing Physician (Group)"),
                                    ], 
                                    style={"padding":"0.8rem"},
                                    width=2,
                                ),
                                dbc.Col(
                                    [
                                        html.H3("User Defined", style={"font-size":"0.6rem"}),
                                        html.Div("------------------"),
                                    ], 
                                    style={"padding":"0.8rem"},
                                    width=2,
                                ),
                            ],
                        ),
                        
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def card_outcome_measure():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Outcome Measure", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(
                                	dbc.Button("Edit Assumption"),
                                    width=4,
                                ),
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.H4("Baseline"),
                                				dbc.Row(
                                					[
                                						dbc.Col("Recommended", width=6),
                                						dbc.Col("User Defined", width=6),
                                					]
                                				)
                                			]
                                		)
                                	],
                                    width=2,
                                ),
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.H4("Target"),
                                				dbc.Row(
                                					[
                                						dbc.Col("Recommended", width=6),
                                						dbc.Col("User Defined", width=6),
                                					]
                                				)
                                			]
                                		)
                                	],
                                    width=2,
                                ),
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.H4("Likelihood to achieve"),
                                				dbc.Row(
                                					[
                                						dbc.Col("Recommended", width=6),
                                						dbc.Col("User Defined", width=6),
                                					]
                                				)
                                			]
                                		)
                                	],
                                    width=2,
                                ),
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.H4("Weight"),
                                				dbc.Row(
                                					[
                                						dbc.Col("Recommended", width=6),
                                						dbc.Col("User Defined", width=6),
                                					]
                                				)
                                			]
                                		)
                                	],
                                    width=2,
                                ),

                            ],

                            
                        ),
                        card_measure_modifier(),
                        card_measure_modifier(),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def card_measure_modifier():
	return dbc.Card(
        		
            	dbc.CardBody(
            		[
            			dbc.Row(
		        			[
		        				dbc.Col("Cost and Utilization Reduction", width=10),
		        				dbc.Col("50"),
		        				dbc.Col("50"),
		        			]
		        		),
		        		html.Hr(className="ml-1"),
            			
            			row_measure_modifier("CHF Related Cost per Patient"),
            			row_measure_modifier("CHF Related Hospitalization Rate"),
            		]
            	),
            )

def row_measure_modifier(measure):
	return dbc.Row(
				[
					dbc.Col(html.Div(measure), width=4),
					dbc.Col(html.Div("4000"), width=1),
					dbc.Col(html.Div("4000"), width=1),
					dbc.Col(html.Div("3500"), width=1),
					dbc.Col(html.Div("900"), width=1),
					dbc.Col(html.Div("Mid"), width=1),
					dbc.Col(html.Div("Low"), width=1),
					dbc.Col(html.Div("25"), width=1),
					dbc.Col(html.Div("25"), width=1),
				]
			)


def card_overall_likelihood_to_achieve():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Outcome Measure", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                dbc.Col(html.Div("High"), width=1),
								dbc.Col(html.Div("Mid"), width=1),
								dbc.Col(html.Div(""), width=2),
                            ],
                            no_gutters=True,
                        ),
                        
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def card_contractural_arrangement_setup():
	return dbc.Card(
                dbc.CardBody(
                    [
                        card_contract_wo_vbc_adjustment(),
                        card_vbc_contract(),
                        card_contract_adjust(),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def card_contract_wo_vbc_adjustment():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Contract without VBC Adjustment", style={"font-size":"1rem", "margin-left":"10px"}), width=4),
                                dbc.Col(html.Div("Rebate"), width=1),
								dbc.Col(html.Div("40%"), width=1),
								dbc.Col(dbc.Button("EDIT Contract Input"), width=2),
                            ],
                            no_gutters=True,
                        ),
                        
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def card_vbc_contract():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("VBC Contract", style={"font-size":"1rem", "margin-left":"10px"}), width=4),
                                dbc.Col(html.Div("Base Rebate"), width=1),
								dbc.Col(html.Div("35%"), width=1),
								dbc.Col(html.Div("Revenue at Risk"), width=1),
								dbc.Col(html.Div("10%"), width=1),
                            ],
                            no_gutters=True,
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def card_contract_adjust():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("simulation_illustration.png"), style={"max-width":"100%","max-height":"100%"}), width=7,),
                                dbc.Col(card_contract_adjust_sub(), width=5)
                            ],
                            no_gutters=True,
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def card_contract_adjust_sub():
	return dbc.Card(
                dbc.CardBody(
                    [
                    	dbc.Col(html.H4("Positive Adjustment", style={"font-size":"1rem", "margin-left":"10px"})),
                    	dbc.Row(
                            [
                                dbc.Col(html.Div(""), width=6),
								dbc.Col(html.Div("Recommended"), width=3),
								dbc.Col(html.Div("User Defined"), width=3),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("Performance Level Threshold"), width=6),
								dbc.Col(html.Div("115%"), width=3),
								dbc.Col(html.Div("115%"), width=3),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("Maximum Positive Adjustment"), width=6),
								dbc.Col(html.Div("10%"), width=3),
								dbc.Col(html.Div("15%"), width=3),
                            ],
                            no_gutters=True,
                        ),

                        html.Hr(className="ml-1"),

                        dbc.Col(html.H4("Negative Adjustment", style={"font-size":"1rem", "margin-left":"10px"})),
                    	dbc.Row(
                            [
                                dbc.Col(html.Div(""), width=6),
								dbc.Col(html.Div("Recommended"), width=3),
								dbc.Col(html.Div("User Defined"), width=3),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("Performance Level Threshold"), width=6),
								dbc.Col(html.Div("85%"), width=3),
								dbc.Col(html.Div("80%"), width=3),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("Maximum Negative Adjustment"), width=6),
								dbc.Col(html.Div("-10%"), width=3),
								dbc.Col(html.Div("-15%"), width=3),
                            ],
                            no_gutters=True,
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def tab_result():
	return html.Div(
				[
					dbc.Row(
						[
							dbc.Col(html.H1("Contract Simulation Result"))
						]
					),
					html.Div(
					    [
					        dbc.Button(
					            "Result 1",
					            id="collapse_button_result_1",
					            className="mb-3",
					            color="primary",
					            block=True,
					        ),
					        dbc.Collapse(
					            collapse_result_1(),
					            id="collapse_result_1",
					        ),
					    ]
					),
					html.Div(
					    [
					        dbc.Button(
					            "Result 2",
					            id="collapse_button_result_2",
					            className="mb-3",
					            color="primary",
					            block=True,
					        ),
					        dbc.Collapse(
					            collapse_result_2(),
					            id="collapse_result_2",
					        ),
					    ]
					),
					html.Div(
					    [
					        dbc.Button(
					            "Result 3",
					            id="collapse_button_result_3",
					            className="mb-3",
					            color="primary",
					            block=True,
					        ),
					        dbc.Collapse(
					            collapse_result_3(),
					            id="collapse_result_3",
					        ),
					    ]
					),
					html.Div(
					    [
					        dbc.Button(
					            "Confounding Factors Needed to be Accounted for in the Contract",
					            id="collapse_button_confounding_factors",
					            className="mb-3",
					            color="primary",
					            block=True,
					        ),
					        dbc.Collapse(
					            collapse_result_3(),
					            id="collapse_confounding_factors",
					        ),
					    ]
					),
					html.Div(
						[
							"",
						],
						style={"height":"2rem"}
					)
				]
			)



def collapse_result_1():
	return dbc.Card(
            	dbc.CardBody(
            		[
            			dbc.Row(
            				[
            					dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6),
            					dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6)
            				]
            			)
            		]
            	)
           	)



def collapse_result_2():
	return dbc.Card(
            	dbc.CardBody(
            		[
            			dbc.Row(
            				[
            					dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6),
            					dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6)
            				]
            			)
            		]
            	)
           	)



def collapse_result_3():
	return dbc.Card(
            	dbc.CardBody(
            		[
            			dbc.Row(
            				[
            					dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6),
            					dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6)
            				]
            			)
            		]
            	)
           	)



def collapse_confounding_factors():
	return dbc.Card(
            	dbc.CardBody(
            		[
            			html.Div(
            				[
            					dbc.Row(
                                    [
                                        dbc.Col(html.H1("All Confounding Factors", style={"color":"#f0a800", "font-size":"1.5rem","padding-top":"1.2rem"}), width=6),
                                        dbc.Col(html.H1("All Confounding Factors", style={"color":"#f0a800", "font-size":"1.5rem","padding-top":"1.2rem"}), width=6),
                                    ]
                                ),
                                html.Img(src=app.get_asset_url("logo-demo.png")),
            				]
            			),
            			dbc.Row(
            				[
            					dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6),
            					dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6)
            				]
            			)
            		]
            	)
           	)




app.layout = create_layout()


@app.callback(
    Output("collapse_result_1", "is_open"),
    [Input("collapse_button_result_1", "n_clicks")],
    [State("collapse_result_1", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse_result_2", "is_open"),
    [Input("collapse_button_result_2", "n_clicks")],
    [State("collapse_result_2", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse_result_3", "is_open"),
    [Input("collapse_button_result_3", "n_clicks")],
    [State("collapse_result_3", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse_confounding_factors", "is_open"),
    [Input("collapse_button_confounding_factors", "n_clicks")],
    [State("collapse_confounding_factors", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True)







