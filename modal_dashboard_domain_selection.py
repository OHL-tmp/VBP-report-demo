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
    "Average IP Cost per Patient" : ["All Causes Average IP Cost per Patient", "CHF Related Average IP Cost per Patient"  ]
},

"checklist-domain-measures-lv1-2" : {
    "Hospitalization Rate" : ["All Causes Hospitalization Rate", "CHF Related Hospitalization Rate"],
    "ER Rate" : ["All Causes ER Rate", "CHF Related ER Rate"  ],
    "Readmission Rate" : [],
    "Incidence Rate of Medical Procedures" : []
},

"checklist-domain-measures-lv1-3" : {
    "Improvement in Clinical Measures" : ["NT-proBNP Improvement %", "LVEF Improvement %", "LAVi Improvement %",
                                         "LVEDVi Improvement %", "LVESVi and E/e’ Improvement %"],
    "Functional Outcomes" : ["Change in Self-Care Score", "Change in Mobility Score"  ],
    "Life Expectancy" : ["CV Mortality Rate"],
    "Disease Progression" : ["Rate of CHF Progression for 24 months"],
    "Clinical Measures Adherence Level" : [],
    "Depressive Symptom Measures" : [],
    "Psychosocial Outcome" : []
},

"checklist-domain-measures-lv1-4" : {
    "Benefit Coverage Parity" : [],
    "Screening Rate" : []
},

"checklist-domain-measures-lv1-5" : {
    "Occurrence of Side Effects" : ["Emergent care rate for medication side effect", "Hospitalization rate for medication side effect"],
    "Occurrence of Adverse Event" : [],
    "Occurrence of Complications" : [],
    "Inappropriate Use" :[]
},

"checklist-domain-measures-lv1-6" : {
    "Medication Adherence" : ["DOT", "PDC", "MPR"],
    "Healthcare-Associated Infections" : [],
    "Patient-reported Care quality outcome" : []
},

"checklist-domain-measures-lv1-7" : {
    "Symptom management" : ["Patient Reported SOB changes", "Patient Reported Fatigue and Tiredness Changes",
                           "Patient Reported Peripheral Oedema Changes", "Patient Reported Disturbed Sleep Changes"],
    "Patient Satisfaction" : []
}}

def modal_dashboard_domain_selection(n):
    return html.Div(
                [
                    dbc.Button("Edit Domain", id="open-centered", className="mb-3", style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"}), 
                    dbc.Modal(
                        [
                            dbc.ModalHeader([
                                html.Div(
                                    [
                                        dbc.Row([
                                             dbc.Col(html.H2("Select Domain", style={"font-size":"2rem"}), width=7),
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
                                                                    html.P("placeholder placeholder placeholder placeholder")
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
        card = dbc.Card(
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
                className="mb-3",
                style={"background-color":"none", "border":"none", "border-radius":"0.5rem"}
            )
        domain_card.append(card)
    return html.Div(domain_card)

def collapse_domain_selection_measures(n):
    domain_set = ["Cost Reduction", "Utilization Reduction", "Improving Disease Outcome",
                 "Decreasing Health Disparities", "Increasing Patient Safety",
                 "Enhancing Care Quality", "Better Patient Experience"]
    return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.Div(
                                    [
                                        dbc.Badge("????",color="primary", className="mr-1"),
                                        domain_set[n],
                                    ],
                                    style={"font-family":"NotoSans-SemiBold", "font-size":"1rem"}
                                )
                            ),
                            html.Div(id = u"dashboard-card-selected-domain-{}".format(n+1),
                                    className="mb-3",
                                    ),
                            dbc.Button(
                                children = "Select",
                                id=u"collapse-button-{}".format(n+1),
                                className="mb-3",
                                style={"margin-right":"20px", "background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"}
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

#domain 1
def checklist_domain_measures_lv1(d):
    domain_focus = list(Domain_options.keys())
    measures_lv1 = Domain_options[domain_focus[d]]
    key = list(measures_lv1.keys())
    n = len(key)
    button_group = []
    for i in range(n):
        
        if len(measures_lv1[key[i]]) == 0:
            disable_status = True
        else:
            disable_status = False
        button_measure_lv1 = dbc.FormGroup(
                [
                    dbc.Row([
                        dbc.Button(
                            u"{}".format(key[i]),
                            id=u"measures-lv1-{}-{}".format(d+1,i+1),
                            color = "link",
                            disabled = disable_status,
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
            )
        button_group.append(button_measure_lv1)
    return html.Div(button_group)




app.layout = modal_dashboard_domain_selection(7)





if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True, port = 8051)
