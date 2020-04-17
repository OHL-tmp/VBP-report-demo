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


# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()



app = dash.Dash(__name__, url_base_pathname='/demo-report/', external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

Domain_options ={
"checklist-domain-measures-lv1-1" : {
    "Average Cost per Patient" : ["All Causes Average Cost per Patient", "CHF Related Average Cost per Patient "],
    "Average IP Cost per Patient" : ["All Causes Average IP Cost per Patient", "CHF Related Average IP Cost per Patient"  ],
    "Hospitalization Rate" : ["All Causes Hospitalization Rate", "CHF Related Hospitalization Rate"],
    "ER Rate" : ["All Causes ER Rate", "CHF Related ER Rate"  ],
    "Readmission Rate" : [],
    "Incidence Rate of Medical Procedures" : []
},

"checklist-domain-measures-lv1-2" : {
    "Improvement in Clinical Measures" : ["NT-proBNP Improvement %", "LVEF Improvement %", "LAVi Improvement %",
                                         "LVEDVi Improvement %", "LVESVi and E/e’ Improvement %"],
    "Functional Outcomes" : ["Change in Self-Care Score", "Change in Mobility Score"  ],
    "Life Expectancy" : ["CV Mortality Rate"],
    "Disease Progression" : ["Rate of CHF Progression for 24 months"],
    "Clinical Measures Adherence Level" : [],
    "Depressive Symptom Measures" : [],
    "Psychosocial Outcome" : []
},

"checklist-domain-measures-lv1-3" : {
    "Benefit Coverage Parity" : [],
    "Screening Rate" : []
},

"checklist-domain-measures-lv1-4" : {
    "Occurrence of Side Effects" : ["Emergent care rate for medication side effect", "Hospitalization rate for medication side effect"],
    "Occurrence of Adverse Event" : [],
    "Occurrence of Complications" : [],
    "Inappropriate Use" :[]
},

"checklist-domain-measures-lv1-5" : {
    "Medication Adherence" : ["DOT", "PDC", "MPR"],
    "Healthcare-Associated Infections" : [],
    "Patient-reported Care quality outcome" : []
},

"checklist-domain-measures-lv1-6" : {
    "Symptom management" : ["Patient Reported SOB changes", "Patient Reported Fatigue and Tiredness Changes",
                           "Patient Reported Peripheral Oedema Changes", "Patient Reported Disturbed Sleep Changes"],
    "Patient Satisfaction" : []
}}

domain_focus = list(Domain_options.keys())

domain_set = ["Cost & Utilization  Reduction", "Improving Disease Outcome",
                 "Decreasing Health Disparities", "Increasing Patient Safety",
                 "Enhancing Care Quality", "Better Patient Experience"]

Triple_Aim_set =["Reducing Cost","Improving Health", "Improving Health","Improving Patient Care",
                "Improving Patient Care","Improving Patient Care"]
Triple_Aim_color = ["#1357DD", "#F5B111","#F5B111", "#df8885", "#df8885", "#df8885"]

domain_ct = len(domain_set)

def modal_dashboard_domain_selection(n):
    return html.Div(
                [
                    dbc.Button("Edit Domain", id="open-centered", className="mb-3", style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"}), 
                    dbc.Modal(
                        [
                            dbc.ModalHeader([
                                dbc.Row([
                                     dbc.Col(html.Div("Select Domain")),
                                     html.Div([
                                         html.Div("Disease"),
                                         dbc.Input(placeholder = "CHF",
                                                  className = "mb-3",
                                                  disabled = True)
                                     ], style = {"display" : "flex"})
                                ]),
                            ]),
                            dbc.ModalBody(
                                card_domain_selection(n)
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Close", id="close-centered", className="ml-auto"
                                )
                            ),
                        ],
                        id="modal-centered",
                        size='lg',
                        scrollable=True,
                    ),
                ]
            )

def card_domain_selection(n):
    domain_card = []
    for i in range(n):
        v = 0
        for m in range(len(list(Domain_options[domain_focus[i]].keys()))):
            v=v+len(list(Domain_options[domain_focus[i]].values())[m])
        if v>0:
            hidden_status = False
        else:
            hidden_status = True    
        card = html.Div([dbc.Card(
                [
                    dbc.CardBody(
                        dbc.Row(
                            [

                                dbc.Col(collapse_domain_selection_measures(i)),
                            ]
                        )
                    ),
                ],
                id=u"dashboard-card-domain-selection-{}".format(i+1),
                className="mb-3"
            )], hidden = hidden_status)
        domain_card.append(card)
    return html.Div(domain_card)

def collapse_domain_selection_measures(n):
    
    return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Badge(Triple_Aim_set[n],style = {"color" : Triple_Aim_color[n]},className="mr-1"),
                            dbc.Col(html.Div(domain_set[n])),
                            dbc.Card(id = u"dashboard-card-selected-domain-{}".format(n+1),
                                    className="mb-3",
                                    color="info"),
                            dbc.Button(
                                children = "Select",
                                id=u"collapse-button-{}".format(n+1),
                                className="mb-3",
                                color="primary",
                            ),
                        ]
                    ),

                    dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Choose Measures", className="card-title"),
                                    checklist_domain_measures_lv1(n),
                                    html.Hr(className="my-2")
                                ]
                            )
                        ),
                        id=u"collapse-{}".format(n+1),
                    ),
                ]
            )

#domain card
def checklist_domain_measures_lv1(d):
    domain_focus = list(Domain_options.keys())
    measures_lv1 = Domain_options[domain_focus[d]]
    key = list(measures_lv1.keys())
    n = len(key)
    button_group = []
    for i in range(n):
        
        if len(measures_lv1[key[i]]) == 0:
            hidden_status = True
        else:
            hidden_status = False
        button_measure_lv1 = html.Div([dbc.FormGroup(
                [
                    dbc.Row([
                        dbc.Button(
                            u"{}".format(key[i]),
                            id=u"measures-lv1-{}-{}".format(d+1,i+1),
                            color = "link",
                            
                        ),
                     dbc.Card(id = u"dashboard-card-selected-{}-{}".format(d+1,i+1),
                                    className="mb-3",
 #                                   color="info"
                             ),   
                    ]),
                    dbc.Collapse(
                           dbc.FormGroup([
                               dbc.Checklist(
                                   options = [{"label" : k, "value": k} for k in measures_lv1[key[i]]],
                                   value=[],
                                   id=u"checklist-domain-measures-lv2-{}-{}".format(d+1,i+1),
                                   inline=True,
                                   persistence = True,
                                   persistence_type = 'session',
                               ),
                           ]),
                        id=u"checklist-domain-measures-lv2-container-{}-{}".format(d+1,i+1),
                    )
                ]
            )],hidden = hidden_status)
        button_group.append(button_measure_lv1)
    return html.Div(button_group)





app.layout = modal_dashboard_domain_selection(domain_ct)





if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True, port = 8051)
