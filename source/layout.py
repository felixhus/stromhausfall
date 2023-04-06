import dash_bootstrap_components as dbc
import dash_extensions as dex
import dash_mantine_components as dmc
from dash import dcc, html

import source.dash_components as dash_components

menu_objects = [
    ['button_house', 'icon_house2.png'],
    ['button_transformer', 'icon_transformer.png'],
    ['button_externalgrid', 'icon_powerplant.png'],
    ['button_pv', 'icon_pv.png'],
    ['button_battery', 'icon_battery.png'],
    ['button_smartmeter', 'icon_meter.png'],
    ['button_switch_cabinet', 'icon_switch_cabinet.png'],
    ['button_line', 'icon_line_lv.png'],
]

house_objects = [
    ['button_dryer', "Föhn"],
    ['button_fridge', "Kühlschrank"],
    ['button_lamp', "Lampe"],
    ['button_stove', "Herd"],
    ['button_tv', "TV"],
]


def app_layout(app):
    app.layout = dmc.NotificationsProvider(dbc.Container([
        dbc.Col([
            dbc.Row(
                dash_components.dash_navbar(),
            ),
            dbc.Row([
                dbc.Col([
                    dmc.Card([
                        dbc.Row(dash_components.add_grid_object_button(object_id=menu_objects[i][0],
                                                                       icon=app.get_asset_url(
                                                                           'Icons/' + menu_objects[i][1])))
                        for i in range(len(menu_objects))
                    ], id='grid_buttons', style={'display': 'block'}, withBorder=True, shadow="sm", radius="md"),
                    html.Div([
                        dbc.Row(dash_components.add_grid_object_button(object_id=house_objects[i][0],
                                                                       name=house_objects[i][1]))
                        for i in range(len(house_objects))
                    ], id='house_buttons', style={'display': 'none'}),
                ], width=1),
                dbc.Col([dash_components.add_cytoscape_layout()], width=7),
                dbc.Col([dash_components.card_start(), dash_components.card_menu()], width=True)
            ]),
            dash_components.add_modal_edit(),
            dash_components.add_modal_readme(),
            dash_components.add_drawer_notifications(),
            dash_components.add_modal_voltage_level(),
            dash_components.add_storage_variables(),
            dash_components.add_modal_timeseries(),
            dash_components.add_modal_load_configuration(),
            dcc.Download(id='download_json'),
            dex.EventListener(id='key_event_listener', events=[{'event': 'keydown', 'props': ["key"]}]),
            html.P(id='init')], width=True),
        html.Div(id='notification_container')
    ], id='main_container'))
