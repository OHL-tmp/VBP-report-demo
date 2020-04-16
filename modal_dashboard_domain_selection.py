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
                className="mb-3"
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
                                    eval("checklist_domain_measures_lv1_"+str(n+1)+"()"),
                                    html.Hr(className="my-2"),
                                    html.Div([
                                               dbc.FormGroup([
                                                   dbc.Checklist(
                                                       value=[],
                                                       id=u"checklist-domain-measures-lv2-{}".format(n+1),
                                                       inline=True,
                                                       persistence = True,
                                                       persistence_type = 'session',
                                                   ),
                                               ]),
                                            ],id=u"checklist-domain-measures-lv2-container-{}".format(n+1)),
                                ]
                            )
                        ),
                        id=u"collapse-{}".format(n+1),
                    ),
                ]
            )

#domain 1
def checklist_domain_measures_lv1_1():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Average Cost per Patient", "value": "Average Cost per Patient"},
                            {"label": "Average IP Cost per Patient", "value":  "Average IP Cost per Patient"},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv1-1",
                        inline=True,
                    ),
                ]
            )


def checklist_domain_measures_lv2_1():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        
                        value=[],
                        id="checklist-domain-measures-lv2-1",
                        inline=True,
                        persistence = True,
                        persistence_type = 'session',
                    ),
                ]
            )

#domain 2
def checklist_domain_measures_lv1_2():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Hospitalization Rate", "value": "Hospitalization Rate"},
                            {"label": "ER Rate", "value": "ER Rate"},
                            {"label": "Readmission Rate", "value": "Readmission Rate", "disabled" : True},
                            {"label": "Incidence Rate of Medical Procedures", "value": "Incidence Rate of Medical Procedures", "disabled" : True},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv1-2",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2_2():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Option 1", "value": 1},
                            {"label": "Option 2", "value": 2},
                            {"label": "Option 3", "value": 3},
                            {"label": "Option 4", "value": 4},
                            {"label": "Option 5", "value": 5},
                            {"label": "Option 6", "value": 6},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv2-2",
                        inline=True,
                    ),
                ]
            )

#domain 3
def checklist_domain_measures_lv1_3():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Improvement in Clinical Measures", "value": "Improvement in Clinical Measures"},
                            {"label": "Functional Outcomes", "value": "Functional Outcomes"},
                            {"label": "Life Expectancy", "value": "Life Expectancy"},
                            {"label": "Disease Progression", "value": "Disease Progression"},
                            {"label": "Clinical Measures Adherence Level", "value": "Clinical Measures Adherence Level", "disabled" : True},
                            {"label": "Depressive Symptom Measures", "value": "Depressive Symptom Measures", "disabled" : True},
                            {"label": "Psychosocial Outcome", "value": "Psychosocial Outcome", "disabled" : True},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv1-3",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2_3():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Option 1", "value": 1},
                            {"label": "Option 2", "value": 2},
                            {"label": "Option 3", "value": 3},
                            {"label": "Option 4", "value": 4},
                            {"label": "Option 5", "value": 5},
                            {"label": "Option 6", "value": 6},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv2-3",
                        inline=True,
                    ),
                ]
            )

#domain 4
def checklist_domain_measures_lv1_4():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Benefit Coverage Parity", "value": "Benefit Coverage Parity", "disabled" : True},
                            {"label": "Screening Rate", "value": "Screening Rate", "disabled" : True},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv1-4",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2_4_1():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Option 1", "value": 1},
                            {"label": "Option 2", "value": 2},
                            {"label": "Option 3", "value": 3},
                            {"label": "Option 4", "value": 4},
                            {"label": "Option 5", "value": 5},
                            {"label": "Option 6", "value": 6},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv2-4",
                        inline=True,
                    ),
                ]
            )

#domain 5
def checklist_domain_measures_lv1_5():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Occurrence of Side Effects", "value": "Occurrence of Side Effects"},
                            {"label": "Occurrence of Adverse Event", "value": "Occurrence of Adverse Event", "disabled" : True},
                            {"label": "Occurrence of Complications", "value": "Occurrence of Complications", "disabled" : True},
                            {"label": "Inappropriate Use", "value": "Inappropriate Use", "disabled" : True},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv1-5",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2_5_1():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Option 1", "value": 1},
                            {"label": "Option 2", "value": 2},
                            {"label": "Option 3", "value": 3},
                            {"label": "Option 4", "value": 4},
                            {"label": "Option 5", "value": 5},
                            {"label": "Option 6", "value": 6},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv2-5",
                        inline=True,
                    ),
                ]
            )


#domain 6
def checklist_domain_measures_lv1_6():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Medication Adherence", "value": "Medication Adherence"},
                            {"label": "Healthcare-Associated Infections", "value": "Healthcare-Associated Infections", "disabled" : True},
                            {"label": "Patient-reported Care quality outcome", "value": "Patient-reported Care quality outcome", "disabled" : True},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv1-6",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2_6_1():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Option 1", "value": 1},
                            {"label": "Option 2", "value": 2},
                            {"label": "Option 3", "value": 3},
                            {"label": "Option 4", "value": 4},
                            {"label": "Option 5", "value": 5},
                            {"label": "Option 6", "value": 6},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv2-6",
                        inline=True,
                    ),
                ]
            )

#domain 7
def checklist_domain_measures_lv1_7():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Symptom management", "value": "Symptom management"},
                            {"label": "Patient Satisfaction", "value": "Patient Satisfaction", "disabled" : True},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv1-7",
                        inline=True,
                    ),
                ]
            )

def checklist_domain_measures_lv2_7_1():
    return dbc.FormGroup(
                [
                    #dbc.Label("Choose measures"),
                    dbc.Checklist(
                        options=[
                            {"label": "Option 1", "value": 1},
                            {"label": "Option 2", "value": 2},
                            {"label": "Option 3", "value": 3},
                            {"label": "Option 4", "value": 4},
                            {"label": "Option 5", "value": 5},
                            {"label": "Option 6", "value": 6},
                        ],
                        value=[],
                        id="checklist-domain-measures-lv2-7",
                        inline=True,
                    ),
                ]
            )


app.layout = modal_dashboard_domain_selection(7)





if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True, port = 8051)
