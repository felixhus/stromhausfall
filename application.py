"""
application.py is the application entry point. Here, the dash app object and server are defined,
the callbacks are included and the app is started.
"""

import dash_bootstrap_components as dbc
from dash import Dash

from callbacks.general_callbacks import general_callbacks
from callbacks.grid_callbacks import grid_callbacks
from callbacks.house_callbacks import house_callbacks
from callbacks.room_callbacks import room_callbacks
from source.layout import app_layout
from source.modules import get_button_dict

app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
app.title = 'PowerHouse'    # Define title for browser tab

server = app.server

rooms = ['bathroom', 'livingroom', 'kitchen', 'office']
button_dict = get_button_dict()  # Get button dict
app_layout(app, button_dict)     # Get layout of app

grid_callbacks(app)                         # Include grid callbacks
general_callbacks(app)                      # Include general callbacks
house_callbacks(app)                        # Include House callbacks
room_callbacks(app, button_dict, rooms)     # Include room callbacks

# Debug callback for development. Can be used to inspect all sort of states.
# Input is the debug button (has to be commentet in in dash_components) and by choosing states one can
# Inspect objects at all time.
# @app.callback(Output('graph_modal', 'figure'),
#               Output('modal_graph', 'opened'),
#               Input('debug_button', 'n_clicks'),
#               State('graph_power_house', 'figure'),
#               prevent_initial_call=True)
# def debug(btn, figure):
#     figure['layout']['height'] = None
#     figure['layout']['width'] = None
#     return figure, True


if __name__ == '__main__':
    app.run_server(debug=False)     # Run app

