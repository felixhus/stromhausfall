import dash_bootstrap_components as dbc
from dash import Dash

from callbacks.bathroom_callbacks import bathroom_callbacks
from callbacks.general_callbacks import general_callbacks
from callbacks.grid_callbacks import grid_callbacks
from callbacks.kitchen_callbacks import kitchen_callbacks
from source.layout import app_layout

app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
app.title = 'PowerHouse'
server = app.server

app_layout(app)     # Get layout of app

grid_callbacks(app)         # Include grid callbacks
bathroom_callbacks(app)     # Include bathroom callbacks
kitchen_callbacks(app)     # Include bathroom callbacks
general_callbacks(app)      # Include general callbacks


# @app.callback(Output('store_menu_change_tab', 'data'),
#               Input('debug_button', 'n_clicks'),
#               State('menu_parent_tabs', 'children'),
#               prevent_initial_call=True)
# def debug(btn, children):
#     tab_id = str(random.randrange(1000))
#     return 'tab1'


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

