import dash_bootstrap_components as dbc
from dash import Dash

from callbacks.bathroom_callbacks import bathroom_callbacks
from callbacks.general_callbacks import general_callbacks
from callbacks.grid_callbacks import grid_callbacks
from callbacks.house_callbacks import house_callbacks
from callbacks.kitchen_callbacks import kitchen_callbacks
from callbacks.livingroom_callbacks import livingroom_callbacks
from callbacks.office_callbacks import office_callbacks
from source.layout import app_layout

app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
app.title = 'PowerHouse'
server = app.server

app_layout(app)     # Get layout of app

grid_callbacks(app)         # Include grid callbacks
bathroom_callbacks(app)     # Include bathroom callbacks
kitchen_callbacks(app)      # Include bathroom callbacks
livingroom_callbacks(app)   # Include livingroom callbacks
office_callbacks(app)       # Include office callbacks
general_callbacks(app)      # Include general callbacks
house_callbacks(app)        # Include House initial callbacks


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
    app.run_server(debug=True, port=8051)

