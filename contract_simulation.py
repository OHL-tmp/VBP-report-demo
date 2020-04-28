#!/usr/bin/env python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import datetime
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
from modal_simulation_input import *



df_sim_rev=pd.read_csv("data/Output_Pharma_Net_Revenue.csv")
df_sim_rebate=pd.read_csv("data/Output_Rebate.csv")
df_sim_cost=pd.read_csv("data/Total_Cost.csv")

## setup
#df_setup=pd.read_csv("data/setup.csv")
df_setup1=pd.read_csv("data/setup_1.csv")
df_setup2=pd.read_csv("data/setup_2.csv")
## 初始化
global measures_select,df_setup_filter

df_setup_filter=pd.read_csv('data/df_setup_filter.csv')
measures_select=['Cost & Utilization Reduction', 'Improving Disease Outcome', 'CHF Related Average Cost per Patient', 'CHF Related Hospitalization Rate', 'NT-proBNP Change %', 'LVEF LS Mean Change %']
domain_index=[0,3]
domain1_index=[1,2]
domain2_index=[4,5]
domain3_index=[]
domain4_index=[]
domain5_index=[]
list_forborder=[[0, True], [0, False], [1, True], [1, False], [2, True], [2, False], [3, True], [3, False], [4, True], [4, False]]
percent_list=[2,4,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,26,27,28]
dollar_list=[1,3,5,6]


                    

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
							        dbc.Tab(tab_setup(), label="Contract Simulation Setup", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
							        dbc.Tab(tab_result(), label="Result", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
							        
							    ], id = 'tab_container'
							)
                        ],
                        className="mb-3",
                        style={"padding-left":"3rem", "padding-right":"3rem"},
                    ),
                    
                ],
                style={"background-color":"#f5f5f5"},
            )

def table_setup(df,rows):
    
    df=df[df['id'].isin(rows)]
    
    table=dash_table.DataTable(
        data=df.to_dict('records'),
        id='computed-table',
        columns=[
        {"name": '', "id":'measures'} ,
        {"name": '', "id":'recom_value'} ,
        {"name": 'Recommended', "id":'tarrecom_value'} ,
        {"name": 'User Defined', "id":'taruser_value', 'editable':True,} ,
        {"name": 'Recommended', "id":'probrecom'} ,
        {"name": 'User Defined', "id":'probuser'} ,
        {"name": 'Recommended', "id":'weight_recom'} ,
        {"name": 'User Defined', "id":'weight_user', 'editable':True,} , 
        {"name": 'highlight_recom', "id":'highlight_recom'} ,
        {"name": 'highlight_user', "id":'highlight_user'} ,
        {"name": 'green_thres', "id":'green_thres'} ,
        {"name": 'yellow_thres', "id":'yellow_thres'} ,
        {"name": 'id', "id":'id'} ,
        ], 
        #row_selectable='multi',        
        

        style_data_conditional=[
            { 'if': {'row_index':c[0],'column_editable': c[1] }, 
             'color': 'grey', 
             'backgroundColor': 'white',
             'font-family': 'NotoSans-CondensedLight',
             'font-weight':'bold', 
             'border':'0px',
             'border-bottom': '1px solid grey',
             'border-top': '1px solid grey',
             #'border-right': '0px',
     
              } if (c[0] in domain_index) and (c[1]==False) else 
            { 'if': {'row_index':c[0] ,'column_editable': c[1],},   
             'border-bottom': '1px solid blue', 
             'border-top': '1px solid grey', 
             #'border-right': '0px',    
              } if (c[0] in domain_index) and (c[1]==True) else 
            {
            'if': {'row_index':c[0] ,'column_editable': c[1], },
            'border': '1px solid blue',
            } if not(c[0] in domain_index) and (c[1]==True) else 
            { 'if': {'row_index':c[0] ,'column_editable': c[1],},   
             'border': '0px',       
             #'border-right': '0px',    
              }
            for c in list_forborder
        
    ]+[{
            'if': {
                'column_id': 'probrecom',
                'filter_query': '{highlight_recom} eq "green"'
            },
            'backgroundColor': 'green',
            'color': 'white',
        },
        {
            'if': {
                'column_id': 'probrecom',
                'filter_query': '{highlight_recom} eq "yellow"'
            },
            'backgroundColor': 'yellow',
            'color': 'white',
        },
        {
            'if': {
                'column_id': 'probrecom',
                'filter_query': '{highlight_recom} eq "red"'
            },
            'backgroundColor': 'red',
            'color': 'white',
        },
            {
            'if': {
                'column_id': 'probuser',
                'filter_query': '{highlight_user} eq "green"'
            },
            'backgroundColor': 'green',
            'color': 'white',
        },
        {
            'if': {
                'column_id': 'probuser',
                'filter_query': '{highlight_user} eq "yellow"'
            },
            'backgroundColor': 'yellow',
            'color': 'white',
        },
        {
            'if': {
                'column_id': 'probuser',
                'filter_query': '{highlight_user} eq "red"'
            },
            'backgroundColor': 'red',
            'color': 'white',
        },
    
    ],
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-Regular',
            'fontSize':12,
            'border':'0px',
            'height': '1.5rem',
        },
        style_cell_conditional=[
            
        {
            'if': {
                'column_id': 'recom_value',
            },
            'backgroundColor': 'grey',
            'color': 'black',
        },
        {
            'if': {
                'column_id': 'tarrecom_value',
            },
            'backgroundColor': 'grey',
            'color': 'black',
        },
        {
            'if': {
                'column_id': 'weight_recom',
            },
            'backgroundColor': 'grey',
            'color': 'black',
        },
            
        
        {
            'if': {
                'column_id': 'highlight_recom',
            },
            'display':'none'
        },
        {
            'if': {
                'column_id': 'highlight_user',
            },
            'display':'none'
        },
        {
            'if': {
                'column_id': 'green_thres',
            },
            'display':'none'
        },
        {
            'if': {
                'column_id': 'yellow_thres',
            },
            'display':'none'
        }, 
        {
            'if': {
                'column_id': 'id',
            },
            'display':'none'
        }, 
        ],
        style_table={
            'back':  colors['blue'],
        },
        style_header={
            'height': '2.5rem',
            'minWidth': '3rem',
            'maxWidth':'3rem',
            'whiteSpace': 'normal',
            'backgroundColor': '#f1f6ff',
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':14,
            'color': '#1357DD',
            'text-align':'center',
            'border':'0px solid grey',
            'text-decoration':'none'
        },
                
    )
    return table 

def tab_setup():
	return html.Div(
				[
					dbc.Row(
						[
							dbc.Col(html.H1("VBC Contract Simulation Setup", style={"padding-left":"2rem","font-size":"3"}), width=9),
							dbc.Col([
                                modal_simulation_input()
                                ], 
                                width=3,
                                style={"padding-top":"1rem"}),
						],
                        style={"padding-top":"2rem"}
					),
					html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(html.H1("Performance Measure Setup", style={"color":"#f0a800", "font-size":"1rem","padding-top":"0.8rem"}), width=9),
                                    
                                ]
                            )
                        ],
                        style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#fff","margin-top":"2rem"}
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
                        style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#fff","margin-top":"2rem"}
                    ),
                    html.Div(
                        [
                        	card_contractural_arrangement_setup(),
                        ]
                    ),
                    html.Div([
                        dbc.Button("Submit for Simulation", color="primary",id = 'button-simulation-submit')
                        ],
                        style={"text-align":"center", "padding-bottom":"2rem"}),

					
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
                style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem"}
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
                                                [html.Div([
                                                    html.H3("Recommended", style={"font-size":"1rem"}),
                                                    html.H5("CHF+AF (Recommended)", style={"font-size":"1rem"}, id = 'target-patient-recom'),
                                                ], hidden = True),],
                                                style={"padding":"0.8rem"},
                                                width=4,
                                            ),
                                dbc.Col(
                                    [
                                        html.H3("Payer Contract", style={"font-size":"1rem"}),
                                        html.Div([
                                            dcc.Dropdown(
                                                id = 'target-patient-input',
                                                options = [{'label':'CHF+AF (Recommended)', 'value':'CHF+AF (Recommended)'},
                                                            {'label':'All CHF Patients', 'value':'All CHF Patients'}],
                                                value = 'CHF+AF (Recommended)',
                                                style={"font-family":"NotoSans-Regular"}
                                            )
                                        ]),
                                    ], 
                                    style={"padding":"0.8rem"},
                                    width=4,
                                ),
                            ],
                            style={"padding-left":"1.5rem"}
                        ),
                        
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
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
                                    style={"padding-left":"2rem"},
                                    width=4,
                                ),
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.H4("Baseline", style={"font-size":"1rem"}),
                                                html.Hr(className="ml-1"),
                                				dbc.Row(
                                					[
                                						dbc.Col("Recommended", width=6),
                                						dbc.Col("Payer Contract", width=6),
                                					],
                                                    style={"font-family":"NotoSans-Condensed", "font-size":"0.8rem","text-align":"center"}
                                				)
                                			]
                                		)
                                	],
                                    style={"text-align":"center"},
                                    width=2,
                                ),
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.H4("Target", style={"font-size":"1rem"}),
                                                html.Hr(className="ml-1"),
                                				dbc.Row(
                                					[
                                						dbc.Col("Recommended", width=6),
                                						dbc.Col("Payer Contract", width=6),
                                					],
                                                    style={"font-family":"NotoSans-Condensed", "font-size":"0.8rem","text-align":"center"}
                                				)
                                			]
                                		)
                                	],
                                    style={"text-align":"center"},
                                    width=2,
                                ),
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.H4("Likelihood to achieve", style={"font-size":"1rem"}),
                                                html.Hr(className="ml-1"),
                                				dbc.Row(
                                					[
                                						dbc.Col("Recommended", width=6),
                                						dbc.Col("Payer Contract", width=6),
                                					],
                                                    style={"font-family":"NotoSans-Condensed", "font-size":"0.8rem","text-align":"center"}
                                				)
                                			]
                                		)
                                	],
                                    style={"text-align":"center"},
                                    width=2,
                                ),
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.H4("Weight", style={"font-size":"1rem"}),
                                                html.Hr(className="ml-1"),
                                				dbc.Row(
                                					[
                                						dbc.Col("Recommended", width=6),
                                						dbc.Col("Payer Contract", width=6),
                                					],
                                                    style={"font-family":"NotoSans-Condensed", "font-size":"0.8rem","text-align":"center"}
                                				)
                                			]
                                		)
                                	],
                                    style={"text-align":"center"},
                                    width=2,
                                ),

                            ],
                            style={"padding-right":"1.5rem", "padding-left":"0rem"}
                            
                        ),
#                        card_measure_modifier(domain_ct),
#                        card_measure_modifier(),
                        html.Div([table_setup(df_setup1,[0,1,2,9,11])],id='table_setup'),
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
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
                                            dbc.Col(domain_set[i], id = u'outcome-domain-{}'.format(i+1), style={"font-family":"NotoSans-Regular","color":"#919191","font-size":"1rem"}, width=10),
                                            dbc.Col(id = u'outcome-domain-weight-recom-{}'.format(i+1), style={"font-family":"NotoSans-Regular","color":"#919191","font-size":"1rem"}),
                                            dbc.Col(id = u'outcome-domain-weight-user-{}'.format(i+1), style={"font-family":"NotoSans-Regular","color":"#919191","font-size":"1rem"}),
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
                        dbc.Col(html.Div('$'+str(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Baseline']), id = u'measure-base-recom-{}-{}'.format(n+1, m+1)), width=0.5),
                        dbc.Col(html.Div('$'+str(df_payor_contract_baseline[df_payor_contract_baseline['Measure'] == measures_lv2[m]]['Baseline']), id = u'measure-base-user-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div('$'+str(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Target']), id = u'measure-target-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(
                            dcc.Input(id = u'measure-target-user-{}-{}'.format(n+1, m+1), 
                                type = 'number', debounce = True, persistence = True, persistence_type = 'session', size="4"), 
                            width=1),
                        dbc.Col(html.Div(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Likelihood'], id = u'measure-like-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div(id = u'measure-like-user-{}-{}'.format(n+1, m+1),style = {"background-color": '#ffffff'}), width=1),
                        dbc.Col(html.Div(recom_weight_pct, id = u'measure-weight-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(
                            dcc.Input(id = u'measure-weight-user-{}-{}'.format(n+1, m+1),
                                type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                min = 0, max = 100, size="4"), 
                            width=1),
                    ]
                )
                ],
                style={"font-family":"NotoSans-Regular","font-size":"1rem"}, 
                id = u"outcome-measure-row-{}-{}".format(n+1,m+1))
        elif m in percent_input:
            card = html.Div([
                dbc.Row(
                    [
                        dbc.Col(html.Div(measures_lv2[m]), width=4),
                        dbc.Col(html.Div('{:.0%}'.format(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Baseline']), id = u'measure-base-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div('{:.0%}'.format(df_payor_contract_baseline[df_payor_contract_baseline['Measure'] == measures_lv2[m]]['Baseline']), id = u'measure-base-user-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div('{:.0%}'.format(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Target']), id = u'measure-target-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(
                            dcc.Input(id = u'measure-target-user-{}-{}'.format(n+1, m+1), 
                                type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                min = 0, max = 100, size="4"), 
                            width=1),
                        dbc.Col(html.Div(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Likelihood'], id = u'measure-like-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div(id = u'measure-like-user-{}-{}'.format(n+1, m+1),style = {"background-color": '#ffffff'}), width=1),
                        dbc.Col(html.Div(recom_weight_pct, id = u'measure-weight-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(
                            dcc.Input(id = u'measure-weight-user-{}-{}'.format(n+1, m+1),
                                type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                min = 0, max = 100, size="4"), 
                            width=1),
                    ]
                )
                ],
                style={"font-family":"NotoSans-Regular","font-size":"1rem"}, 
                id = u"outcome-measure-row-{}-{}".format(n+1,m+1))
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
                                type = 'number', debounce = True, persistence = True, persistence_type = 'session', size="4"), 
                            width=1),
                        dbc.Col(html.Div(df_recom_measure[df_recom_measure['Measure'] == measures_lv2[m]]['Likelihood'], id = u'measure-like-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(html.Div(id = u'measure-like-user-{}-{}'.format(n+1, m+1),style = {"background-color": '#ffffff'}), width=1),
                        dbc.Col(html.Div(recom_weight_pct, id = u'measure-weight-recom-{}-{}'.format(n+1, m+1)), width=1),
                        dbc.Col(
                            dcc.Input(id = u'measure-weight-user-{}-{}'.format(n+1, m+1),
                                type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                min = 0, max = 100, size="4"), 
                            width=1),
                    ]
                )
                ], 
                style={"font-family":"NotoSans-Regular","font-size":"1rem"}, 
                id = u"outcome-measure-row-{}-{}".format(n+1,m+1))
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
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
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
                style={"border":"none", "border-radius":"0.5rem"}
            )

def card_contract_wo_vbc_adjustment():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Contract without VBC Adjustment", style={"font-size":"1rem", "margin-left":"10px"}), width=4),
                                dbc.Col(html.Div("Rebate", style={"font-family":"NotoSans-Condensed","font-size":"1rem","text-align":"center"}), width=1),
								dbc.Col(
                                    dcc.Input(id = 'input-rebate',
                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                        min = 0, max = 100), 
                                    width=3),
								dbc.Col([
									dbc.Button("Edit Rebate Input", id = 'button-edit-rebate-1', style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"}),
									dbc.Modal([
										dbc.ModalHeader(html.H1("EDIT Rebate Input"), style={"font-size":"1rem"}),
										dbc.ModalBody([
											dbc.Row([
												dbc.Col("# of units"),
												dbc.Col("Rebates %"),
												],
												style={"padding":"1rem"}),
											dbc.Row([
												dbc.Col(dbc.InputGroup([
													dbc.Input(),
													dbc.InputGroupAddon('~', addon_type = 'append'),
													dbc.Input(),
													])),
												dbc.Col(dbc.InputGroup([
													dbc.Input(),
													dbc.InputGroupAddon('%', addon_type = 'append'),
													])),
												],
												style={"padding":"1rem"}),
											dbc.Row([
												dbc.Col(html.H4("+ Add another range", style={"font-size":"0.8rem","color":"#1357DD"}), ),
												],
												style={"padding":"1rem"}),
											]),
										dbc.ModalFooter(
											dbc.Button('SAVE', id = 'close-edit-rebate-1', size="sm")
											)
										], id = 'modal-edit-rebate-1'),
									], width=2),
                            ],
                            no_gutters=True,
                        ),
                        
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )

def card_vbc_contract():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("VBC Contract", style={"font-size":"1rem", "margin-left":"10px"}), width=5),
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.Div("Base Rebate", style={"font-family":"NotoSans-Condensed","font-size":"1rem","text-align":"start"}),
                                            dbc.InputGroup(
                                                [
                                                    dcc.Input(id = 'input-base-rebate',
                                                        type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                                        min = 0, max = 100, size="12",style={"text-align":"center"}), 
                                                    dbc.InputGroupAddon("%", addon_type="append"),
                                                ],
                                                className="mb-3",
                                                size="sm"
                                            ),

                                        ]
                                    ),
                                    width=3
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.Div("Risk Share Method", style={"font-family":"NotoSans-Condensed","font-size":"1rem","text-align":"start"}),
                                            dcc.Dropdown(
                                                options = [
                                                                {'label':'Rebate adjustment', 'value':'Rebate adjustment'},
                                                                {'label':'Shared savings/loses', 'value':'Shared savings/loses'},
                                                                {'label':'Money back', 'value':'Money back'},
                                                                {'label':'Formulary upgrade', 'value':'Formulary upgrade'}
                                                            ],
                                                value = 'Rebate adjustment',
                                                style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}
                                            )
                                                
                                        ]
                                    ),
                                    width=3
                                ),
                                    
#								dbc.Col(html.Div("Maximum Positive Adjustment"), width=1),


                                dbc.Col(html.Div("Risk Share Method"), width=1),
                                dbc.Col(dcc.Dropdown(options = [
                                        {'label':'Rebate adjustment', 'value':'Rebate adjustment'},
                                        {'label':'Shared savings/loses', 'value':'Shared savings/loses'},
                                        {'label':'Money back', 'value':'Money back'},
                                        {'label':'Formulary upgrade', 'value':'Formulary upgrade'}
                                    ],
                                    value = 'Rebate adjustment'), width=1),
								dbc.Col([
									dbc.Button("EDIT Rebate Input", id = 'button-edit-rebate-2', style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"}),
									dbc.Modal([
										dbc.ModalHeader(html.H1("Edit Rebate Input"), style={"font-size":"1rem"}),
										dbc.ModalBody([
											dbc.Row([
												dbc.Col("# of units"),
												dbc.Col("Rebates %"),
												],
												style={"padding":"1rem"}),
											dbc.Row([
												dbc.Col(dbc.InputGroup([
													dbc.Input(),
													dbc.InputGroupAddon('~', addon_type = 'append'),
													dbc.Input(),
													])),
												dbc.Col(dbc.InputGroup([
													dbc.Input(),
													dbc.InputGroupAddon('%', addon_type = 'append'),
													])),
												],
												style={"padding":"1rem"}),
											dbc.Row([
												dbc.Col(html.H4("+ Add another range", style={"font-size":"0.8rem","color":"#1357DD"})),
												],
												style={"padding":"1rem"}),
											]),
										dbc.ModalFooter(
											dbc.Button('SAVE', id = 'close-edit-rebate-2', size="sm")
											)
										], id = 'modal-edit-rebate-2'),
									], width=2),
                            ],
                            no_gutters=True,
                        ),
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
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
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )


def card_contract_adjust_sub():
	return dbc.Card(
                dbc.CardBody(
                    [
                    	dbc.Col(html.H1("Positive Adjustment", style={"font-size":"1rem", "padding-bottom":"1rem"})),
                    	dbc.Row(
                            [
                                dbc.Col(html.Div(""), width=4),
								dbc.Col(html.H3("Recommended", style={"font-size":"0.8rem"}), width=4),
								dbc.Col(html.H3("Payer Contract", style={"font-size":"0.8rem"}), width=4),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.H3("Performance Level Threshold", style={"color":"#919191","font-size":"1rem"}), width=4),
								dbc.Col(html.Div("120%", id = 'recom-pos-perf', style={"font-family":"NotoSans-Regular","font-size":"1rem", "text-align":"center"}), width=4),
								dbc.Col(
                                    dbc.InputGroup(
                                        [
                                            dcc.Input(id = 'input-pos-perform',
                                                type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                                min = 100, size="6",style={"text-align":"center"}), 
                                            dbc.InputGroupAddon("%", addon_type="append"),
                                        ],
                                        className="mb-3",
                                        size="sm"
                                    ),
                                    width=4,
                                    style={"text-align":"end"}
                                ),

                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.H3("Rebate Adjustment Cap", style={"color":"#919191","font-size":"1rem"}), width=4),
                                dbc.Col(
                                    dbc.InputGroup(
                                        [
                                            dcc.Input(id = 'input-max-pos-adj',
                                                type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                                min = 0, max = 100, size="6", placeholder = 'input a positive number',style={"text-align":"center"}), 
                                            dbc.InputGroupAddon("%", addon_type="append"),
                                        ],
                                        className="mb-3",
                                        size="sm"
                                    ),
                                    width=4,
                                    style={"text-align":"end"}
                                ),
                                dbc.Col(
                                    dbc.InputGroup(
                                        [
                                            dcc.Input(id = 'input-pos-adj',
                                                type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                                min = 0, size="6",style={"text-align":"center"}), 
                                            dbc.InputGroupAddon("%", addon_type="append"),
                                        ],
                                        className="mb-3",
                                        size="sm"
                                    ),
                                    width=4,
                                    style={"text-align":"end"}
                                ),
                                
                            ],
                            no_gutters=True,
                        ),

                        html.Hr(className="ml-1"),

                        dbc.Col(html.H1("Negative Adjustment", style={"font-size":"1rem", "padding-bottom":"1rem"})),
                    	dbc.Row(
                            [
                                dbc.Col(html.Div(""), width=4),
								dbc.Col(html.H3("Recommended", style={"font-size":"0.8rem"}), width=4),
								dbc.Col(html.H3("Payer Contract", style={"font-size":"0.8rem"}), width=4),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.H3("Performance Level Threshold", style={"color":"#919191","font-size":"1rem"}), width=4),
								dbc.Col(html.Div("80%", id = 'recom-neg-perf', style={"font-family":"NotoSans-Regular","font-size":"1rem", "text-align":"center"}), width=4),
								dbc.Col(
                                    dbc.InputGroup(
                                        [
                                            dcc.Input(id = 'input-neg-perform',
                                                    type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                                    min = 0, max = 100, size="6",style={"text-align":"center"}), 
                                            dbc.InputGroupAddon("%", addon_type="append"),
                                        ],
                                        className="mb-3",
                                        size="sm"
                                    ),
                                    width=4,
                                    style={"text-align":"end"}
                                ),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.H3("Rebate Adjustment Cap", style={"color":"#919191","font-size":"1rem"}), width=4),
                                dbc.Col(
                                    dbc.InputGroup(
                                        [
                                            dbc.InputGroupAddon("-", addon_type="prepend"),
                                            dcc.Input(id = 'input-max-neg-adj',
                                                type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                                min = -100, max = 0, size="6", placeholder = 'input a negative number',style={"text-align":"center"}), 
                                            dbc.InputGroupAddon("%", addon_type="append"),
                                        ],
                                        className="mb-3",
                                        size="sm"
                                    ),
                                    width=4,
                                    style={"text-align":"end"}
                                ),
                                dbc.Col(
                                    dbc.InputGroup(
                                        [
                                            dbc.InputGroupAddon("-", addon_type="prepend"),
                                            dcc.Input(id = 'input-neg-adj',
                                                type = 'number', debounce = True, persistence = True, persistence_type = 'session',
                                                max = 0, size="6",style={"text-align":"center"}), 
                                            dbc.InputGroupAddon("%", addon_type="append"),
                                        ],
                                        className="mb-3",
                                        size="sm"
                                    ),
                                    width=4,
                                    style={"text-align":"end"}
                                ),
                                
                            ],
                            no_gutters=True,
                        ),
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
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
					            "Pharma’s Revenue Projection",
					            id="collapse_button_result_1",
					            className="mb-3",
					            color="light",
					            block=True,
                                style={"font-family":"NotoSans-CondensedBlack","font-size":"1.5rem","border-radius":"0.5rem","border":"1px solid #1357DD","color":"#1357DD"}
					        ),
					        dbc.Collapse(
					            collapse_result_1(),
					            id="collapse_result_1",
                                is_open=True,
					        ),
					    ],
                        style={"padding-top":"1rem"}
					),
					html.Div(
					    [
					        dbc.Button(
					            "Pharma’s Rebate Projection",
					            id="collapse_button_result_2",
					            className="mb-3",
					            color="light",
					            block=True,
                                style={"font-family":"NotoSans-CondensedBlack","font-size":"1.5rem","border-radius":"0.5rem","border":"1px solid #1357DD","color":"#1357DD"}
					        ),
					        dbc.Collapse(
					            collapse_result_2(),
					            id="collapse_result_2",
                                is_open=True,
					        ),
					    ],
                        style={"padding-top":"1rem"}
					),
					html.Div(
					    [
					        dbc.Button(
					            "Plan’s Total Cost Projection for Target Patient",
					            id="collapse_button_result_3",
					            className="mb-3",
					            color="light",
					            block=True,
                                style={"font-family":"NotoSans-CondensedBlack","font-size":"1.5rem","border-radius":"0.5rem","border":"1px solid #1357DD","color":"#1357DD"}
					        ),
					        dbc.Collapse(
					            collapse_result_3(),
					            id="collapse_result_3",
                                is_open=True,
					        ),
					    ],
                        style={"padding-top":"1rem"}
					),
					html.Div(
					    [
					        dbc.Button(
					            "Confounding Factors Needed to be Accounted for in the Contract",
					            id="collapse_button_confounding_factors",
					            className="mb-3",
					            color="light",
					            block=True,
                                style={"font-family":"NotoSans-CondensedBlack","font-size":"1.5rem","border-radius":"0.5rem","border":"1px solid #1357DD","color":"#1357DD"}
					        ),
					        dbc.Collapse(
					            collapse_confounding_factors(),
					            id="collapse_confounding_factors",
					        ),
					    ],
                        style={"padding-top":"1rem"}
					),
					html.Div(
						[
							"",
						],
						style={"height":"2rem"}
					)
				],
                style={"padding-top":"2rem","padding-left":"1rem","padding-right":"1rem"}
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
            	),
                style={"border":"none","padding":"1rem"}
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
            	),
                style={"border":"none","padding":"1rem"}
           	)



def collapse_result_3():
	return dbc.Card(
            	dbc.CardBody(
            		[
            			dbc.Row(
            				[
            					dbc.Col(html.Div([dcc.Graph(id = 'sim_result_box_3',style={"height":"50vh", "width":"90vh"},config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,})]),width=6 ),
            					dbc.Col(html.Div(id = 'sim_result_table_3'), width=6)
            				]
            			)
            		]
            	),
                style={"border":"none","padding":"1rem"}
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
            					dbc.Col(html.Div([table_factor_doc(df_factor_doc)], style={"width":"100%"}), width=12),
            					#dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=6)
            				]
            			)
            		]
            	),
                style={"border":"none","padding":"1rem"}
           	)




app.layout = create_layout()



#link to model
'''
@app.callback(
    [Output('tab_container', 'active_tab'),
    Output('sim_result_box_1','figure'),
    Output('sim_result_table_1','children'),
    Output('sim_result_box_2','figure'),
    Output('sim_result_table_2','children')],
    [Input('button-simulation-submit', 'n_clicks'),
    Input('recom-pos-perf','children'),
    Input('recom-neg-perf','children'),
    Input('input-max-pos-adj','value'),
    Input('input-max-neg-adj','value'),
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
                    'Adj_Limit_U': [re_pos_adj/100],
                    'Perf_Range_L_Min': [1],
                    'Perf_Range_L_Max': [float(re_neg_perf[:-1])/100],
                    'Adj_Limit_L': [re_neg_adj/100]} 
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
            cohort = 'CHF+AF (Recommended)'
        else:
            cohort = 'All CHF Patients'

        t1,t2,t3=Contract_Calculation(Recom_Contract, UD_Measure,UD_Contract,cohort,rebate_novbc/100, rebate_vbc/100)
        t1.reset_index(inplace = True)
        t2.reset_index(inplace = True)
        t3.reset_index(inplace  =True)

        return 'tab-1',sim_result_box(t1),table_sim_result(t1),sim_result_box(t2),table_sim_result(t2)
    return 'tab-0',{},[],{},[]





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
            if measure in percent_input:
            	ur_target = user_target/100
            else: 
            	ur_target = user_target

            if measure in positive_measure:
                if (ur_target-recom_target[0])/recom_target[0] > 0.1:
                    ul = rl -2
                elif (ur_target-recom_target[0])/recom_target[0] > 0.05:
                    ul = rl -1
                elif (ur_target-recom_target[0])/recom_target[0] < -0.05:
                    ul = rl +1
                elif (ur_target-recom_target[0])/recom_target[0] < -0.1:
                    ul = rl +2
                else:
                    ul = rl
            else:
                if (ur_target-recom_target[0])/recom_target[0] > 0.1:
                    ul = rl +2
                elif (ur_target-recom_target[0])/recom_target[0] > 0.05:
                    ul = rl +1
                elif (ur_target-recom_target[0])/recom_target[0] < -0.05:
                    ul = rl -1
                elif (ur_target-recom_target[0])/recom_target[0] < -0.1:
                    ul = rl -2
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
'''

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
'''
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

'''


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


#modal-input 
def parse_contents(contents, filename, date):
	return html.Div([
        html.H6(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        ])

@app.callback(
	Output('output-data-upload', 'children'),
	[Input('upload-data', 'contents')],
	[State('upload-data', 'filename'),
	State('upload-data','last_modified')]
	)
def upload_output(list_of_contents, list_of_names, list_of_dates):
	if list_of_contents is not None:
		children = [
			parse_contents(list_of_contents, list_of_names, list_of_dates) 
		]
		return children


@app.callback(
	Output('popover-age', 'is_open'),
	[Input('button-popover-age', 'n_clicks'), Input('popover-age-submit', 'n_clicks')],
	[State('popover-age', 'is_open')],
	)
def toggle_popover(n1, n2, is_open):
	if n1 or n2:
		return not is_open
	return is_open

@app.callback(
	Output('modal-edit-assumption', 'is_open'),
	[Input('button-edit-assumption', 'n_clicks'), Input('close-edit-assumption', 'n_clicks')],
	[State('modal-edit-assumption', 'is_open')],
	)
def toggle_popover(n1, n2, is_open):
	if n1 or n2:
		return not is_open
	return is_open

@app.callback(
	Output('modal-edit-rebate-1', 'is_open'),
	[Input('button-edit-rebate-1', 'n_clicks'), Input('close-edit-rebate-1', 'n_clicks')],
	[State('modal-edit-rebate-1', 'is_open')],
	)
def toggle_popover(n1, n2, is_open):
	if n1 or n2:
		return not is_open
	return is_open

@app.callback(
	Output('modal-edit-rebate-2', 'is_open'),
	[Input('button-edit-rebate-2', 'n_clicks'), Input('close-edit-rebate-2', 'n_clicks')],
	[State('modal-edit-rebate-2', 'is_open')],
	)
def toggle_popover(n1, n2, is_open):
	if n1 or n2:
		return not is_open
	return is_open	

@app.callback(
    Output('table_setup', 'children'),
#    Output('table_setup', 'hidden'),
#    [Output('computed-table', 'data'),
#    Output('computed-table', 'selected_row_ids')],
    [Input(f'dashboard-card-domain-selection-{d+1}', 'color') for d in range(domain_ct)]
    + [Input(f'checklist-domain-measures-lv2-1-{n+1}', 'value') for n in range(4)]
    + [Input(f'checklist-domain-measures-lv2-2-{n+1}', 'value') for n in range(4)]
    + [Input(f'checklist-domain-measures-lv2-4-1', 'value')]
    + [Input(f'checklist-domain-measures-lv2-5-1', 'value')]
    + [Input(f'checklist-domain-measures-lv2-6-1', 'value')]
    +[Input('target-patient-input','value')]
    #+[Input('computed-table', 'data_timestamp')],
    #[State('computed-table', 'data')]
    )
def update_table(d1,d2,d3,d4,d5,d6,mc1,mc2,mc3,mc4,mc5,mc6,mc7,mc8,mc9,mc10,mc11,cohort):#,timestamp, data
    global domain_index,domain1_index,domain2_index,domain3_index,domain4_index,domain5_index,list_forborder,df_setup_filter,measures_select,df_setup
    if cohort == 'CHF+AF (Recommended)':
        df_setup = df_setup1
    else:
        df_setup = df_setup2
    domain_selected = []
    for i in range(6):
        if eval('d' + str(i+1)) == 'primary':
            domain_selected.append(domain_set[i])
    measure_selected = []
    for i in range(11):
        if eval('mc'+str(i+1)) and len(eval('mc'+str(i+1))) > 0:
            measure_selected.extend(eval('mc'+str(i+1)))
    #ctx = dash.callback_context.triggered
    #print(ctx)
    #triggered = dash.callback_context.triggered[0]['prop_id']
        
    #if triggered == 'dashboard-card-domain-selection-1.color':
    measures_select = domain_selected + measure_selected
    #print(measures_select)
    #df=df_setup[df_setup['measures'].isin(measures_select)]
    rows=df_setup[df_setup['measures'].isin(measures_select)]['id'].to_list()
    
    temp=df_setup[df_setup['measures'].isin(measures_select)]#pd.DataFrame(data)
    domain_index=[]
    domain1_index=[]
    domain2_index=[]
    domain3_index=[]
    domain4_index=[]
    domain5_index=[]
    list_forborder=[]
    #df_setup_filter=df
    
    for i in range(len(temp)):
        list_forborder.append([i,True])
        list_forborder.append([i,False])
        if temp.values[i,0] in ['Cost & Utilization Reduction','Improving Disease Outcome','Increasing Patient Safety','Enhancing Care Quality','Better Patient Experience']:
            domain_index.append(i)
            
    for i in range(len(domain_index)):
        for j in range(len(temp)):
            if i==len(domain_index)-1:
                if(j>domain_index[i]):
                    eval('domain'+str(i+1)+'_index').append(j)
            else: 
                if (j>domain_index[i]) & (j<domain_index[i+1]):
                    eval('domain'+str(i+1)+'_index').append(j)
                    
    return table_setup(df_setup,rows)
    

#    return False #table_setup(df)

@app.callback(
    Output('computed-table', 'data'),
    [Input('computed-table', 'data_timestamp')],
    [State('computed-table', 'data')])
def update_columns(timestamp, data):
    #df_setup_filter=pd.read_csv('data/df_setup_filter.csv')
    #print(measures_select)
    #print(pd.DataFrame(data)['measures'].to_list())
    #global measures_select,df_setup_filter
    #print(set(measures_select)==set(pd.DataFrame(data)['measures'].to_list()))
    #if set(measures_select)==set(pd.DataFrame(data)['measures'].to_list()):
    

    #print(domain_index)
    #print(domain1_index)
    #print(domain2_index)
    #print(domain1_index+domain2_index+domain3_index+domain4_index+domain5_index)
    weight_1=0
    weight_2=0
    weight_3=0
    weight_4=0
    weight_5=0 
    for i in domain1_index+domain2_index+domain3_index+domain4_index+domain5_index:
        #print(i)
        row=data[i]
        row['weight_user']=str(row['weight_user']).replace('$','').replace('%','')
        row['taruser_value']=str(row['taruser_value']).replace('$','').replace('%','')
                       
        if i in domain1_index:
            weight_1=weight_1+float(row['weight_user'])
        if i in domain2_index:
            weight_2=weight_2+float(row['weight_user'])
        if i in domain3_index:
            weight_3=weight_3+float(row['weight_user'])
        if i in domain4_index:
            weight_4=weight_4+float(row['weight_user'])
        if i in domain5_index:
            weight_5=weight_5+float(row['weight_user'])
            
        row['weight_user']= '{}%'.format(row['weight_user']) 
        
        if row['measures'] in ["LVEF LS Mean Change %", "Change in Self-Care Score", "Change in Mobility Score", "DOT", "PDC", "MPR"] :
           # print(row['taruser_value'])
            if float(row['taruser_value'])<=float(row['yellow_thres']):
                row['highlight_user']='yellow'
                row['probuser']='Mid'
                if float(row['taruser_value'])<=float(row['green_thres']):
                    row['highlight_user']='green'
                    row['probuser']='High'
            else:
                row['highlight_user']='red'
                row['probuser']='Low'
                
        else:
            #print(row)
            if float(row['taruser_value'])>=float(row['yellow_thres']):
                row['highlight_user']='yellow'
                row['probuser']='Mid'
                if float(row['taruser_value'])>=float(row['green_thres']):
                    row['highlight_user']='green'
                    row['probuser']='High'
            else:
                row['highlight_user']='red'
                row['probuser']='Low'
            
        if i in percent_list:
            row['taruser_value']='{}%'.format(row['taruser_value'])
        else:
            row['taruser_value']='${}'.format(row['taruser_value']) 
    
    j=0
    for i in domain_index:
        j=j+1
        data[i]['taruser_value']=''
        data[i]['weight_user']=str(eval('weight_'+str(j)))+'%'
#else:
#    data=df_setup_filter.to_dict('records')

    return data #,rows

@app.callback(
    [Output('tab_container', 'active_tab'),
    Output('sim_result_box_1','figure'),
    Output('sim_result_table_1','children'),
    Output('sim_result_box_2','figure'),
    Output('sim_result_table_2','children'),
    Output('sim_result_box_3','figure'),
    Output('sim_result_table_3','children')],
    [Input('button-simulation-submit', 'n_clicks'),
    Input('recom-pos-perf','children'),
    Input('recom-neg-perf','children'),
    Input('input-max-pos-adj','value'),
    Input('input-max-neg-adj','value'),
    Input('input-pos-perform', 'value'),
    Input('input-neg-perform', 'value'),
    Input('input-pos-adj', 'value'),
    Input('input-neg-adj', 'value'),
    Input('target-patient-recom','children'),
    Input('target-patient-input','value'),
    Input('input-rebate','value'),
    Input('input-base-rebate','value'),]
    +[Input('computed-table','derived_virtual_data')]
)
def simulation(submit_button, re_pos_perf, re_neg_perf, re_pos_adj, re_neg_adj, in_pos_perf, in_neg_perf, in_pos_adj, in_neg_adj, cohort_recom, cohort_selected, rebate_novbc, rebate_vbc,data):
#    m1,m2,m3,m4,t1,t2,t3,t4,w1,w2,w3,w4):
    if cohort_selected == 'CHF+AF (Recommended)':
        df = df_setup1
    else:
        df = df_setup2
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    submit = len([1 for i in triggered if i == "button-simulation-submit.n_clicks"])
    if submit:
        
        dff = df if data is None else pd.DataFrame(data)
        
        input1 = {'Perf_Range_U_Min': [1], 
                    'Perf_Range_U_Max': [float(re_pos_perf[:-1])/100], 
                    'Adj_Limit_U': [re_pos_adj/100],
                    'Perf_Range_L_Min': [1],
                    'Perf_Range_L_Max': [float(re_neg_perf[:-1])/100],
                    'Adj_Limit_L': [re_neg_adj/100]} 
        Recom_Contract = pd.DataFrame(input1, columns = ['Perf_Range_U_Min','Perf_Range_U_Max','Adj_Limit_U','Perf_Range_L_Min','Perf_Range_L_Max', 'Adj_Limit_L'])
        
#        selected_measure = []
        measure_list = list(dff['measures'])
        measure_name = []
        target_list = []
        weight_list = []
        for i in range(len(measure_list)):
            if measure_list[i] not in ['Cost & Utilization Reduction','Improving Disease Outcome','Increasing Patient Safety','Enhancing Care Quality','Better Patient Experience']:
                measure_name.append(measure_list[i])
                target_list.append(float(str(list(dff['taruser_value'])[i]).replace('$','').replace('%','')))
                weight_list.append(float(str(list(dff['weight_user'])[i]).replace('$','').replace('%','')))  
                
        print(target_list)
#        target_list = [float(str(i).replace('$','').replace('%','')) for i in  list(dff['taruser_value'])] 
#        weight_list = [float(str(i).replace('$','').replace('%','')) for i in list(dff['weight_user'])]
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


        t1,t2,t3=Contract_Calculation(Recom_Contract, UD_Measure,UD_Contract,cohort_selected,rebate_novbc/100, rebate_vbc/100)
        t1.reset_index(inplace = True)
        t2.reset_index(inplace = True)
        t3.reset_index(inplace  =True)

        return 'tab-1',sim_result_box(t1),table_sim_result(t1),sim_result_box(t2),table_sim_result(t2),sim_result_box(t3),table_sim_result(t3)
    return 'tab-0',{},[],{},[],{},[]

if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True)







