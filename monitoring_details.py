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

from modal_drilldown_tableview import *

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
								html.H2("Volume Based Measure", style={"font-size":"1rem"}),
								html.H4("Volume Based Measure", style={"font-size":"0.8rem", "padding-left":"0.5rem"}),
								html.H4("Volume Based Measure", style={"font-size":"0.8rem", "padding-left":"0.5rem"}),
								html.H4("Volume Based Measure", style={"font-size":"0.8rem", "padding-left":"0.5rem"}),
							]
						)
					],
					className="mr-3",
					style={"border-top":"none", "border-right":"none", "border-bottom":"none", "border-left":"3px solid", "border-radius":"0.5rem", "background-color":"#f5f5f5"}
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
								html.H2("Outcome Based Measure", style={"font-size":"1rem"}),
								html.H4("Outcome Based Measure", style={"font-size":"0.8rem", "padding-left":"0.5rem"}),
								html.H4("Outcome Based Measure", style={"font-size":"0.8rem", "padding-left":"0.5rem"}),
								html.H4("Outcome Based Measure", style={"font-size":"0.8rem", "padding-left":"0.5rem"}),
							]
						)
					],
					className="mr-3",
					style={"border":"none", "border-radius":"0.5rem", "background-color":"#f5f5f5"}
				)
			],
			style={"padding-top":"1rem", "padding-bottom":"1rem"}
		)



def col_content_drilldown():
	return html.Div(
			[
				dbc.Row(
					[
						dbc.Col(card_overview_drilldown(0.08)),
						dbc.Col(card_key_driver_drilldown()),
					]
				),
				card_confounding_factors(),
                html.Div(
                    [
                        modal_drilldown_tableview()
                    ],
                    style={"padding-bottom":"1rem"}
                ),
				card_graph1_performance_drilldown(),
				card_graph2_performance_drilldown(),
				card_table1_performance_drilldown(),
				card_table2_performance_drilldown(),
			]
		)


def card_overview_drilldown(percentage):
    if percentage > 0:
        color = "#dc3545"
        condition = "worse than target"
    elif percentage == 0:
        color = "#1357DD"
        condition = "same as target"
    else:
        color = "#28a745"
        condition = "better than target"

    return html.Div(
			[
				dbc.Row(
                        [
                            dbc.Col(html.H1("Average Episode Cost", style={"font-size":"1.6rem"}), width="auto"),
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H3("worse than target", style={"font-size":"0.8rem", "color":"#fff"}),
                                        html.H2(str(percentage*100)+"%", style={"font-size":"1.2rem", "margin-top":"-9px", "color":"#fff"}),
                                    ],
                                    style={"margin-top":"-20px"}
                                ),
                                style={"height":"2.5rem", "border":"none", "background-color":color, "text-align":"center", "margin-top":"-6px"},
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
                                dbc.Col(element_confounding_factors(0.05, "New technology"), width=3),
                                dbc.Col(element_confounding_factors(-0.02, "Benefit Change"), width=3),
                                dbc.Col(element_confounding_factors(-0.03, "Contracting Change"), width=3),
                                dbc.Col(element_confounding_factors(0.05, "Outlier Impact"), width=3),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def element_confounding_factors(percentage, factor):
    if percentage > 0:
        color = "danger"
    elif percentage == 0:
        color = "secondary"
    else:
        color = "success"

    return dbc.Row(
            [
                dbc.Col(dbc.Badge(str(percentage*100)+"%", color=color, className="mr-1"), width=3, style={"font-family":"NotoSans-SemiBold"}),
                dbc.Col(html.H1(factor, style = {"font-size":"1rem", "padding-top":"0.1rem"}), width=9),
            ],
            style={"padding":"1rem"}
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
                                drillgraph_lv1(df_drilldown,'Age Band')
                            ], 
                            style={"max-height":"80rem"}
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


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
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"max-height":"80rem"})),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )



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
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"max-height":"80rem"})),
                            ],
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
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"max-height":"80rem"})),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )



app.layout = create_layout()


#### callback ####

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


@app.callback(
    [Output('sub_cate_filter', 'options'),
    Output('sub_cate_filter', 'value')],
    [Input('srvc_cate_filter', 'value')]
    )
def sub_filter(v):
    if v:
        sub_filter = filter_list[v]
        return [{"label": k, "value": k} for k in sub_filter],'All'
    return [],''


@app.callback(
    [Output('dimension_filter_1', 'options'),
    Output('dimension_filter_1', 'value')],
    [Input('dimension_filter_selection_1', 'value')]
    )
def filter_dimension_1(v):
    if v:
        return [{"label": k, "value": k} for k in dimension[v]], dimension[v]
    return [],[]

@app.callback(
    [Output('dropdown-dimension-2','options'),
    Output('dropdown-dimension-2','disabled')],
    [Input('dropdown-dimension-1','value')]
    )
def dropdown_menu_2(v):
    if v is None:
        return [], True
    else:
        dropdown_option = []
        for k in list(dimension.keys()):
            if k in v:
                dropdown_option.append({'label' : k, 'value' : k, 'disabled' : True})
            else:
                dropdown_option.append({'label' : k, 'value' : k, 'disabled' : False})
        return dropdown_option, False

@app.callback(
    [Output('dropdown-dimension-3','options'),
    Output('dropdown-dimension-3','disabled')],
    [Input('dropdown-dimension-1','value'),
    Input('dropdown-dimension-2','value')]
    )
def dropdown_menu_3(v1, v2):
    v = [v1, v2]
    if v2 is None:
        return [], True
    else:
        dropdown_option = []
        for k in list(dimension.keys()):
            if k in v:
                dropdown_option.append({'label' : k, 'value' : k, 'disabled' : True})
            else:
                dropdown_option.append({'label' : k, 'value' : k, 'disabled' : False})
        return dropdown_option, False


@app.callback(
    [Output('datatable-tableview', "columns"),
    Output('datatable-tableview', "data")],
    [Input('dropdown-dimension-1','value'),
    Input('dropdown-dimension-2','value'),
    Input('dropdown-dimension-3','value'),
    Input('srvc_cate_filter','value'),
    Input('sub_cate_filter','value'),
    Input('dimension_filter_1','value'),
    Input('dimension_filter_selection_1','value'),
    Input('dropdown-measure-1', 'value')]
    )
def datatable_data_selection(v1, v2, v3, f1, f2, f3, d, m):
    if f1 == 'All':
        cate_cnt = 39
        if f2 == 'All':
            if f3:
                df_drilldown_filtered = df_drilldown[df_drilldown[d].isin(f3)]
            else:
                df_drilldown_filtered = df_drilldown
        else:
            if f3:
                df_drilldown_filtered = df_drilldown[(df_drilldown['Sub Category'].isin([f2])) & (df_drilldown[d].isin(f3))]
            else: 
                df_drilldown_filtered = df_drilldown[df_drilldown['Sub Category'].isin([f2])]
    else:
        cate_cnt = len(filter[f1])-1
        if f2 == 'All':
            if f3:
                df_drilldown_filtered = df_drilldown[(df_drilldown['Service Category'].isin([f1])) & (df_drilldown[d].isin(f3))]
            else:
                df_drilldown_filtered = df_drilldown[df_drilldown['Service Category'].isin([f1])]
        else: 
            if f3:
                df_drilldown_filtered = df_drilldown[(df_drilldown['Service Category'].isin([f1])) & (df_drilldown['Sub Category'].isin([f2])) & (df_drilldown[d].isin(f3))]
            else: 
                df_drilldown_filtered = df_drilldown[(df_drilldown['Service Category'].isin([f1])) & (df_drilldown['Sub Category'].isin([f2]))]
        
    table_column = []
    selected_dimension = []
    if v1 is not None:
        selected_dimension.append(v1)
    if v2 is not None:
        selected_dimension.append(v2)
    if v3 is not None:
        selected_dimension.append(v3)

    table_column.extend(selected_dimension)
    table_column.append("Pt Count")
    percent_list = ['Diff % from Target Utilization', 'Diff % from Target Total Cost', 'Diff % from Target Unit Cost']
    if len(selected_dimension) > 0:
        table_column.extend(measure_ori) 
        df_agg = df_drilldown_filtered[table_column].groupby(by = selected_dimension).sum()
        df_agg['Pt Count'] = df_agg['Pt Count']/cate_cnt
        df_agg['YTD Utilization'] = df_agg['YTD Utilization']/df_agg['Pt Count']
        df_agg['Annualized Utilization'] = df_agg['Annualized Utilization']/df_agg['Pt Count']
        df_agg['Target Utilization'] = df_agg['Target Utilization']/df_agg['Pt Count']
        df_agg['Diff % from Target Utilization'] = (df_agg['Annualized Utilization'] - df_agg['Target Utilization'])/df_agg['Target Utilization']
        df_agg['YTD Total Cost'] = df_agg['YTD Total Cost']/df_agg['Pt Count']
        df_agg['Annualized Total Cost'] = df_agg['Annualized Total Cost']/df_agg['Pt Count']
        df_agg['Target Total Cost'] = df_agg['Target Total Cost']/df_agg['Pt Count']
        df_agg['Diff % from Target Total Cost'] = (df_agg['Annualized Total Cost'] - df_agg['Target Total Cost'])/df_agg['Target Total Cost']
        df_agg['YTD Unit Cost'] = df_agg['YTD Total Cost']/df_agg['YTD Utilization']
        df_agg['Annualized Unit Cost'] = df_agg['Annualized Total Cost']/df_agg['Annualized Utilization']
        df_agg['Target Unit Cost'] = df_agg['Target Total Cost']/df_agg['Target Utilization']
        df_agg['Diff % from Target Unit Cost'] = (df_agg['Annualized Unit Cost'] - df_agg['Target Unit Cost'])/df_agg['Target Unit Cost']
        df_agg.style.format({'Diff % from Target Utilization' : "{:.2%}", 'Diff % from Target Total Cost': "{:.2%}", 'Diff % from Target Unit Cost' : "{:.2%}"})
        df_agg.reset_index(inplace = True)
        show_column = selected_dimension + ["Pt Count"] + m 
        df_agg = df_agg[show_column]
    else:
        show_column = ["Pt Count"] + m 
        df_agg = df_drilldown_filtered[show_column]
    
    
    return [{"name": i, "id": i, "selectable":True,"type":"numeric", "format": FormatTemplate.percentage(1)} if i in percent_list else {"name": i, "id": i, "selectable":True, "type":"numeric","format": Format(precision=0, scheme = Scheme.fixed)} if i == "Pt Count" else {"name": i, "id": i, "selectable":True, "type":"numeric","format": Format(precision=1, scheme = Scheme.fixed)} for i in show_column], df_agg.to_dict('records')




if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True)









