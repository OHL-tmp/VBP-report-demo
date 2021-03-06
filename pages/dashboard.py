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
from utils import *
from figure import *
from modal_dashboard_domain_selection import *

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()


app = dash.Dash(__name__, url_base_pathname='/vbc-demo/dashboard/')

server = app.server

## load data
def load_data():
    global waterfall_domain1, waterfall_domain2, waterfall_domain3, waterfall_domain4, waterfall_domain5, waterfall_domain6, waterfall_domain7
    global domain1_perform,domain2_perform,domain3_perform,domain4_perform,domain5_perform,domain6_perform,domain7_perform
    global bargraph_overall1, waterfall_overall1
    global tbl_utilizer1, piechart_utilizer1, bargraph_script_per_util, bargraph_tot_script, bargraph_tot_script_split, bargraph_tot_unit_split, bargraph_tot_unit
    global bubble_graph_domain
    global df_domain_perform,df_measure_perform
    
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
    
    waterfall_domain1=tbl_measure(df_measure_perform,0)
    domain1_perform=bargraph_perform(df_measure_perform, 0)
    
    waterfall_domain2=tbl_measure(df_measure_perform,1)
    domain2_perform=bargraph_perform(df_measure_perform, 1)
    
    waterfall_domain3=tbl_measure(df_measure_perform,2)
    domain3_perform=bargraph_perform(df_measure_perform, 2)
    
    waterfall_domain4=tbl_measure(df_measure_perform,3)
    domain4_perform=bargraph_perform(df_measure_perform, 3)
    
    waterfall_domain5=tbl_measure(df_measure_perform,4)
    domain5_perform=bargraph_perform(df_measure_perform, 4)
    
    waterfall_domain6=tbl_measure(df_measure_perform,5)
    domain6_perform=bargraph_perform(df_measure_perform, 5)
    
    waterfall_domain7=tbl_measure(df_measure_perform,5)
    domain7_perform=bargraph_perform(df_measure_perform, 5)
    
    
    bargraph_overall1=bargraph_overall(df_overall)
    waterfall_overall1=waterfall_overall(df_waterfall['label'] ,df_waterfall['base'], df_waterfall['adjusted'])
    
    tbl_utilizer1=tbl_utilizer(df_utilizer)
    piechart_utilizer1=piechart_utilizer(df_util_split['Class'],df_util_split['%'])
    bargraph_script_per_util=bargraph_h(df_script_per_util['avg script'] , df_script_per_util['label'])
    bargraph_tot_script=bargraph_h(df_tot_script['tot_script'] , df_tot_script.index)
    bargraph_tot_script_split=bargraph_stack3(df_tot_script_split['dosage'], df_tot_script_split['YTD'], df_tot_script_split['Annualized'] ,df_tot_script_split['Plan Target'])
    bargraph_tot_unit_split=bargraph_stack3(df_tot_unit_split['dosage'], df_tot_unit_split['YTD'], df_tot_unit_split['Annualized'] ,df_tot_unit_split['Plan Target'])
    bargraph_tot_unit=bargraph_h(df_tot_unit['tot_unit'] , df_tot_unit.index)
    
    bubble_graph_domain=bubblegraph(df_domain_perform,[0,1],'Domain')
    


def create_layout():
    load_data()
    return html.Div(
                [ 
                    html.Div([Header_mgmt(app)], style={"height":"6rem"}),
                    
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
                    html.P("As of June 30th.", style={"color":"#000", "font-size":"0.8rem"}),
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
                                                    options = [{'label':"Market Share" , 'value':"Market Share" },
                                                              {'label':"Utilizer Count" , 'value':"Utilizer Count" },
                                                              {'label':"Avg Script (30-day adj) per Utilizer" , 'value':"Avg Script (30-day adj) per Utilizer" },
                                                              {'label':"Total Script Count (30-day adj) by Dosage (in thousand)" , 'value':"Total Script Count (30-day adj) by Dosage (in thousand)" },
                                                              {'label':"Total Units by Dosage (Mn)", 'value': "Total Units by Dosage (Mn)"},],
                                                    value = ["Market Share","Utilizer Count","Avg Script (30-day adj) per Utilizer"],
                                                    labelCheckedStyle={"color": "#057aff"},
                                                    id = "checklist-add-measure",
                                                    style={"font-family":"NotoSans-Condensed", "font-size":"0.8rem", "padding":"1rem"},
                                                ),
                                            ],
                                            style={"padding-top":"0.5rem", "padding-bottom":"2rem"}
                                        ),
                                         
                                        html.Div(
                                            [
                                                dbc.Button("Comfirm", id = "add-button-add-measure",
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
                                card_sub1_volumn_based_measures("Market Share",piechart_utilizer1,0.85),
                                card_sub1_volumn_based_measures("Utilizer Count",tbl_utilizer1,0.6),
                                card_sub1_volumn_based_measures("Avg Script (30-day adj) per Utilizer",bargraph_script_per_util,0.6),
                                card_sub2_volumn_based_measures("Total Script Count (30-day adj) by Dosage (in thousand)",bargraph_tot_script,bargraph_tot_script_split,1,1),
                                card_sub2_volumn_based_measures("Total Units by Dosage (Mn)",bargraph_tot_unit,bargraph_tot_unit_split,1,1),
                            ],
                            className="mb-3",
                        ),
                        
                    ]
                ),
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def card_sub1_volumn_based_measures(volumn_measure, fig, size):
    size = str(int(size*22)) + "rem"
    return html.Div(
	    		[
			        dbc.Card(
		                dbc.CardBody(
		                    [
		                        dbc.Row(
		                            [
		                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="20%"), width=1, align="start", style={"margin-right":"-20px", "margin-top":"-4px"}),
		                                dbc.Col(html.H4(volumn_measure, style={"font-size":"1rem"})),
		                            ],
		                            no_gutters=True,
		                        ),
		                        dbc.Row(
		                            [
		                                dbc.Col(dcc.Graph(figure=fig, style={"height" : size}), width=12),
		                            ],
		                        ),
		                    ]
		                ),
		                className="mb-3",
		                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "max-height":"22rem"}
			        )
	            ],
                id = u"card-container-{}".format(volumn_measure),
                #style={"max-height":"20rem"}
            )


def card_sub2_volumn_based_measures(volumn_measure,fig1,fig2,height1,height2):
    size1 = str(int(height1*14))+"rem"
    size2 = str(int(height2*14))+"rem"
    return html.Div(
			    [
			        dbc.Card(
		                dbc.CardBody(
		                    [
		                        dbc.Row(
		                            [
		                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="20%"), width=1, align="start", style={"margin-right":"-20px", "margin-top":"-4px"}),
		                                dbc.Col(html.H4(volumn_measure, style={"font-size":"1rem"})),
		                            ],
		                            no_gutters=True,
		                        ),
		                        html.Div(
		                            [
		                                dcc.Graph(figure=fig1, style={"height" : size1}),
		                                dcc.Graph(figure=fig2, style={"height" : size2}),
		                            ],
                                    style={"padding":"1rem"}
		                        ),
		                    ]
		                ),
		                className="mb-3",
		                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "max-height":"40rem"}
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
                                card_modify_value_based_measures(),
                                card_overview_value_based_measures(),
                                card_sub_value_based_measures(),
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
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="20%"), width=1, align="start", style={"margin-right":"-20px", "margin-top":"-4px"}),
                                dbc.Col(html.H4("Performance Result of Each Domain", style={"font-size":"1rem"}), width=8),
                                dbc.Button(id = "switch-domain-measure-view", className="mb-3", style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"}),
                            ],
                            no_gutters=True,
                        ),
                        
                        dcc.Graph(style={"height":"20rem"}, id = "bubble_graph_domain")
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "max-height":"23rem"}
            )

def card_modify_value_based_measures():
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="20%"), width=1, align="start", style={"margin-right":"-20px", "margin-top":"-4px"}),
                                dbc.Col(html.H4("Domain Detail"), style={"font-size":"0.4rem"}),
                                dbc.Col(modal_dashboard_domain_selection(domain_ct), width=3),
                            ],
                            no_gutters=True,
                        ),
                        html.Div(
                            [
                                card_buttonGroup_domain_selected(),
                            ],
                            style = {"border":"none", "border-radius":"0.5rem"},
                        ),
                    ]
                ),
                className="mb-3",
                style = {"border":"none", "border-radius":"0.5rem"},
            )

def card_buttonGroup_domain_selected():
    return dbc.Card(
                dbc.CardBody([
                    html.Div([dbc.Button("Cost & Utilization Reduction", 
                                      id = "button-domain-1", active=True,outline=True, color="primary", className="mr-1", style = {"font-family":"NotoSans-Regular", "font-size":"0.8rem"})],
                             id = "buttonGroup-domain-selected-1",
                             hidden = True),
                    html.Div([dbc.Button("Improving Disease Outcome", 
                                      id = "button-domain-2", outline=True, color="primary", className="mr-1", style = {"font-family":"NotoSans-Regular", "font-size":"0.8rem"})],
                             id = "buttonGroup-domain-selected-2",
                             hidden = True),
                    html.Div([dbc.Button("Decreasing Health Disparities", 
                                      id = "button-domain-3", outline=True, color="primary", className="mr-1", style = {"font-family":"NotoSans-Regular", "font-size":"0.8rem"})],
                             id = "buttonGroup-domain-selected-3",
                             hidden = True),
                    html.Div([dbc.Button("Increasing Patient Safety", 
                                      id = "button-domain-4", outline=True, color="primary", className="mr-1", style = {"font-family":"NotoSans-Regular", "font-size":"0.8rem"})],
                             id = "buttonGroup-domain-selected-4",
                             hidden = True),
                    html.Div([dbc.Button("Enhancing Care Quality", 
                                      id = "button-domain-5", outline=True, color="primary", className="mr-1", style = {"font-family":"NotoSans-Regular", "font-size":"0.8rem"})],
                             id = "buttonGroup-domain-selected-5",
                             hidden = True),
                    html.Div([dbc.Button("Better Patient Experience", 
                                      id = "button-domain-6", outline=True, color="primary", className="mr-1", style = {"font-family":"NotoSans-Regular", "font-size":"0.8rem"})],
                             id = "buttonGroup-domain-selected-6",
                             hidden = True),
                ],
                style = {"display": "flex", "border":"none", "border-radius":"1rem","padding":"0.2rem"}),
                
            )


def card_sub_value_based_measures():

    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.H6(id = "card_domain_name")),
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

states = {"Market Share": True, 
    "Utilizer Count": True, 
    "Avg Script (30-day adj) per Utilizer": True,
    "Total Script Count (30-day adj) by Dosage (in thousand)": True,
    "Total Units by Dosage (Mn)": True}

@app.callback(
    [Output("card-container-Market Share","hidden"),
    Output("card-container-Utilizer Count","hidden"),
    Output("card-container-Avg Script (30-day adj) per Utilizer","hidden"),
    Output("card-container-Total Script Count (30-day adj) by Dosage (in thousand)","hidden"),
    Output("card-container-Total Units by Dosage (Mn)","hidden"),],
    [Input("add-button-add-measure","n_clicks"),
    Input("checklist-add-measure","value")],
    [State("card-container-Market Share","hidden"),
    State("card-container-Utilizer Count","hidden"),
    State("card-container-Avg Script (30-day adj) per Utilizer","hidden"),
    State("card-container-Total Script Count (30-day adj) by Dosage (in thousand)","hidden"),
    State("card-container-Total Units by Dosage (Mn)","hidden"),],
)
def add_close_measure_card( ad, v, h1, h2, h3, h4, h5):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    edit = len([1 for i in triggered if i == "add-button-add-measure.n_clicks"])
    checked = v
    if edit:
        for p in ["Market Share", 
            "Utilizer Count",
            "Avg Script (30-day adj) per Utilizer",
            "Total Script Count (30-day adj) by Dosage (in thousand)",
            "Total Units by Dosage (Mn)"]:
            if p in checked:
                states[p] = False
            else:
                states[p] = True
        return states["Market Share"], states["Utilizer Count"], states["Avg Script (30-day adj) per Utilizer"],states["Total Script Count (30-day adj) by Dosage (in thousand)"],states["Total Units by Dosage (Mn)"]
    return h1, h2, h3, h4, h5


# generate selected domain button

def generate_card_domain_button(color):
    if color == "info":
        return False
    return True

for i in range(domain_ct):
    app.callback(
        Output(f"buttonGroup-domain-selected-{i+1}", "hidden"),
        [Input(f"dashboard-card-domain-selection-{i+1}", "color")]
    )(generate_card_domain_button)
    


@app.callback(
    [Output("bubble_graph_domain", "figure"),
     Output("switch-domain-measure-view","children")],
    [Input("dashboard-card-domain-selection-1", "color"),
    Input("dashboard-card-domain-selection-2", "color"),
    Input("dashboard-card-domain-selection-3", "color"),
    Input("dashboard-card-domain-selection-4", "color"),
    Input("dashboard-card-domain-selection-5", "color"),
    Input("dashboard-card-domain-selection-6", "color"),
    Input("switch-domain-measure-view","n_clicks")]
)
def bubble_graph_domain(cr1, cr2, cr3, cr4, cr5, cr6, n):

    trace_selected_number = []
    for i in range(domain_ct):
        if eval("cr"+str(i+1)) == "info":
            trace_selected_number.append(i)    
    bubble_show_traces = []
    
    bubble_graph_domain=bubblegraph(df_domain_perform,trace_selected_number,'Domain')  
    
    bubble_graph_measure=bubblegraph(df_measure_perform,trace_selected_number,'Measure') 
    
    '''for i in range(len(trace_selected_number)):
        bubble_show_traces.append(bubble_graph_domain[trace_selected_number[i]])'''
    
    if n and n%2 == 1:
        return bubble_graph_measure, "Switch to Domains View" #需要替换成measure的图
        
    return bubble_graph_domain, "Switch to Measures View"
    
        

    

# generate domain-related graph
@app.callback(
    [Output("graph-container-domain-selected-1", "figure"),
    Output("graph-container-domain-selected-2", "figure"),
    Output("card_domain_name", "children")],
    [Input("button-domain-1", "n_clicks"),
    Input("button-domain-2", "n_clicks"),
    Input("button-domain-3", "n_clicks"),
    Input("button-domain-4", "n_clicks"),
    Input("button-domain-5", "n_clicks"),
    Input("button-domain-6", "n_clicks")]
)
def generate_domain_related_graph(b1, b2, b3, b4, b5, b6):
    ctx = dash.callback_context

    fig1 = waterfall_domain1
    fig2 = domain1_perform
    name = domain_set[0]
    
    
    if ctx.triggered[0]['value'] == None:
        button_id = "button-domain-1"
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    

    if button_id == "button-domain-1":
        fig1 = waterfall_domain1
        fig2 = domain1_perform
        name = domain_set[0]
    elif button_id == "button-domain-2":
        fig1 = waterfall_domain2
        fig2 = domain2_perform
        name = domain_set[1]
    elif button_id == "button-domain-3":
        fig1 = waterfall_domain3
        fig2 = domain3_perform
        name = domain_set[2]
    elif button_id == "button-domain-4":
        fig1 = waterfall_domain4
        fig2 = domain4_perform
        name = domain_set[3]
    elif button_id == "button-domain-5":
        fig1 = waterfall_domain5
        fig2 = domain5_perform
        name = domain_set[4]
    elif button_id == "button-domain-6":
        fig1 = waterfall_domain6
        fig2 = domain6_perform
        name = domain_set[5]

    
    return fig1, fig2, name

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

##Domain 1-6

def toggle_collapse_domain_selection_measures(n, is_open):
    if n and n%2 == 1:
        return not is_open, "Collapse"
    elif n and n%2 == 0:
        return not is_open, "Edit"
    return is_open, "Select"

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
    Input("checklist-domain-measures-lv2-1-2", "value"),
    Input("checklist-domain-measures-lv2-1-3", "value"),
    Input("checklist-domain-measures-lv2-1-4", "value")],
)
def toggle_collapse_domain_selection_measures_1(is_open, v1, v2, v3, v4):
    measure_count = len(v1) + len(v2) + len(v3) + len(v4)
    if measure_count > 0 and is_open != True: 
        return  "info", u"{} measures selected".format(measure_count)
    return "light", ""    

## Domain 2
@app.callback(
    [Output("dashboard-card-domain-selection-2", "color"),
    Output("dashboard-card-selected-domain-2", "children")],
    [Input("collapse-2", "is_open"),
    Input("checklist-domain-measures-lv2-2-1", "value"),
    Input("checklist-domain-measures-lv2-2-2", "value"),
    Input("checklist-domain-measures-lv2-2-3", "value")],
)
def toggle_collapse_domain_selection_measures_2(is_open, v1, v2, v3):
    measure_count = len(v1) + len(v2) +len(v3)
    if measure_count > 0 and is_open != True: 
        return  "info", u"{} measures selected".format(measure_count)
    return "light", "" 

## Domain 4
@app.callback(
    [Output("dashboard-card-domain-selection-4", "color"),
    Output("dashboard-card-selected-domain-4", "children")],
    [Input("collapse-4", "is_open"),
    Input("checklist-domain-measures-lv2-4-1", "value")],
)
def toggle_collapse_domain_selection_measures_4(is_open, v1):
    measure_count = len(v1) 
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






if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True, port=8051)
