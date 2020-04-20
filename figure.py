# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:01:53 2020

@author: rongxu
"""

import pandas as pd
from numpy import arange
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
            x=0.3,y=-0.05
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
            family="NotoSans-CondensedLight",
            size=12,
            color="#7f7f7f"
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
            family="NotoSans-CondensedLight",
            size=12,
            color="#7f7f7f"
        ),
    )
    return fig_waterfall   

def tbl_utilizer(df_utilizer):
    utilizer_tbl = go.Figure(data=[
        go.Table(
            header=dict(
                values=df_utilizer.columns,
                line_color='white' ,       
                fill_color=colors['yellow'],
                align=['left','center'],
                font=dict(color='white',size=10)
            ),
            cells=dict(
                values=df_utilizer.T,
                line_color='white' ,       
                fill_color='lightgrey',
                font=dict(size=10)
            )
        )
    ])
    
    utilizer_tbl.update_layout(
       autosize=True,
       margin=dict(l=0,r=0,b=30,t=50,pad=0),
       paper_bgcolor=colors["transparent"],
       font=dict(
            family="NotoSans-CondensedLight",
            size=12,
            color="#38160f"
        ),
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
            textinfo='label+percent'
        )
    ])
    fig_util_split.update_layout(
       showlegend=False,
       margin=dict(l=0,r=0,b=0,t=0,pad=0),
       paper_bgcolor=colors["transparent"],
       font=dict(
            family="NotoSans-CondensedLight",
            size=12,
            color="#7f7f7f"
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
                    color=[colors['grey'],colors['blue'],colors['blue']],
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
            family="NotoSans-CondensedLight",
            size=12,
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
                    color=colors['blue'],
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
                    color=colors['blue'],
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
            x=0,y=-0.05
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
            family="NotoSans-CondensedLight",
            size=8,
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
                                             colorbar=dict(len=0.5,
                                                           tickmode='array',
                                                           tickvals=[0.1,0.5,0.9],
                                                           ticktext=['High risk','Medium risk','Low risk'])))

    for k in traces:
        fig_domain_perform.add_trace(
                go.Scatter(        
                x=df_domain_perform[df_domain_perform['Domain']==domain_set[k]]['Weight'] , 
                y=df_domain_perform[df_domain_perform['Domain']==domain_set[k]]['Performance Diff from Target'] ,
                x0=0,y0=0,
                text=df_domain_perform[df_domain_perform['Domain']==domain_set[k]][obj],
                mode='markers+text',
                name=domain_set[k],
                #dx=0.1,dy=0.1,
                marker=dict(
                    size=df_domain_perform[df_domain_perform['Domain']==domain_set[k]]['Weight']*200,
                    color=domain_colordict[domain_set[k]],
                    opacity=0.8
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
            size=8,
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
            family="NotoSans-CondensedLight",
            size=12,
            color="#7f7f7f"
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
            family="NotoSans-CondensedLight",
            size=14,
            color="#38160f"
        ),
    )
    return fig_measure_perform

def tbl_measure(df_measure_perform,d): # data, 0 or 1 or 2..... domain number

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
    return tbl