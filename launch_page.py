#!/usr/bin/env python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table

import pandas as pd
import numpy as np

import dashboard
import monitoring_details

app = dash.Dash(__name__, url_base_pathname='/vbc-demo/launch/')

server = app.server

def launch_layout():
    return dbc.Col([

                    html.Div(
                        [
                            
                            html.Video(src=app.get_asset_url("launch_mesh.mov"), autoPlay=True, loop=True, style={"height":"45rem","border-bottom":"none", "text-align":"center"})
                        ],
                        style={"text-align":"center"}
                    ),
                    html.Div(
                        [
                            html.P("Powered by One Health Link")
                        ],
                        style={"text-align":"center", "font-size":"0.6rem"}
                    ),
                    html.Div(
                        [
                            html.H1("ValueGen Solution",style={"background-color":"transparent","font-size":"5rem"}),
                            dbc.Card([
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(dbc.Button("Contract Optimizer", color="light", className="mr-1", href = "/vbc-demo/contract-optimizer/", style={"font-family":"NotoSans-Regular", "font-size":"1rem", "padding":"1rem","border-radius":"1rem","border":"1ps solid #386010","box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)"}), style={"border-radius":"1rem","width":"5rem"}),
                                                dbc.Col(dbc.Button("Contract Manager", color="light", className="mr-1", href = "/vbc-demo/contract-manager/", style={"font-family":"NotoSans-Regular", "font-size":"1rem", "padding":"1rem", "padding":"1rem", "border-radius":"1rem","border":"1ps solid #386010","box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)"}), style={"border-radius":"1rem","width":"5rem"}),
                                                dbc.Col(dbc.Button("Contract Validator", color="light", className="mr-1", href = "/vbc-demo/contract-validator/", style={"font-family":"NotoSans-Regular", "font-size":"1rem", "padding":"1rem", "border-radius":"1rem","border":"1ps solid #386010","box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)"}), style={"border-radius":"1rem","width":"5rem"}),
                                                dbc.Col(dbc.Button("Tele Case Manager", color="light", className="mr-1", href = "/vbc-demo/tele-case-manager/", style={"font-family":"NotoSans-Regular", "font-size":"1rem", "padding":"1rem", "border-radius":"1rem","border":"1ps solid #386010","box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)"}), style={"border-radius":"1rem","width":"5rem"}),
                                            ],
                                            style={"background-color":"none", "font-family":"NotoSans-Regular", "font-size":"1rem", "border":"none","padding-top":"1rem","padding-bottom":"1rem","padding-left":"20rem","padding-right":"20rem"}
                                        )
                                    ]
                                )

                            ],
                            style={"background-color":"transparent", "border":"none"}
                            ),
                        ],
                        style={"margin-top":"-30rem","background-color":"transparent","text-align":"center"}
                    )
                    
                ])

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/vbc-demo/contract-manager/":
        return dashboard.create_layout(app)
    else:
        return launch_layout()
     

if __name__ == "__main__":
    app.run_server(host="127.0.0.1", port = 8052)
                        