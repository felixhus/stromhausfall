import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_mantine_components as dmc
import numpy as np
from dash import dash_table, dcc, html
from dash_iconify import DashIconify

import source.plot as plot
import source.stylesheets as stylesheets

devices = {'bathroom': [["Föhn", 'button_add_hairdryer', 'icon-park-outline:hair-dryer'],
                        ["Zahnbürste", 'button_add_toothbrush', 'mdi:toothbrush-electric'],
                        ["Bügeleisen", 'button_add_iron', 'tabler:ironing-1']],
           'kitchen': [["Wasserkocher", 'button_add_kettle', 'material-symbols:kettle-outline'],
                       ["Kaffeemaschine", 'button_add_coffee', 'ic:outline-coffee'],
                       ["Ofen", 'button_add_oven', 'material-symbols:oven-gen-outline']]}

urls = {'cyto_bathroom': 'url(/assets/background_bathroom.png)', 'cyto_kitchen': 'url(/assets/background_kitchen.png)'}

device_dict_init = {'house1': {}, 'rooms': {}, 'last_id': 1}


def add_storage_variables():
    return html.Div([dcc.Store(id='start_of_line'), dcc.Store(id='store_add_node'),
                     dcc.Store(id='store_line_edit_active'), dcc.Store(id='store_selected_element_grid'),
                     dcc.Store(id='store_selected_element_house'), dcc.Store('store_custom_house', data=None),
                     dcc.Store(id='store_element_deleted'), dcc.Store(id='store_notification1'),
                     dcc.Store(id='store_notification2'), dcc.Store(id='store_notification4'),
                     dcc.Store(id='store_notification3'), dcc.Store(id='store_notification5'),
                     dcc.Store(id='store_notification6'), dcc.Store(id='store_notification7'),
                     dcc.Store(id='store_notification8'),
                     dcc.Store(id='store_get_voltage'), dcc.Store(id='store_update_switch'),
                     dcc.Store(id='store_edge_labels'), dcc.Store(id='store_timestep'),
                     dcc.Store(id='store_flow_data'), dcc.Store(id='store_menu_change_tab_grid'),
                     dcc.Store(id='store_menu_change_tab_house'), dcc.Store(id='store_menu_inputs', data={}),
                     dcc.Store(id='store_grid_object_dict', data={}),
                     dcc.Store(id='store_device_dict', data=device_dict_init),
                     dcc.Store(id='store_results_house')])


def add_grid_object_button(object_id, name=None, linked_object=None, icon=None):
    """
    Methode erzeugt einen Button für das Menü, um Grid-Objekte hinzuzufügen.
    :param object_id: Id des Buttons
    :param linked_object: Node, der beim Klicken zum Grid hinzugefügt wird.
    :param name: Name des Buttons
    :param icon: Pfad zum anzuzeigenden Icon
    :return: DBC Button
    """
    # children = html.Img(src=icon, width=stylesheets.button_add_components_style['width'])
    if icon is not None:
        children = html.Img(src=icon, height=str(stylesheets.button_add_components_style['icon_width']))
    else:
        children = name
    return dmc.Button(id=object_id, children=children, style=stylesheets.button_add_components_style)


def add_cytoscape_grid(nodes, edges):
    cytoscape = dbc.Card(
        children=[dbc.CardBody(
            cyto.Cytoscape(
                id='cyto1',
                layout={'name': 'preset'},
                autoRefreshLayout=False,
                style={'width': '100%', 'height': '100%', 'background': '#e6ecf2', 'frame': 'blue'},
                elements=edges + nodes,
                stylesheet=stylesheets.cyto_stylesheet)),
            dbc.CardFooter(dmc.Slider(
                id='timestep_slider', value=0, updatemode='drag',
                min=1, max=10, step=1))],
        # withBorder=True,
        # shadow="sm",
        # radius="md",
        style={'height': '100%'})
    return cytoscape


def add_menu_dropdown(room_type):
    item_list = []
    for item in devices[room_type]:
        item_list.append(dmc.MenuItem(item[0], id=item[1], icon=DashIconify(icon=item[2])))
    item_list.append(dmc.MenuDivider())
    item_list.append(
        dmc.MenuItem("Schließen", id='button_close_menu_' + room_type,
                     icon=DashIconify(icon='material-symbols:close-rounded'),
                     color='red'))
    return dmc.MenuDropdown(item_list)


def add_cytoscape(cyto_id, elements):
    return html.Div(cyto.Cytoscape(
        id=cyto_id,
        layout={'name': 'preset'},
        autoRefreshLayout=False,
        elements=elements,
        style={'background': '#e6ecf2', 'frame': 'blue', 'height': '200px',
               'background-image': urls[cyto_id], 'background-size': 'contain', 'background-repeat': 'no-repeat'},
        stylesheet=stylesheets.cyto_stylesheet))


def add_cytoscape_layout():
    elements = [
        {'data': {'id': 'power_strip'}, 'classes': 'power_strip_style'},
        {'data': {'id': 'plus', 'parent': 'power_strip'}, 'position': {'x': 75, 'y': 175},
         'classes': 'room_node_style', 'style': {'background-image': ['/assets/Icons/icon_plus.png']}}]

    return dbc.Card(
        children=[
            dbc.CardBody(
                dmc.Tabs([
                    dmc.TabsList([
                        dmc.Tab("Netz", value="grid", icon=DashIconify(icon='tabler:chart-grid-dots')),
                        dmc.Tab("Haus", value="house1", disabled=True, id='tab_house',
                                icon=DashIconify(icon='material-symbols:house-siding-rounded')),
                        dmc.Tab("Einstellungen", value="settings",
                                icon=DashIconify(icon='material-symbols:settings-outline'))
                    ]),
                    dmc.TabsPanel(children=[
                        cyto.Cytoscape(
                            id='cyto1',
                            layout={'name': 'preset'},
                            autoRefreshLayout=False,
                            elements=[],
                            style={'background': '#e6ecf2', 'frame': 'blue', 'height': '475px'},
                            stylesheet=stylesheets.cyto_stylesheet)],
                        value='grid'),
                    dmc.TabsPanel(children=[
                        dbc.Container([
                            dbc.Row([
                                dbc.Col([
                                    dmc.Menu([
                                        dmc.MenuTarget(html.Div(id='menu_target_bathroom')),
                                        add_menu_dropdown('bathroom')
                                    ], id='menu_devices_bathroom', position='left-start', withArrow=True),
                                    add_cytoscape('cyto_bathroom', elements)
                                ], width=6),
                                dbc.Col([
                                    dmc.Menu([
                                        dmc.MenuTarget(html.Div(id='menu_target_kitchen')),
                                        add_menu_dropdown('kitchen')
                                    ], id='menu_devices_kitchen', position='left-start', withArrow=True),
                                    add_cytoscape('cyto_kitchen', elements)
                                ], width=6)
                            ]),
                            dmc.Space(h=20),
                            dbc.Row([
                                dbc.Col([
                                    cyto.Cytoscape(
                                        id='cyto_house3',
                                        layout={'name': 'preset'},
                                        autoRefreshLayout=False,
                                        elements=[],
                                        style={'background': '#e6ecf2', 'height': '200px'},
                                        stylesheet=stylesheets.cyto_stylesheet)
                                ], width=6),
                                dbc.Col([
                                    cyto.Cytoscape(
                                        id='cyto_house4',
                                        layout={'name': 'preset'},
                                        autoRefreshLayout=False,
                                        elements=[],
                                        style={'background': '#e6ecf2', 'frame': 'blue', 'height': '200px', },
                                        stylesheet=stylesheets.cyto_stylesheet)
                                ], width=6)
                            ]),
                        ])
                    ], value='house1'),
                    dmc.TabsPanel(children=[
                        dmc.Space(h=20),
                        dmc.NumberInput(
                            id='input_week', label="Kalenderwoche",
                            value=1, step=1,
                            min=1, max=52,
                            style={"width": 250},
                        ),
                        dmc.Space(h=20),
                        dmc.NumberInput(
                            id='input_year', label="Jahr",
                            value=2015, step=1,
                            min=2015, max=2015,
                            style={"width": 250}, disabled=True
                        )
                    ], value='settings')
                ],
                    id='tabs_main', value='grid', color="blue", orientation="horizontal", allowTabDeactivation=True)
            ),
            dbc.CardFooter(dmc.Slider(
                id='timestep_slider', value=0, updatemode='drag',
                min=1, max=10, step=1))
        ], style={'height': '100%'}
    )


def add_room(id_cyto, elements):
    cytoscape_room = dbc.Card(
        children=[
            cyto.Cytoscape(
                id=id_cyto,
                layout={'name': 'preset'},
                autoRefreshLayout=False,
                style={'width': '100%', 'height': '100%', 'background': '#e6ecf2', 'frame': 'blue', },
                # 'background-image': background_bath_url},
                elements=elements,
                stylesheet=stylesheets.cyto_stylesheet)],
        style={'height': '100%'})
    return cytoscape_room


def add_modal_readme():
    with open('README.md', encoding='UTF-8') as file:
        content_readme = file.read()
    return dmc.Modal(
        title="Readme",
        id="modal_readme",
        children=dcc.Markdown(content_readme),
        opened=False,
        size='55%'
    )


def add_modal_edit():
    return dmc.Modal(
        title="Edit",
        id='modal_edit',
        children=[
            dmc.Text("", id='modal_text'),
            dmc.Space(h=20),
            dmc.ChipGroup([
                dmc.Chip(x, value=x) for x in ["Last", "Einspeisung"]], value="Last", id='chips_type'
            ),
            dmc.Space(h=20),
            dmc.NumberInput(
                id='power_input',
                label="Leistung dieses Elements in kW:",
                # description="From 0 to infinity, in steps of 5",
                value=0,
                min=0,
                step=0.1, precision=1,
                stepHoldDelay=500, stepHoldInterval=100,
                icon=DashIconify(icon="material-symbols:download"),
                style={"width": 250},
            ),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='modal_edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='modal_edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline")),
                dmc.Button("Schließen", variant='outline', id='modal_edit_close_button')
            ], position='right')
        ]
    )


def add_modal_voltage_level():
    return dmc.Modal(
        title="Spannungsebene auswählen",
        id='modal_voltage',
        children=[
            dmc.Text(
                "Möchtest du das Element mit der Ober- oder Unterspannungsseite des Transformators verbinden (20kV oder 400V)?"),
            dmc.Space(h=20),
            dmc.ButtonGroup([
                dmc.Button("20 kV", id='button_voltage_hv', variant='outline',
                           leftIcon=DashIconify(icon="ph:arrow-fat-lines-up")),
                dmc.Button("400 V", id='button_voltage_lv', variant='outline',
                           rightIcon=DashIconify(icon="ph:arrow-fat-lines-down"))
            ])
        ]
    )


def dash_navbar():
    navbar = dbc.Navbar(
        dbc.Container([
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(dmc.Button(
                            [
                                "Notifications",
                                dbc.Badge(
                                    id='bade_notifications',
                                    color="danger",
                                    pill=True,
                                    text_color="white",
                                    className="position-absolute top-0 start-100 translate-middle",
                                ),
                            ],
                            id='button_notifications',
                            color="primary",
                            className="position-relative",
                        )),
                        dbc.Col(dbc.NavbarBrand("PowerHouse", className="ms-2"))
                    ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dmc.Group([
                dmc.Button("Beispielnetz", id='example_button', n_clicks=0, variant='gradient',
                           gradient={"from": "teal", "to": "blue", "deg": 60}),
                dmc.Button("README", id='button_readme', n_clicks=0,
                           leftIcon=DashIconify(icon="mdi:file-document"), variant='gradient'),
                dmc.Menu([
                    dmc.MenuTarget(dmc.Button("Menü", leftIcon=DashIconify(icon="material-symbols:menu-rounded"),
                                              variant='gradient'),),
                    dmc.MenuDropdown([
                        dmc.MenuItem("Konfiguration speichern", icon=DashIconify(icon="iconoir:save-action-floppy"),
                                     id='menu_item_save'),
                        dmc.MenuItem("Konfiguration laden", icon=DashIconify(icon="iconoir:load-action-floppy"),
                                     id='menu_item_load'),
                    ])
                ], trigger='hover', openDelay=100, closeDelay=200, transition="rotate-right", transitionDuration=150),
                dmc.Button("Debug", id='debug_button', variant="gradient", leftIcon=DashIconify(icon='gg:debug'),
                           gradient={"from": "grape", "to": "pink", "deg": 35})
            ], spacing=10
            ),
        ]), color="dark", dark=True
    )
    return navbar


def card_start():
    card = dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src="https://images.unsplash.com/photo-1598528133401-228e74463adb?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80",
                    # height=160,
                )
            ),
            dmc.Group(
                [
                    dmc.Text("Power House Simulator", weight=500),
                    dmc.Badge("Beta", color="blue", variant="light"),
                ],
                position="apart",
                mt="md",
                mb="xs",
            ),
            dmc.Text(
                "Verstehe durch ausprobieren, was in deinem Haus und Stromnetz um dich herum wirklich passiert!",
                size="sm",
                color="dimmed",
            ),
            dmc.Space(h=20),
            dmc.Button("Start", leftIcon=DashIconify(icon='material-symbols:play-arrow-outline-rounded'),
                       id='button_start')
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"height": '100%'},
    )
    return dmc.Modal([card], id='modal_start', opened=True, withCloseButton=False, radius=10)


def card_menu():
    card = dmc.Card(
        children=[dmc.LoadingOverlay(
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Bearbeiten", value="edit",
                                    icon=DashIconify(icon="material-symbols:edit-square-outline")),
                            dmc.Tab("Ergebnisse", value="results", icon=DashIconify(icon="fluent:poll-16-regular")),
                        ]
                    ),
                    dmc.TabsPanel(children=[
                        dmc.Space(h=20),
                        dmc.Tabs(children=[
                            add_menu_tab_panel('empty', None, None),
                            add_menu_tab_panel('init_ids', None, None),
                        ], id='menu_parent_tabs'),
                        dmc.Space(h=20),
                        dmc.Group([
                            dmc.Button("Berechnen", id='button_calculate', rightIcon=DashIconify(icon="ph:gear-light")),
                            dmc.Switch(
                                id='active_switch_house',
                                thumbIcon=DashIconify(
                                    icon="material-symbols:mode-off-on", width=16,
                                    color=dmc.theme.DEFAULT_COLORS["teal"][5]
                                ),
                                size="md",
                                color="teal",
                                checked=False,
                                style={'display': 'none'}
                            ),
                            dmc.Switch(
                                id='active_switch_grid',
                                thumbIcon=DashIconify(
                                    icon="material-symbols:mode-off-on", width=16,
                                    color=dmc.theme.DEFAULT_COLORS["orange"][5]
                                ),
                                size="md",
                                color="orange",
                                checked=False,
                                style={'display': 'block'}
                            )
                        ], position='apart')],
                        value="edit"),
                    dmc.TabsPanel(children=[
                        dmc.Tabs(children=[
                            add_result_tab_panel('empty'),
                            add_result_tab_panel('house')
                        ], id='result_parent_tabs'),
                        dmc.Space(h=20),
                        dmc.Alert(children="", id="alert_externalgrid", color='primary', hide=True),
                        dmc.CardSection(
                            dmc.Image(id='graph_image', src='assets/temp/graph.png', withPlaceholder=True,
                                      style={'display': 'none'})
                        ),
                    ], value="results"),
                ],
                id='tabs_menu', value='edit', color="blue", orientation="horizontal",
            ), loaderProps={"variant": "bars", "color": "blue", "size": "lg"})
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"height": '100%'},
    )
    return html.Div([card], id='card_menu', style={'display': 'block'})


def add_result_tab_panel(tab_value):
    if tab_value == 'empty':
        return dmc.TabsPanel(
            value=tab_value
        )
    elif tab_value == 'house':
        return dmc.TabsPanel([
            dmc.Space(h=20),
            dcc.Graph(id='graph_power_house'),
            dcc.Graph(id='graph_sunburst_house'),
        ],
            value=tab_value
        )


def add_menu_tab_panel(tab_value, selected_element, element_dict):
    if tab_value == 'house':
        control, fade = 'preset', True  # Get values from element and show tab dependent on them
        if element_dict[selected_element]['config_mode'] == 'custom':
            control, fade = 'custom', False
        return dmc.TabsPanel([
            dmc.TextInput(
                id='name_input',
                style={"width": 200},
                value=element_dict[selected_element]['name'],
                icon=DashIconify(icon="emojione-monotone:name-badge"),
            ),
            dmc.Space(h=20),
            dmc.SegmentedControl(id='house_mode', value=control,
                                 data=[{'value': 'preset', 'label': "Fertige Profile"},
                                       {'value': 'custom', 'label': "Selbst basteln"}]),
            dbc.Fade([
                dmc.Space(h=20),
                dmc.Select(
                    label=["Lastprofil ",
                           dbc.Badge(DashIconify(icon="ic:round-plus"), id='pill_add_profile', pill=True,
                                     color='primary')],
                    placeholder="Auswahl",
                    id='load_profile_select',
                    value=element_dict[selected_element]['selected_power_option'],
                    data=[
                        {'value': key, 'label': key}
                        for key in element_dict[selected_element]['power_options']
                    ],
                )], id='house_fade', is_in=fade),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"))
            ], position='right'),
            dmc.Space(h=20),
            # dcc.Graph(figure=plot.plot_device_timeseries(np.linspace(0, 24, num=1440),
            #                                              element_dict[selected_element]['power'],
            #                                              'rgb(175, 173, 222)'), id='graph_device',
            #           style={'width': '100%'})
        ],
            value=tab_value)
    elif tab_value == 'pv':
        postcode = element_dict[selected_element]['location'][0]
        if postcode is None:
            postcode = ""
        return dmc.TabsPanel([
            dmc.TextInput(
                id='name_input',
                style={"width": 200},
                value=element_dict[selected_element]['name'],
                icon=DashIconify(icon="emojione-monotone:name-badge"),
            ),
            dmc.Space(h=20),
            dmc.TextInput(id='postcode_input', placeholder='Postleitzahl', icon=DashIconify(icon="mdi:home-location"),
                          value=postcode),
            dmc.Space(h=20),
            get_compass(element_dict[selected_element]['orientation']),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"))
            ], position='right'),
            dmc.Space(h=20),
            dcc.Graph(figure=plot.plot_pv_timeseries(np.linspace(0, 168, num=169),
                                                     element_dict[selected_element]['power'],
                                                     'rgb(255, 248, 94)'), id='graph_pv',
                      style={'width': '100%'}),
            dmc.Space(h=20)
        ],
            value=tab_value)
    elif tab_value == 'line':
        return dmc.TabsPanel([
            dmc.Text("Leitung"),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"))
            ], position='right')],
            value=tab_value
        )
    elif tab_value == 'device_preset':
        return dmc.TabsPanel([
            # dmc.Text("Gerät Badezimmer"),
            dmc.TextInput(
                id='name_input',
                style={"width": 200},
                value=element_dict[selected_element]['name'],
                icon=DashIconify(icon="emojione-monotone:name-badge"),
            ),
            dmc.Space(h=20),
            dmc.Select(
                label=["Lastprofil ",
                       dbc.Badge(DashIconify(icon="ic:round-plus"), id='pill_add_profile', pill=True, color='primary')],
                placeholder="Auswahl",
                id='load_profile_select',
                value=element_dict[selected_element]['selected_power_option'],
                data=[
                    {'value': key, 'label': key}
                    for key in element_dict[selected_element]['power_options']
                ],
            ),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"))
            ], position='right'),
            dmc.Space(h=20),
            dcc.Graph(figure=plot.plot_device_timeseries(np.linspace(0, 24, num=1440),
                                                         element_dict[selected_element]['power'],
                                                         'rgb(175, 173, 222)'), id='graph_device',
                      style={'width': '100%'})
        ],
            value=tab_value)
    elif tab_value == 'device_custom':
        return dmc.TabsPanel([
            dmc.TextInput(
                id='name_input',
                style={"width": 200},
                value=element_dict[selected_element]['name'],
                icon=DashIconify(icon="emojione-monotone:name-badge"),
            ),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Select(
                    label=["Lastprofil ",
                           dbc.Badge(DashIconify(icon="ic:round-plus"), id='pill_add_profile', pill=True,
                                     color='primary')],
                    placeholder="Auswahl",
                    id='load_profile_select',
                    value=element_dict[selected_element]['selected_power_option'],
                    data=[
                        {'value': key, 'label': key}
                        for key in element_dict[selected_element]['power_options']
                    ],
                ),
                dmc.TimeInput(id='time_input_menu', label="Einschalten um", clearable=True,
                              icon=DashIconify(icon='material-symbols:avg-time-outline'))
            ], noWrap=True, grow=True),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"))
            ], position='right'),
            dmc.Space(h=20),
            dcc.Graph(figure=plot.plot_device_timeseries(np.linspace(0, 24, num=1440),
                                                         element_dict[selected_element]['power'],
                                                         'rgb(175, 173, 222)'), id='graph_device',
                      style={'width': '100%'}),
            dmc.Space(h=10),
            dmc.SegmentedControl(
                id='pagination_days_menu',
                value='mo',
                data=[
                    {'value': 'mo', 'label': 'MO'}, {'value': 'tu', 'label': 'DI'}, {'value': 'wd', 'label': 'MI'},
                    {'value': 'th', 'label': 'DO'}, {'value': 'fr', 'label': 'FR'}, {'value': 'sa', 'label': 'SA'},
                    {'value': 'su', 'label': 'SO'}
                ]
            )
        ],
            value=tab_value)
    elif tab_value == 'lamp':
        return dmc.TabsPanel([
            # dmc.Text("Lampe"),
            dmc.TextInput(
                id='name_input',
                style={"width": 200},
                value=element_dict[selected_element]['name'],
                icon=DashIconify(icon="emojione-monotone:name-badge"),
            ),
            dmc.Space(h=20),
            dmc.Select(
                label=["Lastprofil ",
                       dbc.Badge(DashIconify(icon="ic:round-plus"), id='pill_add_profile', pill=True, color='primary')],
                placeholder="Auswahl",
                id='load_profile_select',
                value=element_dict[selected_element]['selected_power_option'],
                data=[
                    {'value': key, 'label': key}
                    for key in element_dict[selected_element]['power_options']
                    # {'value': value,
                    #  'label': dmc.Group([DashIconify(
                    #      icon=element_dict[selected_element]['power_options'][value]['icon']), value])}
                    # for value in element_dict[selected_element]['power_options']
                ],
                # style={"width": 200},
            ),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"))
            ], position='right'),
            dcc.Graph(figure=plot.plot_device_timeseries(np.linspace(0, 24, num=1440),
                                                         element_dict[selected_element]['power'],
                                                         'rgb(175, 173, 222)'), id='graph_device',
                      style={'width': '100%'})
        ],
            value=tab_value
        )
    elif tab_value == 'power_strip':
        return dmc.TabsPanel([
            dmc.Text([DashIconify(icon='mdi:power-socket-de'),
                      " Die einzelnen Steckdosen der Steckdosenleiste können durch Klicken an- und ausgeschaltet werden."])
        ], value=tab_value)
    elif tab_value == 'empty':
        return dmc.TabsPanel([
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"))
            ], position='right', style={'display': 'none'})],
            value=tab_value
        )
    elif tab_value == 'init_ids':  # If there are components in the menu tabs, which act as inputs or Outputs of
        return dmc.TabsPanel([  # Callbacks, they are not present when the callback is created, because the tab
            dmc.SegmentedControl(id='house_mode', data=[]),  # is only created when a node was clicked.
            dbc.Fade(id='house_fade'),  # This hidden tab initializes the ids of these.
            dmc.SegmentedControl(id='pagination_days_menu', data=[])
        ], value=tab_value)


def get_compass(orientation):
    return html.Div([dmc.Grid(children=[
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
        dmc.Grid(children=[
            dmc.ActionIcon(
                DashIconify(icon='gis:north-arrow', width=20, rotate=3),
                size="lg",
                variant="transparent",
                id='button_west',
                color='blue'
            ),
            dmc.ActionIcon(
                DashIconify(icon='ri:compass-discover-line', width=20, rotate=0),
                size="lg",
                variant="transparent",
                id='button_compass',
                color='blue',
                style={'transform': f'rotate({orientation-45}deg)'}
            ),
            dmc.ActionIcon(
                DashIconify(icon='gis:north-arrow', width=20, rotate=1),
                size="lg",
                variant="transparent",
                id='button_east',
                color='blue'
            )
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


def add_modal_timeseries():
    return dmc.Modal(
        title='Neue Lastkurve anlegen',
        id='modal_timeseries',
        children=[
            dash_table.DataTable(
                id='timeseries_table',
                columns=[
                    {'id': 'time', 'name': 'Zeit in min'},
                    {'id': 'power', 'name': 'Leistung in W'}],
                data=[
                    {'time': '', 'power': ''}],
                editable=True,
                row_deletable=True
            ),
            dmc.Space(h=20),
            dmc.TextInput(
                id='textinput_profile_name',
                style={"width": 200},
                placeholder="Name des Lastprofils",
                icon=DashIconify(icon="mdi:graph-timeline-variant"),
            ),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button('Wert hinzufügen', id='button_add_value'),
                dmc.Button('Profil speichern', id='button_save_profile')]),
            dmc.Space(h=20),
            dmc.Text("Speichern hat leider noch keine Funktion.", color='red')
        ],
        opened=False
    )


def add_modal_load_configuration():
    return dmc.Modal(
        title='Konfiguration laden',
        id='modal_load_configuration',
        children=[
            dcc.Upload(
                id='upload_configuration',
                children=html.Div([
                    'Datei hier ablegen oder ',
                    html.A('Auswählen')
                ]),
                style={
                    'width': '100%',
                    'height': '100px',
                    'lineHeight': '100px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False
            ),
            dmc.Text(id='text_filename_load'),
            dmc.Space(h=10),
            dmc.Text("Die aktuelle Konfiguration durch die geladene überschreiben?"),
            dmc.Space(h=10),
            dmc.Button("Laden", id='button_load_configuration', leftIcon=DashIconify(icon="iconoir:load-action-floppy"))
        ],
        opened=False
    )


def add_drawer_notifications():
    return dmc.Drawer(title="Nachrichten:", id='drawer_notifications', padding="md", children=[])
