import dash_bootstrap_components as dbc
import dash_extensions as dex
import dash_mantine_components as dmc
from dash import dcc, html

import source.dash_components as dash_components

menu_objects = [
    ['button_house', 'bi:house-door', True, "Wohnhaus/Wohnung"],
    ['button_transformer', 'Icons/icon_transformer.png', True, "Transformator"],
    ['button_externalgrid', 'Icons/icon_powerplant.png', True, "Das Stromnetz"],
    ['button_pv', 'fa6-solid:solar-panel', True, "Solaranlage"],
    ['button_battery', 'material-symbols:battery-charging-20-outline', False, "Batteriespeicher"],
    # ['button_smartmeter', 'icon_meter.png', True, "Smart Meter"],
    ['button_switch_cabinet', 'icon-park-outline:connection-point', True, "Verteilerkasten"],
    ['button_line', 'mdi:powerline', True, "Leitung"],
]


def app_layout(app, button_dict):
    app.layout = dmc.NotificationsProvider(dbc.Container([
        dbc.Col([
            dbc.Row(
                dash_components.dash_navbar(),
            ),
            dbc.Row([
                dbc.Col([
                    dmc.Card([
                        dbc.Row(dash_components.add_grid_object_button(object_id=menu_objects[i][0],
                                                                       enable=menu_objects[i][2],
                                                                       name=menu_objects[i][3],
                                                                       icon=menu_objects[i][1], app=app))
                        for i in range(len(menu_objects))
                    ], id='grid_buttons', style={'display': 'block'}, withBorder=True, shadow="sm", radius="md"),
                ], width=1),
                dbc.Col([dash_components.add_cytoscape_layout(button_dict)], width=7),
                dbc.Col([dash_components.card_start(), dash_components.card_menu()], width=True)
            ]),
            dash_components.add_modal_readme(),
            dash_components.add_drawer_notifications(),
            dash_components.add_modal_voltage_level(),
            dash_components.add_storage_variables(),
            # dash_components.add_modal_timeseries(),
            dash_components.add_modal_devices(),
            dash_components.add_modal_load_configuration(),
            dash_components.add_modal_graph(),
            dcc.Download(id='download_json'),
            dcc.Interval(id='interval_refresh', interval=100, max_intervals=1),
            dcc.Interval(id='interval_backup', interval=10000),
            dex.EventListener(id='key_event_listener', events=[{'event': 'keydown', 'props': ["key"]}]),
            html.P(id='init')], width=True),
        html.Div(id='notification_container')
    ], id='main_container'))
