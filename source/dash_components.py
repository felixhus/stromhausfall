import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_mantine_components as dmc
import plot
from dash import dash_table, dcc, html
from dash_iconify import DashIconify

import source.stylesheets as stylesheets

devices = {'bathroom': [["Föhn", 'button_add_hairdryer', 'icon-park-outline:hair-dryer'],
                        ["Zahnbürste", 'button_add_toothbrush', 'mdi:toothbrush-electric'],
                        ["Bügeleisen", 'button_add_iron', 'tabler:ironing-1']]}


def add_storage_variables():
    return html.Div([dcc.Store(id='start_of_line'), dcc.Store(id='store_add_node'),
                     dcc.Store(id='store_line_edit_active'), dcc.Store(id='store_selected_element_grid'),
                     dcc.Store(id='store_selected_element_house'),
                     dcc.Store(id='store_element_deleted'), dcc.Store(id='store_notification1'),
                     dcc.Store(id='store_notification2'), dcc.Store(id='store_notification4'),
                     dcc.Store(id='store_notification3'), dcc.Store(id='store_notification5'),
                     dcc.Store(id='store_get_voltage'), dcc.Store(id='store_update_switch'),
                     dcc.Store(id='store_edge_labels'), dcc.Store(id='store_timestep'),
                     dcc.Store(id='store_flow_data'), dcc.Store(id='store_menu_change_tab_grid'),
                     dcc.Store(id='store_menu_change_tab_house'), dcc.Store(id='store_menu_inputs', data={}),
                     dcc.Store(id='store_grid_object_dict', data={}),
                     dcc.Store(id='store_device_dict', data={'house1': {}})])


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
        dmc.MenuItem("Schließen", id='button_close_menu', icon=DashIconify(icon='material-symbols:close-rounded'),
                     color='red'))
    return dmc.MenuDropdown(item_list)


def add_cytoscape(cyto_id, elements):
    return html.Div(cyto.Cytoscape(
        id=cyto_id,
        layout={'name': 'preset'},
        autoRefreshLayout=False,
        elements=elements,
        style={'background': '#e6ecf2', 'frame': 'blue', 'height': '200px'},
        stylesheet=stylesheets.cyto_stylesheet))


def add_cytoscape_layout():
    elements = [
        {'data': {'id': 'power_strip'}, 'classes': 'power_strip_style'},
        {'data': {'id': 'plus', 'parent': 'power_strip'}, 'position': {'x': 75, 'y': 175},
         'classes': 'room_node_style', 'style': {'background-image': ['/assets/Icons/icon_plus.png']}},
        {'data': {'id': 'socket1', 'parent': 'power_strip'}, 'position': {'x': 35, 'y': 175},
         'classes': 'socket_node_style_on', 'linked_device': 'lamp'},
        {'data': {'id': 'lamp'}, 'position': {'x': 35, 'y': 25}, 'classes': 'room_node_style',
         'style': {'background-image': ['/assets/Icons/icon_bulb.png']}, 'linked_socket': 'socket1'},
        {'data': {'source': 'socket1', 'target': 'lamp'}}]

    return dbc.Card(
        children=[
            dbc.CardBody(
                dmc.Tabs([
                    dmc.TabsList([
                        dmc.Tab("Netz", value="grid", icon=DashIconify(icon='tabler:chart-grid-dots')),
                        dmc.Tab("Haus 1", value="house1",
                                icon=DashIconify(icon='material-symbols:house-siding-rounded'))
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
                                        dmc.MenuTarget(html.Div(id='menu_target')),
                                        add_menu_dropdown('bathroom')
                                    ], id='menu_devices', position='left-start', withArrow=True),
                                    add_cytoscape('cyto_bathroom', elements)
                                ], width=6),
                                dbc.Col([
                                    cyto.Cytoscape(
                                        id='cyto_house2',
                                        layout={'name': 'preset'},
                                        autoRefreshLayout=False,
                                        elements=[],
                                        style={'background': '#e6ecf2', 'frame': 'blue', 'height': '200px', },
                                        stylesheet=stylesheets.cyto_stylesheet)
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
                    ], value='house1')
                ],
                    id='tabs_main', value='grid', color="blue", orientation="horizontal")
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
                # dmc.Button("Debug", id='debug_button', variant="gradient", leftIcon=DashIconify(icon='gg:debug'),
                #            gradient={"from": "grape", "to": "pink", "deg": 35})
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
    return html.Div([card], id='card_start')


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
                            add_menu_tab_panel('empty', None, None)
                        ], id='menu_parent_tabs'),
                        # dmc.Container(id='menu_parent_container',
                        #               children=[]),
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
                        dmc.Space(h=20),
                        dmc.Alert(children="", id="alert_externalgrid", color='primary', hide=True),
                        dmc.CardSection(
                            dmc.Image(id='graph_image', src='assets/temp/graph.png', withPlaceholder=True,
                                      style={'display': 'none'})
                        ),
                    ], value="results"),
                ],
                id='tabs', value='edit', color="blue", orientation="horizontal",
            ), loaderProps={"variant": "bars", "color": "blue", "size": "lg"})
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"height": '100%'},
    )
    return html.Div([card], id='card_menu', style={'display': 'none'})


def add_menu_tab_panel(tab_value, selected_element, element_dict):
    if tab_value == 'house':
        return dmc.TabsPanel([
            dmc.Text("Haus"),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"))
            ], position='right')],
            value=tab_value
        )
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
    elif tab_value == 'device_bathroom':
        return dmc.TabsPanel([
            dmc.Text("Gerät Badezimmer"),
            dmc.TextInput(
                id='name_input',
                style={"width": 200},
                value=element_dict[selected_element]['name'],
                icon=DashIconify(icon="emojione-monotone:name-badge"),
            ),
            dmc.Space(h=20),
            dmc.Select(
                label=["Geräteklasse ",
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
            dcc.Graph(figure=plot.plot_device_timeseries(list(range(24*60)), element_dict[selected_element]['power'],
                                                         'rgba(255, 255, 126,0.5)'))
            ],
            value=tab_value)
    elif tab_value == 'lamp':
        return dmc.TabsPanel([
            dmc.Text("Lampe"),
            dmc.TextInput(
                id='name_input',
                style={"width": 200},
                value=element_dict[selected_element]['name'],
                icon=DashIconify(icon="emojione-monotone:name-badge"),
            ),
            dmc.Space(h=20),
            dmc.Select(
                label=["Geräteklasse ",
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
            dcc.Graph(figure=plot.plot_device_timeseries(list(range(24 * 60)), element_dict[selected_element]['power'],
                                                         'rgba(255, 255, 126,0.5)'))
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


def add_drawer_notifications():
    return dmc.Drawer(title="Nachrichten:", id='drawer_notifications', padding="md", children=[])
