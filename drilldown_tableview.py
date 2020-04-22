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

#df_drilldown = pd.read_csv("data/drilldown_sample_5.csv")
#df_drilldown["Diff % from Target Utilization"] = df_drilldown.apply(lambda x: format( x['Annualized Utilization'] - x['Target Utilization']/x['Target Utilization'], '.2%'), axis = 1)
#df_drilldown['Diff % from Target Total Cost'] = df_drilldown.apply(lambda x: format( x['Annualized Total Cost'] - x['Target Total Cost']/x['Target Total Cost'], '.2%'), axis = 1)
#df_drilldown['YTD Unit Cost'] = df_drilldown.apply(lambda x: round( x['YTD Total Cost']/x['YTD Utilization'], 2), axis = 1)
#df_drilldown['Annualized Unit Cost'] = df_drilldown.apply(lambda x: round( x['Annualized Total Cost']/x['Annualized Utilization'], 2), axis = 1)
#df_drilldown['Target Unit Cost'] = df_drilldown.apply(lambda x: round( x['Target Total Cost']/x['Target Utilization'], 2), axis = 1)
#df_drilldown['Diff % from Target Unit Cost'] = df_drilldown.apply(lambda x: format( x['Annualized Unit Cost'] - x['Target Unit Cost']/x['Target Unit Cost'], '.2%'), axis = 1)

dimension = {'Age Band' : ['<65', '65-74', '75-85', '>=85'], 'Gender' : ['F', 'M'], 
'Comorbidity Type' : ['Coronary heart disease ', 'Chronic pulmonary disease', 'Renal disease', 'Atrial fibrillation', 'Cerebrovascular disease', 'Diabetes'], 
'Risk Score Band' : ['Low', 'Mid', 'High'], 'NYHA Class' : ['I', 'II', 'III', 'IV'], 
       'Medication Adherence' : ['Compliant', 'Non-compliant'], 'Managing Physician (Group)': ['Group A', 'Group B', 'Group C', 'Group D']}
measure = ['YTD Utilization', 'Annualized Utilization', 'Target Utilization', 'Diff % from Target Utilization',
		'YTD Total Cost', 'Annualized Total Cost', 'Target Total Cost', 'Diff % from Target Total Cost',
		'YTD Unit Cost', 'Annualized Unit Cost', 'Target Unit Cost', 'Diff % from Target Unit Cost']
measure_ori = ['YTD Utilization', 'Annualized Utilization', 'Target Utilization',
		'YTD Total Cost', 'Annualized Total Cost', 'Target Total Cost']
filter_list = {'All' : ['All', 'Heart Failure', 'Renal Failure', 'Pleural effusion', 'Acute myocardial infarction', 'Cardiac Arrhythmia', 'Cardiac arrest and ventricular fibrillation', 'Hypertension',
       'CABG', 'CEA', 'PCI', 'ICD', 'Others', 'Cardiac dysrhythmias', 'Respiratory system and chest symptoms', 'COPD', 'Diabetes', 'AMI', 'Aftercare following surgery', 'Durable Medical Equipment (DME)',
       'Lab/Pathology', 'Radiology', 'Ambulance', 'Observation', 'Outpatient Surgery', 'Administered Drugs', 'Anesthesia', 'Office Visits', 'Surgical', 'Other Services', 'ACE /ARB',
       'Beta Blocker', 'Aldosterone receptor antagonists', 'Vasodilators', 'Diuretics', 'Other Rx', 'Entresto', 'Home Health', 'SNF', 'Hospice'], 
       'IP' : ['All', 'Acute myocardial infarction', 'CABG', 'CEA', 'Cardiac Arrhythmia', 'Cardiac arrest and ventricular fibrillation', 'Heart Failure', 'Hypertension', 'ICD', 'Others', 'PCI', 'Pleural effusion', 'Renal Failure'],
 		'OP ER' : ['All', 'AMI', 'Aftercare following surgery', 'COPD', 'Cardiac dysrhythmias', 'Diabetes', 'Heart Failure', 'Hypertension', 'Others', 'Respiratory system and chest symptoms'], 
 		'OP Others' : ['All', 'Ambulance', 'Durable Medical Equipment (DME)', 'Lab/Pathology', 'Observation', 'Others', 'Outpatient Surgery', 'Radiology'], 
 		'PH' : ['All', 'Administered Drugs', 'Anesthesia', 'Lab/Pathology', 'Office Visits', 'Other Services', 'Radiology', 'Surgical'], 
 		'Drug - Others' : ['All', 'ACE /ARB', 'Aldosterone receptor antagonists', 'Beta Blocker', 'Diuretics', 'Other Rx', 'Vasodilators'], 
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
									html.H4("Select Dimension", style={"font-size":"1rem","padding-left":"0.5rem", "padding-top":"0.5rem"}),
									html.H5("First Dimension", style={"font-size":"0.8rem","color":"#919191","padding-left":"0.5rem", "padding-top":"0.5rem"}),
									dcc.Dropdown(
										id = "dropdown-dimension-1",
										options = [{"label": k, "value": k} for k in list(dimension.keys())],
										placeholder ="...",
										value = 'Risk Score Band',
										clearable = False,
										),
									html.H5("Second Dimension", style={"font-size":"0.8rem","color":"#919191","padding-left":"0.5rem", "padding-top":"0.5rem"}),
									dcc.Dropdown(
										id = "dropdown-dimension-2",
										disabled=True,
										placeholder ="...",
										
										),
									html.H5("Third Dimension", style={"font-size":"0.8rem","color":"#919191","padding-left":"0.5rem", "padding-top":"0.5rem"}),
									dcc.Dropdown(
										id = "dropdown-dimension-3",
										disabled=True,
										placeholder ="...",
										
										),
									html.H4("Select Measures", style={"font-size":"1rem","padding-left":"0.5rem", "padding-top":"1rem"}),
									dcc.Dropdown(
										id = "dropdown-measure-1",
										options = [{"label": k, "value": k} for k in measure],
										value = ['YTD Total Cost', 'Annualized Total Cost', 'Target Total Cost', 'Diff % from Target Total Cost'],
										placeholder ="Select measures",
										multi = True,
										),
								]
							),
							html.Hr(className="ml-1"),
							html.Div(
								[
									html.H4("Filters", style={"font-size":"1rem","padding-left":"0.5rem", "padding-top":"0.5rem"}),
									html.H5("Service Category", style={"font-size":"0.8rem","color":"#919191","padding-left":"0.5rem", "padding-top":"0.5rem"}),
									dcc.Dropdown(
										id = "srvc_cate_filter",
										options = [{"label": k, "value": k} for k in list(filter_list.keys())],
										placeholder = "Select Service Category",
										value = 'All',
										clearable = False,
										),
									html.H5("Sub Category", style={"font-size":"0.8rem","color":"#919191","padding-left":"0.5rem", "padding-top":"0.5rem"}),
									dcc.Dropdown(
										id = "sub_cate_filter",
										placeholder = "Select Sub Category",
										value = 'All',
										clearable = False,
										),
									html.H5("Filter for Dimensions", style={"font-size":"0.8rem","color":"#919191","padding-left":"0.5rem", "padding-top":"0.5rem"}),
									dcc.Dropdown(
										id = "dimension_filter_selection_1",
										options = [{"label": k, "value": k} for k in list(dimension.keys())],
										placeholder = "Add a Filter",
										),
									html.H5("", style={"font-size":"0.8rem"}),
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
										style_header = {'height': 'auto', 'width':'auto','whiteSpace':'normal','font-family':'NotoSans-CondensedLight','font-size':'auto','backgroundColor': '#dce7fc','color':'#1357DD'},
										style_cell = {'font-family':'NotoSans-Condensed','font-size':'0.8rem','textAlign': 'center'},
										#fixed_rows={ 'headers': True, 'data': 0 },
										style_table = {'textAlign': 'center'},
										sort_action='native',
										page_size=200,
										style_data_conditional=[
									        {
									            'if': {'row_index': 'odd'},
									            'backgroundColor': 'rgb(248, 248, 248)'
									        }],
										)
								],
								style={"padding-left":"1rem","padding-right":"1rem","padding-bottom":"1rem","overflow":"scroll",'max-height':'60rem'}
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
