import dash_bootstrap_components as dbc
import source.stylesheets as stylesheets
from dash import dcc, html
import dash_cytoscape as cyto


def add_storage_variables():
    return html.Div([dcc.Store(id='start_of_line'), dcc.Store(id='store_add_node')])


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
    return dbc.Button(id=object_id, children=children, style=stylesheets.button_add_components_style)


def add_cytoscape_grid(nodes, edges):
    return cyto.Cytoscape(
        id='cyto1',
        layout={'name': 'preset'},
        autoRefreshLayout=False,
        style={'width': '800px', 'height': '100%', 'background': '#e6ecf2', 'frame': 'blue'},
        elements=edges + nodes,
        stylesheet=stylesheets.cyto_stylesheet
    )


def add_modal_readme():
    with open('README.md', encoding='UTF-8') as file:
        content_readme = file.read()
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Readme")),
        dbc.ModalBody(dcc.Markdown(content_readme), id="modal_readme_body")
    ],
        id="modal_readme",
        is_open=False,
    )


def add_modal_edit():
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Header")),
        dbc.ModalBody("Edit grid element here", id="modal_body"),
        dbc.ModalFooter(
            dbc.Button(
                "Close", id="close_modal", className="ms-auto", n_clicks=0
            )
        ),
    ],
        id="modal",
        is_open=False,
    )

# def readme_content():
#     with open('readme.md', encoding='UTF-8') as file:
#         content = file.read()
#     return dcc.Markdown(content)
