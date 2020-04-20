import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


def Header_mgmt(app):
    return html.Div([get_header_mgmt(app)])

def Header_contract(app):
    return html.Div([get_header_contract(app)])


def get_header_mgmt(app):
    header = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem", "padding-top":"1px"})
                                ]
                            )
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dcc.Link(
                                        "Dashboard",
                                        href="/vbc-demo/dashboard/",
                                        className="tab first",
                                    ),
                                    dcc.Link(
                                        "Drilldown",
                                        href="/vbc-demo/drilldown/",
                                        className="tab",
                                    ),
                                    dcc.Link(
                                        "Report Generator",
                                        href="/vbc-demo/report-generator/",
                                        className="tab",
                                    ),
                                    dcc.Link(
                                        "Back to Homepage", 
                                        href="/vbc-demo/launch/", 
                                        className="tab"
                                    ),
                                ],
                                style={"margin-top":"8px"}
                            )
                        ),
                    ]    
                )
            ],
            style={"padding-top":"1rem"},
        )
            
    return header

def get_header_contract(app):
    header = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.Img(src=app.get_asset_url("logo-demo.png"), style={"height":"4rem", "padding-top":"1px"})
                                ]
                            )
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dcc.Link(
                                        "Contract Simulation",
                                        href="/vbc-demo/contract-simulation/",
                                        className="tab first",
                                    ),
                                    dcc.Link(
                                        "Metrics Library",
                                        href="/vbc-demo/metrics-library/",
                                        className="tab",
                                    ),
                                    dcc.Link(
                                        "Contract Generator",
                                        href="/vbc-demo/contract-generator/",
                                        className="tab",
                                    ),
                                    dcc.Link(
                                        "Back to Homepage", 
                                        href="/vbc-demo/launch/", 
                                        className="tab"
                                    ),
                                ],
                                style={"margin-top":"8px"}
                            )
                        ),
                    ]    
                )
            ],
            style={"padding-top":"1rem"},
        )
            
    return header



def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
