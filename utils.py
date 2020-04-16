import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


def Header(app):
    return html.Div([get_header(app)])


def get_header(app):
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
                                        href="/demo-report/dashboard",
                                        className="tab first",
                                    ),
                                    dcc.Link(
                                        "Price Performance",
                                        href="/dash-financial-report/price-performance",
                                        className="tab",
                                    ),
                                    dcc.Link(
                                        "Portfolio & Management",
                                        href="/dash-financial-report/portfolio-management",
                                        className="tab",
                                    ),
                                    dcc.Link(
                                        "Fees & Minimums", href="/dash-financial-report/fees", className="tab"
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
