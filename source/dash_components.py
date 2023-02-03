import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify

import source.stylesheets as stylesheets


def add_storage_variables():
    return html.Div([dcc.Store(id='start_of_line'), dcc.Store(id='store_add_node'),
                     dcc.Store(id='line_edit_active'), dcc.Store(id='selected_element'),
                     dcc.Store(id='element_deleted'), dcc.Store(id='store_notification')])


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
    cytoscape = cyto.Cytoscape(
        id='cyto1',
        layout={'name': 'preset'},
        autoRefreshLayout=False,
        style={'width': '100%', 'height': '100%', 'background': '#e6ecf2', 'frame': 'blue'},
        elements=edges + nodes,
        stylesheet=stylesheets.cyto_stylesheet
    )
    return cytoscape


def add_modal_readme():
    with open('README.md', encoding='UTF-8') as file:
        content_readme = file.read()
    return dmc.Modal(
        title="Readme",
        id="modal_readme",
        children=dcc.Markdown(content_readme),
        opened=False
        # dbc.ModalHeader(dbc.ModalTitle("Readme")),
        # dbc.ModalBody(dcc.Markdown(content_readme), id="modal_readme_body")
    )


def add_modal_edit():
    return dmc.Modal(
        title="Edit",
        id='modal_edit',
        children=[
            dmc.Text("", id='modal_text'),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='modal_edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Schließen", variant='outline', id='modal_edit_close_button')
            ], position='right')
        ]
    )


def add_modal_voltage_level():
    return dmc.Modal(
        title="Spannungsebene auswählen",
        id='modal_voltage',
        children=[
            dmc.Text("Möchtest du das Element mit der Ober- oder Unterspannungsseite des Transformators verbinden (20kV oder 400V)?"),
            
        ]
    )


def dash_navbar():
    PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
    navbar = dbc.Navbar(
        dbc.Container([
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("PowerHouse", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dmc.Group([
                dmc.Button("README", id='button_readme', n_clicks=0,
                           leftIcon=DashIconify(icon="mdi:file-document"), variant='gradient'),
                dmc.Button("Debug", id='debug_button')],
                spacing=10
            ),
        ]), color="dark", dark=True
    )
    return navbar


def card_side():
    card = dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src="https://images.unsplash.com/photo-1598528133401-228e74463adb?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80",
                    height=160,
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
            dbc.Stack([
                # html.P("Grid elements", style={'margin-right': '10px', 'margin-top': '27px'}),
                dmc.Switch(id='menu_switch', style={'margin-top': '0px'}),
                html.P("House elements", style={'margin-left': '10px', 'margin-top': '27px'})], direction='horizontal'),
            dbc.Stack([
                # html.P("Netz bearbeiten", style={'margin-right': '10px', 'margin-top': '27px'}),
                dmc.Switch(id='mode_switch', style={'margin-top': '0px'},
                           offLabel=DashIconify(icon="material-symbols:edit-outline"),
                           onLabel=DashIconify(icon="material-symbols:calculate-outline")),
                dbc.Spinner(html.P("Berechnen", id='calculate', style={'margin-left': '10px', 'margin-top': '27px'}))],
                direction='horizontal'),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"width": 350, 'marginTop': 50},
    )
    return card
