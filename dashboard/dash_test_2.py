import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dash_daq as daq  # graphique jauge

df=pd.read_csv("../python_preprocessing/data_process.csv")



# https://www.bootstrapcdn.com/bootswatch/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
# ************************************************************************
app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1("get_score",
                        className='text-center text-primary mb-4'),
                width=12)
    ),

    dbc.Row([

        dbc.Col([
            dcc.Dropdown(id='id_client', multi=False, value='score',
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['target'].unique())],
                         ),
            # graphique jauge
            daq.Gauge(
                color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
                value=2,
                label='Default',
                max=10,
                min=0,
            ),
            dcc.Graph(id='line-fig', figure={})
        ],  # width={'size':5, 'offset':1, 'order':1},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            dcc.Dropdown(id='id_client', multi=True, value=['DAYS_BIRTH', 'AMT_INCOME_TOTAL'],
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['DAYS_BIRTH'].unique())],
                         ),
            dcc.Graph(id='line-fig2', figure={})
        ],  # width={'size':5, 'offset':0, 'order':2},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

    ], justify='start'),  # Horizontal:start,center,end,between,around

    dbc.Row([
        dbc.Col([
            html.P("get_info_client:",
                   style={"textDecoration": "underline"}),
            dcc.Checklist(id='my-checklist', value=['FB', 'GOOGL', 'AMZN'],
                          options=[{'label': x, 'value': x}
                                   for x in sorted(df['Symbols'].unique())],
                          labelClassName="mr-3"),
            dcc.Graph(id='my-hist', figure={}),
        ],  # width={'size':5, 'offset':1},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

        # Graphique avec un jauge



        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody(
                        html.P(
                            "We're better together. Help each other out!",
                            className="card-text")
                    ),
                    dbc.CardImg(
                        src="https://media.giphy.com/media/Ll0jnPa6IS8eI/giphy.gif",
                        bottom=True),
                ],
                style={"width": "24rem"},
            )
        ],  # width={'size':5, 'offset':1},
            xs=12, sm=12, md=12, lg=5, xl=5
        )
    ], align="center")  # Vertical: start, center, end

], fluid=True)


# Callback section: connecting the components
# ************************************************************************
# Line chart - Single
@app.callback(
    Output('line-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'] == stock_slctd]
    figln = px.line(dff, x='Date', y='High')
    return figln


# Line chart - multiple
@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-dpdn2', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    figln2 = px.line(dff, x='Date', y='Open', color='Symbols')
    return figln2


# Histogram
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-checklist', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    dff = dff[dff['Date'] == '2020-12-03']
    fighist = px.histogram(dff, x='Symbols', y='Close')
    return fighist


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)

# https://youtu.be/0mfIK8zxUds
