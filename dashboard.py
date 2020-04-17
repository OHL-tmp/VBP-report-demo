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
from figure import bargraph_overall,waterfall_overall,tbl_utilizer,piechart_utilizer,bargraph_h,bargraph_stack3,bubblegraph,bargraph_perform,waterfall_domain
from modal_dashboard_domain_selection import *

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()


app = dash.Dash(__name__, url_base_pathname='/demo-report/')

server = app.server

## load data
def load_data():
    global waterfall_domain1, waterfall_domain2, waterfall_domain3, waterfall_domain4, waterfall_domain5, waterfall_domain6, waterfall_domain7
    global bargraph_overall1, waterfall_overall1
    global tbl_utilizer1, piechart_utilizer1, bargraph_script_per_util, bargraph_tot_script, bargraph_tot_script_split, bargraph_tot_unit_split, bargraph_tot_unit
    global bubble_graph_domain
    
    df_overall = pd.read_csv("data/overall_performance.csv")
    df_waterfall = pd.read_csv("data/overall_waterfall.csv")
    df_utilizer= pd.read_csv("data/utilizer_tbl.csv")
    df_util_split=pd.read_csv("data/util_split.csv")
    df_script_per_util=pd.read_csv("data/script_per_util.csv")
    df_tot_script_split=pd.read_csv("data/tot_script_split.csv")
    df_tot_unit_split=pd.read_csv("data/tot_unit_split.csv")
    df_domain_perform=pd.read_csv("data/domain_perform.csv")
    df_domain_waterfall = pd.read_csv("data/domain_waterfall.csv")
    df_measure_perform=pd.read_csv("data/measure_performance.csv")
    df_tot_script=pd.DataFrame(df_tot_script_split.sum(axis=0)[1:4,],columns=['tot_script']).iloc[[2,1,0],]
    df_tot_unit=pd.DataFrame(df_tot_unit_split.sum(axis=0)[1:4,],columns=['tot_unit']).iloc[[2,1,0],]
    
    waterfall_domain1=waterfall_domain(df_domain_waterfall['label'] ,df_domain_waterfall['base'], df_domain_waterfall['adjusted'])
    domain1_perform=bargraph_perform(df_measure_perform['performance'], df_measure_perform['Measure'])
    
    waterfall_domain2=waterfall_domain(df_domain_waterfall['label'] ,df_domain_waterfall['base'], df_domain_waterfall['adjusted'])
    domain2_perform=bargraph_perform(df_measure_perform['performance'], df_measure_perform['Measure'])
    
    waterfall_domain3=waterfall_domain(df_domain_waterfall['label'] ,df_domain_waterfall['base'], df_domain_waterfall['adjusted'])
    domain3_perform=bargraph_perform(df_measure_perform['performance'], df_measure_perform['Measure'])
    
    waterfall_domain4=waterfall_domain(df_domain_waterfall['label'] ,df_domain_waterfall['base'], df_domain_waterfall['adjusted'])
    domain4_perform=bargraph_perform(df_measure_perform['performance'], df_measure_perform['Measure'])
    
    waterfall_domain5=waterfall_domain(df_domain_waterfall['label'] ,df_domain_waterfall['base'], df_domain_waterfall['adjusted'])
    domain5_perform=bargraph_perform(df_measure_perform['performance'], df_measure_perform['Measure'])
    
    waterfall_domain6=waterfall_domain(df_domain_waterfall['label'] ,df_domain_waterfall['base'], df_domain_waterfall['adjusted'])
    domain6_perform=bargraph_perform(df_measure_perform['performance'], df_measure_perform['Measure'])
    
    waterfall_domain7=waterfall_domain(df_domain_waterfall['label'] ,df_domain_waterfall['base'], df_domain_waterfall['adjusted'])
    domain7_perform=bargraph_perform(df_measure_perform['performance'], df_measure_perform['Measure'])
    
    
    bargraph_overall1=bargraph_overall(df_overall['month'],df_overall['base'],df_overall['adjusted'])
    waterfall_overall1=waterfall_overall(df_waterfall['label'] ,df_waterfall['base'], df_waterfall['adjusted'])
    
    tbl_utilizer1=tbl_utilizer(df_utilizer)
    piechart_utilizer1=piechart_utilizer(df_util_split['Class'],df_util_split['%'])
    bargraph_script_per_util=bargraph_h(df_script_per_util['avg script'] , df_script_per_util['label'])
    bargraph_tot_script=bargraph_h(df_tot_script['tot_script'] , df_tot_script.index)
    bargraph_tot_script_split=bargraph_stack3(df_tot_script_split['dosage'], df_tot_script_split['YTD'], df_tot_script_split['Annualized'] ,df_tot_script_split['Plan Target'])
    bargraph_tot_unit_split=bargraph_stack3(df_tot_unit_split['dosage'], df_tot_unit_split['YTD'], df_tot_unit_split['Annualized'] ,df_tot_unit_split['Plan Target'])
    bargraph_tot_unit=bargraph_h(df_tot_unit['tot_unit'] , df_tot_unit.index)
    
    bubble_graph_domain=bubblegraph(df_domain_perform['weight'] ,df_domain_perform['performance'] ,df_domain_perform['domain'])
    

def create_layout():
    load_data()
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
                    card_year_to_date_metrics("Total Patients", "464"),
                    card_year_to_date_metrics("Total Gross Scripts", "1,088"),
                    card_year_to_date_metrics("Total Scripts(30-day adjusted)", "1,457"),
                    card_year_to_date_metrics("Total Units(Tablets)", "87,426"),
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
                style={"background-color":"#dfdfdf", "border":"none", "border-radius":"0.5rem"}
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
                                        html.H2("$ 12,261,985", style={"font-size":"1.5rem", "margin-top":"-5px", "color":"#fff"}),
                                    ],
                                    style={"margin-top":"-16px"}
                                ),
                                style={"height":"3rem", "background-color":"#1357DD", "text-align":"center"},
                            ),
                        ]
                    ),
                    html.P("As for April 30th.", style={"color":"#000", "font-size":"0.8rem"}),
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(figure=bargraph_overall1), width=7),
                            dbc.Col(dcc.Graph(figure=waterfall_overall1), width=5),
                        ],
                    ),
                ],
                style={"padding-bottom":"30rem", "padding-right":"2rem", "max-height":"5rem"},
            )

def card_main_volumn_based_measures():

    return dbc.Card(
                dbc.CardBody(
                    [
                        html.H1("Volumn Based Measures", className="mb-3", style={"font-size":"1.5rem"}),
                        html.Div(
                            [
                                dbc.Button(
                                    "Edit Measures",
                                    id="button-add-measure",
                                    className="mb-3",
                                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},
                                ),
                                dbc.Popover([
                                    dbc.PopoverHeader("Eidt Measures"),
                                    dbc.PopoverBody([
                                        html.Div(
                                            [
                                                dbc.Checklist(
                                                    options = [{'label':"Utilizer Count and Market Share" , 'value':"Utilizer Count and Market Share" },
                                                              {'label':"Avg Script (30-day adj) per Utilizer" , 'value':"Avg Script (30-day adj) per Utilizer" },
                                                              {'label':"Total Script Count (30-day adj) by Dosage (in thousand)" , 'value':"Total Script Count (30-day adj) by Dosage (in thousand)" },
                                                              {'label':"Total Units by Dosage (Mn)", 'value': "Total Units by Dosage (Mn)"},],
                                                    value = ["Utilizer Count and Market Share","Avg Script (30-day adj) per Utilizer","Total Script Count (30-day adj) by Dosage (in thousand)","Total Units by Dosage (Mn)"],
                                                    labelCheckedStyle={"color": "#057aff"},
                                                    id = "checklist-add-measure",
                                                    style={"font-family":"NotoSans-CondensedBlack", "font-size":"0.8rem", "padding":"1rem"},
                                                ),
                                            ],
                                            style={"padding-top":"0.5rem", "padding-bottom":"2rem"}
                                        ),
                                         
                                        html.Div(
                                            [
                                                dbc.Button("ADD", id = "add-button-add-measure",
                                                   className="mb-3",
                                                   style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},
                                                )
                                            ],
                                            style={"text-align":"center"}
                                        )
                                        
                                    ]
                                    ),
                                ],
                                id = "popover-add-measure",
                                is_open = False,
                                target = "button-add-measure",
                                placement = "top",
                                ),
                                
                            ],
                            style={"text-align":"end"},
                        ),
                        html.Div(
                            [
                                card_sub2_volumn_based_measures("Utilizer Count and Market Share",tbl_utilizer1,piechart_utilizer1,0.6,0.4),
                                card_sub1_volumn_based_measures("Avg Script (30-day adj) per Utilizer",bargraph_script_per_util),
                                card_sub2_volumn_based_measures("Total Script Count (30-day adj) by Dosage (in thousand)",bargraph_tot_script,bargraph_tot_script_split,0.5,0.5),
                                card_sub2_volumn_based_measures("Total Units by Dosage (Mn)",bargraph_tot_unit,bargraph_tot_unit_split,0.5,0.5),
                            ],
                            className="mb-3",
                        ),
                        
                    ]
                ),
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def card_sub1_volumn_based_measures(volumn_measure, fig):
    return html.Div(
	    		[
			        dbc.Card(
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
		                                dbc.Col(dcc.Graph(figure=fig, style={"height" : "12rem"}), width=12),
		                            ],
		                        ),
		                    ]
		                ),
		                className="mb-3",
		                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "max-height":"20rem"}
			        )
	            ],
                id = u"card-container-{}".format(volumn_measure),
                #style={"max-height":"20rem"}
            )


def card_sub2_volumn_based_measures(volumn_measure,fig1,fig2,size1,size2):
    size1 = int(size1*12)
    size2 = int(size2*12)
    return html.Div(
			    [
			        dbc.Card(
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
		                                dbc.Col(dcc.Graph(figure=fig1, style={"height" : "14rem"}), width=size1),
		                                dbc.Col(dcc.Graph(figure=fig2, style={"height" : "14rem"}), width=size2),
		                            ],
		                        ),
		                    ]
		                ),
		                className="mb-3",
		                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "max-height":"20rem"}
		            )
		        ], id = u"card-container-{}".format(volumn_measure)
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
                       dcc.Graph(figure=bubble_graph_domain, style={"height":"20rem"})
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "max-height":"20rem"}
            )

def card_modify_value_based_measures():
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="20%"), width=1, align="start", style={"margin-right":"-20px", "margin-top":"-4px"}),
                                dbc.Col(html.H6("Domain Detail")),
                                dbc.Col(modal_dashboard_domain_selection(7), width=3),
                            ],
                            no_gutters=True,
                        ),
                        html.Div(
                            [
                                dbc.Col(
                                    [
                                     card_buttonGroup_domain_selected(),
                                    ], 
                                    width="100%"
                                ),
                            ],
                            style = {"border":"none", "border-radius":"0.5rem"},
                        ),
                    ]
                ),
                className="mb-3",
                style = {"border-radius":"0.5rem"},
            )

def card_buttonGroup_domain_selected():
    return dbc.Card(
                dbc.CardBody([
                    html.Div([dbc.Button("Cost Reduction", 
                                      id = "button-domain-1")],
                             id = "buttonGroup-domain-selected-1",
                             hidden = True),
                    html.Div([dbc.Button("Utilization Reduction", 
                                      id = "button-domain-2")],
                             id = "buttonGroup-domain-selected-2",
                             hidden = True),
                    html.Div([dbc.Button("Improving Disease Outcome", 
                                      id = "button-domain-3")],
                             id = "buttonGroup-domain-selected-3",
                             hidden = True),
                    html.Div([dbc.Button("Decreasing Health Disparities", 
                                      id = "button-domain-4")],
                             id = "buttonGroup-domain-selected-4",
                             hidden = True),
                    html.Div([dbc.Button("Increasing Patient Safety", 
                                      id = "button-domain-5")],
                             id = "buttonGroup-domain-selected-5",
                             hidden = True),
                    html.Div([dbc.Button("Enhancing Care Quality", 
                                      id = "button-domain-6")],
                             id = "buttonGroup-domain-selected-6",
                             hidden = True),
                    html.Div([dbc.Button("Better Patient Experience", 
                                      id = "button-domain-7")],
                             id = "buttonGroup-domain-selected-7",
                             hidden = True),
                ],
                style = {"display": "flex", "border":"none", "border-radius":"0.5rem"}),
                className="mb-3"
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
                                dcc.Graph(id = "graph-container-domain-selected-1", style={"height":"20rem"}),
                                dcc.Graph(id = "graph-container-domain-selected-2", style={"height":"20rem"}),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
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

def generate_card_domain_button(color):
    if color == "info":
        return False
    return True

for i in range(7):
    app.callback(
        Output(f"buttonGroup-domain-selected-{i+1}", "hidden"),
        [Input(f"dashboard-card-domain-selection-{i+1}", "color")]
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
        fig1 = waterfall_domain1
        fig2 = domain1_perform
    elif button_id == "button-domain-2":
        fig1 = waterfall_domain2
        fig2 = domain2_perform
    elif button_id == "button-domain-3":
        fig1 = waterfall_domain3
        fig2 = domain3_perform
    elif button_id == "button-domain-4":
        fig1 = waterfall_domain4
        fig2 = domain4_perform
    elif button_id == "button-domain-5":
        fig1 = waterfall_domain5
        fig2 = domain5_perform
    elif button_id == "button-domain-6":
        fig1 = waterfall_domain6
        fig2 = domain6_perform
    elif button_id == "button-domain-7":
        fig1 = waterfall_domain7
        fig2 = domain7_perform
    
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

##Domain 1-7

def toggle_collapse_domain_selection_measures(n, is_open):
    if n and n%2 == 1:
        return not is_open, "Collapse"
    elif n and n%2 == 0:
        return not is_open, "Edit"
    return is_open, "Select"

for i in range(7):
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
    if len(v) > 0:
        return "info", u"{} measures selected".format(len(v))
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
    Output("dashboard-card-selected-domain-1", "children")],
    [Input("collapse-1", "is_open"),
    Input("checklist-domain-measures-lv2-1-1", "value"),
    Input("checklist-domain-measures-lv2-1-2", "value")],
)
def toggle_collapse_domain_selection_measures_1(is_open, v1, v2):
    measure_count = len(v1) + len(v2)
    if measure_count > 0 and is_open != True: 
        return  "info", u"{} measures selected".format(measure_count)
    return "light", ""    

## Domain 2
@app.callback(
    [Output("dashboard-card-domain-selection-2", "color"),
    Output("dashboard-card-selected-domain-2", "children")],
    [Input("collapse-2", "is_open"),
    Input("checklist-domain-measures-lv2-2-1", "value"),
    Input("checklist-domain-measures-lv2-2-2", "value")],
)
def toggle_collapse_domain_selection_measures_2(is_open, v1, v2):
    measure_count = len(v1) + len(v2)
    if measure_count > 0 and is_open != True: 
        return  "info", u"{} measures selected".format(measure_count)
    return "light", "" 

## Domain 3
@app.callback(
    [Output("dashboard-card-domain-selection-3", "color"),
    Output("dashboard-card-selected-domain-3", "children")],
    [Input("collapse-3", "is_open"),
    Input("checklist-domain-measures-lv2-3-1", "value"),
    Input("checklist-domain-measures-lv2-3-2", "value"),
    Input("checklist-domain-measures-lv2-3-3", "value"),
    Input("checklist-domain-measures-lv2-3-4", "value")],
)
def toggle_collapse_domain_selection_measures_3(is_open, v1, v2, v3, v4):
    measure_count = len(v1) + len(v2) + len(v3) + len(v4)
    if measure_count > 0 and is_open != True: 
        return  "info", u"{} measures selected".format(measure_count)
    return "light", "" 

## Domain 5
@app.callback(
    [Output("dashboard-card-domain-selection-5", "color"),
    Output("dashboard-card-selected-domain-5", "children")],
    [Input("collapse-5", "is_open"),
    Input("checklist-domain-measures-lv2-5-1", "value")],
)
def toggle_collapse_domain_selection_measures_5(is_open, v1):
    measure_count = len(v1) 
    if measure_count > 0 and is_open != True: 
        return  "info", u"{} measures selected".format(measure_count)
    return "light", "" 

## Domain 6
@app.callback(
    [Output("dashboard-card-domain-selection-6", "color"),
    Output("dashboard-card-selected-domain-6", "children")],
    [Input("collapse-6", "is_open"),
    Input("checklist-domain-measures-lv2-6-1", "value")],
)
def toggle_collapse_domain_selection_measures_6(is_open, v1):
    measure_count = len(v1)
    if measure_count > 0 and is_open != True: 
        return  "info", u"{} measures selected".format(measure_count)
    return "light", "" 

## Domain 7
@app.callback(
    [Output("dashboard-card-domain-selection-7", "color"),
    Output("dashboard-card-selected-domain-7", "children")],
    [Input("collapse-7", "is_open"),
    Input("checklist-domain-measures-lv2-7-1", "value")],
)
def toggle_collapse_domain_selection_measures_7(is_open, v1):
    measure_count = len(v1)
    if measure_count > 0 and is_open != True: 
        return  "info", u"{} measures selected".format(measure_count)
    return "light", "" 







if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True)

