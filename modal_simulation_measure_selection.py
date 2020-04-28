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



app = dash.Dash(__name__)

server = app.server

df_recom_measure = pd.read_csv("data/recom_measure.csv")

Domain_options ={
"checklist-domain-measures-lv1-1" : {
    "Average Cost per Patient" : ["All Causes Average Cost per Patient", "CHF Related Average Cost per Patient"],
    "Average IP Cost per Patient" : ["All Causes Average IP Cost per Patient", "CHF Related Average IP Cost per Patient"  ],
    "Hospitalization Rate" : ["All Causes Hospitalization Rate", "CHF Related Hospitalization Rate"],
    "ER Rate" : ["All Causes ER Rate", "CHF Related ER Rate"  ],
    "Readmission Rate" : [],
    "Incidence Rate of Medical Procedures" : []
},

"checklist-domain-measures-lv1-2" : {
    "Improvement in Clinical Measures" : ["NT-proBNP Change %", "LVEF LS Mean Change %", "LAVi LS Mean Change",
                                         "LVEDVi LS Mean Change", "LVESVi LS Mean Change", "E/e' LS Mean Change"],
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

default_measure = list(df_recom_measure["Measure"])

domain_focus = list(Domain_options.keys())

domain_set = ["Cost & Utilization Reduction", "Improving Disease Outcome",
                 "Decreasing Health Disparities", "Increasing Patient Safety",
                 "Enhancing Care Quality", "Better Patient Experience"]
domain_measure = {"Cost & Utilization Reduction" : 8, "Improving Disease Outcome" : 10,
                 "Decreasing Health Disparities" : 0, "Increasing Patient Safety" : 2,
                 "Enhancing Care Quality" : 3, "Better Patient Experience" : 4}

Triple_Aim_set =["Reducing Cost","Improving Health", "Improving Health","Improving Patient Care",
                "Improving Patient Care","Improving Patient Care"]
Triple_Aim_color = ["#1db954", "#ffa319","#ffa319", "#6147d6", "#6147d6", "#6147d6"]

dollar_input = ["All Causes Average Cost per Patient", "CHF Related Average Cost per Patient", "All Causes Average IP Cost per Patient", "CHF Related Average IP Cost per Patient"]

percent_input = ["All Causes Hospitalization Rate", "CHF Related Hospitalization Rate", "All Causes ER Rate", "CHF Related ER Rate",
"NT-proBNP Change %", "LVEF LS Mean Change %",
"CV Mortality Rate", "Rate of CHF Progression for 24 months", "Emergent care rate for medication side effect", "Hospitalization rate for medication side effect"]


domain_ct = len(domain_set)

def modal_optimizer_domain_selection(n):
    return html.Div(
                [
                    dbc.Button("Edit Measure", id="open-centered", className="mb-3", style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"}), 
                    dbc.Modal(
                        [
                            dbc.ModalHeader([
                                html.Div(
                                    [
                                        dbc.Row([
                                             dbc.Col(html.H2("Select Measures", style={"font-size":"2rem"}), width=7),
                                             dbc.Col(
                                                [
                                                    dbc.Card(
                                                        dbc.CardBody(
                                                            [
                                                                html.Div(
                                                                    [
                                                                        dbc.Row(
                                                                            [
                                                                                dbc.Col(html.H2("Disease", style={"font-size":"1rem","padding":"0.6rem"})),
                                                                                dbc.Col(dbc.Input(placeholder = "CHF",className = "mb-3",disabled = True, style={"font-family":"NotoSans-SemiBold", "font-size":"1rem", "border":"none"}))
                                                                            ]
                                                                        )
                                                                    ],
                                                                    style={"margin-top":"-1rem"}
                                                                ),
                                                                html.Div(
                                                                    [
                                                                    dbc.Row(
                                                                            [
                                                                                dbc.Col(html.H2("Brand Name", style={"font-size":"1rem","padding":"0.6rem"})),
                                                                                dbc.Col(dbc.Input(placeholder = "Entresto",className = "mb-3",disabled = True, style={"font-family":"NotoSans-SemiBold", "font-size":"1rem", "border":"none"}))
                                                                            ]
                                                                        ),
                                                                    html.P("25 out of XX measures XXX", style={"font-size":"0.7rem"}),
                                                                    ]
                                                                )
                                                            ],
                                                            style={"background-color":"#none", "border":"none", "border-radius":"0.5rem"}
                                                        )
                                                    )
                                                ],
                                                width=5
                                            )
                                             
                                        ]),
                                    ]
                                )
                            ],
                            style={"background-image":"url('./assets/domain_selection_bg_s.png')","backgroud-size":"auto"}
                            ),
                            dbc.ModalBody(
                                card_domain_selection(n)
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "SUBMIT", id="close-centered", className="ml-auto",
                                    style={"margin-right":"20px", "background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Black", "font-size":"1rem"}
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
                outline=True,
                id=u"dashboard-card-domain-selection-{}".format(i+1),
                className="mb-3",
                style={"border-radius":"0.5rem"}
            )], hidden = hidden_status)
        domain_card.append(card)
    return html.Div(domain_card)

def collapse_domain_selection_measures(n):
    
    return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.Div([Triple_Aim_set[n]], className="mr-1", style={"font-family":"NotoSans-Condensed", "font-size":"0.8rem","color":"#fff","padding-right":"0.4rem","padding-left":"0.4rem","margin-top":"0.2rem","border":"none","border-radius":"5rem","background-color":Triple_Aim_color[n]}), width="auto"),
                            dbc.Col(html.Div(domain_set[n]),
                                    style={"font-family":"NotoSans-SemiBold", "font-size":"1rem"}
                                ),
                            html.Div(id = u"dashboard-card-selected-domain-{}".format(n+1),
                                    className="mb-3",
                                    style={"font-family":"NotoSans-Condensed","font-size":"1rem","padding-right":"1rem"}),
                            dbc.Button(
                                children = "Select",
                                id=u"collapse-button-{}".format(n+1),
                                color="primary",
                                className="mr-1",
                                style={"margin-right":"20px", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem", "height":"1.6rem"}
                            ),
                        ]
                    ),

                    dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H2("Choose Measures", className="card-title", style={"font-family":"NotoSans-Condensed","font-size":"01rem","color":"#a1a1a1"}),
                                    checklist_domain_measures_lv1(n)
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
        default = []    
        for v in measures_lv1[key[i]]:
            if v in default_measure:
                default.append(v)
        button_measure_lv1 = html.Div([dbc.FormGroup(
                [
                    dbc.Row([
                        dbc.Button(
                            u"{}".format(key[i]),
                            id=u"measures-lv1-{}-{}".format(d+1,i+1),
                            color = "light",
                            style={"background-color":"#ebebeb","border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem", "height":"2rem"}
                        ),
                        html.Div(
                            [
                                dbc.Badge(id = u"dashboard-card-selected-{}-{}".format(d+1,i+1),
                                    color="primary",
                                    className="ml-1",
                                    #style={"padding":"0.8rem"}
                                 ),   
                            ],
                            #style={"margin-top":"0.8rem","margin-bottom":"0.8rem"}
                        )
                        
                        ]),
                    dbc.Collapse(
                           dbc.FormGroup([
                               dbc.Checklist(
                                   options = [{"label" : k, "value": k} for k in measures_lv1[key[i]]],
                                   value=default,
                                   id=u"checklist-domain-measures-lv2-{}-{}".format(d+1,i+1),
                                   inline=True,
                                   persistence = True,
                                   persistence_type = 'session',
                               ),
                               html.Hr(className="my-2")
                           ]),
                        id=u"checklist-domain-measures-lv2-container-{}-{}".format(d+1,i+1),
                        style={"margin-top":"1rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}
                    )
                ]
            )],
            hidden = hidden_status,
            style={"padding-left":"2rem", "padding-right":"2rem"})
        button_group.append(button_measure_lv1)
    return html.Div(button_group)


