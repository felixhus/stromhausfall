"""
layout.py creates the whole website dash layout by defining dash components and importing them from
dash_components.py.
"""

import dash_bootstrap_components as dbc
import dash_extensions as dex
import dash_mantine_components as dmc
from dash import dcc, html

import source.dash_components as dash_components

# root_path = '/home/stromhausfall/mysite/'
root_path = ''

# This list defines the buttons to add components to the grid. Structure:
# [dash button-id, iconify icon name, boolean if enabled or disabled, name for tooltip]
menu_objects = [
    ['button_house', 'bi:house-door', True, "Wohnhaus/Wohnung"],
    ['button_transformer', 'assets/Icons/icon_transformer.png', True, "Transformator"],
    ['button_externalgrid', 'assets/Icons/icon_powerplant.png', True, "Das Stromnetz"],
    ['button_pv', 'fa6-solid:solar-panel', True, "Solaranlage"],
    ['button_battery', 'material-symbols:battery-charging-20-outline', False, "Batteriespeicher"],
    # ['button_smartmeter', 'icon_meter.png', True, "Smart Meter"],
    ['button_switch_cabinet', 'icon-park-outline:connection-point', True, "Verteilerkasten"],
    ['button_line', 'mdi:powerline', True, "Leitung"],
]


def app_layout(app, button_dict):
    """
    Set layout of the given dash app. This function defines the whole layout by creating the main components in a grid,
    adding all dash components defined in "dash_components.py" and creating intervals, notification handlers and more.

    :param app: Dash app to add layout to
    :type app: dash app
    :param button_dict: Dictionary of menu buttons for the rooms.
    :type button_dict: dict
    :return: None
    """

    app.layout = dmc.NotificationsProvider(dbc.Container([
        dbc.Col([
            dbc.Row(
                dash_components.dash_navbar(),
            ),
            dbc.Row([
                dbc.Col([
                    dmc.Card([      # Button Card on the left
                        dbc.Row(dash_components.add_grid_object_button(object_id=menu_objects[i][0],
                                                                       enable=menu_objects[i][2],
                                                                       name=menu_objects[i][3],
                                                                       icon=menu_objects[i][1], app=app))
                        for i in range(len(menu_objects))
                    ], id='grid_buttons', style={'display': 'block'}, withBorder=True, shadow="sm", radius="md"),
                ], width=1),
                dbc.Col([dash_components.add_main_card_layout(button_dict)], width=7),  # Main Card in the middle
                dbc.Col([dash_components.add_card_start(), dash_components.add_card_menu()], width=True)    # Menu card on the right
            ]),
            dash_components.add_modal_readme(),             # Import all components from dash_components.py
            dash_components.add_drawer_notifications(),
            dash_components.add_modal_voltage_level(),
            dash_components.add_storage_variables(),
            dash_components.add_modal_devices(),
            dash_components.add_modal_load_configuration(),
            dash_components.add_modal_graph(),
            dash_components.add_tutorial(),
            dcc.Download(id='download_json'),               # Create downloads, intervals, event listeners etc.
            dcc.Interval(id='interval_refresh', interval=100, max_intervals=1),
            dcc.Interval(id='interval_backup', interval=10000),
            dex.EventListener(id='key_event_listener', events=[{'event': 'keydown', 'props': ["key"]}]),
        ], width=True),
        # dmc.Card(["Tutorial"], id='card_tutorial', withBorder=True, shadow="sm", radius="md"),
        html.Div(id='notification_container')
    ], id='main_container'))
