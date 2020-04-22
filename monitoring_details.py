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

df_drilldown=pd.read_csv("data/Drilldown sample V5.csv")
dimensions=df_drilldown.columns[0:12]

all_dimension=[]
for i in list(df_drilldown.columns[0:14]):
    all_dimension.append([i,'All'])
    for j in list(df_drilldown[i].unique()):
        all_dimension.append([i,j])
all_dimension=pd.DataFrame(all_dimension,columns=['dimension','value'])

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()


app = dash.Dash(__name__, url_base_pathname='/vbc-demo/monitor/')

server = app.server

def create_layout():
#    load_data()
    return html.Div(
                [ 
                    html.Div([Header_mgmt(app)], style={"height":"6rem"}),
                    
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(html.Div(
		                                    	[
		                                    		col_menu_drilldown(),
		                                    	]
		                                    ),
                                   		width=3),
                                    dbc.Col(col_content_drilldown(), width=9),
                                ]
                            ),
                        ],
                        className="mb-3",
                    ),
                    
                ],
                style={"padding-left":"3rem", "padding-right":"3rem", "background-color":"#f5f5f5"},
            )


def col_menu_drilldown():

	return html.Div(
				[
					card_menu_volumn_based_measure(),
					card_menu_outcome_based_measure(),
				]
			)


def card_menu_volumn_based_measure():
	return html.Div(
			[
				dbc.Card(
					[
						dbc.CardBody(
							[
								html.H2("Volume Based Measure"),
								html.H4("Volume Based Measure"),
								html.H4("Volume Based Measure"),
								html.H4("Volume Based Measure"),
							]
						)
					],
					className="mr-3",
					style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
				)
			],
			style={"padding-top":"1rem", "padding-bottom":"1rem"}
		)

def card_menu_outcome_based_measure():
	return html.Div(
			[
				dbc.Card(
					[
						dbc.CardBody(
							[
								html.H2("Outcome Based Measure"),
								html.H4("Outcome Based Measure"),
								html.H4("Outcome Based Measure"),
								html.H4("Outcome Based Measure"),
							]
						)
					],
					className="mr-3",
					style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
				)
			],
			style={"padding-top":"1rem", "padding-bottom":"1rem"}
		)



def col_content_drilldown():
	return html.Div(
			[
				dbc.Row(
					[
						dbc.Col(card_overview_drilldown()),
						dbc.Col(card_key_driver_drilldown()),
					]
				),
				card_confounding_factors(),
				card_graph1_performance_drilldown(),
				card_graph2_performance_drilldown(),
				card_table1_performance_drilldown(),
				card_table2_performance_drilldown(),
			]
		)


def card_overview_drilldown():
	return html.Div(
			[
				dbc.Row(
                        [
                            dbc.Col(html.H1("Average Episode Cost"), width="auto"),
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H3("worse than target", style={"font-size":"0.5rem", "color":"#fff"}),
                                        html.H2("8%", style={"font-size":"1.5rem", "margin-top":"-5px", "color":"#fff"}),
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
                            html.Img(src=app.get_asset_url("logo-demo.png")),
                        ],
                    ),
                ],
		)


def card_key_driver_drilldown():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
		                        dbc.Col(html.H4("Key Dribvers", style={"font-size":"1rem", "margin-left":"10px"})),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=6),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=6),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=6),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=6),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=6),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem"}
            )



def card_confounding_factors():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Confounding Factors Unaccounted for in the Contract", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=3),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=3),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=3),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem"}), width=3),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def card_graph1_performance_drilldown():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Performance Drilldown by Patient Cohort: By Comorbidity Type", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                         html.Div(
                            [
                                html.Div( mod_criteria_button()), 
                                html.Div(drillgraph_lv1(drilldata_process(df_drilldown,'Risk Score Band'),'dashtable_lv1'),id="drill_lv1",style={"padding-top":"2rem","padding-bottom":"2rem"}), 
                            ], 
                            style={"max-height":"80rem"}
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def mod_criteria_button():
    return [
                                dbc.Button(
                                    "Modify criteria",
                                    id="button-mod-dim-lv1",
                                    className="mb-3",
                                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},
                                ),
                                dbc.Popover([
                                    dbc.PopoverHeader("Modify criteria"),
                                    dbc.PopoverBody([
                                        html.Div(
                                            [
                                                dbc.RadioItems(
                                                    options = [{'label':c , 'value':c} for c in dimensions
                                                              ],
                                                    value = "Risk Score Band",
                                                    labelCheckedStyle={"color": "#057aff"},
                                                    id = "list-dim-lv1",
                                                    style={"font-family":"NotoSans-Condensed", "font-size":"0.8rem", "padding":"1rem"},
                                                ),
                                            ],
                                            style={"padding-top":"0.5rem", "padding-bottom":"2rem"}
                                        )
                                         
                                       
                                        
                                    ]
                                    ),
                                ],
                                id = "popover-mod-dim-lv1",
                                is_open = False,
                                target = "button-mod-dim-lv1",
                                placement = "top",
                                ),
                                
                            ]
    

    
def card_graph2_performance_drilldown():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Performance Drilldown by Provider: By Physician Group", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col([html.Div("Risk Score Band",id="filter1_2_name"),
                                         html.Div(filter_template("Risk Score Band","filter1_2_value",default_val='All')),
                                         html.Div(drillgraph_lv1(drilldata_process(df_drilldown,'Managing Physician (Group)'),'dashtable_lv2'),id="drill_lv2",style={"padding-top":"2rem","padding-bottom":"2rem"}), 
                     ]
                   , style={"max-height":"80rem"}),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def filter_template(dim,idname,default_val='All'):
    return(dcc.Dropdown(
                                id=idname,
                                options=[{'label': i, 'value': i} for i in all_dimension[all_dimension['dimension']==dim].loc[:,'value']],
                                value=default_val
                            ))

def card_table1_performance_drilldown():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Performance by Drilldown Service Categories", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col( [html.Div("Risk Score Band",id="filter1_3_name"),
                                        html.Div(filter_template("Risk Score Band","filter1_3_value",default_val='All')),
                                        html.Div("Managing Physician (Group)",id="filter2_3_name"),
                                        html.Div(filter_template("Managing Physician (Group)","filter2_3_value",default_val='All')),
                                        html.Div(dashtable_lv3(drilldata_process(df_drilldown,'Service Category'),'Service Category','dashtable_lv3'),id="drill_lv3"),]                                       
                                        ),
                            ],
                         style={"max-height":"80rem"}
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )



def card_table2_performance_drilldown():
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Service Category Drilldown: By Condition", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col([html.Div("Risk Score Band",id="filter1_4_name"),
                                        html.Div(filter_template("Risk Score Band","filter1_4_value",default_val='All')),
                                        html.Div("Managing Physician (Group)",id="filter2_4_name"),
                                        html.Div(filter_template("Managing Physician (Group)","filter2_4_value",default_val='All')),
                                        html.Div("Service Category",id="filter3_4_name"),
                                        html.Div(filter_template("Service Category","filter3_4_value",default_val='All')),
                                        html.Div(dashtable_lv3(drilldata_process(df_drilldown,'Sub Category'),'Sub Category','dashtable_lv4'),id="drill_lv4"),]
                     
                                 ),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

app.layout = create_layout()

# modify lv1 criteria
@app.callback(
    Output("popover-mod-dim-lv1","is_open"),
    [Input("button-mod-dim-lv1","n_clicks"),],
   # Input("mod-button-mod-measure","n_clicks"),
    [State("popover-mod-dim-lv1", "is_open")],
)
def toggle_popover_mod_criteria(n1, is_open):
    if n1 :
        return not is_open
    return is_open

#update lv1 table and filter1 on following page based on criteria button
@app.callback(
   [ Output("drill_lv1","children"),
     Output("filter1_2_name","children"),
     Output("filter1_2_value","options"),
     Output("filter1_3_name","children"),
     Output("filter1_3_value","options"),
     Output("filter1_4_name","children"),
     Output("filter1_4_value","options"),     
   ],
   [Input("list-dim-lv1","value")] 
)
def update_table_dimension(dim):
    f1_name=dim
    filter1_value_list=[{'label': i, 'value': i} for i in all_dimension[all_dimension['dimension']==dim].loc[:,'value']]
    
    return drillgraph_lv1(drilldata_process(df_drilldown,dim),'dashtable_lv1'),f1_name,filter1_value_list,f1_name,filter1_value_list,f1_name,filter1_value_list

#update filter1 on following page based on selected columns

@app.callback(
   [ Output("filter1_2_value","value"),   
     Output("filter1_3_value","value"),  
     Output("filter1_4_value","value"),  
   ],
   [ Input("dashtable_lv1","selected_columns"),
   ] 
)
def update_filter1value(col):
    if col==[]:
        col_1='All'
    else:col_1=col[0]        
    
    return col_1,col_1,col_1

#update filter2 on following page based on selected columns

@app.callback(
   [ Output("filter2_3_value","value"),   
     Output("filter2_4_value","value"),  
   ],
   [ Input("dashtable_lv2","selected_columns"),
   ] 
)
def update_filter2value(col):
    if col==[]:
        col_1='All'
    else:col_1=col[0]        
    
    return col_1,col_1

#update filter3 on following page based on selected rows

'''@app.callback(
   [ Output("filter3_4_value","value"),    
   ],
   [Input("dashtable_lv3","selected_rows"),
    Input("dashtable_lv3","data"),
   ] 
)
def update_filter3value(row,data):
    row_1=row[0]        
    print(data)
    return row_1'''

#update lv2 on filter1

@app.callback(
   [ Output("drill_lv2","children"),    
   ],
   [ Input("filter1_2_name","children"),
     Input("filter1_2_value","value"),
   ] 
)
def update_table2(dim,val):       
    
    return drillgraph_lv1(drilldata_process(df_drilldown,'Managing Physician (Group)',dim1=dim,f1=val),'dashtable_lv2')


#update lv3 on filter1,filter2

@app.callback(
   [ Output("drill_lv3","children"),    
   ],
   [ Input("filter1_3_name","children"),
     Input("filter1_3_value","value"),
     Input("filter2_3_name","children"),
     Input("filter2_3_value","value"),
   ] 
)
def update_table2(dim1,val1,dim2,val2):       
    
    return [dashtable_lv3(drilldata_process(df_drilldown,'Service Category',dim1,val1,dim2,val2),'Service Category','dashtable_lv3')]

#update lv4 on filter1,filter2,filter3

'''@app.callback(
   [ Output("drill_lv4","children"),    
   ],
   [ Input("filter1_4_name","children"),
     Input("filter1_4_value","value"),
     Input("filter2_4_name","children"),
     Input("filter2_4_value","value"),
     Input("filter3_4_name","children"),
     Input("filter3_4_value","value"),
   ] 
)
def update_table2(dim1,val1,dim2,val2,dim3,val3):       
    
    return [dashtable_lv3(drilldata_process(df_drilldown,'Sub Category',dim1,val1,dim2,val2,dim3,val3))],'Sub Category','dashtable_lv4')'''

#drillgraph_lv2=drillgraph_lv1(drilldata_process(df_drilldown,'Managing Physician (Group)',dim1=dim,f1=col_1),'dashtable_lv2')
#drillgraph_lv3=dashtable_lv3(df,tableid)





if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8051)









