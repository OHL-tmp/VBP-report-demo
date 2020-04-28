#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:10:52 2020
@author: yanen
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
from launch_page import app

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve(app)
DATA_PATH = BASE_PATH.joinpath("Data").resolve(app)




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

'''def generate_card_domain_button(color):
    if color == "primary":
        return False
    return True

for i in range(domain_ct):
    app.callback(
        Output(f"buttonGroup-domain-selected-{i+1}", "hidden"),
        [Input(f"dashboard-card-domain-selection-{i+1}", "color")]
    )(generate_card_domain_button)'''
    


'''@app.callback(
    [Output("contract_monitor_card", "hidden"),
    Output("additional_monitor_card", "hidden"),
    Output("switch-contract-additional-view","children")],
    [Input("switch-contract-additional-view","n_clicks")]
)
def switch_monitor_view(n):    
    if n and n%2 == 1:
        return True, False, "Switch to Contract Monitor" 
        
    return False, True, "Switch to Additional Watchlist"
    '''
        

    

# generate domain-related graph
@app.callback(
    [Output("graph-container-domain-selected-1", "children"),
    Output("graph-container-domain-selected-2", "figure"),
    Output("card_domain_name", "children"),
    Output("button-domain-1", "active"),
    Output("button-domain-2", "active"),
    Output("button-domain-3", "active"),
    Output("button-domain-4", "active"),
    Output("button-domain-5", "active"),
    Output("button-domain-6", "active")],
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
    ac = [True, False, False, False, False, False]
    
    
    if ctx.triggered[0]['value'] == None:
        button_id = "button-domain-1"
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    

    if button_id == "button-domain-1":
        fig1 = waterfall_domain1
        fig2 = domain1_perform
        name = domain_set[0]
        ac = [True, False, False, False, False, False]
    elif button_id == "button-domain-2":
        fig1 = waterfall_domain2
        fig2 = domain2_perform
        name = domain_set[1]
        ac = [False, True, False, False, False, False]
    elif button_id == "button-domain-3":
        fig1 = waterfall_domain3
        fig2 = domain3_perform
        name = domain_set[2]
        ac = [False, False, True, False, False, False]
    elif button_id == "button-domain-4":
        fig1 = waterfall_domain4
        fig2 = domain4_perform
        name = domain_set[3]
        ac = [False, False, False, True, False, False]
    elif button_id == "button-domain-5":
        fig1 = waterfall_domain5
        fig2 = domain5_perform
        name = domain_set[4]
        ac = [False, False, False, False, True, False]
    elif button_id == "button-domain-6":
        fig1 = waterfall_domain6
        fig2 = domain6_perform
        name = domain_set[5]
        ac = [False, False, False, False, False, True]

    
    return fig1, fig2, name, ac[0], ac[1], ac[2], ac[3], ac[4], ac[5]

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


# submit measure selection
@app.callback(
    Output("table_measure_watchlist", "children"),
    [Input("close-centered","n_clicks")]+[Input(f"checklist-domain-measures-lv2-{d+1}-{i+1}", "value") for d in range(domain_ct) for i in range(len(list(Domain_options[list(Domain_options.keys())[d]].keys())))],
    )
def generate_measure_watchlist(n, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    submit = len([1 for i in triggered if i == "close-centered.n_clicks"])
    #switch = len([1 for i in triggered if i == "switch-contract-additional-view.n_clicks"])
    measure_to_watch = []
    if submit:
        for i in range(24):
            if eval("v"+str(i+1)) and len(eval("v"+str(i+1))) > 0:
                measure_to_watch.extend(eval("v"+str(i+1)))
    return tbl_non_contract(df_nocontract,measure_to_watch)
