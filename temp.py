# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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

def table_sim_result(df):
    df['scenario']=['Contract','w/o','VBC Payout','Contract with','VBC Payout','(Recommended)','Contract with','VBC Payout','(User Defined)']
    df['Best Estimate']=df['Best Estimate']*1
    df['id']=[i for i in range(0,9)]
    df.set_index('id', inplace=True, drop=False)
   
    table=dash_table.DataTable(
        data=df.to_dict('records'),
        #id=tableid,
        columns=[
        {"name": ["Contract Type","Contract Type"], "id": "scenario"},
        {"name": ["Item","Item"], "id": "Item"},
        {"name": ["","Best Estimate(Mn)"], "id": "Best Estimate",'type':'numeric','editable':True,},
        {"name": [ "Full Range","Low(Mn)"], "id": "Worst",'editable':True,},
        {"name": [ "Full Range","High(Mn)"], "id": "Best",},
        {"name": [ "Likely Range(90% Probability)","Low(Mn)"], "id": "Lower End",},
        {"name": [ "Likely Range(90% Probability)","High(Mn)"], "id": "Higher End" ,},
        ],  
        merge_duplicate_headers=True,
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_data_conditional=[
        {
            'if': {
                'column_id': 'Best',
                'filter_query': '{Worst} > 0.6'
            },
            'backgroundColor': '#3D9970',
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
            { 'if': {'row_index':c }, 
             'color': 'black', 
             'font-family': 'NotoSans-CondensedLight',
             'border-top': '1px solid grey',
             'border-left': '1px solid grey',
             'border-right': '1px solid grey',
             'decimal-separator':',',
              } if c in [0,3,6] else 
            
            { 'if': {'row_index':c }, 
             'color': 'black', 
             'font-family': 'NotoSans-CondensedBlackItalic',
             'border-left': '1px solid grey',
             'border-right': '1px solid grey',
             'text-decoration':'underline'
              } if c in [1,4,7] else 
            { "if": {"row_index":c },
             'font-family': 'NotoSans-CondensedLight',
             'backgroundColor':'rgba(191,191,191,0.7)',
             'color': '#1357DD',
             'fontWeight': 'bold',
             'border-bottom': '1px solid grey',
             'border-left': '1px solid grey',
             'border-right': '1px solid grey',
              } if c in [2,5,8]  else 
            { "if": {"column_id":"scenario" }, 
             'font-family': 'NotoSans-CondensedLight',
             'backgroundColor':'white',
             'color': 'black',
             'fontWeight': 'bold', 
             'text-decoration':'none'
              } for c in range(0,10)
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
            'border':'1px solid grey',
            'text-decoration':'none'
        },
        style_header_conditional=[
            { 'if': {'column_id':'scenario'},
            'backgroundColor': colors['transparent'],
            'color': colors['transparent'],
            'border':'0px'          
            },
            { 'if': {'column_id':'Item'},
            'backgroundColor': colors['transparent'],
            'color': colors['transparent'],
            'border':'0px' , 
            'border-right':'1px solid grey' ,
            },
        ],
        
        
    )
    return table

app = dash.Dash(__name__)

app.layout = html.Div([table_sim_result(df_sim_rev)])

if __name__ == '__main__':
    app.run_server(debug=True, port=8049)