# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.



import dash_daq as daq
import dash_bootstrap_components as dbc
import pandas as pd
import requests
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.graph_objects as go
# all request here
#data = requests.get(f"http://127.0.0.1:5000/get_feature_importance").json()
CURRENT_CLIENT_ID = 193423
req=requests.get(f"http://127.0.0.1:5000/get_score/{CURRENT_CLIENT_ID}").json()
info_client=requests.get(f"http://127.0.0.1:5000/get_info_client/{CURRENT_CLIENT_ID}").json()
info_client=pd.Series(info_client['info_client']).to_frame().T.iloc[:,2:]
# print(info_client)
id_client=requests.get("http://127.0.0.1:5000/get_id_client").json()
id_client=id_client["data"][:30] # les 30 premiers

#df=requests.get("http://127.0.0.1:5000/get_correlation").json()
#df=pd.Series(df['correlation']).to_frame()
# df=requests.get("http://127.0.0.1:5000/relevant_features").json()
# print (id_client)
# x=['DAYS_BIRTH', 'DAYS_EMPLOYED', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3', 'AMT_INCOME_TOTAL', 'AMT_ANNUITY']
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])
# Instanciate the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Build layout
app.layout = html.Div(
    [
        # titre principal
        html.Div([
            html.Div([
                html.H1("Dashboard sur le remboursement de credit",
                        style={
                    "margin-top": "0px",
                    "color": "Black"
				}
                        ),
                html.H2("Projet 7", style={
                                    "margin-bottom": "0px",
                                    "color": "Black"
					                }),
                    ],id="title"
                )
            ],id = "header",
			className = "row flex-display",
			style = {
            "margin-bottom":"25px"
            }
        ),
        html.H4(f"Welcome user {CURRENT_CLIENT_ID} !"), html.H1(f"", className = "row flex-display",
                                        style = {
                                            "margin-bottom":"25px"
                                        }),
        dash_table.DataTable(
            info_client.to_dict('records'),
            [{"name": str(i), "id": str(i)} for i in info_client.columns],
        ),
        html.Br(),
        html.Div(
            [
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H4("Feature importance of the model", className = "row flex-display",
                                        style = {
                                            "margin-bottom":"25px"
                                        }),
                            html.Img(src="assets/lgbm_importances01.png", height=400),
                        ])
                    ], width=6),
                    dbc.Col([
                        html.Div([
                            html.H4("Distribution of Ages", className = "row flex-display",
                                        style = {
                                            "margin-bottom":"25px"
                                        }),
                            html.Img(src="assets/distribution_age_credit.png", height=400),

                        ])
                    ], width=6),
                ]),
            ]
        ),
        # Gestion des autres clients
        html.H4("Other clients"),

        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P("select Id Client"),
                        dcc.Dropdown(
                            id_client,
                            id='current_id_user',
                            value = 193423,
                            placeholder = "Select Id client",
                        ),
                    ]),
                ], width=4),
                dbc.Col([
                    html.P("select feature 1"),
                    dcc.Dropdown(
                        info_client.columns,
                        id='feature1',
                        value = info_client.columns[0],
                        placeholder = "Select feature 1",
                    ),
                ], width=4),
                dbc.Col([
                    html.P("select feature 2"),
                    dcc.Dropdown(
                        info_client.columns,
                        id='feature2',
                        value = info_client.columns[1],
                        placeholder = "Select feature 2",
                    ),
                ], width=4),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Graph(id = 'scatter_plot_bivarie')
                    ], className = "create_container"),
                ], width=6),
                dbc.Col([
                    html.Div([
                        daq.Gauge(
                            id='gauge_solvabilite_client',
                            color={"gradient": True,
                                   "ranges": {"green": [0, 0.3], "yellow": [0.3, 0.6], "red": [0.6, 1]}},
                            value=0.5,
                            label='Default',
                            max=1,
                            min=0,
                        ),
                    ], className = "create_container"),
                ], width=6),
            ]),
        ])

        # html.Div([
        #     dcc.Graph(
        #         id="pie_chart",
        #         config={
        #             "DisplayModeBar": "hover"
        #         }
        #     )
        # ]),
        # html.Div([
        #     dcc.RadioItems(
        #         id='radio-items',
        #         labelStyle={"display": "inline-block"},
        #         value="feature",
        #         options=[{'label': 'feature', 'value': 'feature'},
        #                  {'label': 'Importance', 'value': 'Importance'}],
        #     ),
        #     dcc.Graph(id = 'bar_chart',
        #               config = {'displayModeBar': 'hover'}, style = {'height': '350px'}),


        # ])
    ]
)

# bar chart
"""@app.callback(
    Output('bar_chart', 'value'),
    Input('radio-items', 'value')
)
def update_bar_cart(id_user):
    dataf = requests.get(f"http://127.0.0.1:5000/get_feature_importance").json()
    dataf=pd.Series(data[data])
    return data"""

@app.callback(
    Output('gauge_solvabilite_client', 'value'),
    Input('current_id_user', 'value'))
def update_gauge_value(id_user):
    #print(id_user) # c'est l'id lorsqu'on change des valeurs dans la liste déroulante
    score_client= requests.get(f"http://127.0.0.1:5000/get_score/{id_user}").json()
    prediction = float(score_client["prediction"][1])
    return prediction

@app.callback(
    Output('scatter_plot_bivarie', 'figure'),
    Input('feature1', 'value'),
    Input('feature2', 'value'),
    Input('current_id_user', 'value'))
def update_graph(feature1, feature2, id_client):
    info_client=requests.get(f"http://127.0.0.1:5000/get_info_client/{id_client}").json()
    info_client=pd.Series(info_client['info_client']).to_frame().T.iloc[:,2:]
    feature1_data= requests.get(f"http://127.0.0.1:5000/get_feature/{feature1}").json()["data"]
    feature2_data= requests.get(f"http://127.0.0.1:5000/get_feature/{feature2}").json()["data"]
    fig = go.Figure()

    # Add scatter trace with medium sized markers
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=feature1_data,
            y=feature2_data,
            marker=dict(
                color='LightSkyBlue',
                size=5,
                line=dict(
                    color='MediumPurple',
                    width=2
                )
            ),
            showlegend=False
        )
    )
    # Add trace with large marker
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=[info_client[feature1][0]],
            y=[info_client[feature2][0]],
            marker=dict(
                color='red',
                size=40,
                line=dict(
                    color='red',
                    width=12
                )
            ),
            showlegend=False
        )
    )
    fig.update_xaxes(title=feature1)
    fig.update_yaxes(title=feature2,)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)