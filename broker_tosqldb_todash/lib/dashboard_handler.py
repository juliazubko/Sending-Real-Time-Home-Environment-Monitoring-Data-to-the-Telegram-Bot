import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import sqlite3
import pandas as pd


class DashBoardHandler:
    def __init__(self, db_file, sensor_table_name):
        self.db_file = db_file
        self.sensor_table_name = sensor_table_name
        self.app = dash.Dash(__name__)

        # Define CSS styles
        colors = {
            'background': '#212946',  # Dark blue
            'text': 'gray'
        }

        self.app.layout = html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
            html.H1(children="Sensor Data", style={'textAlign': 'center', 'color': colors['text']}),
            dcc.Graph(id='live-update-graph-temperature', style={'height': '50vh',
                                                                 'width': '100%', 'display': 'block'}),
            dcc.Graph(id='live-update-graph-humidity', style={'height': '50vh',
                                                              'width': '100%', 'display': 'block'}),
            dcc.Interval(
                id='interval-component',
                interval=2 * 1000,  # in milliseconds
                n_intervals=0
            )
        ])

        self.app.callback(Output('live-update-graph-temperature', 'figure'),
                          Output('live-update-graph-humidity', 'figure'),
                          #  Output('live-update-graph-bar', 'figure'),
                          [Input('interval-component', 'n_intervals')])(self.update_graphs)

    def update_graphs(self, n):
        # Create a connection to SQLite database
        conn = sqlite3.connect(self.db_file)

        # Fetch sensor data
        df_sensor = pd.read_sql_query("SELECT * from {}".format(self.sensor_table_name), conn)

        conn.close()

        # Get the current temp_dht value
        current_temp_dht = df_sensor['temp_dht'].iloc[-1]

        # Graph data for Temperature
        graph_temp = {
            'data': [
                {
                    'x': df_sensor['time'],
                    'y': df_sensor['temp_analog'],
                    'name': 'temp_analog',
                    'line': {'color': 'lime', 'width': 1},
                    'fill': 'tozeroy',
                    'fillcolor': 'rgba(0,255,0,0.05)',
                    'mode': 'lines',
                    'type': 'scattergl'
                },
                {
                    'x': df_sensor['time'],
                    'y': df_sensor['temp_dht'],
                    'name': 'temp_dht',
                    'line': {'color': 'cyan', 'width': 1},
                    'fill': 'tozeroy',
                    'fillcolor': 'rgba(0,255,255,0.05)',
                    'mode': 'lines',
                    'type': 'scattergl'
                }
            ],
            'layout': {
                'title': {'text': 'Temperature Data', 'font': {'color': 'gray'}},
                'plot_bgcolor': '#212946',
                'paper_bgcolor': '#212946',
                'xaxis': {'gridcolor': '#2A3459', 'color': 'gray',
                          'title': {'text': 'Time', 'font': {'color': 'gray'}}},
                'yaxis': {'gridcolor': '#2A3459', 'color': 'gray',
                          'title': {'text': 'Temperature', 'font': {'color': 'gray'}},
                          'range': [current_temp_dht - 2, current_temp_dht + 2]},
                'legend': {'font': {'color': 'gray'}}
            }
        }

        # Get the current humidity value
        current_humidity = df_sensor.iloc[-1]['humidity']

        # Graph data for Humidity
        graph_humidity = {
            'data': [
                {
                    'x': df_sensor['time'],
                    'y': df_sensor['humidity'],
                    'name': 'humidity',
                    'line': {'color': 'magenta', 'width': 1},
                    'fill': 'tozeroy',
                    'fillcolor': 'rgba(255,0,255,0.05)',
                    'mode': 'lines',
                    'type': 'scattergl'
                }
            ],
            'layout': {
                'title': {'text': 'Humidity Data', 'font': {'color': 'gray'}},
                'plot_bgcolor': '#212946',
                'paper_bgcolor': '#212946',
                'xaxis': {'gridcolor': '#2A3459', 'color': 'gray',
                          'title': {'text': 'Time', 'font': {'color': 'gray'}}},
                'yaxis': {'gridcolor': '#2A3459', 'color': 'gray',
                          'title': {'text': 'Humidity', 'font': {'color': 'gray'}},
                          'range': [current_humidity - 20, current_humidity + 20]},
                'legend': {'font': {'color': 'gray'}}
            }
        }

        graph_temp['layout'].update(showlegend=True)
        graph_humidity['layout'].update(showlegend=True)

        return graph_temp, graph_humidity

    def run(self):
        self.app.run_server(debug=False)
