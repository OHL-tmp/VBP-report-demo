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


app = dash.Dash(__name__, url_base_pathname='/vbc-demo/dashboard/')

server = app.server

df_drilldown = pd.read_csv("data/drilldown_sample_2.csv")
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
filter = {'All' : ['All', 'Heart Failure', 'Renal Failure', 'Pleural effusion', 'Acute myocardial infarction', 'Supraventricular tachycardia', 'Cardiac arrest and ventricular fibrillation', 'Hypertension',
       'Others', 'Respiratory disease', 'Cardiac rhythm monitoring', 'Myocardial infarction', 'Anaemia', 'Hypotension', 'Stroke', 'Surgery', 'Observation', 'Ambulance', 'Radiology',
       'Lab/Pathology', 'DME', 'PCP Visit', 'Specialist Visit', 'Anesthesia', 'ACE', 'ARB', 'AA', 'Beta Blocker', 'Entresto', 'Home Health', 'SNF', 'Hospice'], 
       'IP' : ['All', 'Acute myocardial infarction', 'Cardiac arrest and ventricular fibrillation', 'Heart Failure', 'Hypertension', 'Others', 'Pleural effusion', 'Renal Failure', 'Supraventricular tachycardia'],
 		'OP ER' : ['All', 'Anaemia', 'Cardiac rhythm monitoring', 'Heart Failure', 'Hypotension', 'Myocardial infarction', 'Others', 'Respiratory disease', 'Stroke'], 
 		'OP Others' : ['All', 'Ambulance', 'DME', 'Lab/Pathology', 'Observation', 'Others', 'Radiology', 'Surgery'], 
 		'PH' : ['All', 'Anesthesia', 'Lab/Pathology', 'Others', 'PCP Visit', 'Radiology', 'Specialist Visit', 'Surgery'], 'Drug - Others' : ['All', 'AA', 'ACE', 'ARB', 'Beta Blocker', 'Others'], 
 		'Drug - Entresto': ['All', 'Entresto'], 'Home Health' : ['All', 'Home Health'], 'SNF' : ['All', 'SNF'], 'Hospice' : ['All', 'Hospice']}

def tableview():
	return html.Div([
			dbc.Row([
				dbc.Col([
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
					], width = 3),
				dbc.Col([
					dash_table.DataTable(
						id = 'datatable-tableview',
						style_header = {'height': 'auto','width':'10px', 'minwidth':'10px', 'maxwidth': '10px'},
						)
					], width = 6),
				dbc.Col([
					html.H5("Filters"),
					html.H6("Service Category"),
					dcc.Dropdown(
						id = "srvc_cate_filter",
						options = [{"label": k, "value": k} for k in list(filter.keys())],
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

					], width = 3),
				])
		])

app.layout = tableview()

@app.callback(
	[Output('sub_cate_filter', 'options'),
	Output('sub_cate_filter', 'value')],
	[Input('srvc_cate_filter', 'value')]
	)
def sub_filter(v):
	if v:
		sub_filter = filter[v]
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
    app.run_server(host="127.0.0.1",debug=True, port=8051)