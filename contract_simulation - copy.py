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

from modal_simulation_measure_selection import *
from contract_calculation import *
from configure_simulation import *

df_sim_rev=pd.read_csv("data/Output_Pharma_Net_Revenue.csv")
df_sim_rebate=pd.read_csv("data/Output_Rebate.csv")
df_factor_doc=pd.read_csv("data/confounding_factors_doc.csv")


# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()


app = dash.Dash(__name__, url_base_pathname='/vbc-demo/contract-optimizer/')

server = app.server

#df_recom_measure = pd.read_csv("data/recom_measure.csv")
df_payor_contract_baseline = pd.read_csv("data/payor_contract_baseline.csv")
df_performance_assumption = pd.read_csv("data/performance_assumption.csv")


positive_measure = ["LVEF LS Mean Change %", "Change in Self-Care Score", "Change in Mobility Score", "DOT", "PDC", "MPR" ]

def create_layout():
#    load_data()
    return html.Div(
                [ 
                    html.Div([Header_mgmt(app, False, False, True, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                    
                    html.Div(
                        [
                            dbc.Tabs(
							    [
							        dbc.Tab(tab_setup(), label="Contract Simulation Setup"),
							        dbc.Tab(tab_result(), label="Result"),
							        
							    ], id = 'tab_container'
							)
                        ],
                        className="mb-3",
                        style={"padding-left":"3rem", "padding-right":"3rem"},
                    ),
                    
                ],
                style={"background-color":"#f5f5f5"},
            )


def tab_setup():
	return html.Div(
				[
					dbc.Row(
						[
							dbc.Col(html.H1("VBC Contract Simulation Setup")),
							dbc.Col([
                                dbc.Button("Edit Assumption", id = 'button-edit-assumption'),
                                dbc.Modal([
                                    dbc.ModalHeader("Edit Assumption"),
                                    dbc.ModalBody("模型需要的其他assumptions"),
                                    dbc.ModalFooter(
                                        dbc.Button("SUBMIT", id = 'close-edit-assumption')
                                        )
                                    ], id = 'modal-edit-assumption'),
                                ]),
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
                                    dbc.Col(html.H1("Contractual Arrangement Setup", style={"color":"#f0a800", "font-size":"1rem","padding-top":"0.8rem"}), width=9),
                                    
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
                    html.Div([
                        dbc.Button("Submit for Simulation", id = 'button-simulation-submit')
                        ]),
                    dcc.Interval(
                        id = 'interval',
                        interval = 1*1000,
                        n_intervals=0)
					
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
                                        html.H5("Class III & IV CHF Patients", id = 'target-patient-recom'),
                                    ], 
                                    style={"padding":"0.8rem"},
                                    width=2,
                                ),
                                dbc.Col(
                                    [
                                        html.H3("Payer Contract", style={"font-size":"0.6rem"}),
                                        html.Div([
                                            dcc.Dropdown(id = 'target-patient-input',
                                                options = [{'label':'All Classes', 'value':'All Classes'},
                                                {'label':'Class III & IV CHF Patients', 'value':'Class III & IV CHF Patients'}],
                                                value = 'All Classes'),
                                            ]),
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
#                                	dbc.Button("Edit Assumption"),
                                    modal_dashboard_domain_selection(domain_ct),
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
                                						dbc.Col("Payer Contract", width=6),
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
                                						dbc.Col("Payer Contract", width=6),
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
                                						dbc.Col("Payer Contract", width=6),
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
                                						dbc.Col("Payer Contract", width=6),
                                					]
                                				)
                                			]
                                		)
                                	],
                                    width=2,
                                ),

                            ],

                            
                        ),
                        card_measure_modifier(domain_ct),
#                        card_measure_modifier(),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def card_measure_modifier(n):
    card_outcome_domain_container = []
    for i in range(n):
        card = html.Div(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(domain_set[i], id = u'outcome-domain-{}'.format(i+1), width=10),
                                            dbc.Col(id = u'outcome-domain-weight-recom-{}'.format(i+1)),
                                            dbc.Col(id = u'outcome-domain-weight-user-{}'.format(i+1)),
                                        ]
                                    ),
                                    html.Hr(className="ml-1"),
                                    row_measure_modifier_combine(i),
                                ]
                            ),
                        ),
                    ], 
                    id = u'outcome-domain-container-{}'.format(i+1),
                    hidden = True
                )

        card_outcome_domain_container.append(card)

    return html.Div(card_outcome_domain_container)


def row_measure_modifier_combine(n):
    card_outcome_measure_container = []
    measures_lv1 = Domain_options[domain_focus[n]]
    key = list(measures_lv1.keys())
    measures_lv2 = []
    for i in range(len(key)):
        for k in measures_lv1[key[i]]:
            measures_lv2 = measures_lv2 + [k]
    for m in range(len(measures_lv2)):
        recom_weight = df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Weight']
        if len(recom_weight) >0:
            recom_weight_pct = '{:.0%}'.format(recom_weight.values[0])
        else:
            recom_weight_pct = ""
        if measures_lv2[m] in dollar_input:
            card = html.Div([
                dbc.Row(
                    [
                        dbc.Col(html.Div(measures_lv2[m], id = 'measure-name-{}-{}'.format(n+1, m+1)), width=4),
                        dbc.Col(html.Div(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Baseline'], id = u'measure-base-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div(df_payor_contract_baseline[df_payor_contract_baseline['Measure'] == measures_lv2[m]]['Baseline'], id = u'measure-base-user-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Target'], id = u'measure-target-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(
                            dcc.Input(id = u'measure-target-user-{}-{}'.format(n+1, m+1), 
                                type = 'number', debounce = True, persistence = True, persistence_type = 'session'), 
                            width=1),
                        dbc.Col(html.Div(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Likelihood'], id = u'measure-like-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div(id = u'measure-like-user-{}-{}'.format(n+1, m+1),style = {"background-color": '#ffffff'}), width=1),
                        dbc.Col(html.Div(recom_weight_pct, id = u'measure-weight-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(
                            dcc.Input(id = u'measure-weight-user-{}-{}'.format(n+1, m+1),
                                type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                min = 0, max = 100), 
                            width=1),
                    ]
                )
                ], id = u"outcome-measure-row-{}-{}".format(n+1,m+1))
        elif measures_lv2[m] in percent_input:
            card = html.Div([
                dbc.Row(
                    [
                        dbc.Col(html.Div(measures_lv2[m], id = 'measure-name-{}-{}'.format(n+1, m+1)), width=4),
                        dbc.Col(html.Div(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Baseline']*100, id = u'measure-base-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div(df_payor_contract_baseline[df_payor_contract_baseline['Measure'] == measures_lv2[m]]['Baseline']*100, id = u'measure-base-user-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Target']*100, id = u'measure-target-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(
                            dcc.Input(id = u'measure-target-user-{}-{}'.format(n+1, m+1), 
                                type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                min = 0, max = 100), 
                            width=1),
                        dbc.Col(html.Div(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Likelihood'], id = u'measure-like-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div(id = u'measure-like-user-{}-{}'.format(n+1, m+1),style = {"background-color": '#ffffff'}), width=1),
                        dbc.Col(html.Div(recom_weight_pct, id = u'measure-weight-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(
                            dcc.Input(id = u'measure-weight-user-{}-{}'.format(n+1, m+1),
                                type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                min = 0, max = 100), 
                            width=1),
                    ]
                )
                ], id = u"outcome-measure-row-{}-{}".format(n+1,m+1))
        else:
            card = html.Div([
    #            row_measure_modifier(measures_lv2[m])
                dbc.Row(
                    [
                        dbc.Col(html.Div(measures_lv2[m], id = 'measure-name-{}-{}'.format(n+1, m+1)), width=4),
                        dbc.Col(html.Div(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Baseline'], id = u'measure-base-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div(df_payor_contract_baseline[df_payor_contract_baseline['Measure'] == measures_lv2[m]]['Baseline'], id = u'measure-base-user-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Target'], id = u'measure-target-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(
                            dcc.Input(id = u'measure-target-user-{}-{}'.format(n+1, m+1), 
                                type = 'number', debounce = True, persistence = True, persistence_type = 'session'), 
                            width=1),
                        dbc.Col(html.Div(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Likelihood'], id = u'measure-like-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div(id = u'measure-like-user-{}-{}'.format(n+1, m+1),style = {"background-color": '#ffffff'}), width=1),
                        dbc.Col(html.Div(recom_weight_pct, id = u'measure-weight-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(
                            dcc.Input(id = u'measure-weight-user-{}-{}'.format(n+1, m+1),
                                type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                min = 0, max = 100), 
                            width=1),
                    ]
                )
                ], id = u"outcome-measure-row-{}-{}".format(n+1,m+1))
        card_outcome_measure_container.append(card)
    return html.Div(card_outcome_measure_container)




def card_overall_likelihood_to_achieve():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Overall likelihood to achieve", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                dbc.Col(html.Div(id = 'overall-like-recom'), width=1),
								dbc.Col(html.Div(id = 'overall-like-user', style = {'background-color' : '#ffffff'}), width=1),
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
								dbc.Col(
                                    dcc.Input(id = 'input-rebate',
                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                        min = 0, max = 100), 
                                    width=1),
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
								dbc.Col(
                                    dcc.Input(id = 'input-base-rebate',
                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                        min = 0, max = 100), 
                                    width=1),
#								dbc.Col(html.Div("Maximum Positive Adjustment"), width=1),
								
#                                dbc.Col(html.Div("Maximum Negative Adjustment"), width=1),
                                
                                dbc.Col(html.Div("Risk Share Method"), width=1),
                                dbc.Col(dcc.Dropdown(options = [
                                        {'label':'Rebate adjustment', 'value':'Rebate adjustment'},
                                        {'label':'Shared savings/loses', 'value':'Shared savings/loses'},
                                        {'label':'Money back', 'value':'Money back'},
                                        {'label':'Formulary upgrade', 'value':'Formulary upgrade'}
                                    ],
                                    value = 'Rebate adjustment'), width=1),
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
								dbc.Col(html.Div("Payer Contract"), width=3),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("Performance Level Threshold"), width=6),
								dbc.Col(html.Div("115%", id = 'recom-pos-perf'), width=3),
								dbc.Col(
                                    dcc.Input(id = 'input-pos-perform',
                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                        min = 100), 
                                     width=3),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("Rebate Adjustment Cap"), width=6),
								dbc.Col(
                                    dcc.Input(id = 'input-max-pos-adj',
                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                        min = 0, max = 100, placeholder = 'input a positive number'), 
                                    width=3),
								dbc.Col(
                                    dcc.Input(id = 'input-pos-adj',
                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                        min = 0, max = 100, placeholder = 'input a positive number'), 
                                     width=3),
                            ],
                            no_gutters=True,
                        ),

                        html.Hr(className="ml-1"),

                        dbc.Col(html.H4("Negative Adjustment", style={"font-size":"1rem", "margin-left":"10px"})),
                    	dbc.Row(
                            [
                                dbc.Col(html.Div(""), width=6),
								dbc.Col(html.Div("Recommended"), width=3),
								dbc.Col(html.Div("Payer Contract"), width=3),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("Performance Level Threshold"), width=6),
								dbc.Col(html.Div("85%", id = 'recom-neg-perf'), width=3),
								dbc.Col(
                                    dcc.Input(id = 'input-neg-perform',
                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                        min = 0, max = 100), 
                                     width=3),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("Rebate Adjustment Cap"), width=6),
								dbc.Col(
                                    dcc.Input(id = 'input-max-neg-adj',
                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                        min = -100, max = 0, placeholder = 'input a negative number'), 
                                    width=3),
								dbc.Col(
                                    dcc.Input(id = 'input-neg-adj',
                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                        min = -100, max = 0, placeholder = 'input a negative number'), 
                                     width=3),
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
                                is_open = True,
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
                                is_open = True,
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
                                is_open = True,
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
					            collapse_confounding_factors(),
					            id="collapse_confounding_factors",
                                is_open = True,
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
            					dbc.Col(html.Div([dcc.Graph(id = 'sim_result_box_1',style={"height":"50vh", "width":"90vh"})]),width=6 ),
            					dbc.Col(html.Div(id = 'sim_result_table_1'), width=6)
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
            					dbc.Col(html.Div([dcc.Graph(id = 'sim_result_box_2',style={"height":"50vh", "width":"90vh"})]),width=6 ),
            					dbc.Col(html.Div(id = 'sim_result_table_2'), width=6)
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
            					dbc.Col([table_factor_doc(df_factor_doc)], width=6),
            					dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6)
            				]
            			)
            		]
            	)
           	)




app.layout = create_layout()

#modal-edit-assumption
@app.callback(
    Output("modal-edit-assumption", "is_open"),
    [Input("button-edit-assumption", "n_clicks"), Input("close-edit-assumption", "n_clicks")],
    [State("modal-edit-assumption", "is_open")],
    )
def toggle_modal_simulation_measure_selection(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#input modal measure
@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
    )
def toggle_modal_simulation_measure_selection(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


def toggle_collapse_domain_selection_measures(n, is_open):
    if n and n%2 == 1:
        return not is_open, "Confirm"
    elif n and n%2 == 0:
        return not is_open, "Edit"
    return is_open, "Edit"

for i in range(domain_ct):
    app.callback(
        [Output(f"collapse-{i+1}", "is_open"), 
         Output(f"collapse-button-{i+1}","children")],
        [Input(f"collapse-button-{i+1}", "n_clicks")],
        [State(f"collapse-{i+1}", "is_open")],
    )(toggle_collapse_domain_selection_measures)


def open_measure_lv2(n, is_open):
    if n:
        return [not is_open]
    return [is_open]

for d in range(len(list(Domain_options.keys()))):
    for i in range(len(list(Domain_options[list(Domain_options.keys())[d]].keys()))):
        app.callback(
            [Output(f"checklist-domain-measures-lv2-container-{d+1}-{i+1}","is_open")],
            [Input(f"measures-lv1-{d+1}-{i+1}","n_clicks")],
            [State(f"checklist-domain-measures-lv2-container-{d+1}-{i+1}","is_open")],
        )(open_measure_lv2)


def sum_selected_measure(v):
    if v and len(v) > 0:
        return "primary", u"{}".format(len(v))
    return "light", ""

for d in range(len(list(Domain_options.keys()))):
    for i in range(len(list(Domain_options[list(Domain_options.keys())[d]].keys()))):
        app.callback(
            [Output(f"dashboard-card-selected-{d+1}-{i+1}", "color"),
            Output(f"dashboard-card-selected-{d+1}-{i+1}", "children")],
            [Input(f"checklist-domain-measures-lv2-{d+1}-{i+1}", "value")],
        )(sum_selected_measure)

## Domain 1
@app.callback(
    [Output("dashboard-card-domain-selection-1", "color"),
    Output("dashboard-card-domain-selection-1", "outline"),
    Output("dashboard-card-selected-domain-1", "children")],
    [Input("checklist-domain-measures-lv2-1-1", "value"),
    Input("checklist-domain-measures-lv2-1-2", "value"),
    Input("checklist-domain-measures-lv2-1-3", "value"),
    Input("checklist-domain-measures-lv2-1-4", "value")],
)
def toggle_collapse_domain_selection_measures_1(v1, v2, v3, v4):
    if v1:
        len1 = len(v1)
    else:
        len1 = 0
    if v2:
        len2 = len(v2)
    else:
        len2 = 0
    if v3:
        len3 = len(v3)
    else:
        len3= 0
    if v4:
        len4 = len(v4)
    else:
        len4= 0
    measure_count = len1 + len2 + len3 + len4
    if measure_count > 0: 
        return  "primary", True, u"{} measures selected".format(measure_count)
    return "light", False, ""    

## Domain 2
@app.callback(
    [Output("dashboard-card-domain-selection-2", "color"),
    Output("dashboard-card-domain-selection-2", "outline"),
    Output("dashboard-card-selected-domain-2", "children")],
    [Input("checklist-domain-measures-lv2-2-1", "value"),
    Input("checklist-domain-measures-lv2-2-2", "value"),
    Input("checklist-domain-measures-lv2-2-3", "value")],
)
def toggle_collapse_domain_selection_measures_2(v1, v2, v3):
    if v1:
        len1 = len(v1)
    else:
        len1 = 0
    if v2:
        len2 = len(v2)
    else:
        len2 = 0
    if v3:
        len3 = len(v3)
    else:
        len3= 0
    measure_count = len1 + len2 +len3
    if measure_count > 0: 
        return  "primary", True, u"{} measures selected".format(measure_count)
    return "light", False, "" 

## Domain 4
@app.callback(
    [Output("dashboard-card-domain-selection-4", "color"),
    Output("dashboard-card-domain-selection-4", "outline"),
    Output("dashboard-card-selected-domain-4", "children")],
    [Input("checklist-domain-measures-lv2-4-1", "value")],
)
def toggle_collapse_domain_selection_measures_4(v1):
    if v1:
        measure_count = len(v1)
    else: 
        measure_count = 0
    if measure_count > 0: 
        return  "primary", True, u"{} measures selected".format(measure_count)
    return "light", False, "" 

## Domain 5
@app.callback(
    [Output("dashboard-card-domain-selection-5", "color"),
    Output("dashboard-card-domain-selection-5", "outline"),
    Output("dashboard-card-selected-domain-5", "children")],
    [Input("checklist-domain-measures-lv2-5-1", "value")],
)
def toggle_collapse_domain_selection_measures_5(v1):
    if v1:
        measure_count = len(v1)
    else: 
        measure_count = 0
    if measure_count > 0: 
        return  "primary", True, u"{} measures selected".format(measure_count)
    return "light", False, "" 

## Domain 6
@app.callback(
    [Output("dashboard-card-domain-selection-6", "color"),
    Output("dashboard-card-domain-selection-6", "outline"),
    Output("dashboard-card-selected-domain-6", "children")],
    [Input("checklist-domain-measures-lv2-6-1", "value")],
)
def toggle_collapse_domain_selection_measures_6(v1):
    if v1:
        measure_count = len(v1)
    else: 
        measure_count = 0
    if measure_count > 0: 
        return  "primary", True, u"{} measures selected".format(measure_count)
    return "light", False, ""   


##update outcome measures - could update-interval
def show_domain_card(color):
    if color == 'primary':
        return [False]
    return [True]

for d in range(domain_ct):
    app.callback(
        [Output(f'outcome-domain-container-{d+1}', 'hidden')],
        [Input(f'dashboard-card-domain-selection-{d+1}', 'color')]
        )(show_domain_card)


#interval-related
def update_user_weight(v):
    ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    m_no = ctx[-1]
    d_no = ctx[-3]
    d_name = domain_no[d_no]
    m_name = domain_to_measure[d_name][m_no-1]
    try:
        selected_measure[m_name][-1] = v
        return [False]
    except:
        return [False]    

for d in range(domain_ct):
    for m in range(domain_measure[domain_set[d]]):
        app.callback(
            Output(f'measure-weight-user-{d+1}-{m+1}', 'disabled'),
            [Input(f'measure-weight-user-{d+1}-{m+1}', 'value')]
            )(update_user_weight)

def update_user_target(v):
    ctx = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    m_no = ctx[-1]
    d_no = ctx[-3]
    d_name = domain_no[d_no]
    m_name = domain_to_measure[d_name][m_no-1]
    try:
        if m_name in percent_input:
            selected_measure[m_name][4] = v/100
        else:
            selected_measure[m_name][4] = v
        return [False]
    except:
        return [False]    

for d in range(domain_ct):
    for m in range(domain_measure[domain_set[d]]):
        app.callback(
            Output(f'measure-target-user-{d+1}-{m+1}', 'disabled'),
            [Input(f'measure-target-user-{d+1}-{m+1}', 'value')]
            )(update_user_target)


@app.callback(
    [Output(f'outcome-domain-weight-user-{i+1}', 'children') for i in range(domain_ct)]
    +[Output(f'outcome-domain-weight-recom-{i+1}', 'children') for i in range(domain_ct)]
    +[Output('overall-like-recom', 'children'), Output('overall-like-user', 'children')],
    [Input('interval', 'n_intervals')]
    )
def auto_update(n_interval):
    result = []
    for i in range(domain_ct):
        result.append('{:.0%}'.format(sum([v[-1] for k,v in selected_measure.items() if k in  domain_to_measure[domain_no[i+1]]])/100))
    for i in range(domain_ct):
        result.append('{:.0%}'.format(sum([v[-2] for k,v in selected_measure.items() if k in  domain_to_measure[domain_no[i+1]]])))

    re_like = np.mean([v[4] for k,v in selected_measure.items()])
    if re_like <= 1.5:
        result.append('Low')
    elif re_like <= 2.5:
        result.append('Mid')
    elif re_like > 2.5:
        result.append('High')
    else:
        result.append('')

    ur_like = np.mean([v[-3] for k,v in selected_measure.items()])
    if ur_like <= 1.5:
        result.append('Low')
    elif ur_like <= 2.5:
        result.append('Mid')
    elif ur_like > 2.5:
        result.append('High')
    else:
        result.append('')
    return tupple(result)

def cal_measure_likelihood(recom_like, recom_target, user_target, measure, h):
    if h == False:
        if user_target:
            if recom_like[0] == 'High':
                rl = 3
            elif recom_like[0] == 'Mid':
                rl = 2
            else:
                rl = 1
            
            if measure in positive_measure:
                if (user_target-recom_target[0])/recom_target[0] > 0.05:
                    ul = rl -1
                elif (user_target-recom_target[0])/recom_target[0] < -0.05:
                    ul = rl +1
                else:
                    ul = rl
            else:
                if (user_target-recom_target[0])/recom_target[0] > 0.05:
                    ul = rl +1
                elif (user_target-recom_target[0])/recom_target[0] < -0.05:
                    ul = rl -1
                else:
                    ul = rl

            if ul <= 1:
                selected_measure[measure][-3]=1
                return ['Low',{"background-color": '#C00000'}]
            elif ul == 2:
                selected_measure[measure][-3]=2
                return ['Mid',{"background-color": '#ffffff'}]
            else:
                selected_measure[measure][-3]=3
                return ['High',{"background-color": '#ffffff'}]
        return ['',{"background-color": '#ffffff'}]
    return ['',{"background-color": '#ffffff'}]

for d in range(domain_ct):
    for m in range(domain_measure[domain_set[d]]):
        app.callback(
            [Output(f'measure-like-user-{d+1}-{m+1}', 'children'),
            Output(f'measure-like-user-{d+1}-{m+1}', 'style')],
            [Input(f'measure-like-recom-{d+1}-{m+1}', 'children'),
            Input(f'measure-target-recom-{d+1}-{m+1}', 'children'),
            Input(f'measure-target-user-{d+1}-{m+1}', 'value'),
            Input(f'measure-name-{d+1}-{m+1}', 'children'),
            Input(f'outcome-measure-row-{d+1}-{m+1}', 'hidden')]
            )(cal_measure_likelihood)


def show_measure_row(measure):
    if measure in list(selected_measure.keys()):
        return False
    return True

for d in range(domain_ct):
    for m in range(domain_measure[domain_set[d]]):
        app.callback(
            [Output(f'outcome-measure-row-{d+1}-{m+1}', 'hidden')],
            [Input(f'measure-name-{d+1}-{m+1}', 'children')]
            )(show_measure_row)


if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True, port=8052)







