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
            'backgroundColor': '#3D9970',
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

############################################################
################Drilldown###################################  
############################################################ 
def drill_bubble(df):
    n=len(df)
    
    colorbar=dict(
        len=1,
       tickmode='array',
       tickvals=[-0.5,0.5],
       ticktext=['Low risk','High risk'],
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
            y=df['performance'],
            text=df['performance'],
            textposition='middle left',
            texttemplate='%{y:.1%}',
            mode="markers+text",
            marker=dict(
                size=df['Weight']*600,
                sizemode='area',
                color=df['performance'],#df['performance'].apply(lambda x: 'red' if x>0 else 'green'),
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
            y=df['Contribution'],
            text=df['Contribution'],
            textposition='middle left',
            texttemplate='%{y:.1%}',
            mode="markers+text",
            marker=dict(
                size=df['Weight']*600,
                sizemode='area',
                color=df['Contribution'],#df['Contribution'].apply(lambda x: 'red' if x>0 else 'green'),
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
        hovermode=False
    )
    return fig

def drillgraph_table(df_table):
    tbl=dash_table.DataTable(
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
            'fontSize':8
        },
        style_cell_conditional=[
            {'if': {'column_id': df_table.columns[0]},
             'width': '250px',
             'fontWeight': 'bold',
            }, 
            {'if': {'column_id': 'highlight'},
            'display': 'none'}
        ],
        style_table={
            'back':  colors['blue']
        },
        style_header={
            'height': '60px',
            'backgroundColor': colors['yellow'],
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':10,
            'color': 'white'
        },
    )
    return tbl

def drillgraph_lv1(df_drilldown,dimension):
    df=df_drilldown.groupby([dimension])[['YTD Total Cost','Annualized Total Cost','Target Total Cost','Pt Count']].agg(np.sum).reset_index()
    df['Pt Count']=df['Pt Count']/39
    allvalue=df.sum().values  
    allvalue[0]='All'
    df.loc[-1] = allvalue
    df.index = df.index + 1 
    df = df.sort_index()
    df['Avg YTD']=df['YTD Total Cost']/df['Pt Count']
    df['Avg Target']=df['Target Total Cost']/df['Pt Count']
    df['Avg Annualized']=df['Annualized Total Cost']/df['Pt Count']
    df['Weight']=df['Annualized Total Cost']/allvalue[2]
    df['Contribution']=(df['Annualized Total Cost']-df['Target Total Cost'])/allvalue[3]
    df['performance']=(df['Avg Annualized']-df['Avg Target'])/df['Avg Target']
    df_table=pd.DataFrame(df.apply(lambda x: "{:,.1f}".format(x['Avg YTD']), axis=1)).T
    df_table.columns=df[dimension]
    
    drillgraph=html.Div(
        [
        dbc.Row(
            [
                dbc.Col([ html.Div("YTD Cost per Episode"), 
                        html.Div("% Diff from Target"),
                        html.Div("Contribution to Overall Difference"),]
                       
                       ),

                dbc.Col(
                      [ html.Div(drillgraph_table(df_table),style={"padding":"2rem"}),
                        html.Div(dcc.Graph(figure=drill_bubble(df),config={'displayModeBar': False})),]
                ),
            ])
        ]
    )
    
    return drillgraph

    


