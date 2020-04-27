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

df_sim_rev=pd.read_csv("data/Output_Pharma_Net_Revenue.csv")
df_sim_rebate=pd.read_csv("data/Output_Rebate.csv")
df_factor_doc=pd.read_csv("data/confounding_factors_doc.csv")


# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()

#modebar display
button_to_rm=['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverClosestCartesian','hoverCompareCartesian','hoverClosestGl2d', 'hoverClosestPie', 'toggleHover','toggleSpikelines']


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
        if m in dollar_input:
            card = html.Div([
                dbc.Row(
                    [
                        dbc.Col(html.Div(measures_lv2[m]), width=4),
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
        elif m in percent_input:
            card = html.Div([
                dbc.Row(
                    [
                        dbc.Col(html.Div(measures_lv2[m]), width=4),
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
								dbc.Col(html.Div("Maximum Positive Adjustment"), width=1),
								dbc.Col(
                                    dcc.Input(id = 'input-max-pos-adj',
                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                        min = 0, max = 100, placeholder = 'input a positive number'), 
                                    width=1),
                                dbc.Col(html.Div("Maximum Negative Adjustment"), width=1),
                                dbc.Col(
                                    dcc.Input(id = 'input-max-neg-adj',
                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                        min = -100, max = 0, placeholder = 'input a negative number'), 
                                    width=1),
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
                                dbc.Col(html.Div("Maximum Positive Adjustment"), width=6),
								dbc.Col(html.Div(id = 'recom-max-pos-adj'), width=3),
								dbc.Col(
                                    dcc.Input(id = 'input-pos-adj',
                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                        min = 0), 
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
                                dbc.Col(html.Div("Maximum Negative Adjustment"), width=6),
								dbc.Col(html.Div(id = 'recom-max-neg-adj'), width=3),
								dbc.Col(
                                    dcc.Input(id = 'input-neg-adj',
                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                        max = 0), 
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
					            collapse_confounding_factors(),
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
            					dbc.Col(html.Div([dcc.Graph(id = 'sim_result_box_1',style={"height":"50vh", "width":"90vh"},config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,})]),width=6 ),
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
            					dbc.Col(html.Div([dcc.Graph(id = 'sim_result_box_2',style={"height":"50vh", "width":"90vh"},config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,})]),width=6 ),
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

#link to model

@app.callback(
    [Output('tab_container', 'active_tab'),
    Output('sim_result_box_1','figure'),
    Output('sim_result_table_1','children'),
    Output('sim_result_box_2','figure'),
    Output('sim_result_table_2','children')],
    [Input('button-simulation-submit', 'n_clicks'),
    Input('recom-pos-perf','children'),
    Input('recom-neg-perf','children'),
    Input('recom-max-pos-adj','children'),
    Input('recom-max-neg-adj','children'),
    Input('input-pos-perform', 'value'),
    Input('input-neg-perform', 'value'),
    Input('input-pos-adj', 'value'),
    Input('input-neg-adj', 'value'),
    Input('target-patient-recom','children'),
    Input('target-patient-input','value'),
    Input('input-rebate','value'),
    Input('input-base-rebate','value'),]
    + [Input('measure-name-1-2', 'children'),
    Input('measure-name-1-6', 'children'),
    Input('measure-name-2-1', 'children'),
    Input('measure-name-2-2', 'children'),]
    +[Input('measure-target-user-1-2', 'value'),
    Input('measure-target-user-1-6', 'value'),
    Input('measure-target-user-2-1', 'value'),
    Input('measure-target-user-2-2', 'value'),]
    +[Input('measure-weight-user-1-2', 'value'),
    Input('measure-weight-user-1-6', 'value'),
    Input('measure-weight-user-2-1', 'value'),
    Input('measure-weight-user-2-2', 'value'),]
#    + [Input(f'outcome-measure-row-1-{m+1}', 'hidden') for m in range(8)]
#    + [Input(f'outcome-measure-row-2-{m+1}', 'hidden') for m in range(10)]
#    + [Input(f'outcome-measure-row-4-{m+1}', 'hidden') for m in range(2)]
#    + [Input(f'outcome-measure-row-5-{m+1}', 'hidden') for m in range(3)]
#    + [Input(f'outcome-measure-row-6-{m+1}', 'hidden') for m in range(4)]
#    + [Input(f'measure-name-1-{m+1}', 'children') for m in range(8)]
#    + [Input(f'measure-name-2-{m+1}', 'children') for m in range(10)]
#    + [Input(f'measure-name-4-{m+1}', 'children') for m in range(2)]
#    + [Input(f'measure-name-5-{m+1}', 'children') for m in range(3)]
#    + [Input(f'measure-name-6-{m+1}', 'children') for m in range(4)]
#    + [Input(f'measure-target-user-1-{m+1}', 'value') for m in range(8)]
#    + [Input(f'measure-target-user-2-{m+1}', 'value') for m in range(10)]
#    + [Input(f'measure-target-user-4-{m+1}', 'value') for m in range(2)]
#    + [Input(f'measure-target-user-5-{m+1}', 'value') for m in range(3)]
#    + [Input(f'measure-target-user-6-{m+1}', 'value') for m in range(4)]
#    + [Input(f'measure-weight-user-1-{m+1}', 'value') for m in range(8)]
#    + [Input(f'measure-weight-user-2-{m+1}', 'value') for m in range(10)]
#    + [Input(f'measure-weight-user-4-{m+1}', 'value') for m in range(2)]
#    + [Input(f'measure-weight-user-5-{m+1}', 'value') for m in range(3)]
#    + [Input(f'measure-weight-user-6-{m+1}', 'value') for m in range(4)]
    )
#def simulation(submit_button, re_pos_perf, re_neg_perf, re_pos_adj, re_neg_adj, in_pos_perf, in_neg_perf, in_pos_adj, in_neg_adj, cohort_recom, cohort_selected, rebate_novbc, rebate_vbc,
# h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12,h13,h14,h15,h16,h17,h18,h19,h20,h21,h22,h23,h24,h25,h26,h27,
# m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,m22,m23,m24,m25,m26,m27,
# t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24,t25,t26,t27,
# w1,w2,w3,w4,w5,w6,w7,w8,w9,w10,w11,w12,w13,w14,w15,w16,w17,w18,w19,w20,w21,w22,w23,w24,w25,w26,w27):
def simulation(submit_button, re_pos_perf, re_neg_perf, re_pos_adj, re_neg_adj, in_pos_perf, in_neg_perf, in_pos_adj, in_neg_adj, cohort_recom, cohort_selected, rebate_novbc, rebate_vbc,
    m1,m2,m3,m4,t1,t2,t3,t4,w1,w2,w3,w4):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    submit = len([1 for i in triggered if i == "button-simulation-submit.n_clicks"])
    if submit:
        input1 = {'Perf_Range_U_Min': [1], 
                    'Perf_Range_U_Max': [float(re_pos_perf[:-1])/100], 
                    'Adj_Limit_U': [float(re_pos_adj[:-1])/100],
                    'Perf_Range_L_Min': [1],
                    'Perf_Range_L_Max': [float(re_neg_perf[:-1])/100],
                    'Adj_Limit_L': [float(re_neg_adj[:-1])/100]} 
        Recom_Contract = pd.DataFrame(input1, columns = ['Perf_Range_U_Min','Perf_Range_U_Max','Adj_Limit_U','Perf_Range_L_Min','Perf_Range_L_Max', 'Adj_Limit_L'])
        
#        selected_measure = []
        measure_name = [m1,m2,m3,m4]
        target_list = [t1,t2,t3,t4]
        weight_list = [w1,w2,w3,w4]
#        for i in range(27):
#            if eval('h'+str(i+1)) ==False:
#                selected_measure.append(i+1)
#        for k in selected_measure:
#            measure_name.append(eval('m'+str(i+1)))
#            target_list.append(eval('t'+str(i+1)))
#            weight_list.append(eval('w'+str(i+1)))
        
#        print(selected_measure,measure_name,target_list,weight_list)
        input2 = {'Measure': measure_name, 
                'Target': target_list, 
                'Weight': list(np.array(weight_list)/100)} 
        UD_Measure = pd.DataFrame(input2, columns = ['Measure', 'Target', 'Weight']) 
        UD_Measure['Target'] = UD_Measure.apply(lambda x: x['Target']/100 if x['Measure'] in percent_input else x['Target'], axis = 1)

        input3 = {'Perf_Range_U_Min': [1], 
                        'Perf_Range_U_Max': [in_pos_perf/100], 
                        'Adj_Limit_U': [in_pos_adj/100],
                        'Perf_Range_L_Min': [1],
                        'Perf_Range_L_Max': [in_neg_perf/100],
                        'Adj_Limit_L': [in_neg_adj/100]} 
        UD_Contract = pd.DataFrame(input3, columns = ['Perf_Range_U_Min','Perf_Range_U_Max','Adj_Limit_U','Perf_Range_L_Min','Perf_Range_L_Max', 'Adj_Limit_L']) 

        if cohort_selected == cohort_recom:
            cohort = Recom_Pt_cohort
        else:
            cohort = 'Cohort2'

        t1,t2=Contract_Calculation(Recom_Contract, UD_Measure,UD_Contract,cohort,rebate_novbc/100, rebate_vbc/100)
        t1.reset_index(inplace = True)
        t2.reset_index(inplace = True)

        return 'tab-1',sim_result_box(t1),table_sim_result(t1),sim_result_box(t2),table_sim_result(t2)
    return 'tab-0',{},[],{},[]



#input
@app.callback(
    Output("modal-edit-assumption", "is_open"),
    [Input("button-edit-assumption", "n_clicks"), Input("close-edit-assumption", "n_clicks")],
    [State("modal-edit-assumption", "is_open")],
    )
def toggle_modal_simulation_measure_selection(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

##input likelihood

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
                return ['Low',{"background-color": '#C00000'}]
            elif ul == 2:
                return ['Mid',{"background-color": '#ffffff'}]
            else:
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

@app.callback(
    Output('overall-like-recom', 'children'),
    [Input(f'measure-like-recom-1-{m+1}', 'children') for m in range(8)]
    + [Input(f'measure-like-recom-2-{m+1}', 'children') for m in range(10)]
    + [Input(f'measure-like-recom-4-{m+1}', 'children') for m in range(2)]
    + [Input(f'measure-like-recom-5-{m+1}', 'children') for m in range(3)]
    + [Input(f'measure-like-recom-6-{m+1}', 'children') for m in range(4)]
    )
def overall_like(l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,l16,l17,l18,l19,l20,l21,l22,l23,l24,l25,l26,l27):
    ml_list = []
    for i in range(27):
        if eval('l'+str(i+1)):
            if eval('l'+str(i+1) +'[0]') == 'High':
                ml = 3
            elif eval('l'+str(i+1) +'[0]') == 'Mid':
                ml = 2
            else:
                ml = 1
            ml_list.append(ml)
    avg_ml = np.mean(ml_list)
    if avg_ml <= 1.5:
        return 'Low'
    elif avg_ml <= 2.5:
        return 'Mid'
    elif avg_ml > 2.5:
        return 'High'
    else:
        return ''

@app.callback(
    [Output('overall-like-user', 'children'),
    Output('overall-like-user', 'style')],
    [Input(f'measure-like-user-1-{m+1}', 'children') for m in range(8)]
    + [Input(f'measure-like-user-2-{m+1}', 'children') for m in range(10)]
    + [Input(f'measure-like-user-4-{m+1}', 'children') for m in range(2)]
    + [Input(f'measure-like-user-5-{m+1}', 'children') for m in range(3)]
    + [Input(f'measure-like-user-6-{m+1}', 'children') for m in range(4)]
    )
def overall_like(l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,l16,l17,l18,l19,l20,l21,l22,l23,l24,l25,l26,l27):
    ml_list = []
    for i in range(27):
        if eval('l'+str(i+1)):
            if eval('l'+str(i+1) ) == 'High':
                ml = 3
            elif eval('l'+str(i+1)) == 'Mid':
                ml = 2
            elif eval('l'+str(i+1) ) == 'Low':
                ml = 1
            ml_list.append(ml)
    if len(ml_list) > 0:
        avg_ml = np.mean(ml_list)
        if avg_ml <= 1.5:
            return 'Low', {"background-color": '#C00000'}
        elif avg_ml <= 2.5 and avg_ml > 1.5:
            return 'Mid',{"background-color": '#ffffff'}
        elif avg_ml > 2.5:
            return 'High',{"background-color": '#ffffff'}
        else:
            return '',{"background-color": '#ffffff'}
    else:
        return '',{"background-color": '#ffffff'}


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

##update outcome measures
def show_domain_card(color):
    if color == 'primary':
        return [False]
    return [True]

for d in range(domain_ct):
    app.callback(
        [Output(f'outcome-domain-container-{d+1}', 'hidden')],
        [Input(f'dashboard-card-domain-selection-{d+1}', 'color')]
        )(show_domain_card)


###domain 1
@app.callback(
    Output('outcome-domain-weight-user-1', 'children'),
    [Input(f'measure-weight-user-1-{m+1}', 'value') for m in range(8)]
    )
def cal_domain_weight(v1, v2, v3, v4, v5, v6, v7, v8):
    if v1:
        n1 = v1
    else:
        n1 = 0
    if v2:
        n2 = v2
    else:
        n2 = 0
    if v3:
        n3 = v3
    else:
        n3 = 0
    if v4:
        n4 = v4
    else:
        n4 = 0
    if v5:
        n5 = v5
    else:
        n5 = 0
    if v6:
        n6 = v6
    else:
        n6 = 0
    if v7:
        n7 = v7
    else:
        n7 = 0
    if v8:
        n8 = v8
    else:
        n8 = 0
    w = sum([n1, n2, n3, n4, n5, n6, n7, n8])
    return '{:.0%}'.format(w/100)

@app.callback(
    Output('outcome-domain-weight-recom-1', 'children'),
    [Input(f'measure-weight-recom-1-{m+1}', 'children') for m in range(8)]
    )
def cal_domain_weight(v1, v2, v3, v4, v5, v6, v7, v8):
    if v1:
        n1 = float(v1[:-1])
    else:
        n1 = 0
    if v2:
        n2 = float(v2[:-1])
    else:
        n2 = 0
    if v3:
        n3 = float(v3[:-1])
    else:
        n3 = 0
    if v4:
        n4 = float(v4[:-1])
    else:
        n4 = 0
    if v5:
        n5 = float(v5[:-1])
    else:
        n5 = 0
    if v6:
        n6 = float(v6[:-1])
    else:
        n6 = 0
    if v7:
        n7 = float(v7[:-1])
    else:
        n7 = 0
    if v8:
        n8 = float(v8[:-1])
    else:
        n8 = 0
    
    w = sum([n1, n2, n3, n4, n5, n6, n7, n8])
    return '{:.0%}'.format(w/100)


@app.callback(
    [Output(f'outcome-measure-row-1-{m+1}', 'hidden') for m in range(8) ],
    [Input(f'checklist-domain-measures-lv2-1-{n+1}', 'value') for n in range(4)] + [Input(f'measure-name-1-{m+1}','children') for m in range(8)]
    )
def show_measure_row_1(v1, v2, v3, v4, m1, m2, m3, m4, m5 ,m6, m7, m8):
    v = v1+v2+v3+v4
    if m1 in v:
        h1 = False
    else:
        h1 = True
    if m2 in v:
        h2 = False
    else:
        h2 = True
    if m3 in v:
        h3 = False
    else:
        h3 = True
    if m4 in v:
        h4 = False
    else:
        h4 = True
    if m5 in v:
        h5 = False
    else:
        h5 = True
    if m6 in v:
        h6 = False
    else:
        h6 = True
    if m7 in v:
        h7 = False
    else:
        h7 = True
    if m8 in v:
        h8 = False
    else:
        h8 = True
    
    return h1, h2, h3, h4, h5, h6, h7, h8


###domain 2
@app.callback(
    Output('outcome-domain-weight-user-2', 'children'),
    [Input(f'measure-weight-user-2-{m+1}', 'value') for m in range(10)]
    )
def cal_domain_weight(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10):
    if v1:
        n1 = v1
    else:
        n1 = 0
    if v2:
        n2 = v2
    else:
        n2 = 0
    if v3:
        n3 = v3
    else:
        n3 = 0
    if v4:
        n4 = v4
    else:
        n4 = 0
    if v5:
        n5 = v5
    else:
        n5 = 0
    if v6:
        n6 = v6
    else:
        n6 = 0
    if v7:
        n7 = v7
    else:
        n7 = 0
    if v8:
        n8 = v8
    else:
        n8 = 0
    if v9:
        n9 = v9
    else:
        n9 = 0
    if v10:
        n10 = v10
    else:
        n10 = 0
    w = sum([n1, n2, n3, n4, n5, n6, n7, n8, n9, n10])
    return '{:.0%}'.format(w/100)

@app.callback(
    Output('outcome-domain-weight-recom-2', 'children'),
    [Input(f'measure-weight-recom-2-{m+1}', 'children') for m in range(10)]
    )
def cal_domain_weight(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10):
    if v1:
        n1 = float(v1[:-1])
    else:
        n1 = 0
    if v2:
        n2 = float(v2[:-1])
    else:
        n2 = 0
    if v3:
        n3 = float(v3[:-1])
    else:
        n3 = 0
    if v4:
        n4 = float(v4[:-1])
    else:
        n4 = 0
    if v5:
        n5 = float(v5[:-1])
    else:
        n5 = 0
    if v6:
        n6 = float(v6[:-1])
    else:
        n6 = 0
    if v7:
        n7 = float(v7[:-1])
    else:
        n7 = 0
    if v8:
        n8 = float(v8[:-1])
    else:
        n8 = 0
    if v9:
        n9 = float(v9[:-1])
    else:
        n9 = 0
    if v10:
        n10 = float(v10[:-1])
    else:
        n10 = 0
    w = sum([n1, n2, n3, n4, n5, n6, n7, n8, n9, n10])
    return '{:.0%}'.format(w/100)


@app.callback(
    [Output(f'outcome-measure-row-2-{m+1}', 'hidden') for m in range(10) ],
    [Input(f'checklist-domain-measures-lv2-2-{n+1}', 'value') for n in range(4)] + [Input(f'measure-name-2-{m+1}','children') for m in range(10)]
    )
def show_measure_row_2(v1, v2, v3, v4, m1, m2, m3, m4, m5 ,m6, m7, m8, m9, m10):
    v = v1+v2+v3+v4
    if m1 in v:
        h1 = False
    else:
        h1 = True
    if m2 in v:
        h2 = False
    else:
        h2 = True
    if m3 in v:
        h3 = False
    else:
        h3 = True
    if m4 in v:
        h4 = False
    else:
        h4 = True
    if m5 in v:
        h5 = False
    else:
        h5 = True
    if m6 in v:
        h6 = False
    else:
        h6 = True
    if m7 in v:
        h7 = False
    else:
        h7 = True
    if m8 in v:
        h8 = False
    else:
        h8 = True
    if m9 in v:
        h9 = False
    else:
        h9 = True
    if m10 in v:
        h10 = False
    else:
        h10 = True

    return h1, h2, h3, h4, h5, h6, h7, h8, h9, h10

###domain 4
@app.callback(
    Output('outcome-domain-weight-user-4', 'children'),
    [Input(f'measure-weight-user-4-{m+1}', 'value') for m in range(2)]
    )
def cal_domain_weight(v1, v2):
    if v1:
        n1 = v1
    else:
        n1 = 0
    if v2:
        n2 = v2
    else:
        n2 = 0

    w = sum([n1, n2])
    return '{:.0%}'.format(w/100)

@app.callback(
    Output('outcome-domain-weight-recom-4', 'children'),
    [Input(f'measure-weight-recom-4-{m+1}', 'children') for m in range(2)]
    )
def cal_domain_weight(v1, v2):
    if v1:
        n1 = float(v1[:-1])
    else:
        n1 = 0
    if v2:
        n2 = float(v2[:-1])
    else:
        n2 = 0
   
    w = sum([n1, n2])
    return '{:.0%}'.format(w/100)

@app.callback(
    [Output(f'outcome-measure-row-4-{m+1}', 'hidden') for m in range(2) ],
    [Input(f'checklist-domain-measures-lv2-4-1', 'value')] + [Input(f'measure-name-4-{m+1}','children') for m in range(2)]
    )
def show_measure_row_4(v1, m1, m2):
    v = v1
    if m1 in v:
        h1 = False
    else:
        h1 = True
    if m2 in v:
        h2 = False
    else:
        h2 = True

    return h1, h2

###domain 5
@app.callback(
    Output('outcome-domain-weight-user-5', 'children'),
    [Input(f'measure-weight-user-5-{m+1}', 'value') for m in range(3)]
    )
def cal_domain_weight(v1, v2, v3):
    if v1:
        n1 = v1
    else:
        n1 = 0
    if v2:
        n2 = v2
    else:
        n2 = 0
    if v3:
        n3 = v3
    else:
        n3 = 0

    w = sum([n1, n2, n3])
    return '{:.0%}'.format(w/100)

@app.callback(
    Output('outcome-domain-weight-recom-5', 'children'),
    [Input(f'measure-weight-recom-5-{m+1}', 'children') for m in range(3)]
    )
def cal_domain_weight(v1, v2, v3):
    if v1:
        n1 = float(v1[:-1])
    else:
        n1 = 0
    if v2:
        n2 = float(v2[:-1])
    else:
        n2 = 0
    if v3:
        n3 = float(v3[:-1])
    else:
        n3 = 0
    
    w = sum([n1, n2, n3])
    return '{:.0%}'.format(w/100)

@app.callback(
    [Output(f'outcome-measure-row-5-{m+1}', 'hidden') for m in range(3) ],
    [Input(f'checklist-domain-measures-lv2-5-1', 'value')] + [Input(f'measure-name-5-{m+1}','children') for m in range(3)]
    )
def show_measure_row_5(v1, m1, m2, m3):
    v = v1
    if m1 in v:
        h1 = False
    else:
        h1 = True
    if m2 in v:
        h2 = False
    else:
        h2 = True
    if m3 in v:
        h3 = False
    else:
        h3 = True

    return h1, h2, h3

###domain 6
@app.callback(
    Output('outcome-domain-weight-user-6', 'children'),
    [Input(f'measure-weight-user-6-{m+1}', 'value') for m in range(4)]
    )
def cal_domain_weight(v1, v2, v3, v4):
    if v1:
        n1 = v1
    else:
        n1 = 0
    if v2:
        n2 = v2
    else:
        n2 = 0
    if v3:
        n3 = v3
    else:
        n3 = 0
    if v4:
        n4 = v4
    else:
        n4 = 0

    w = sum([n1, n2, n3, n4])
    return '{:.0%}'.format(w/100)

@app.callback(
    Output('outcome-domain-weight-recom-6', 'children'),
    [Input(f'measure-weight-recom-6-{m+1}', 'children') for m in range(4)]
    )
def cal_domain_weight(v1, v2, v3, v4):
    if v1:
        n1 = float(v1[:-1])
    else:
        n1 = 0
    if v2:
        n2 = float(v2[:-1])
    else:
        n2 = 0
    if v3:
        n3 = float(v3[:-1])
    else:
        n3 = 0
    if v4:
        n4 = float(v4[:-1])
    else:
        n4 = 0

    w = sum([n1, n2, n3, n4])
    return '{:.0%}'.format(w/100)

@app.callback(
    [Output(f'outcome-measure-row-6-{m+1}', 'hidden') for m in range(4) ],
    [Input(f'checklist-domain-measures-lv2-6-1', 'value')] + [Input(f'measure-name-6-{m+1}','children') for m in range(4)]
    )
def show_measure_row_6(v1, m1, m2, m3, m4):
    v = v1
    if m1 in v:
        h1 = False
    else:
        h1 = True
    if m2 in v:
        h2 = False
    else:
        h2 = True
    if m3 in v:
        h3 = False
    else:
        h3 = True
    if m4 in v:
        h4 = False
    else:
        h4 = True

    return h1, h2, h3, h4


# contratual
@app.callback(
    Output('recom-max-pos-adj', 'children'),
    [Input('input-max-pos-adj', 'value')]
    )
def show_max_pos_adj(v):
    if v:
        return '{:.0%}'.format(v/100)
    return ""

@app.callback(
    Output('recom-max-neg-adj', 'children'),
    [Input('input-max-neg-adj', 'value')]
    )
def show_max_neg_adj(v):
    if v:
        return '{:.0%}'.format(v/100)
    return ""


# results
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







