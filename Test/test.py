import dash
import dash_html_components as html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

app = dash.Dash(__name__)

app.layout = html.Div([dmc.Grid(children=[
    dmc.ActionIcon(
        DashIconify(icon=icon, width=20, rotate=rotation),
        size="lg",
        variant="transparent",
        id=button_id,
        color='blue'
    )
    for icon, button_id, rotation in zip(['gis:point', 'gis:north-arrow-n', 'gis:point'],
                                         ['button_north_west', 'button_north', 'button_north_east'], [0, 0, 0])
    ]),
    dmc.Grid(children=[dmc.ActionIcon(
        DashIconify(icon=icon, width=20, rotate=rotation),
        size="lg",
        variant="transparent",
        id=button_id,
        color='blue'
    )
    for icon, button_id, rotation in zip(['gis:north-arrow', 'fluent:compass-northwest-28-regular', 'gis:north-arrow'],
                                         ['button_west', 'button_compass', 'button_east'], [3, 0, 1])
    ]),
    dmc.Grid(children=[dmc.ActionIcon(
        DashIconify(icon=icon, width=20, rotate=rotation),
        size="lg",
        variant="transparent",
        id=button_id,
        color='blue'
    )
    for icon, button_id, rotation in zip(['gis:point', 'gis:north-arrow', 'gis:point'],
                                         ['button_south_west', 'button_south', 'button_south_east'], [0, 2, 0])
    ]),
])
# compass: fluent:compass-northwest-28-regular
if __name__ == '__main__':
    app.run_server(debug=True)
