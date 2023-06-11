"""
application.py is the application entry point. Here, the dash app object and server are defined,
the callbacks are included and the app is started.
"""

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State
import pandas as pd
import json

from source.callbacks.general_callbacks import general_callbacks
from source.callbacks.grid_callbacks import grid_callbacks
from source.callbacks.house_callbacks import house_callbacks
from source.callbacks.room_callbacks import room_callbacks
from source.layout import app_layout
from source.modules import get_button_dict

app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
app.title = 'WattWerkstatt'    # Define title for browser tab

server = app.server

rooms = ['bathroom', 'livingroom', 'kitchen', 'office']
button_dict = get_button_dict()  # Get button dict
app_layout(app, button_dict)     # Get layout of app

grid_callbacks(app)                         # Include grid callbacks
general_callbacks(app)                      # Include general callbacks
house_callbacks(app)                        # Include House callbacks
room_callbacks(app, button_dict, rooms)     # Include room callbacks


# Debug callback for development. Can be used to inspect all sort of states.
# Input is the debug button (has to be commented in in dash_components) and by choosing states one can
# Inspect objects at all time.
# @app.callback(Output('download_json', 'data', allow_duplicate=True),
#               Input('debug_button', 'n_clicks'),
#               State('store_power_grid', 'data'),
#               prevent_initial_call=True)
# def debug(btn, data):
#     df_data = pd.read_json(data, orient='index')
#     print("Done")
#     return dict(content=json.dumps(df_data.to_dict()), filename="plot.json")


if __name__ == '__main__':
    app.run_server(debug=True)     # Run app

