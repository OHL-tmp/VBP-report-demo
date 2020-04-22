import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash_table.FormatTemplate as FormatTemplate

import pandas as pd
import numpy as np

import pathlib
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash_table.Format import Format, Scheme



'''app = dash.Dash(__name__, url_base_pathname='/vbc-demo/dashboard/')

server = app.server'''

df_drilldown = pd.read_csv("data/drilldown_sample_2.csv",nrows=500)
#df_drilldown["Diff % from Target Utilization"] = df_drilldown.apply(lambda x: format( x['Annualized Utilization'] - x['Target Utilization']/x['Target Utilization'], '.2%'), axis = 1)
#df_drilldown['Diff % from Target Total Cost'] = df_drilldown.apply(lambda x: format( x['Annualized Total Cost'] - x['Target Total Cost']/x['Target Total Cost'], '.2%'), axis = 1)
#df_drilldown['YTD Unit Cost'] = df_drilldown.apply(lambda x: round( x['YTD Total Cost']/x['YTD Utilization'], 2), axis = 1)
#df_drilldown['Annualized Unit Cost'] = df_drilldown.apply(lambda x: round( x['Annualized Total Cost']/x['Annualized Utilization'], 2), axis = 1)
#df_drilldown['Target Unit Cost'] = df_drilldown.apply(lambda x: round( x['Target Total Cost']/x['Target Utilization'], 2), axis = 1)
#df_drilldown['Diff % from Target Unit Cost'] = df_drilldown.apply(lambda x: format( x['Annualized Unit Cost'] - x['Target Unit Cost']/x['Target Unit Cost'], '.2%'), axis = 1)

dimension = {'Age Band' : ['<65', '65-75', '75-85', '>85'], 'Gender' : ['F', 'M'], 'Comorbidity Type' : ['Coronary heart disease ', 'Chronic pulmonary disease',
       'Renal disease', 'Atrial fibrillation', 'Cerebrovascular disease','Diabetes'], 'Risk Score Band' : ['<1.0', '1.0-2.0', '2.0-3.0', '>3.0'], 'NYHA Class' : ['I', 'II', 'III', 'IV'], 
       'Medication Adherence' : ['Compliant', 'Non-compliant'], 'Managing Physician (Group)': ['Group A', 'Group B', 'Group C', 'Group D', 'Group E', 'Group F']}
measure = ['YTD Utilization', 'Annualized Utilization', 'Target Utilization', 'Diff % from Target Utilization',
		'YTD Total Cost', 'Annualized Total Cost', 'Target Total Cost', 'Diff % from Target Total Cost',
		'YTD Unit Cost', 'Annualized Unit Cost', 'Target Unit Cost', 'Diff % from Target Unit Cost']
measure_ori = ['YTD Utilization', 'Annualized Utilization', 'Target Utilization',
		'YTD Total Cost', 'Annualized Total Cost', 'Target Total Cost']
filter_list = {'All' : ['All', 'Heart Failure', 'Renal Failure', 'Pleural effusion', 'Acute myocardial infarction', 'Supraventricular tachycardia', 'Cardiac arrest and ventricular fibrillation', 'Hypertension',
       'Others', 'Respiratory disease', 'Cardiac rhythm monitoring', 'Myocardial infarction', 'Anaemia', 'Hypotension', 'Stroke', 'Surgery', 'Observation', 'Ambulance', 'Radiology',
       'Lab/Pathology', 'DME', 'PCP Visit', 'Specialist Visit', 'Anesthesia', 'ACE', 'ARB', 'AA', 'Beta Blocker', 'Entresto', 'Home Health', 'SNF', 'Hospice'], 
       'IP' : ['All', 'Acute myocardial infarction', 'Cardiac arrest and ventricular fibrillation', 'Heart Failure', 'Hypertension', 'Others', 'Pleural effusion', 'Renal Failure', 'Supraventricular tachycardia'],
 		'OP ER' : ['All', 'Anaemia', 'Cardiac rhythm monitoring', 'Heart Failure', 'Hypotension', 'Myocardial infarction', 'Others', 'Respiratory disease', 'Stroke'], 
 		'OP Others' : ['All', 'Ambulance', 'DME', 'Lab/Pathology', 'Observation', 'Others', 'Radiology', 'Surgery'], 
 		'PH' : ['All', 'Anesthesia', 'Lab/Pathology', 'Others', 'PCP Visit', 'Radiology', 'Specialist Visit', 'Surgery'], 'Drug - Others' : ['All', 'AA', 'ACE', 'ARB', 'Beta Blocker', 'Others'], 
 		'Drug - Entresto': ['All', 'Entresto'], 'Home Health' : ['All', 'Home Health'], 'SNF' : ['All', 'SNF'], 'Hospice' : ['All', 'Hospice']}

def tableview():
	return html.Div(
		[
			dbc.Row(
				[
					dbc.Col(
						[
							html.Div(
								[
									html.H5("Select Dimension"),
									dcc.Dropdown(
										id = "dropdown-dimension-1",
										options = [{"label": k, "value": k} for k in list(dimension.keys())],
										placeholder ="Select a dimension",
										
										),
									dcc.Dropdown(
										id = "dropdown-dimension-2",
										disabled=True,
										placeholder ="Select a dimension",
										
										),
									dcc.Dropdown(
										id = "dropdown-dimension-3",
										disabled=True,
										placeholder ="Select a dimension",
										
										),
									html.H5("Select Measures"),
									dcc.Dropdown(
										id = "dropdown-measure-1",
										options = [{"label": k, "value": k} for k in measure],
										value = measure_ori,
										placeholder ="Select measures",
										multi = True,
										),
								]
							),
							html.Div(
								[
									html.H5("Filters"),
									html.H6("Service Category"),
									dcc.Dropdown(
										id = "srvc_cate_filter",
										options = [{"label": k, "value": k} for k in list(filter_list.keys())],
										placeholder = "Select Service Category",
										value = 'All',
										),
									html.H6("Sub Category"),
									dcc.Dropdown(
										id = "sub_cate_filter",
										placeholder = "Select Sub Category",
										),
									html.H6("Filter for Dimensions"),
									dcc.Dropdown(
										id = "dimension_filter_selection_1",
										options = [{"label": k, "value": k} for k in list(dimension.keys())],
										placeholder = "Add a Filter",
										),
									dcc.Dropdown(
										id = "dimension_filter_1",
										placeholder = "Select Sub Category",
										multi = True,
										),
								]
							)
						],
						width=3,
						style={"overflow-y":"scroll"}
					),
						
					dbc.Col(
						[
							html.Div(
								[
									dash_table.DataTable(
										id = 'datatable-tableview',
										style_header = {'height': 'auto', 'width':'auto','whiteSpace':'normal','font-family':'NotoSans-CondensedLight','font-size':'auto'},
										style_cell = {'font-family':'NotoSans-Condensed','font-size':'0.8rem'},
										#fixed_rows={ 'headers': True, 'data': 0 },
										style_table = {'textAlign': 'center'},
										sort_action='native',
										page_size=200,
										)
								],
								style={"padding-left":"1rem","padding-bottom":"1rem","overflow-x":"scroll",'max-height':'60rem'}
							)
							
						],
						width = 9,
						
					),
				]
			)
		]
	)

# app.layout = tableview()

'''
if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True, port=8051)'''