import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import numpy as np

app = dash.Dash(__name__, url_base_pathname='/vbc-demo/launch/', external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

def launch_layout():
    return dbc.Col([
                    html.Div(
                        [
                            html.H2("ValueGen Solution"),
                            html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem", "padding-top":"1px"})
                        ]
                    ),
                    dbc.Card([
                        dbc.CardBody([
                            dbc.CardLink("Contract Optimizer", href = "/vbc-demo/contract-optimizer/"),
                        ]),
                        dbc.CardBody([
                            dbc.CardLink("Contract Manager", href = "/vbc-demo/contract-manager/"),  
                        ]),
                        dbc.CardBody([
                            dbc.CardLink("Contract Validator", href = "/vbc-demo/contract-alidator/"),  
                        ]),
                        dbc.CardBody([
                            dbc.CardLink("Tele Case Manager", href = "/vbc-demo/tele-case-manager/"),  
                        ]),
                    ]),
    ])
        
app.layout = launch_layout()        

if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=False, port = 8052)
                        