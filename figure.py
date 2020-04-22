# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:01:53 2020

@author: rongxu
"""

import pandas as pd
import numpy as np
from numpy import arange
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc 
import dash_bootstrap_components as dbc
from dash_table.Format import Format, Scheme
import dash_table.FormatTemplate as FormatTemplate

colors={'blue':'rgba(18,85,222,100)','yellow':'rgba(246,177,17,100)','transparent':'rgba(255,255,255,0)','grey':'rgba(191,191,191,100)',
       'lightblue':'rgba(143,170,220,100)'}

domain_set = ["Cost & Utilization  Reduction", "Improving Disease Outcome",
                 "Decreasing Health Disparities", "Increasing Patient Safety",
                 "Enhancing Care Quality", "Better Patient Experience"]

domain_colordict={'Cost & Utilization  Reduction':'red','Improving Disease Outcome':'green','Decreasing Health Disparities':'grey'
                  ,'Increasing Patient Safety':'yellow' ,'Enhancing Care Quality':'blue' ,'Better Patient Experience':'white'}
    
  
def bargraph_overall(df):  #df_overall['month'] df_overall['base'] df_overall['adjusted']
    
    x_overall=df['month']
    y1_overall=df['base']
    y2_overall=df['adjusted']
    y3_trend=df['trend']
    n=len(x_overall)
    
    fig_overall = make_subplots(specs=[[{"secondary_y": True}]])

    fig_overall.add_trace(
        go.Bar(
            name='Cumulative Revenue', 
            x=x_overall, 
            y=y1_overall,
            text=y1_overall,
            textposition='auto',
            texttemplate='%{y:.2s}',
            marker=dict(
                color=colors['blue'],
                opacity=arange(0.34,0.34+0.06*n,0.06) 
                       )
        ),
        row=1,col=1,secondary_y=False,
    )
        
    fig_overall.add_trace(    
        go.Bar(
            name='Monthly Revenue', 
            x=x_overall, 
            y=y2_overall,
            text=y2_overall,
            textposition='inside',
            texttemplate='%{y:.2s}',
            marker=dict(
                color=colors['yellow'],
                opacity=arange(0.34,0.34+0.06*n,0.06) 
                       )
        ),
        row=1,col=1,secondary_y=False,
    )
    
    
    fig_overall.add_trace(
        go.Scatter(
            x=x_overall[1:], 
            y=y3_trend[1:],
            name="Monthly Increasing",
            marker=dict(color=colors['grey']),
            mode='lines+markers+text',
            line=dict(color=colors['grey']),
            textfont=dict(
            family="NotoSans-CondensedLight",
            size=12,
            color="black"
            ),
            text=y3_trend[1:],
            textposition='top center',
            texttemplate='%{y:.1%}'
        ),
        row=1,col=1,secondary_y=True,
    )
    # Change the bar mode
    fig_overall.update_layout(
        barmode='stack',
        title='placeholder',
        plot_bgcolor=colors['transparent'],
        paper_bgcolor=colors['transparent'],
        legend=dict(
            orientation='h',
            x=0.0,y=-0.1
        ),
        yaxis = dict(
            showgrid = True, 
            gridcolor =colors['grey'],
            nticks=5,
            showticklabels=True,
            zeroline=True,
            zerolinecolor=colors['grey'],
            zerolinewidth=1,
        ),
        yaxis2 = dict(
        showticklabels=False,
       # tickformat='%',
        rangemode="tozero",
       # nticks=3,
       # showgrid = True,
       # gridcolor =colors['grey'],
        ),
        modebar=dict(
            bgcolor=colors['transparent']
        ),
        
        margin=dict(l=10,r=10,b=100,t=40,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=12,
            color="#38160f"
        ),
    )
    return fig_overall

def waterfall_overall(x,y1,y2): #df_waterfall['label']  df_waterfall['base'] df_waterfall['adjusted']

    x_waterfall=x
    y1_waterfall=y1
    y2_waterfall=y2
    fig_waterfall = go.Figure(data=[
        go.Bar(
            
            x=x_waterfall, 
            y=y1_waterfall,
            text=y1_waterfall,
            textposition='auto',
            textfont=dict(color=['white','white',colors['transparent'],'white','white']),
            texttemplate='%{y:.2s}',
            marker=dict(
                    color=[colors['blue'],colors['blue'],colors['transparent'],colors['blue'],colors['grey']],
                    opacity=[1,0.7,0,0.7,0.7]
                    ),
            marker_line=dict( color = colors['transparent'] )
            
        ),
        go.Bar(     
            x=x_waterfall, 
            y=y2_waterfall,
            text=y2_waterfall,
            textposition='outside',
            textfont=dict(color=[colors['transparent'],colors['transparent'],'black',colors['transparent'],'black']),
            texttemplate='%{y:.2s}',
            marker=dict(
                    color=colors['yellow'],
                    opacity=0.7
                    )
        )
    ])
    # Change the bar mode
    fig_waterfall.update_layout(
        barmode='stack',
        title='placeholder',
        plot_bgcolor=colors['transparent'],
        paper_bgcolor=colors['transparent'],
        yaxis = dict(
            showgrid = True, 
            gridcolor =colors['grey'],
            nticks=5,
            showticklabels=True,
            zeroline=True,
            zerolinecolor=colors['grey'],
            zerolinewidth=1,
        ),
        showlegend=False,
        modebar=dict(
            bgcolor=colors['transparent']
        ),
        margin=dict(l=10,r=10,b=100,t=40,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=12,
            color="#38160f"
        ),
    )
    return fig_waterfall  

def tbl_utilizer(df_utilizer):
    utilizer_tbl=dash_table.DataTable(
        data=df_utilizer.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df_utilizer.columns],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-CondensedBlack',
            'fontSize':16,
            'backgroundColor':"#f7f7f7"
        },
        style_cell_conditional=[
            {'if': {'column_id': df_utilizer.columns[0]},
             'width': '6rem',
             'font-family':'NotoSans-Condensed',
            },     
        ],
        style_table={
            'back':  colors['blue']
        },
        style_header={
            'height': '4rem',
            'backgroundColor': "#f5b111",
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':14,
            'color': '#381610'
        },
    )
    
       
    return utilizer_tbl

def piechart_utilizer(label,value): #df_util_split['Class']  df_util_split['%']
    label_pie=label
    value_pie=value
    fig_util_split = go.Figure(data=[
        go.Pie(        
            labels=label_pie, 
            values=value_pie,
            pull=[0,0,0.1,0],
            marker=dict(
                    colors=["#1357DD","F5B111","#df8885"]            
                    ),
            textinfo='label+percent',
            textposition='auto'
        )
    ])
    fig_util_split.update_layout(
       showlegend=False,
       margin=dict(l=0,r=0,b=0,t=0,pad=0),
       paper_bgcolor=colors["transparent"],
       font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
    )   
    return fig_util_split

def bargraph_h(x,y):#df_script_per_util['avg script']  df_script_per_util['label']
    x_script_per_util=x
    y_script_per_util=y
    fig_script_per_util = go.Figure(data=[
        go.Bar(        
            x=x_script_per_util, 
            y=y_script_per_util,
            text=x_script_per_util,
            textposition='inside', 
            texttemplate='%{x:.2s}',
            width=0.5,
            textangle=0,
            marker=dict(
                    color=[colors['grey'],'#1357DD','#1357DD'],
                    opacity=[0.7,0.7,1]
                    ),
            orientation='h'
        )
    ])
    # Change the bar mode
    fig_script_per_util.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        showlegend=False,
        margin=dict(l=0,r=0,b=30,t=30,pad=10),
       font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
    )
    return fig_script_per_util

def bargraph_stack3(x,y1,y2,y3) : #   df_tot_script_split['dosage'] df_tot_script_split['YTD'] df_tot_script_split['Annualized'] df_tot_script_split['Plan Target']
    x_tot_script_split=x
    y1_tot_script_split=y1
    y2_tot_script_split=y2
    y3_tot_script_split=y3
    fig_tot_script_split = go.Figure(data=[
        go.Bar(
            name='YTD', 
            x=x_tot_script_split, 
            y=y1_tot_script_split,
            text=y1_tot_script_split,
            textposition='auto',
            textangle=0,
            texttemplate='%{y:.2s}',
            marker=dict(
                    color='#1357DD',
                    opacity=1
                    )
        ),
        go.Bar(
            name='Annualized', 
            x=x_tot_script_split, 
            y=y2_tot_script_split,
            text=y2_tot_script_split,
            textposition='inside',
            textangle=0,
            texttemplate='%{y:.2s}',
            marker=dict(
                    color='#1357DD',
                    opacity=0.7
                    )
        ),
        go.Bar(
            name='Plan Target', 
            x=x_tot_script_split, 
            y=y3_tot_script_split,
            text=y3_tot_script_split,
            textposition='inside',
            textangle=0,
            texttemplate='%{y:.2s}',
            marker=dict(
                    color=colors['grey'],
                    opacity=0.7
                    )
        )
    ])
    # Change the bar mode
    fig_tot_script_split.update_layout(
        barmode='group',
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        legend=dict(
            orientation='h',
            x=0.2,y=-0.2
        ),
        yaxis = dict(
            showgrid = True, 
            gridcolor =colors['grey'],
            nticks=5,
            showticklabels=True,
            zeroline=True,
            zerolinecolor=colors['grey'],
            zerolinewidth=1
        ),
        #hovermode=True,
        margin=dict(l=0,r=0,b=30,t=50,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
    )    
    return fig_tot_script_split


def bubblegraph(df_domain_perform,traces,obj): # 数据，[0,1] ,'Domain' or 'Measure'
    
    x = [0+1*i/100 for i in range(100)]
    y = [-0.15+0.3*i/100 for i in range(100)]
    z = []

    for xi in x:
        zt = []
        for yi in y:
            zt.append(0.8-0.6*(1-xi)-yi)
        z.append(zt)

    fig_domain_perform = go.Figure()

    fig_domain_perform.add_trace( go.Heatmap(x=x,y=y,z=z,
                                             colorscale=[[0, 'rgba(241,0,28,0.6)'], [0.3, 'rgba(241,0,28,0.2)'], 
                                                         [0.5, 'rgba(241,0,28,0)'],[1, 'rgba(241,0,28,0)']],
                                             colorbar=dict(len=1,
                                                           tickmode='array',
                                                           tickvals=[0.08,0.6],
                                                           ticktext=['High risk','Low risk'],
                                                           x=1,y=0.7
                                                           )))

    for k in traces:
        fig_domain_perform.add_trace(
                go.Scatter(        
                x=df_domain_perform[df_domain_perform['Domain']==domain_set[k]]['Weight'] , 
                y=df_domain_perform[df_domain_perform['Domain']==domain_set[k]]['Performance Diff from Target'] ,
                x0=0,y0=0,
                #text=df_domain_perform[df_domain_perform['Domain']==domain_set[k]][obj],
                mode='markers+text',             
                name=domain_set[k],
                #dx=0.1,dy=0.1,
                marker=dict(
                    size=df_domain_perform[df_domain_perform['Domain']==domain_set[k]]['Weight']*4000,
                    color=domain_colordict[domain_set[k]],
                    opacity=0.8,
                    sizemode='area',
                )

            )
        )

    annotations = []
    annotations.append(dict(xref='paper', yref='paper',
                            x=0, y=1,
                            text='Performance<br>(% diff from target)',
                            font=dict(family='NotoSans-CondensedLight', size=8, color='#38160f'),
                            showarrow=False))
    annotations.append(dict(xref='paper', yref='paper',
                            x=0.98, y=0.47,
                            text='Weight',
                            font=dict(family='NotoSans-CondensedLight', size=8, color='#38160f'),
                            showarrow=False))

    fig_domain_perform.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        annotations=annotations,
        showlegend=True,
        xaxis = dict(
            tickmode='linear',
            range=[0,0.9],
            tick0=0,
            dtick=0.1,
            showticklabels=True,
            tickformat='%',
            position=0.47,

            showgrid=True,
            gridcolor =colors['grey'],

            zeroline=False,
            zerolinecolor='grey',
            rangemode="tozero"
        ),
        margin=dict(l=0,r=0,b=50,t=10,pad=0),
       font=dict(
            family="NotoSans-CondensedLight",
            size=12,
            color="#38160f"
        ),
        yaxis = dict(
            #showgrid = True, 
            #gridcolor =colors[3],
            showline=True,
            linecolor='grey',
            tickmode='linear',
            dtick=0.05,
            range=[-0.15,0.15],
            tickformat='%',
            showticklabels=True,
            zeroline=True,
            zerolinecolor='grey',
            ticks='inside'
        ),
        legend=dict(
            orientation='h',
            x=0,y=-0.05
        ),
        hovermode=False,
        modebar=dict(
            bgcolor=colors['transparent']
        ),
    )
    return fig_domain_perform
    '''
def bubblegraph(x,y,t):#df_domain_perform['weight'] df_domain_perform['performance'] df_domain_perform['domain']
    x_domain_perform=x
    y_domain_perform=y
    t_domain_perform=t
    color_set=['rgb(93, 164, 214)', 'rgb(255, 144, 14)', 'rgb(44, 160, 101)', 'rgb(255, 65, 54)']
    opacity_set=[1, 0.8, 0.6, 0.4]
    bubble_traces = []
    for i in range(len(x)):
        bubble_traces.append(go.Scatter(dict(x = [x_domain_perform[i]], y = [y_domain_perform[i]],
                                      x0=0,y0=0,
            text=t_domain_perform[i],
            mode='markers+text',
            #dx=0.1,dy=0.1,
            marker=dict(
                size=60,
                color=color_set[i],
                opacity=opacity_set[i]),
            name = i+1)))
    return bubble_traces



def bubblegraph_layout():
    bubble_layout = dict(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        #showlegend=True,
       # shapes=dict(x0=0,y0=0),
        xaxis = dict(
            tickmode='linear',
            tick0=0,
            dtick=0.1,
            showticklabels=True,
            tickformat='%',
            position=0.37,
            
            showgrid=True,
            gridcolor =colors['grey'],
            
            zeroline=False,
            zerolinecolor='grey',
            rangemode="tozero"
        ),
        margin=dict(l=0,r=10,b=50,t=10,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
        yaxis = dict(
            #showgrid = True, 
            #gridcolor =colors[3],
            showline=True,
            linecolor='grey',
            tickmode='linear',
            dtick=0.1,
            tickformat='%',
            showticklabels=True,
            zeroline=True,
            zerolinecolor='grey',
            ticks='inside'
        ),
        hovermode=False
    )
    return bubble_layout
'''
def waterfall_domain(x,y1,y2): #df_waterfall['label']  df_waterfall['base'] df_waterfall['adjusted']

    x_waterfall=x
    y1_waterfall=y1
    y2_waterfall=y2
    fig_waterfall = go.Figure(data=[
        go.Bar(
            
            x=x_waterfall, 
            y=y1_waterfall,
            text=y1_waterfall,
            textposition='auto',
            textfont=dict(color=['white','white','white',colors['transparent'],'white']),
            texttemplate='%{y:.2s}',
            marker=dict(
                    color=[colors['blue'],colors['blue'],colors['grey'],colors['transparent'],colors['grey']],
                    opacity=[1,0.7,0.7,0,0.7]
                    ),
            marker_line=dict( color = colors['transparent'] )
            
        ),
        go.Bar(     
            x=x_waterfall, 
            y=y2_waterfall,
            text=y2_waterfall,
            textposition='inside',
            texttemplate='%{y:.2s}',
            marker=dict(
                    color=colors['yellow'],
                    opacity=0.7
                    )
        )
    ])
    # Change the bar mode
    fig_waterfall.update_layout(
        barmode='stack',
        plot_bgcolor=colors['transparent'],
        paper_bgcolor=colors['transparent'],
        yaxis = dict(
            showgrid = True, 
            gridcolor =colors['grey'],
            nticks=5,
            showticklabels=True,
            zeroline=True,
            zerolinecolor=colors['grey'],
            zerolinewidth=1,
        ),
        showlegend=False,
        modebar=dict(
            bgcolor=colors['transparent']
        ),
        margin=dict(l=10,r=10,b=100,t=40,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
    )
    return fig_waterfall  

def bargraph_perform(df_measure_perform,d): #df_measure_perform, 0 or 1 or 2.... domain number

    x=df_measure_perform[df_measure_perform['Domain']==domain_set[d]]['Performance Diff from Target']
    y=df_measure_perform[df_measure_perform['Domain']==domain_set[d]]['Measure']
    
    fig_measure_perform = go.Figure(data=[
        go.Bar(        
            x=x, 
            y=y,
            text=x,
            textposition='inside',
            texttemplate='%{x}',
            marker=dict(
                    color=x.apply(lambda x: 'green' if x>0 else 'red'),
                    opacity=0.7
                    ),
            orientation='h',
            width=0.5
        )
    ])
    # Change the bar mode
    fig_measure_perform.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        showlegend=False,
        xaxis=dict(
            tickformat='%',
            zeroline=True,
            zerolinecolor='black'
        ),
        modebar=dict(
                bgcolor=colors['transparent']
                ),
        margin=dict(l=0,r=0,b=30,t=50,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
    )
    return fig_measure_perform

'''def tbl_measure(df_measure_perform,d): 

    df=df_measure_perform[df_measure_perform['Domain']==domain_set[d]].iloc[:,1:6]
    tbl = go.Figure(data=[
        go.Table(
            header=dict(
                values=df.columns,
                line_color='white' ,       
                fill_color=colors['yellow'],
                align=['left','center'],
                font=dict(color='white',size=10)
            ),
            cells=dict(
                values=df.T,
                line_color='white' ,       
                fill_color='lightgrey',
                font=dict(size=10)
            ),
            columnwidth=[0.4,0.15,0.15,0.15,0.15],
        )
    ])
    
    tbl.update_layout(
       autosize=True,
       margin=dict(l=0,r=0,b=30,t=50,pad=0),
       paper_bgcolor=colors["transparent"],
       font=dict(
            family="NotoSans-CondensedLight",
            size=12,
            color="#38160f"
        ),
    )     
    return tbl'''

def tbl_measure(df_measure_perform,d):
    df=df_measure_perform[df_measure_perform['Domain']==domain_set[d]].iloc[:,1:]
    if len(df)>0 :
        df['highlight']=df.apply(lambda x : 1 if (x['Performance Diff from Target']<0.05)& (x['Weight']>0.3)  else 0, axis=1)
    else: df['highlight']=1
    
    measure_tbl=dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[ {'id': c, 'name': c} for c in df.columns ],
        sort_action="native",
        sort_mode='multi',
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_data_conditional=[
        {
            'if': {'column_id':c,
                'filter_query': '{highlight} eq 1' },
            'backgroundColor': 'rgba(255,0,0,0.6)',
            'color': 'white',
        }  for c in df.columns
        ],
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-CondensedBlack',
            'fontSize':14
        },
        style_cell_conditional=[
            {'if': {'column_id': df.columns[0]},
             'width': '2.5rem',
             'font-family':'NotoSans-CondensedLight',
            }, 
            {'if': {'column_id': 'highlight'},
            'display': 'none'}
        ],
        style_table={
            'back':  colors['blue']
        },
        style_header={
            'height': '2rem',
            'backgroundColor': '#F5B111',
            'fontWeight': 'bold',
            'font-family':'NotoSans-Condensed',
            'fontSize':12,
            'color': '#381610'
        },
    )
    
       
    return html.Div(measure_tbl, style={"padding":"1rem"})

def tbl_non_contract(df,measures):
    df=df[df['Measure'].isin(measures)]
    
    measure_tbl=dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[ {'id': c, 'name': c} for c in df.columns ],
        sort_action="native",
        sort_mode='multi',
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-CondensedBlack',
            'fontSize':14
        },
        style_cell_conditional=[
            {'if': {'column_id': df.columns[0]},
             'width': '2.5rem',
             'font-family':'NotoSans-CondensedLight',
            },            
        ],
        style_table={
            'back':  colors['blue']
        },
        style_header={
            'height': '2rem',
            'backgroundColor': '#F5B111',
            'fontWeight': 'bold',
            'font-family':'NotoSans-Condensed',
            'fontSize':12,
            'color': '#381610'
        },
    )
    
       
    return measure_tbl

############################################################
################Drilldown###################################  
############################################################ 
def drill_bubble(df):
    df['Weight']=df['Annualized_Total_cost']/(df['Annualized_Total_cost'].sum()/2)
    n=len(df)
    
    colorbar=dict(
        len=1,
       tickmode='array',
       tickvals=[-0.5,0.5],
       ticktext=['Low risk','High risk'],
       thickness=5,
       #x=1,y=0.7
    )
    colorscale=[[0, 'rgba(0,255,0,1)'],[0.5, 'rgba(0,255,0,0.2)'],[0.5, 'rgba(255,0,0,0.2)'], [1, 'rgba(255,0,0,1)']]
    color_axis=dict(cmin=-0.5,cmax=0.5,colorscale=colorscale,colorbar=colorbar,)

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights = [0.5,0.5],
        specs=[[{"type": "scatter"}],
               [{"type": "scatter"}]]
    )

    fig.add_trace(
        go.Scatter(
            x=[0.5+i for i in range(n)],
            y=df['% Cost Diff from Target'],
            text=df['% Cost Diff from Target'],
            textposition='top center',
            texttemplate='%{y:.1%}',
            mode="markers+text",
            marker=dict(
                size=df['Weight']*600,
                sizemode='area',
                color=df['% Cost Diff from Target'],#df['performance'].apply(lambda x: 'red' if x>0 else 'green'),
                cmin=-0.5,
                cmax=0.5,
                #opacity=0.8,
                colorbar=colorbar,
                colorscale=colorscale,

                #coloraxis=coloraxis1
            )

        ),
        row=1, col=1
    )


    fig.add_trace(
        go.Scatter(
            x=[0.5+i for i in range(n)],
            y=df['Contribution to Overall Performance Difference'],
            text=df['Contribution to Overall Performance Difference'],
            textposition='top center',
            texttemplate='%{y:.1%}',
            mode="markers+text",
            marker=dict(
                size=df['Weight']*600,
                sizemode='area',
                color=df['Contribution to Overall Performance Difference'],#df['Contribution'].apply(lambda x: 'red' if x>0 else 'green'),
                cmin=-0.5,
                cmax=0.5,
                #opacity=0.8,
                colorbar=colorbar,
                colorscale=colorscale,
                #coloraxis=coloraxis2
            )

        ),
        row=2, col=1
    )
    fig.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        showlegend=False,#tickmode='array',tickvals=[0,1,2,3,4,5,6],
        modebar=dict( bgcolor=colors['transparent']),
        xaxis=dict(showline=True,mirror=True,linecolor=colors['grey'],showticklabels=False,range=[0,n],dtick=1,autorange=False,gridcolor=colors['grey'],zeroline=True ,zerolinecolor=colors['grey']),
        xaxis2=dict(showline=True,mirror=True,linecolor=colors['grey'],showticklabels=False,range=[0,n],dtick=1,autorange=False,gridcolor=colors['grey'],zeroline=True ,zerolinecolor=colors['grey']),
        yaxis=dict(showline=True,mirror=True,linecolor=colors['grey'],showticklabels=False,range=[-0.5,0.5],autorange=False,zeroline=True ,zerolinecolor=colors['grey']),
        yaxis2=dict(showline=True,mirror=True,linecolor=colors['grey'],showticklabels=False,range=[-0.5,0.5],autorange=False
                    ,zeroline=True ,zerolinecolor=colors['grey'] ),
        #coloraxis=dict(cmin=-0.5,cmax=0.5,colorscale=colorscale,colorbar=colorbar,),
        #coloraxis2=dict(cmin=-0.5,cmax=0.5,colorscale=colorscale,colorbar=colorbar,),
        #margin=dict(l=115)
        hovermode=False,
        margin=dict(l=2,r=2,b=2,t=2,pad=0),
        height=300,

    )
    return fig

def drillgraph_table(df_table,tableid):
    tbl=dash_table.DataTable(
        id=tableid,
        data=df_table.to_dict('records'),
        columns=[ {'id': c, 'name': c,"selectable": True} for c in df_table.columns ],
        column_selectable="single",
        selected_columns=[],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
       
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':12
        },
        style_cell_conditional=[
            {'if': {'column_id': df_table.columns[0]},
             
             'fontWeight': 'bold',
            }, 
            {'if': {'column_id': 'highlight'},
            'display': 'none'}
        ],
        style_table={
            'back':  colors['blue'],
        },
        style_header={
            'height': '4rem',
            'minWidth': '3rem',
            'maxWidth':'3rem',
            'whiteSpace': 'normal',
            'backgroundColor': colors['yellow'],
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':14,
            'color': 'white',
            'text-align':'center',
        },
    )
    return tbl

def drillgraph_lv1(df,tableid):

    df=df.reindex(range(len(df)-1,-1,-1))
    df_table=df[['YTD Avg Episode Cost',df.columns[0]]]
    df_table1=pd.DataFrame(df_table.apply(lambda x: "{:,.1f}".format(x['YTD Avg Episode Cost']), axis=1)).T
    df_table1.columns=df_table[df_table.columns[1]]
    
    drillgraph= [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(html.H2("YTD Cost per Episode",style={"font-size":"1rem","display":"table-cell", "vertical-align":"middle"}), style={"height":"6rem","display":"table"}),
                            html.Div(html.H2("% Diff from Target", style={"font-size":"1rem","display":"table-cell", "vertical-align":"middle"}), style={"height":"10rem","display":"table"}),
                            html.Div(html.H2("Contribution to Overall Difference", style={"font-size":"1rem","display":"table-cell", "vertical-align":"middle"}), style={"height":"10rem","display":"table"}),
                        ],
                        width=3,
                        style={"padding-left":"2rem"}
                    ),

                    dbc.Col(
                        [
                            html.Div(
                                [
                                    drillgraph_table(df_table1,tableid)
                                ],
                                style={"padding-left":"1rem","padding-right":"7rem"}
                            ),
                            html.Div(
                                [
                                    dcc.Graph(figure=drill_bubble(df),config={'displayModeBar': False})
                                ],
                                style={"padding-top":"1rem","padding-bottom":"2rem"}
                            ),
                        ],
                        width=9,
                    ),
                ]
            )
        ]
        #style={"padding-top":"2rem","padding-bottom":"2rem"}
    
    
    return drillgraph
       
   
def dashtable_lv3(df,dimension,tableid):
     
    table_lv3=dash_table.DataTable(
        data=df.to_dict('records'),
        id=tableid,
        columns=[
        {"name": ["", dimension], "id": dimension},
        {"name": ["Total Episode Cost", "YTD Avg Episode Cost"], "id": "YTD Avg Episode Cost",'type': 'numeric',"format":FormatTemplate.money(0)},
        {"name": ["Total Episode Cost", "% Cost Diff from Target"], "id": "% Cost Diff from Target",'type': 'numeric',"format":FormatTemplate.percentage(1)},
        {"name": ["Total Episode Cost", "Contribution to Overall Performance Difference"], "id": "Contribution to Overall Performance Difference",'type': 'numeric',"format":FormatTemplate.percentage(1)},
        {"name": ["Utilization Rate", "YTD Avg Utilization Rate"], "id": "YTD Avg Utilization Rate",'type': 'numeric',"format":Format( precision=2, scheme=Scheme.fixed,),},
        {"name": ["Utilization Rate", "% Util Diff from Target"], "id": "% Util Diff from Target",'type': 'numeric',"format":FormatTemplate.percentage(1)},
        {"name": ["Unit Cost", "YTD Avg Cost per Unit"], "id": "YTD Avg Cost per Unit",'type': 'numeric',"format":FormatTemplate.money(0)},
        {"name": ["Unit Cost", "% Unit Cost Diff from Target"], "id": "% Unit Cost Diff from Target",'type': 'numeric',"format":FormatTemplate.percentage(1)},
    ],
        merge_duplicate_headers=True,
        sort_action="native",
        sort_mode='single',
        #sort_by={"column_id":"Contribution to Overall Performance Difference","direction":"desc"},
        row_selectable='single',
        selected_rows=[],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
       
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':12
        },
        style_cell_conditional=[
            {'if': {'column_id': df.columns[0]},
             
             'fontWeight': 'bold',
            }, 
            
        ],
        style_table={
            'back':  colors['blue'],
        },
        style_header={
            'height': '4rem',
            'minWidth': '3rem',
            'maxWidth':'3rem',
            'whiteSpace': 'normal',
            'backgroundColor': colors['yellow'],
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':14,
            'color': 'white',
            'text-align':'center',
        },
    )
    return table_lv3

def drilldata_process(df_drilldown,dimension,dim1='All',f1='All',dim2='All',f2='All',dim3='All',f3='All'):#dimension='Sub Category'    
    if f1!='All':
        df_pre=df_drilldown[df_drilldown[dim1]==f1]
        if f2!='All':
            df_pre=df_pre[df_pre[dim2]==f2]
            if  f3!='All':
                df_pre=df_pre[df_pre[dim3]==f3]
    else :
        df_pre=df_drilldown

    df_pre2=df_pre.groupby(list(np.unique([dimension,'Service Category', 'Sub Category'])))[df_pre.columns[14:]].agg(np.sum).reset_index()
    
    df=df_pre2.groupby([dimension]).agg(YTD_Total_cost=pd.NamedAgg(column='YTD Total Cost',aggfunc=sum)
                                             ,Annualized_Total_cost=pd.NamedAgg(column='Annualized Total Cost',aggfunc=sum)
                                             ,Target_Total_cost=pd.NamedAgg(column='Target Total Cost',aggfunc=sum)
                                             ,YTD_Utilization=pd.NamedAgg(column='YTD Utilization',aggfunc=sum)
                                             ,Annualized_Utilization=pd.NamedAgg(column='Annualized Utilization',aggfunc=sum)
                                             ,Target_Utilization=pd.NamedAgg(column='Target Utilization',aggfunc=sum)
                                             ,Pt_Count=pd.NamedAgg(column='Pt Count',aggfunc=np.mean)
                                             ).reset_index()
    allvalue=df.sum().values 
    allvalue[0]='All'
    if dimension in ['Service Category', 'Sub Category']:
        allvalue[-1]=df['Pt_Count'].mean()
  
    df.loc[len(df)] = allvalue
    
    df['YTD Avg Episode Cost']=df['YTD_Total_cost']/df['Pt_Count']
    df['Target Avg Episode Cost']=df['Target_Total_cost']/df['Pt_Count']
    df['Annualized Avg Episode Cost']=df['Annualized_Total_cost']/df['Pt_Count']

    df['% Cost Diff from Target']=(df['Annualized Avg Episode Cost']-df['Target Avg Episode Cost'])/df['Target Avg Episode Cost']
    df['Contribution to Overall Performance Difference']=(df['Annualized_Total_cost']-df['Target_Total_cost'])/allvalue[3]

    df['YTD Avg Utilization Rate']=df['YTD_Utilization']/df['Pt_Count']
    df['Target Avg Utilization Rate']=df['Target_Utilization']/df['Pt_Count']
    df['Annualized Avg Utilization Rate']=df['Annualized_Utilization']/df['Pt_Count']

    df['% Util Diff from Target']=(df['Annualized Avg Utilization Rate']-df['Target Avg Utilization Rate'])/df['Target Avg Utilization Rate']

    df['YTD Avg Cost per Unit']=df['YTD_Total_cost']/df['YTD_Utilization']
    df['Target Avg Cost per Unit']=df['Target_Total_cost']/df['Target_Utilization']
    df['Annualized Avg Cost per Unit']=df['Annualized_Total_cost']/df['Annualized_Utilization']

    df['% Unit Cost Diff from Target']=(df['Annualized Avg Cost per Unit']-df['Target Avg Cost per Unit'])/df['Target Avg Cost per Unit']
    
    return df


    


