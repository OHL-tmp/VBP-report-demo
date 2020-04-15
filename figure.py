# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:01:53 2020

@author: rongxu
"""

import pandas as pd
from numpy import arange
import plotly
import plotly.graph_objects as go

colors={'blue':'rgba(18,85,222,100)','yellow':'rgba(246,177,17,100)','transparent':'rgba(255,255,255,0)','grey':'rgba(191,191,191,100)',
       'lightblue':'rgba(143,170,220,100)'}



def bargraph_overall(x,y1,y2):  #df_overall['month'] df_overall['base'] df_overall['adjusted']

    x_overall=x
    y1_overall=y1
    y2_overall=y2
    n=len(x)

    fig_overall = go.Figure(data=[
        go.Bar(
            name='Revenue before adj', 
            x=x_overall, 
            y=y1_overall,
            text=y1_overall,
            textposition='auto',
            marker=dict(
                color=colors['blue'],
                opacity=arange(0.34,0.34+0.06*n,0.06) 
                       )
        ),
        go.Bar(
            name='Adj', 
            x=x_overall, 
            y=y2_overall,
            text=y2_overall,
            textposition='inside',
            marker=dict(
                color=colors['yellow'],
                opacity=arange(0.34,0.34+0.06*n,0.06) 
                       )
        )
    ])
    # Change the bar mode
    fig_overall.update_layout(
        barmode='stack',
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
            zerolinewidth=1
        ),
        hovermode=False,
        modebar=dict(
        bgcolor=colors['transparent']
        )
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
            textposition='inside',
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
            zerolinewidth=1
        ),
        hovermode=False,
        showlegend=False,
        modebar=dict(
        bgcolor=colors['transparent']
        )
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
        #width=1000       
    )     
    return utilizer_tbl

def piechart_utilizer(label,value): #df_util_split['Class']  df_util_split['%']
    label_pie=label
    value_pie=value
    fig_util_split = go.Figure(data=[
        go.Pie(        
            labels=label_pie, 
            values=value_pie,
            pull=[0.1,0,0],
            marker=dict(
                    colors=[colors['blue'],colors['yellow'],colors['grey']]            
                    ),
            textinfo='label+percent'
        )
    ])
    fig_util_split.update_layout(
       hovermode=False,
       showlegend=False       
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
            width=0.5,
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
        hovermode=False,
        showlegend=False,
        margin=dict(l=80,r=80,t=100,b=80,pad=10)
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
        hovermode=False
    )    
    return fig_tot_script_split

def bubblegraph(x,y,t):#df_domain_perform['weight'] df_domain_perform['performance'] df_domain_perform['domain']
    x_domain_perform=x
    y_domain_perform=y
    t_domain_perform=t
    fig_domain_perform = go.Figure(data=[
        go.Scatter(        
            x=x_domain_perform, 
            y=y_domain_perform,
            x0=0,y0=0,
            text=t_domain_perform,
            mode='markers+text',
            #dx=0.1,dy=0.1,
            marker=dict(
                size=60,
                color=['rgb(93, 164, 214)', 'rgb(255, 144, 14)', 'rgb(44, 160, 101)', 'rgb(255, 65, 54)'],
                opacity=[1, 0.8, 0.6, 0.4]
            )
        )
    ])
    fig_domain_perform.update_layout(
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
    return fig_domain_perform

def bargraph_perform(x,y): #df_measure_perform['performance'] df_measure_perform['Measure']
    x_measure_perform=x
    y_measure_perform=y
    fig_measure_perform = go.Figure(data=[
        go.Bar(        
            x=x_measure_perform, 
            y=y_measure_perform,
            text=x_measure_perform,
            textposition='inside',
            texttemplate='%{x}',
            marker=dict(
                    color=['red','green','green'],
                    opacity=[0.7,0.7,0.7]
                    ),
            orientation='h'
        )
    ])
    # Change the bar mode
    fig_measure_perform.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        hovermode=False,
        showlegend=False,
        xaxis=dict(
            tickformat='%',
            zeroline=True,
            zerolinecolor='black'
        ),
        modebar=dict(
                bgcolor=colors['transparent']
                )
    )
    return fig_measure_perform