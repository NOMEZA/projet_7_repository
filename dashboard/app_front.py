# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html,dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests
import dash_daq as daq
from json import loads # interpreter mon json et change en liste (transformer la representation de chaine de caractère  de la liste en liste python puisque le rendu ressemble en une liste de liste)

# all request here
#req=requests.get("http://127.0.0.1:5000/get_score/12")
data=requests.get("http://127.0.0.1:5000/get_info_client/100002").json()
data=pd.Series(data['info_client']).to_frame()
id_client=requests.get("http://127.0.0.1:5000/get_id_client").json()
id_client=id_client["data"][:30] # les 30 premiers
df=requests.get("http://127.0.0.1:5000/get_correlation").json()
df=pd.Series(df['correlation']).to_frame()
df=requests.get("http://127.0.0.1:5000/relevant_features").json()
#print (id_client)
x=['DAYS_BIRTH', 'DAYS_EMPLOYED', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3', 'AMT_INCOME_TOTAL', 'AMT_ANNUITY']

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
app = Dash(__name__)

# Build layout
app.layout = html.Div(
    [
        # titre principal
        html.Div([
            html.Div([
                html.H3("Dashboard sur le remboursement de credit"),
                html.H5("Projet 7")
                    ]
                )
            ],
        ),
        html.Div([
            html.P("select Id Client"),
            dcc.Dropdown(
                id_client,
                id='current_id_user',
                value = 193423,
                placeholder = "Select Id client",
            ),
        ]),
        html.Div([ 
            daq.Gauge(
                id='gauge_solvabilite_client',
                color={"gradient":True,"ranges":{"green":[0,0.3],"yellow":[0.3,0.6],"red":[0.6,1]}},
                value=0.5,
                label='Default',
                max=1,
                min=0,
                ),
            ]),
        # html.Div()
    ]
)

# histogramm chart
""" @app.callback(
    Output('histo_feature', 'value'),
    Input('current_id_user', 'value')
)
def update_histogram(id_user):
    data = requests.get(f"http://127.0.0.1:5000/relevant_features/{id_user}").json()
    data = ['DAYS_BIRTH', 'DAYS_EMPLOYED', 'EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3', 'AMT_INCOME_TOTAL',
                     'AMT_ANNUITY']
    data=pd.Series(data['relevant'])
    return data """

@app.callback(
    Output('gauge_solvabilite_client', 'value'),
    Input('current_id_user', 'value'))
def update_gauge_value(id_user):
    #print(id_user) # c'est l'id lorsqu'on change des valeurs dans la liste déroulante
    data = requests.get(f"http://127.0.0.1:5000/get_score/{id_user}").json()
    print(data)
    prediction = float(data["prediction"][1])
    return prediction
if __name__ == '__main__':
    app.run_server(debug=True, port=8000)