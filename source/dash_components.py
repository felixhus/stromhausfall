"""
dash_components.py contains the functions to create the components of the layout. Most of them at the first
loading of the app, some dynamically.
"""

import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_mantine_components as dmc
import numpy as np
from dash import dash_table, dcc, html
from dash_iconify import DashIconify

import source.plot as plot
import source.stylesheets as stylesheets
from source.modules import get_icon_url

# URLs of the background pictures of the rooms
# TODO: Change these to open source, in best case to dynamically loaded pictures (like iconify)
urls = {'cyto_bathroom': 'url(/assets/background_bathroom.png)', 'cyto_kitchen': 'url(/assets/background_kitchen.png)',
        'cyto_livingroom': 'url(/assets/background_livingroom.png)',
        'cyto_office': 'url(/assets/background_office.png)'}

# Initial dict for the device dict to create the first level keys
device_dict_init = {'house1': {}, 'rooms': {}, 'last_id': 1}


def add_storage_variables():
    """
    Here the DCC store objects are defined, which store different data throughout the app.
    :return: All dash store objects.
    """

    return html.Div([dcc.Store(id='start_of_line'),
                     # Store the id of a pressed button to add a grid object. Triggers the Callback to add the object.
                     dcc.Store(id='store_add_node'),
                     # Store if the line edit mode is active or not
                     dcc.Store(id='store_line_edit_active'),
                     # Store the id of the element of the node or edge which was clicked in the grid cytoscape
                     dcc.Store(id='store_selected_element_grid'),
                     # Store the id of the element of the node which was clicked in a room cytoscape
                     dcc.Store(id='store_selected_element_house'),
                     # Store id of house in the grid which is the one configured in detail by the user
                     dcc.Store(id='store_custom_house', data=None, storage_type='session'),

                     dcc.Store(id='store_element_deleted'), dcc.Store(id='store_notification'),
                     # Store ids of nodes to connect to pass them to the voltage modal
                     dcc.Store(id='store_get_voltage'),
                     # Store the generated edge labels and pass them to a callback which displays them
                     dcc.Store(id='store_edge_labels'),

                     dcc.Store(id='store_timestep'),

                     dcc.Store(id='store_flow_data'),
                     # Store the menu tab of the grid to change to. Is changed if a node/edge of the grid was clicked
                     dcc.Store(id='store_menu_change_tab_grid'),
                     # Store the menu tab of the house to change to. Is changed if a node of the house was clicked
                     dcc.Store(id='store_menu_change_tab_house'),
                     # Store the gridObject_dict, Dictionary with all grid objects in it
                     dcc.Store(id='store_grid_object_dict', data={}),
                     # Store Already used random profiles from IZES
                     dcc.Store(id='store_used_profiles', data=[1], storage_type='session'),
                     # Store the device_dict, dictionary with all device objects in it
                     dcc.Store(id='store_device_dict', data=device_dict_init),

                     dcc.Store(id='store_results_house_power'),
                     # Store the settings from the settings tab
                     dcc.Store(id='store_settings', data={}),

                     dcc.Store(id='store_results_house_energy'),
                     # Store a collection of all relevant data here to reload on a page refresh
                     dcc.Store(id='store_backup', storage_type='session'),
                     # Changed if an enter press is detected. Is then resetted with None in the save-callbacks
                     dcc.Store(id='store_save_by_enter', data=None),

                     dcc.Store(id='store_own_device_dict', data={}, storage_type='session'),

                     dcc.Store(id='store_menu_elements_house', storage_type='session')])


def add_grid_object_button(object_id, name=None, icon=None, enable=True, app=None):
    """
    This function creates a button for the left menu to add a grid object.
    :param object_id: dash-id of the button
    :type object_id: str
    :param name: Name of the button for the tooltip.
    :type name: str
    :param icon: In case of Iconify icon: iconify name; In case of png-Icon: path of the png-file
    :type icon: str
    :param enable: Boolean, if button should be enabled (False=Disabled)
    :type enable: bool
    :param app: Dash app
    :return: DBC button and tooltip showing the name
    :rtype: list
    """

    if icon is not None:
        if icon.endswith('.png'):  # If a png picture is given as the logo
            icon = app.get_asset_url(icon)
            children = html.Img(src=icon, height=str(stylesheets.button_add_components_style['icon_width']) + 'px')
        else:  # If a dash iconify icon is given
            children = DashIconify(icon=icon, width=stylesheets.button_add_components_style['icon_width'],
                                   color='black')
    else:
        children = name
    return [dmc.Button(id=object_id, children=children, style=stylesheets.button_add_components_style,
                       disabled=not enable), dbc.Tooltip(name, target=object_id)]


def add_menu_dropdown(room_type: str, button_dict: dict):
    """
    This function creates a menu dropdown containing the given devices from button_dict for a given room.
    Only the devices are considered, which have a standard room named in the database.
    The button_dict has to contain: Name, dash id, iconify icon.
    :param room_type: One of the following room types: bathroom, livingroom, kitchen, office
    :type room_type: str
    :param button_dict: Dictionary of menu buttons for the rooms.
    :type button_dict: dict
    :return: DMC MenuDropdown
    """

    item_list = []
    for item in button_dict[room_type]:  # Create a menu item for each device in room
        item_list.append(dmc.MenuItem(item[0], id=item[1], icon=DashIconify(icon=item[2])))
    item_list.append(dmc.MenuDivider())
    item_list.append(
        dmc.MenuItem("Weitere", id='button_additional_' + room_type,  # Add a menu item for additional devices
                     icon=DashIconify(icon='mdi:more-circle-outline')))
    item_list.append(dmc.MenuDivider())
    item_list.append(
        dmc.MenuItem("Schließen", id='button_close_menu_' + room_type,  # Add a menu item to close the menu
                     icon=DashIconify(icon='material-symbols:close-rounded'),
                     color='red'))
    return dmc.MenuDropdown(item_list)


def add_cytoscape(cyto_id: str, elements: list):
    """
    Returns a dash cytoscape with the given id and the given elements in it. These are the power strip
    and the plus-element in case of a room cytoscape.
    :param cyto_id: dash id of cytoscape to add
    :type cyto_id: str
    :param elements: Elements to add to this cytoscape
    :type elements: dict
    :return: hmtl-Div with dash cytoscape in it
    """

    return html.Div(cyto.Cytoscape(
        id=cyto_id,
        layout={'name': 'preset'},
        autoRefreshLayout=False,
        elements=elements,
        style={'background': '#e6ecf2', 'frame': 'blue', 'height': '200px',
               'background-image': urls[cyto_id], 'background-size': 'contain', 'background-repeat': 'no-repeat'},
        stylesheet=stylesheets.cyto_stylesheet))


def add_main_card_layout(button_dict: dict):
    """
    This function adds the main card layout to the app. It contains the following tabs:
    - Netz - Grid: The grid cytoscape to build your grid with drag&drop is added here.
    - Haus - House: The rooms with their cytoscapes and add-device-menus are added here.
    - Einstellungen - Settings: The dash components for settings inputs are added here.
    :param button_dict: Dictionary of menu buttons for the rooms.
    :type button_dict: dict
    :return: Main card layout of the app
    """

    # Specifies the elements which are in the room cytoscapes on initialization, the power strip and plus button
    elements = [
        {'data': {'id': 'power_strip'}, 'classes': 'power_strip_style'},
        {'data': {'id': 'plus', 'parent': 'power_strip'}, 'position': {'x': 75, 'y': 175},
         'classes': 'room_node_style', 'style': {'background-image': get_icon_url('ic:round-plus')}}]

    return dbc.Card(
        children=[
            dbc.CardBody(
                dmc.Tabs([  # Tabs of main card in the middle: Grid, House, Settings
                    dmc.TabsList([
                        dmc.Tab("Netz", value="grid", icon=DashIconify(icon='tabler:chart-grid-dots')),
                        dmc.Tab("Haus", value="house1", disabled=True, id='tab_house',
                                icon=DashIconify(icon='material-symbols:house-siding-rounded')),
                        dmc.Tab("Einstellungen", value="settings",
                                icon=DashIconify(icon='material-symbols:settings-outline'))
                    ]),
                    dmc.TabsPanel(children=[  # Content of Grid-Tab
                        cyto.Cytoscape(  # Grid Cytoscape
                            id='cyto_grid',
                            layout={'name': 'preset'},
                            autoRefreshLayout=False,
                            elements=[],
                            style={'background': '#e6ecf2', 'frame': 'blue', 'height': '400px'},
                            stylesheet=stylesheets.cyto_stylesheet)],
                        value='grid'),
                    dmc.TabsPanel(children=[  # Content of the House-Tab
                        dbc.Container([
                            dbc.Row([
                                dbc.Col([  # Bathroom Cytoscape and menu to add devices
                                    dmc.Menu([
                                        dmc.MenuTarget(html.Div(id='menu_target_bathroom')),
                                        add_menu_dropdown('bathroom', button_dict)
                                    ], id='menu_devices_bathroom', position='left-start', withArrow=True),
                                    add_cytoscape('cyto_bathroom', elements)
                                ], width=6),
                                dbc.Col([  # Livingroom Cytoscape and menu to add devices
                                    dmc.Menu([
                                        dmc.MenuTarget(html.Div(id='menu_target_livingroom')),
                                        add_menu_dropdown('livingroom', button_dict)
                                    ], id='menu_devices_livingroom', position='left-start', withArrow=True),
                                    add_cytoscape('cyto_livingroom', elements)
                                ], width=6)
                            ]),
                            dmc.Space(h=20),
                            dbc.Row([
                                dbc.Col([  # Kitchen Cytoscape and menu to add devices
                                    dmc.Menu([
                                        dmc.MenuTarget(html.Div(id='menu_target_kitchen')),
                                        add_menu_dropdown('kitchen', button_dict)
                                    ], id='menu_devices_kitchen', position='left-start', withArrow=True),
                                    add_cytoscape('cyto_kitchen', elements)
                                ], width=6),
                                dbc.Col([  # Office Cytoscape and menu to add devices
                                    dmc.Menu([
                                        dmc.MenuTarget(html.Div(id='menu_target_office')),
                                        add_menu_dropdown('office', button_dict)
                                    ], id='menu_devices_office', position='left-start', withArrow=True),
                                    add_cytoscape('cyto_office', elements)
                                ], width=6)
                            ]),
                        ])
                    ], value='house1'),
                    dmc.TabsPanel(children=[  # Content of the settings-Tab
                        dmc.Space(h=20),
                        dmc.NumberInput(  # Number Input for the calendar week
                            id='input_week', label="Kalenderwoche",
                            value=1, step=1,
                            min=1, max=52, stepHoldDelay=500, stepHoldInterval=150,
                            style={"width": 250},
                        ),
                        dmc.Space(h=20),
                        dmc.NumberInput(  # Number Input for the year, disabled because current database
                            id='input_year', label="Jahr",  # only has data for 2015
                            value=2015, step=1,
                            min=2015, max=2015, stepHoldDelay=500, stepHoldInterval=100,
                            style={"width": 250}, disabled=True
                        ),
                        dmc.Space(h=20),
                        dmc.NumberInput(  # Number Input for the electrical energy costs in ct/kWh
                            id='input_cost_kwh', label="Stromkosten pro kWh in ct",
                            value=30, step=0.1,
                            min=0, max=300, stepHoldDelay=500, stepHoldInterval=100,
                            style={"width": 250}
                        ),
                        dmc.Space(h=15),
                        # Button to update all settings. Disabled because not implemented yet
                        # TODO: Implement update button of settings
                        dmc.Button("Aktualisieren - Work in progress", disabled=True, id='button_update_settings',
                                   leftIcon=DashIconify(icon='ci:arrows-reload-01')),
                    ], value='settings')
                ],
                    id='tabs_main', value='grid', color="blue", orientation="horizontal", allowTabDeactivation=True)
            ),
            dbc.CardFooter(dmc.Slider(  # Slider to select timestep in grid calculation result
                id='timestep_slider', value=0, updatemode='drag',
                min=1, max=10, step=1))
        ], style={'height': '100%'}
    )


def add_modal_readme():
    """
    Adds a modal to the layout, which shows the README of the project for help.
    :return: DMC Modal
    """
    with open('README.md', encoding='UTF-8') as file:
        content_readme = file.read()
    return dmc.Modal(
        title="Readme",
        id="modal_readme",
        children=dcc.Markdown(content_readme),
        opened=False,
        size='55%'
    )


def add_modal_voltage_level():
    """
    Return modal to choose the voltage level of a grid component. This is necessary if the voltage level of both
    components to connect is not specified.
    :return: DMC Modal
    """

    return dmc.Modal(
        title="Spannungsebene auswählen",
        id='modal_voltage',
        closeOnEscape=False, closeOnClickOutside=False, withCloseButton=False,
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
    """
    Creates the Navigation bar of the app.
    :return: DBC Navbar
    """

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
                                    id='badge_notifications',
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
            # TODO: Implement a progress bar function properly. This was a first try:
            # dmc.Group([
            #     dmc.Progress(id='progress_bar', value=0, striped=True, animate=True, color='pink', style={'width': 250}),
            #     dmc.Space(h=5),
            #     dmc.Code("", id='progress_text', style={'display': 'none'})
            # ]),
            dmc.Group([
                dmc.Button("README", id='button_readme', n_clicks=0,
                           leftIcon=DashIconify(icon="mdi:file-document"), variant='gradient'),
                dmc.Menu([
                    dmc.MenuTarget(dmc.Button("Menü", leftIcon=DashIconify(icon="material-symbols:menu-rounded"),
                                              variant='gradient'), ),
                    dmc.MenuDropdown([
                        dmc.MenuItem("Konfiguration speichern", icon=DashIconify(icon="iconoir:save-action-floppy"),
                                     id='menu_item_save'),
                        dmc.MenuItem("Konfiguration laden", icon=DashIconify(icon="iconoir:load-action-floppy"),
                                     id='menu_item_load'),
                        dmc.MenuItem("Download eigene Geräte",
                                     icon=DashIconify(icon="material-symbols:sim-card-download-outline"),
                                     id='menu_item_own_devices'),
                    ])
                ], trigger='hover', openDelay=100, closeDelay=200, transition="rotate-right", transitionDuration=150),
                # dmc.Button("Debug", id='debug_button', variant="gradient", leftIcon=DashIconify(icon='gg:debug'),
                #            gradient={"from": "grape", "to": "pink", "deg": 35})
            ], spacing=10
            ),
        ]), color="dark", dark=True
    )
    return navbar


def add_card_start():
    """
    Creates the card which is shown when the app is loaded. It has buttons to either start the app
    or load an existing configuration.
    Returns an opened DMC Modal with the content card in it.
    :return: DMC Modal
    """

    card = dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src="assets/crayon_powerhouse.png", height=250,
                )
            ),
            dmc.Group(
                [
                    dmc.Text("Strom-Haus-Fall", weight=500),
                    # TODO: Remove the beta badge
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
            dmc.Group([
                dmc.Button("Start", leftIcon=DashIconify(icon='material-symbols:play-arrow-outline-rounded'),
                           id='button_start'),
                dmc.Button("Konfiguration laden", leftIcon=DashIconify(icon='iconoir:load-action-floppy'),
                           id='button_start_load')
            ])
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"height": '100%'},
    )
    return dmc.Modal([card], id='modal_start', opened=True, withCloseButton=False, radius=10)


def add_card_menu():
    """
    Creates the card on the right side of the app, which contains all settings of components and results.
    Also contains the loading overlay to display a loader when something is loading or calculating
    :return: DMC Card
    """

    return dmc.Card(
        children=[dmc.LoadingOverlay(  # Loading overlay: Shows loader each time something in the card loads.
            dmc.Tabs(  # Tabs of the card
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Bearbeiten", value="edit",
                                    icon=DashIconify(icon="material-symbols:edit-square-outline")),
                            dmc.Tab("Ergebnisse", value="results", icon=DashIconify(icon="fluent:poll-16-regular")),
                            dmc.Tab("Kosten", value="costs", icon=DashIconify(icon="tabler:pig-money"))
                        ]
                    ),
                    dmc.TabsPanel(children=[  # Edit Tab
                        dmc.Space(h=20),
                        # This Tab contains a Tabbing components itself, but without visible tabs. This is used to
                        # change between different menus for different components (grid or house devices).
                        # The Tab Panels for the components are created dynamically while the app is running.
                        # That's how it is possible to easily switch between different menus just by setting the
                        # "value" of the "menu_parent_Tabs.
                        # There are two tab panels initially added, one "empty" so there always is one.
                        # One "init_ids" which is never visible but contains dummy components with dash ids, which
                        # are used in callbacks as inputs, so they have to exist at rendering the app in the beginning.
                        # If these components are created dynamically, a dummy one with the same id is created in the
                        # "init_ids" tab so no exception is thrown.
                        dmc.Tabs(children=[
                            add_menu_tab_panel('empty'),  # Add empty tab so one always exists
                            add_menu_tab_panel('init_ids'),  # Add dummy components with needed ids
                        ], id='menu_parent_tabs'),
                        dmc.Space(h=20),
                        dmc.Group([
                            dmc.Button("Berechnen", id='button_calculate', rightIcon=DashIconify(icon="ph:gear-light")),
                            # This switch can activate or disable each device, so that it is not used in calculation
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
                            # TODO: This switch does not have a function implemented yet. It should turn on and off
                            # TODO: grid components.
                            dmc.Switch(
                                id='active_switch_grid',
                                thumbIcon=DashIconify(
                                    icon="material-symbols:mode-off-on", width=16,
                                    color=dmc.theme.DEFAULT_COLORS["gray"][5]
                                ),
                                size="md",
                                color="gray",
                                checked=False,
                                style={'display': 'block'}
                            )
                        ], position='apart')],
                        value="edit"),
                    dmc.TabsPanel(children=[    # Results tab panel
                        dmc.Tabs(children=[
                            add_result_tab_panel('empty'),  # For more information see comments above
                            add_result_tab_panel('house'),
                            add_result_tab_panel('grid')
                        ], id='result_parent_tabs'),
                    ], value="results"),
                    # TODO: Costs for grid objects
                    dmc.TabsPanel(children=[    # Tabs Panel for energy costs
                        dmc.Text("Keine Kosten berechnet!")
                    ], value='costs', id='cost_tab')
                ],
                id='tabs_menu', value='edit', color="blue", orientation="horizontal",
            ), loaderProps={"variant": "bars", "color": "blue", "size": "lg"})
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"height": '100%'},
    )


def add_result_tab_panel(tab_value):
    """
    This function returns the tabs panels for results of calculations.
    :param tab_value: Which tab panel should be created? Could be 'empty', 'house' or 'grid'
    :type tab_value: str
    :return: DMC Tabs Panel
    """

    if tab_value == 'empty':    # Dummy tabs panel, empty
        return dmc.TabsPanel(
            value=tab_value
        )
    elif tab_value == 'house':  # Tabs panel for the results of the house calculation
        return dmc.TabsPanel([
            dmc.Space(h=20),
            dcc.Graph(id='graph_power_house'),
            dmc.Space(h=10),
            dmc.SegmentedControl(
                id='pagination_days_results',
                value='mo',
                fullWidth=320,
                data=[
                    {'value': 'mo', 'label': 'MO'}, {'value': 'tu', 'label': 'DI'}, {'value': 'wd', 'label': 'MI'},
                    {'value': 'th', 'label': 'DO'}, {'value': 'fr', 'label': 'FR'}, {'value': 'sa', 'label': 'SA'},
                    {'value': 'su', 'label': 'SO'}, {'value': 'tot', 'label': 'TOT'}
                ]
            ),
            dmc.Space(h=10),
            dmc.Checkbox(label="Legende anzeigen", id='checkbox_show_legend'),
            dcc.Graph(id='graph_sunburst_house'),
        ], value=tab_value)
    elif tab_value == 'grid':   # Tabs panel for the results of the grid calculation
        return dmc.TabsPanel([
            dmc.Space(h=20),
            dmc.Alert(children="Bitte einen Zeitpunkt mit dem Slider auswählen",
                      id="alert_externalgrid", color='primary', hide=False),
            dmc.Space(h=10),
            dmc.Alert(children="Bitte einen Zeitpunkt mit dem Slider auswählen",
                      id="alert_time", color='primary', hide=False)
        ], value=tab_value)


def add_menu_tab_panel(tab_value: str, selected_element=None, element_dict=None):
    """
    This function returns the tabs panels for clicked object (grid components or devices in the house).
    It loads the stored properties from the element_dict and shows them in the inputs.
    :param tab_value: Which tabs panel should be created? The tab value is the type of the object clicked
    :type tab_value: str
    :param selected_element: The id of the selected element in the cytoscape
    :type selected_element: str
    :param element_dict: The element dictionary which contains all information about the existing elements.
    :type element_dict: dict
    :return: DMC tab panel
    """

    # TODO: Currently on every click a new tab panel is created, even if the object type was clicked before.
    # TODO: It would make the application faster, if only the values are loaded and the old tap panel was used.
    # See general_callbacks.manage_menu_tabs

    if selected_element is None:
        selected_element = {}
    if tab_value == 'house':  # Tab panel for house
        control, fade = 'preset', True  # Get values from element and show tab dependent on them
        checkbox_random = element_dict[selected_element]['power_profile'] is None
        if element_dict[selected_element]['config_mode'] == 'custom':  # Check if the house profile is custom
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
                                 data=[{'value': 'preset', 'label': "Fertiges Profil"},
                                       {'value': 'custom', 'label': "Selbst basteln"}]),
            dbc.Fade([
                dmc.Space(h=20),
                # This checkbox is only shown for houses with random load profiles, not for a custom house
                dmc.Checkbox(label="Beim Speichern zufälliges Lastprofil laden?", id='checkbox_random_profile',
                             checked=checkbox_random)
            ], id='house_fade', is_in=fade),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"))
            ], position='right'),
            dmc.Space(h=20),
            dcc.Graph(figure=plot.plot_house_timeseries(element_dict[selected_element]['power'], 'rgb(64, 130, 109)'),
                      id='graph_house',
                      style={'width': '100%'}),
            dmc.Space(h=20)
        ], value=tab_value)
    elif tab_value == 'pv':     # Tab panel for solar module
        postcode = element_dict[selected_element]['location'][0]    # Get saved postcode
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
            dmc.Group([
                get_compass(element_dict[selected_element]['orientation']),     # Get button group (compass)
                dmc.Stack([
                    dmc.Group([
                        dmc.Text("Leistung [kWp]"),
                        dmc.NumberInput(
                            id='input_kwp',
                            value=element_dict[selected_element]['rated_power'],
                            step=0.1, min=0.1, max=100, stepHoldDelay=500, stepHoldInterval=150, precision=1,
                            style={"width": 85})
                    ]),
                    dmc.Group([
                        dmc.Text("Neigung"),
                        dmc.Select(
                            placeholder="Auswahl",
                            id='tilt_select',
                            value=element_dict[selected_element]['tilt'],
                            style={"width": 115},
                            data=[
                                {'value': 0, 'label': 'Liegend'}, {'value': 15, 'label': 'Flachdach'},
                                {'value': 35, 'label': 'Steildach'}, {'value': 90, 'label': 'Fassade'}
                            ]),
                    ]),
                ], align='end')

            ], position='apart'),
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
        ], value=tab_value)
    elif tab_value == 'transformer':    # Tab panel for transformer
        return dmc.TabsPanel([
            dmc.TextInput(
                id='name_input',
                style={"width": 200},
                value=element_dict[selected_element]['name'],
                icon=DashIconify(icon="emojione-monotone:name-badge"),
            ),
            dmc.Space(h=20),
            # TODO: The power setting has no effect, but with it a overload check could be implemented.
            dmc.Select(
                label=["Leistung:"],
                placeholder="Auswahl",
                id='transformer_power_select',
                value=element_dict[selected_element]['rating'],
                data=[
                    {'value': 250, 'label': '250 kVA'}, {'value': 400, 'label': '400 kVA'},
                    {'value': 630, 'label': '630 kVA'}, {'value': 800, 'label': '800 kVA'}
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
        ], value=tab_value)
    elif tab_value == 'externalgrid':   # Tab panel for the external grid
        return dmc.TabsPanel([
            dmc.TextInput(
                id='name_input',
                style={"width": 200},
                value=element_dict[selected_element]['name'],
                icon=DashIconify(icon="emojione-monotone:name-badge"),
                disabled=True,
            ),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"), disabled=True)
            ], position='right'),
            dmc.Space(h=20),
        ], value=tab_value)
    elif tab_value == 'switch_cabinet':     # Tab panel for the switch_cabinet
        return dmc.TabsPanel([
            dmc.TextInput(
                id='name_input',
                style={"width": 200},
                value=element_dict[selected_element]['name'],
                icon=DashIconify(icon="emojione-monotone:name-badge"),
            ),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"))
            ], position='right'),
            dmc.Space(h=20),
        ],
            value=tab_value)
    elif tab_value == 'line':   # Tab panel for the line
        return dmc.TabsPanel([
            dmc.Text("Leitung"),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"), disabled=True)
            ], position='right')],
            value=tab_value
        )
    elif tab_value == 'device_preset':  # Tab panel for device with preset daily profile
        return dmc.TabsPanel([
            dmc.TextInput(
                id='name_input',
                style={"width": 200},
                value=element_dict[selected_element]['name'],
                icon=DashIconify(icon="emojione-monotone:name-badge"),
            ),
            dmc.Space(h=20),
            dmc.Select(
                label=["Lastprofil "],
                placeholder="Auswahl",
                id='load_profile_select_preset',
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
                      style={'width': '100%'}),
            dmc.Space(h=10),
            dmc.SegmentedControl(       # Control to select day of the week to plot
                id='pagination_days_menu',
                value='mo',
                fullWidth=320,
                data=[
                    {'value': 'mo', 'label': 'MO'}, {'value': 'tu', 'label': 'DI'}, {'value': 'wd', 'label': 'MI'},
                    {'value': 'th', 'label': 'DO'}, {'value': 'fr', 'label': 'FR'}, {'value': 'sa', 'label': 'SA'},
                    {'value': 'su', 'label': 'SO'}
                ]
            )
        ], value=tab_value)
    elif tab_value == 'device_custom':  # Tab panel for device with custom profile
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
                    label=["Lastprofil "],
                    placeholder="Auswählen",
                    id='load_profile_select_custom',
                    disabled=False,  # Development
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
            dmc.SegmentedControl(           # Control to select day of the week to plot
                id='pagination_days_menu',
                value='mo',
                fullWidth=320,
                data=[
                    {'value': 'mo', 'label': 'MO'}, {'value': 'tu', 'label': 'DI'}, {'value': 'wd', 'label': 'MI'},
                    {'value': 'th', 'label': 'DO'}, {'value': 'fr', 'label': 'FR'}, {'value': 'sa', 'label': 'SA'},
                    {'value': 'su', 'label': 'SO'}
                ]
            )
        ],
            value=tab_value)
    elif tab_value == 'lamp':   # Tab panel for a lamp device, identical to device_preset
        return dmc.TabsPanel([
            dmc.TextInput(
                id='name_input',
                style={"width": 200},
                value=element_dict[selected_element]['name'],
                icon=DashIconify(icon="emojione-monotone:name-badge"),
            ),
            dmc.Space(h=20),
            dmc.Select(
                label=["Lastprofil "],
                placeholder="Auswahl",
                id='load_profile_select_preset',
                value=element_dict[selected_element]['selected_power_option'],
                data=[
                    {'value': key, 'label': key}
                    for key in element_dict[selected_element]['power_options']
                ],
            ),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button', disabled=True,
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"))
            ], position='right'),
            dcc.Graph(figure=plot.plot_device_timeseries(np.linspace(0, 24, num=1440),
                                                         element_dict[selected_element]['power'],
                                                         'rgb(175, 173, 222)'), id='graph_device',
                      style={'width': '100%'}),
            dmc.Space(h=10),
            dmc.SegmentedControl(
                id='pagination_days_menu',
                value='mo',
                fullWidth=320,
                data=[
                    {'value': 'mo', 'label': 'MO'}, {'value': 'tu', 'label': 'DI'}, {'value': 'wd', 'label': 'MI'},
                    {'value': 'th', 'label': 'DO'}, {'value': 'fr', 'label': 'FR'}, {'value': 'sa', 'label': 'SA'},
                    {'value': 'su', 'label': 'SO'}
                ]
            )
        ], value=tab_value)
    elif tab_value == 'power_strip':    # Tab panel for the power strip, only show info text
        return dmc.TabsPanel([
            dmc.Text([DashIconify(icon='mdi:power-socket-de'),
                      " Die einzelnen Steckdosen der Steckdosenleiste können durch Klicken an- und ausgeschaltet werden."])
        ], value=tab_value)
    elif tab_value == 'empty':      # Empty tab panel so that the delete and save buttons always exist.
        return dmc.TabsPanel([
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Speichern", color='green', variant='outline', id='edit_save_button',
                           leftIcon=DashIconify(icon="material-symbols:save-outline"))
            ], position='right', style={'display': 'none'})],
            value=tab_value)
    elif tab_value == 'init_ids':
        # If there are components in the menu tabs, which act as inputs or Outputs of
        # Callbacks, they are not present when the callback is created, because the tab
        # is only created when a node was clicked. This hidden tab initializes the ids of these.
        return dmc.TabsPanel([
            dmc.SegmentedControl(id='house_mode', data=[]),
            dbc.Fade(id='house_fade'),
            dmc.SegmentedControl(id='pagination_days_menu', data=[]),
            dcc.Graph(id='graph_pv'),
            dcc.Graph(id='graph_house'),
            dmc.Checkbox(id='checkbox_random_profile')
        ], value=tab_value)


def get_compass(orientation: int):
    """
    Returns nine DMC ActionItems, which act as buttons in form of a compass. Each has the id "button_" followed
    by the direction. The parameter "orientation" is used to set the rotation of the needle of the compass.
    :param orientation: Orientation of the compass needle, (north: 0, east: 90, south: 180, west: 270)
    :type orientation: int
    :return: html-Div with 9 DMC Action Items in form of a compass
    """

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
                style={'transform': f'rotate({orientation - 45}deg)'}
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


def add_cost_badge(name, cost, icon=None):
    """
    Creates a cost badge for a device containing a DMC ThemeIcon and a DMC Badge showing the yearly energy cost for
    the device. Also, a tooltip with the device name is created.
    :param name:
    :type name: str
    :param cost:
    :type cost: float
    :param icon:
    :type icon: str
    :return: Html-Div
    """

    cost = str(round(cost / 100, 2)) + "€"
    badge = html.Div(children=[
        dmc.ThemeIcon(
            size=70,
            color="indigo",
            variant="filled",
            children=DashIconify(icon=icon, width=40),
        ),
        html.Br(),
        dmc.Badge(cost)
    ], style={'margin-left': 10, 'margin-bottom': 10}, id='cost_badge_' + name)
    tooltip = dbc.Tooltip(name, placement='bottom', target='cost_badge_' + name)
    return html.Div([badge, tooltip])


def add_device_costs(cost_tuple):
    """
    Creates a grid of device-cost badges. The given tuples have to contain (name, cost, icon).
    Also creates a title for the cost page.
    :param cost_tuple: list of tuples of costs of devices
    :type cost_tuple: list
    :return: Html-Div
    """

    grid = dmc.Grid(children=[
        add_cost_badge(element[0], element[1], element[2])
        for element in cost_tuple
    ], gutter='lg')
    return html.Div(children=[dmc.Space(h=20), dmc.Text("Jährliche Stromkosten pro Gerät:"), dmc.Space(h=25), grid])


def add_modal_graph():
    """
    Modal to show a full screen version of a graph. Is used by outputting the "figure" property of "graph_modal".
    :return: DMC Modal
    """

    return dmc.Modal(
        id='modal_graph',
        fullScreen=True, zIndex=10000,
        children=[
            dcc.Graph(id='graph_modal')
        ]
    )


def add_modal_devices():
    """
    Creates the modal to choose from all devices or create own ones. It is called by the "Weitere" button in a room
    menu. It has three tabs: additional, own, new.
    :return: DMC Modal
    """

    return dmc.Modal(
        title="Weitere Geräte auswählen",
        id='modal_additional_devices', opened=False, size=500,
        children=[
            dmc.Tabs([
                dmc.TabsList([
                    dmc.Tab("Weitere", value='additional', icon=DashIconify(icon='material-symbols:clear-all-rounded')),
                    dmc.Tab("Eigene", value='own', icon=DashIconify(icon='mdi:user-outline')),
                    dmc.Tab("Neues hinzufügen", value='new', icon=DashIconify(icon='mdi:package-variant-plus'))
                ]),
                # Tabs Panel to add additional devices. Here one can choose from all devices, not just the
                # room-standard ones as in the menu. You can also choose the room to add to.
                dmc.TabsPanel(value='additional', children=[dmc.Card(id='card_additional_devices', children=[
                    add_card_additional_devices([], None, False)
                ])]),
                # Tabs panel to add one of your own devices. They are listed here or can be loaded from a json-file.
                dmc.TabsPanel(value='own', children=[dmc.Card(id='card_own_devices_load', children=[
                    add_card_own_devices()
                ]), dmc.Card(id='card_own_devices_add', children=html.P(id='button_add_own_device'))]),
                # Tabs panel to add a new own device
                dmc.TabsPanel(value='new', children=[dmc.Card(id='card_new_devices', children=[
                    add_card_new_device()
                ])]),
            ], id='tabs_additional_devices', value='additional')
        ]
    )


def add_card_additional_devices(devices, radio_room, own=False):
    """
    Creates a card to select from a list of devices. It contains a radio-select of the devices, a radio-select
    of the room to add to and a button to add a selected device.
    :param devices: List of devices, either as tuples or as dicts
    :type devices: list
    :param radio_room: Preset value of the room radio-select
    :param own: str
    :return: HTML-Div
    """

    data = []
    for device in devices:
        # if device is given as dict (own devices) -> Convert to tuple
        if type(device) is dict:
            device = (device['type'], None, device['name'], device['menu_type'], device['icon'])
        # create list of devices with their icons
        content = dmc.Group([
            DashIconify(icon=device[4], inline=True),
            device[2]
        ])
        data.append([device[0], content])
    # Create radioGroup with devices
    radio_devices = dmc.RadioGroup(
        [dmc.Radio(l, value=k) for k, l in data],
        id='radiogroup_devices',
        label="Gerät auswählen",
        size='sm', orientation='vertical'
    )
    data = [['bathroom', 'Bad'], ['livingroom', 'Wohnzimmer'], ['kitchen', 'Küche'], ['office', 'Büro']]
    # Create radioGroup with rooms
    radio_rooms = dmc.RadioGroup(
        [dmc.Radio(l, value=k) for k, l in data],
        id='radiogroup_room', value=radio_room,
        label="In Raum",
        size='sm', orientation='vertical'
    )
    # Add button, the button-id is different depending on if this is the card to add additional devices or to add
    # own devices.
    if not own:
        button = dmc.Button("Hinzufügen", id='button_add_additional_device',
                            leftIcon=DashIconify(icon='material-symbols:add-box-outline'))
    else:
        button = dmc.Button("Hinzufügen", id='button_add_own_device',
                            leftIcon=DashIconify(icon='material-symbols:add-box-outline'))
    return html.Div([
        dmc.Group([
            radio_devices, radio_rooms
        ], align='initial', spacing=25),
        dmc.Space(h=20),
        button
    ])


def add_card_own_devices():
    """
    This returns the card to load a json-file with own devices. If they are loaded, the function
    "add_card_additional_devices" is used to create a list of them.
    :return: Html-Div
    """

    return html.Div([
        dcc.Upload(
            id='upload_own_devices',
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
        dmc.Text(id='text_filename_load_own', color='blue', underline=True),
        dmc.Space(h=10),
        dmc.Text("Datei mit zuvor heruntergeladenen eigenen Geräten auswählen."),
        dmc.Space(h=10),
        dmc.Button("Laden", id='button_load_own_devices', leftIcon=DashIconify(icon="iconoir:load-action-floppy"))
    ])


def add_card_new_device():
    """
    This creates the card to add a new own device to the app. It creates inputs for the name, type, icon and
    csv/xls/xlsx-file and displays a help section on how to create a device.
    :return: Html-Div
    """

    # Create table for help section
    header = [html.Thead(html.Tr([html.Th("time"), html.Th("Profil 1"), html.Th("Profil 2")]))]
    body = [html.Tbody([
        html.Tr([html.Td("07:01:00"), html.Td("100"), html.Td("75")]),
        html.Tr([html.Td("07:02:00"), html.Td("100"), html.Td("100")]),
        html.Tr([html.Td("07:02:30"), html.Td("100"), html.Td("125")]),
        html.Tr([html.Td("07:03:00"), html.Td("100"), html.Td("150")]),
        html.Tr([html.Td("07:05:00"), html.Td("0"), html.Td("125")]),
        html.Tr([html.Td("07:20:00"), html.Td("50"), html.Td("100")]),
    ])]
    children = html.Div([
        html.Div([
            dmc.Text("Eigenes Gerät hinzufügen:"),
            dmc.Space(h=10),
            dmc.TextInput(id='input_new_name', label="Gerätename *"),   # Input for device name
            dmc.Space(h=10),
            dmc.Text("Art des Lastprofils"),
            dmc.ChipGroup(      # Input for type of device (preset/custom)
                [dmc.Chip(l, value=k) for k, l in [['device_preset', 'Konstant'], ['device_custom', 'Variabel']]],
                value=None, id='input_new_menu_type'
            ),
            dmc.Space(h=10),
            # Input for iconify icon of the device
            dmc.TextInput(id='input_new_icon', icon=DashIconify(icon='ic:outline-device-unknown'),
                          label=dcc.Link("Hier Icon auswählen", href="https://icon-sets.iconify.design/",
                                         target="_blank"),
                          placeholder='ic:outline-device-unknown'),
            dmc.Space(h=10),
            dmc.Text('CSV-Datei für Lastprofile'),
            dcc.Upload(         # Upload of csv- or xls/xlsx file with load profiles
                id='upload_new_device',
                children=html.Div([
                    'Hier ablegen oder ',
                    html.A('Auswählen')
                ]),
                style={
                    'width': '100%',
                    'height': '50px',
                    'lineHeight': '50px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'margin': '0px'
                },
                multiple=False
            ),
            dmc.Text(id='text_filename_load_new', color='#FF7F50', underline=True),
            dmc.Space(h=15),
            dmc.Button("Erstellen", id='button_add_new_device',
                       leftIcon=DashIconify(icon='material-symbols:add-box-outline'))
        ]),
        dmc.Space(h=25),
        # Help section which describes how to add a device
        dmc.Paper([
            html.B("Hilfe beim Erstellen"), html.Br(), html.Br(),
            html.B("Gerätename: "), "Für welches Gerät fügst du Lastprofile hinzu?", html.Br(), html.Br(),
            html.B("Art des Lastprofils: "), html.Br(), html.U("Konstant: "),
            "Dein Gerät hat ein Lastprofil, das jeden Tag gleich ist (z.B. Kühlschrank). - ", html.Br(),
            html.U("Variabel: "),
            "Dein Gerät hat ein Lastprofil, welches immer unterschiedlich ist. Du willst einstellen können, wann das Gerät angeschaltet wird.",
            html.Br(), html.Br(),
            html.B("Icon: "),
            "Klicke auf den Link und such dir ein Icon aus, das zu deinem Gerät passt. Füg dann hier den Namen des Icons ein.",
            html.Br(), html.Br(),
            html.B("CSV-Datei: "),
            "Die Lastprofile lädst du in Form einer CSV-Datei hoch. Diese muss in der ersten Spalte (\"time\") "
            "die Zeitpunkte der Messungen enthalten, die weiteren Spaltennamen geben die Namen der Lastprofile "
            "des Geräts an. Die Einheit der Leistungen is [W].",
            html.Br(), html.Br(),
            dmc.Table(header + body)
        ], withBorder=True, shadow='l', p=10)
    ])
    return children


def add_modal_timeseries():
    """
    NOT IN USE! This is a modal to create a load profile of a device inside the app with a dash data table.
    Not running, under development.
    :return: DMC Modal
    """
    # TODO complete this to create whole devices with load profiles in the app itself.

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
    """
    Modal to load a previously saved configuration. Takes a json-file as an upload.
    :return: DMC Modal
    """

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
            dmc.Text(id='text_filename_load', color='blue', underline=True),
            dmc.Space(h=10),
            dmc.Text("Die aktuelle Konfiguration durch die geladene überschreiben?"),
            dmc.Space(h=10),
            dmc.Button("Laden", id='button_load_configuration', leftIcon=DashIconify(icon="iconoir:load-action-floppy"))
        ],
        opened=False
    )


def add_drawer_notifications():
    """
    Returns the drawer where the app notifications are shown.
    :return: DMC Drawer
    """
    return dmc.Drawer(title="Nachrichten:", id='drawer_notifications', padding="md", children=[])
