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
from launch_page import app



# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("Data").resolve()


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
     Output("dimname_on_lv1","children"),
   ],
   [Input("list-dim-lv1","value")] 
)
def update_table_dimension(dim):
    f1_name=dim
    filter1_value_list=[{'label': i, 'value': i} for i in all_dimension[all_dimension['dimension']==dim].loc[:,'value']]
    
    return drillgraph_lv1(drilldata_process(df_drilldown,dim),'dashtable_lv1'),f1_name,filter1_value_list,f1_name,filter1_value_list,f1_name,filter1_value_list,'By '+f1_name

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

@app.callback(
   Output("filter3_4_value","value"),   
   [Input("dashtable_lv3","selected_row_ids"),
    Input("dashtable_lv3","data"),
   ] 
)
def update_filter3value(row,data):
    
    if row is None or row==[]:
        row_1='All'
    else:
        row_1=row[0]  
    return row_1
    
#update lv2 on filter1

@app.callback(
    Output("drill_lv2","children"),    
   [ Input("filter1_2_name","children"),
     Input("filter1_2_value","value"),
   ] 
)
def update_table2(dim,val):       
    
    return drillgraph_lv1(drilldata_process(df_drilldown,'Managing Physician (Group)',dim1=dim,f1=val),'dashtable_lv2')


#update lv3 on filter1,filter2

@app.callback(
   Output("dashtable_lv3","data"), 
   [ Input("filter1_3_name","children"),
     Input("filter1_3_value","value"),
     Input("filter2_3_name","children"),
     Input("filter2_3_value","value"),
     Input('dashtable_lv3', 'sort_by'),
   ] 
)
def update_table3(dim1,val1,dim2,val2,sort_dim):
    #global data_lv3
    
    data_lv3=drilldata_process(df_drilldown,'Service Category',dim1,val1,dim2,val2)       
    #data_lv3.to_csv('data/overall_performance.csv')
    if sort_dim==[]:
        sort_dim=[{"column_id":"Contribution to Overall Performance Difference","direction":"desc"}]
  
    df1=data_lv3[0:len(data_lv3)-1].sort_values(by=sort_dim[0]['column_id'],ascending= sort_dim[0]['direction']=='asc')
    df1=pd.concat([df1,data_lv3[len(data_lv3)-1:len(data_lv3)]])
    df1['id']=df1[df1.columns[0]]
    df1.set_index('id', inplace=True, drop=False)
    return df1.to_dict('records')



#update lv4 on filter1,filter2,filter3

@app.callback(
    Output("dashtable_lv4","data"),    
   [ Input("filter1_4_name","children"),
     Input("filter1_4_value","value"),
     Input("filter2_4_name","children"),
     Input("filter2_4_value","value"),
     Input("filter3_4_name","children"),
     Input("filter3_4_value","value"),
     Input('dashtable_lv4', 'sort_by'),
   ] 
)
def update_table4(dim1,val1,dim2,val2,dim3,val3,sort_dim):
    
    #global data_lv4
    data_lv4=drilldata_process(df_drilldown,'Sub Category',dim1,val1,dim2,val2,dim3,val3)   
    
    if sort_dim==[]:
        sort_dim=[{"column_id":"Contribution to Overall Performance Difference","direction":"desc"}]
  
    df1=data_lv4[0:len(data_lv4)-1].sort_values(by=sort_dim[0]['column_id'],ascending= sort_dim[0]['direction']=='asc')
    df1=pd.concat([df1,data_lv4[len(data_lv4)-1:len(data_lv4)]])
    
    return df1.to_dict('records')


#sort lv3 on selected dimension
'''@app.callback(
    Output('drill_lv3', "children"),
    [ Input('dashtable_lv3', 'sort_by'),],
)
def sort_table3(sort_dim):
    if sort_dim==[]:
        df1=data_lv3
    else:    
        df1=data_lv3[0:len(data_lv3)-1].sort_values(by=sort_dim[0]['column_id'],ascending= sort_dim[0]['direction']=='asc')
        df1=pd.concat([df1,data_lv3[len(data_lv3)-1:len(data_lv3)]])
        #df1['id']=df1[df1.columns[0]]
        #df1.set_index('id', inplace=True, drop=False)
    
    return [dashtable_lv3(df1,'Service Category','dashtable_lv3',0)]'''


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
    [Output('dimension_filter_1', 'options'),
    Output('dimension_filter_1', 'value'),
    Output('dimension_filter_1', 'multi')],
    [Input('dimension_filter_selection_1', 'value')]
    )
def filter_dimension_1(v):
    if v:
        if v == 'Service Category':
            return [{"label": 'All', "value": 'All'}]+[{"label": k, "value": k} for k in list(filter_list.keys())], 'All', False
        else:
            return [{"label": k, "value": k} for k in dimension[v]], dimension[v], True
    return [], [], True


@app.callback(
    [Output('dimension_filter_2', 'options'),
    Output('dimension_filter_2', 'value'),
    Output('dimension_filter_2', 'multi')],
    [Input('dimension_filter_selection_1', 'value'),
    Input('dimension_filter_selection_2', 'value'),
    Input('dimension_filter_1', 'value')]
    )
def filter_dimension_1(v1, v2, v3):
    if v2:
        if v2 == 'Service Category':
            return [{"label": 'All', "value": 'All'}]+[{"label": k, "value": k} for k in list(filter_list.keys())], 'All', False
        elif v1 == 'Service Category' and v2 == 'Sub Category':
            sub_filter = filter_list[v3]
            if v3 == 'All':
                return [], 'All', False
            return [{"label": k, "value": k} for k in sub_filter], sub_filter, True
        else:
            return [{"label": k, "value": k} for k in dimension[v2]], dimension[v2], True
    return [], [], True

    
@app.callback(
    Output('dropdown-dimension-2','clearable'),
    [Input('dropdown-dimension-3','value')]
    )
def dropdown_clear(v):
    if v:
        return False
    return True

@app.callback(
    [Output('dropdown-dimension-2','options'),
    Output('dropdown-dimension-2','disabled')],
    [Input('dropdown-dimension-1','value')]
    )
def dropdown_menu_2(v):
    if v is None:
        return [], True
    elif v == 'Service Category':
        dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0] + [{"label": 'Service Category', "value": 'Service Category', 'disabled' : True}, {"label": 'Sub Category', "value": 'Sub Category'}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0]
        return dropdown_option, False
    else:
        dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0 and k != v] + [{"label": 'Service Category', "value": 'Service Category'}, {"label": 'Sub Category', "value": 'Sub Category', 'disabled' : True}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0 or k ==v]
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
    elif 'Service Category' in v and 'Sub Category' not in v:
        dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0] + [{"label": 'Service Category', "value": 'Service Category', 'disabled' : True}, {"label": 'Sub Category', "value": 'Sub Category'}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0]
        return dropdown_option, False
    elif 'Service Category' in v and 'Sub Category' in v:
        dropdown_option =  [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0] + [{"label": 'Service Category', "value": 'Service Category', 'disabled' : True}, {"label": 'Sub Category', "value": 'Sub Category', 'disabled' : True}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0]
        return dropdown_option, False
    else:
        dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0 and k not in v] + [{"label": 'Service Category', "value": 'Service Category'}, {"label": 'Sub Category', "value": 'Sub Category', 'disabled' : True}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0 or k in v]
        return dropdown_option, False

@app.callback(
    [Output('dimension_filter_selection_2', 'options'),
    Output('dimension_filter_selection_2', 'disabled')],
    [Input('dimension_filter_selection_1', 'value'),
    Input('dimension_filter_1', 'value')]
    )
def filter_menu_2(v, f):
    if v is None:
        return [], True
    elif v == 'Service Category':
        if f =='All':
            dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0] + [{"label": 'Service Category', "value": 'Service Category', 'disabled' : True}, {"label": 'Sub Category', "value": 'Sub Category', 'disabled' : True}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0]
            return dropdown_option, False
        else:
            dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0] + [{"label": 'Service Category', "value": 'Service Category', 'disabled' : True}, {"label": 'Sub Category', "value": 'Sub Category'}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0]
            return dropdown_option, False
    else:
        dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0 and k != v] + [{"label": 'Service Category', "value": 'Service Category'}, {"label": 'Sub Category', "value": 'Sub Category', 'disabled' : True}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0 or k ==v]
        return dropdown_option, False

@app.callback(
    [Output('datatable-tableview', "columns"),
    Output('datatable-tableview', "data")],
    [Input('dropdown-dimension-1','value'),
    Input('dropdown-dimension-2','value'),
    Input('dropdown-dimension-3','value'),
    Input('dimension_filter_selection_1','value'),
    Input('dimension_filter_selection_2','value'),
    Input('dimension_filter_1','value'),
    Input('dimension_filter_2','value'),
    Input('dropdown-measure-1', 'value')]
    )
def datatable_data_selection(v1, v2, v3, d1, d2, f1, f2, m):
    if d1:
        if d1 == 'Service Category':
            if d2 is None:
                if f1 == 'All':
                    df_drilldown_filtered = df_drilldown
                    cate_cnt = cate_mix_cnt
                else:
                    df_drilldown_filtered = df_drilldown[df_drilldown['Service Category'].isin([f1])]
                    cate_cnt = len(filter_list[f1])
            elif f1 != 'All' and d2 == 'Sub Category':
                df_drilldown_filtered = df_drilldown[(df_drilldown['Service Category'].isin([f1])) & (df_drilldown['Sub Category'].isin(f2))]
                cate_cnt = len(f2)
            else:
                df_drilldown_filtered = df_drilldown[df_drilldown[d2].isin(f2)]
                if f1 == 'All':
                    cate_cnt = cate_mix_cnt
                else:
                    cate_cnt = len(filter_list[f1])
        elif d2 == 'Service Category':
            if f2 == 'All':
                df_drilldown_filtered = df_drilldown[df_drilldown[d1].isin(f1)]
                cate_cnt = cate_mix_cnt
            else:
                df_drilldown_filtered = df_drilldown[(df_drilldown['Service Category'].isin([f2])) & (df_drilldown[d1].isin(f1))]
                cate_cnt = len(filter_list[f2])
        else:
            if d2:
                df_drilldown_filtered = df_drilldown[(df_drilldown[d1].isin(f1)) & (df_drilldown[d2].isin(f2))]
                cate_cnt = cate_mix_cnt
            else: 
                df_drilldown_filtered = df_drilldown[df_drilldown[d1].isin(f1)]
                cate_cnt = cate_mix_cnt
    else:
        df_drilldown_filtered = df_drilldown
        cate_cnt = cate_mix_cnt

    table_column = []
    selected_dimension = []
    if v1 is not None:
        selected_dimension.append(v1)
    if v2 is not None:
        selected_dimension.append(v2)
    if v3 is not None:
        selected_dimension.append(v3)

    table_column.extend(list(set(selected_dimension + ['Service Category', 'Sub Category'])))
    table_column.append("Pt Count")
    percent_list = ['Diff % from Target Utilization', 'Diff % from Target Total Cost', 'Diff % from Target Unit Cost', 'Patient %']
    dollar_list = ['YTD Total Cost', 'Annualized Total Cost', 'Target Total Cost', 'YTD Unit Cost', 'Annualized Unit Cost', 'Target Unit Cost']
    if len(selected_dimension) > 0:
#        ptct_dimension = set(selected_dimension + ['Service Category', 'Sub Category'])
        table_column.extend(measure_ori) 
        df_agg_pre = df_drilldown_filtered[table_column].groupby(by = list(set(selected_dimension + ['Service Category', 'Sub Category']))).sum().reset_index()
        df_agg = df_agg_pre[table_column].groupby(by = selected_dimension).agg({'Pt Count':'mean', 'YTD Utilization':'sum', 'Annualized Utilization':'sum', 'Target Utilization':'sum', 
            'YTD Total Cost':'sum', 'Annualized Total Cost':'sum', 'Target Total Cost':'sum'}).reset_index()
#        df_agg['Pt Count'] = df_agg['Pt Count']/cate_cnt
        df_agg['Patient %'] = df_agg['Pt Count']/895500
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
#        df_agg.style.format({'Diff % from Target Utilization' : "{:.2%}", 'Diff % from Target Total Cost': "{:.2%}", 'Diff % from Target Unit Cost' : "{:.2%}"})
#        df_agg.reset_index(inplace = True)
        show_column = selected_dimension + ['Patient %'] + m 
        if 'Diff % from Target Total Cost' in m:
            df_agg =  df_agg[show_column].sort_values(by =  'Diff % from Target Total Cost', ascending =False)
        else:
            df_agg = df_agg[show_column]
    else:
        show_column = ['Patient %'] + m 
        df_agg = df_drilldown_filtered[show_column]
    
    
    return [{"name": i, "id": i, "selectable":True,"type":"numeric", "format": FormatTemplate.percentage(1)} if i in percent_list else {"name": i, "id": i, "selectable":True, "type":"numeric","format": FormatTemplate.money(0)} if i in dollar_list else {"name": i, "id": i, "selectable":True, "type":"numeric","format": Format(precision=1, scheme = Scheme.fixed)} for i in show_column], df_agg.to_dict('records')

