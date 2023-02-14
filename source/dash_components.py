import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify

import source.stylesheets as stylesheets


def add_storage_variables():
    return html.Div([dcc.Store(id='start_of_line'), dcc.Store(id='store_add_node'),
                     dcc.Store(id='line_edit_active'), dcc.Store(id='selected_element'),
                     dcc.Store(id='element_deleted'), dcc.Store(id='store_notification1'),
                     dcc.Store(id='store_notification2'), dcc.Store(id='store_get_voltage'),
                     dcc.Store(id='store_edge_labels')])


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
    cytoscape = dmc.Card(
        children=[cyto.Cytoscape(
            id='cyto1',
            layout={'name': 'preset'},
            autoRefreshLayout=False,
            style={'width': '100%', 'height': '100%', 'background': '#e6ecf2', 'frame': 'blue'},
            elements=edges + nodes,
            stylesheet=stylesheets.cyto_stylesheet)],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"height": '100%'})
    return cytoscape


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
                dmc.Button("Debug", id='debug_button', variant="gradient",
                           gradient={"from": "grape", "to": "pink", "deg": 35})], spacing=10
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
                        dmc.Button("Berechnen", id='button_calculate', rightIcon=DashIconify(icon="ph:gear-light"))],
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


def add_drawer_notifications():
    return dmc.Drawer(title="Nachrichten:", id='drawer_notifications', padding="md", children=[])

# def card_plot_graph():
#     card = dmc.Card(
#         id='card_graph',
#         children=[
#             # dmc.CardSection(
#             #     dmc.Image(id='graph_image', src='assets/temp/graph.png', withPlaceholder=True)
#             # ),
#             dmc.Text("Gerichteter Graph des erstellten Netzes:")
#         ],
#         withBorder=True,
#         shadow="sm",
#         radius="md",
#         style={"width": 350, 'marginTop': 50, 'display': 'none'})
#     return card
